"""Handles the websocket connection to the Pusher server."""

from __future__ import annotations

import asyncio
import json
import logging
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Tuple
from collections import defaultdict

import aiohttp
from typing_extensions import TypeAlias

logger = logging.getLogger(__name__)

Callback: TypeAlias = Callable[..., Awaitable[None]]
EventCallbacks: TypeAlias = Dict[str, List[Tuple[Callback, Any, Any]]]


class ConnectionState(Enum):
    """Enum for the current state of the connection."""

    INITIALISED = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3
    UNAVAILABLE = 4
    FAILED = 5


class Connection:
    """Handles the websocket connection to the Pusher server."""

    def __init__(
        self,
        url: str,
        aiohttp_session: aiohttp.ClientSession | None = None,
        reconnect_handler: Callable[[], Awaitable[None]] | None = None,
        reconnect_interval: int = 10,
        server_ping_interval: int = 120,
        client_ping_interval: int | None = None,
    ) -> None:
        """Initialise the connection.

        Args:
            url: The URL to connect to
            aiohttp_session: The aiohttp session to use for the connection.
            If not provided, a new session will be created.
            server_ping_interval: The interval at which the server sends ping messages
            client_ping_interval: The interval at which ping messages are sent to the server.
            None means no ping messages are sent.
        """
        self.aiohttp_session = (
            aiohttp.ClientSession() if aiohttp_session is None else aiohttp_session
        )
        self.url = url
        self.event_callbacks: EventCallbacks = defaultdict(list)
        self.socket: aiohttp.ClientWebSocketResponse | None = None
        self.reconnect_handler = reconnect_handler or (lambda: None)

        self._socket_id: str | None = None

        self._state: ConnectionState = ConnectionState.INITIALISED

        self._reconnect_interval = reconnect_interval
        self._receive_timeout = server_ping_interval
        self._heartbeat_interval = client_ping_interval

        self._should_disconnect = False
        self._should_reconnect = False

        self.bind("pusher:connection_established", self._on_connection_established)

    def bind(
        self, event_name: str, callback: Callback, *args: Any, **kwargs: Any
    ) -> None:
        """Bind an event to a callback

        Args:
            event_name: The name of the event to bind to
            callback: The callback function to call when the event is received
            *args: Any positional arguments to pass to the callback
            **kwargs: Any keyword arguments to pass to the callback
        """
        self.event_callbacks[event_name].append((callback, args, kwargs))

    async def connect(self) -> None:
        """Connect to the socket."""
        self._state = ConnectionState.CONNECTING
        try:
            # After receive_timeout seconds of not receiving a message, the
            # connection will be closed, and the should_reconnect flag will be
            # set to True.
            async with self.aiohttp_session.ws_connect(  # type: ignore
                self.url,
                receive_timeout=self._receive_timeout,
                heartbeat=self._heartbeat_interval,
                autoping=True,
            ) as socket:
                self.socket = socket

                await self._on_open()

                async for msg in socket:
                    if msg.type == aiohttp.WSMsgType.ERROR:  # type: ignore
                        await self._on_error(socket.exception())
                    else:
                        await self._on_message((msg.data))  # type: ignore

                await self._on_close()
        except asyncio.TimeoutError:
            await self._on_timeout()
        except Exception as err:  # pylint: disable=broad-except
            await self._on_error(err)

        while self._should_reconnect and not self._should_disconnect:
            self._state = ConnectionState.UNAVAILABLE
            await asyncio.sleep(self._reconnect_interval)
            await self.connect()

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        self._should_reconnect = False
        self._should_disconnect = True
        if self.socket:
            await self.socket.close()

    async def reconnect(self) -> None:
        """Reconnect to the socket."""
        logger.info("Connection: Reconnect in %s s", self._reconnect_interval)

        self._should_reconnect = True
        if self.socket:
            await self.socket.close()

    async def _on_open(self):
        print("Connection opened")
        logger.info("Connection: Connection opened")
        await self.send_ping()

    async def _on_message(self, msg: str):
        params = self._parse_message(msg)

        if "event" in params:
            if "channel" not in params:
                # We've got a connection event.  Lets handle it.
                if params["event"] in self.event_callbacks:
                    for func, args, kwargs in self.event_callbacks[params["event"]]:
                        asyncio.create_task(
                            func(params.get("data", None), *args, **kwargs)  # type: ignore
                        )
                else:
                    logger.info("Connection: Unhandled event")
            else:
                # We've got a channel event.  Lets pass it up to the pusher
                # so it can be handled by the appropriate channel.
                # self.event_handler(
                #     params["event"], params.get("data"), params["channel"]
                # )
                raise NotImplementedError

    async def _on_error(self, err: BaseException | None):
        print(f"Error occurred: {err}")
        logger.exception("Connection: Unhandled exception occurred")
        self._state = ConnectionState.FAILED
        self._should_reconnect = True

    async def _on_timeout(self):
        print("Connection: Did not receive any data in time.  Reconnecting.")
        logger.info("Connection: Did not receive any data in time.  Reconnecting.")
        self._state = ConnectionState.FAILED
        self._should_reconnect = True

    async def _on_close(self):
        print("Connection closed")

    @staticmethod
    def _parse_message(msg: str) -> dict[str, Any]:
        """Parse a message received from the server.

        Args:
            msg: The message to parse.
        """
        return json.loads(msg)

    async def send_ping(self):
        """Send a ping to the server.

        Raises:
            ConnectionError: If not connected.
        """
        logger.info("Connection: ping to pusher")
        if not self.socket:
            raise ConnectionError("Not connected.")

        try:
            await self.socket.send_json({"event": "pusher:ping"})
        except aiohttp.WebSocketError as err:
            logger.error("Failed send ping: %s", err)

    async def _on_connection_established(self, data: str):
        """Handle a connection established event.

        Args:
            data: The data received with the event.
        """
        data_dict = self._parse_message(data)
        self._socket_id = data_dict["socket_id"]

        self._state = ConnectionState.CONNECTED

        if self._should_reconnect:
            # Since we've opened a connection, we don't need to try to reconnect
            self._should_reconnect = False

            self.reconnect_handler()

            logger.info("Connection: Established connection after reconnecting")
            print("Connection: Established connection after reconnecting")
        else:
            logger.info("Connection: Established connection")

            print("Connection: Connection established")


async def test_connection():
    # pylint: disable=missing-function-docstring

    connection_url = "wss://ws-eu.pusher.com/app/e529828bbaae823d57d5?protocol=7&client=Aiopusher&version=0.1.0"
    connection = Connection(connection_url)

    # Connect to the server
    await connection.connect()


asyncio.run(test_connection())


# async def subscribe(self, channel: str):
#     """Subscribe to a given channel.

#     Args:
#         channel: The name of the channel to subscribe to.

#     Raises:
#         ConnectionError: If not connected.
#     """
#     logger.info("Connection: subscribing to channel %s", channel)
#     if not self.socket:
#         raise ConnectionError("Not connected.")

#     try:
#         await self.socket.send_json(
#             {"event": "pusher:subscribe", "data": {"channel": channel}}
#         )
#     except aiohttp.WebSocketError as err:
#         logger.error("Failed to subscribe to channel %s: %s", channel, err)
