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
        server_ping_interval: int = 120,
    ) -> None:
        """Initialise the connection.

        Args:
            url: The URL to connect to
            aiohttp_session: The aiohttp session to use for the connection.
            If not provided, a new session will be created.
            server_ping_interval: The interval at which the server sends ping messages
        """
        self.aiohttp_session = (
            aiohttp.ClientSession() if aiohttp_session is None else aiohttp_session
        )
        self.url = url
        self.event_callbacks: EventCallbacks = defaultdict(list)
        self.socket: aiohttp.ClientWebSocketResponse | None = None

        self._state: ConnectionState = ConnectionState.INITIALISED

        self._receive_timeout = server_ping_interval

        self._should_reconnect = False
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
                heartbeat=60,
                receive_timeout=self._receive_timeout,
                autoping=True,
            ) as socket:
                self._state = ConnectionState.CONNECTED
                self.socket = socket

                await self._on_open()

                async for msg in socket:
                    if msg.type == aiohttp.WSMsgType.ERROR:  # type: ignore
                        await self._on_error(socket.exception())
                    else:
                        await self._on_message((msg.data))  # type: ignore

                await self._on_close()
        except asyncio.TimeoutError:
            logger.info("Connection: Connection timeout")
            self._state = ConnectionState.UNAVAILABLE
            self._should_reconnect = True

    async def _on_open(self):
        print("Connection opened")
        logger.info("Connection: Connection opened")
        await self.send_ping()
        await self.subscribe("my-channel")

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

                # check if channel is "my-channel", if so, print the data
                if params["channel"] == "my-channel":
                    print(params.get("data"))

    async def _on_error(self, err: BaseException | None):
        print(f"Error occurred: {err}")
        logger.info("Connection: Error occurred: %s", err)
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

    async def subscribe(self, channel: str):
        """Subscribe to a given channel.

        Args:
            channel: The name of the channel to subscribe to.

        Raises:
            ConnectionError: If not connected.
        """
        logger.info(f"Connection: subscribing to channel {channel}")
        if not self.socket:
            raise ConnectionError("Not connected.")

        try:
            await self.socket.send_json(
                {"event": "pusher:subscribe", "data": {"channel": channel}}
            )
        except aiohttp.WebSocketError as err:
            logger.error(f"Failed to subscribe to channel {channel}: {err}")

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

    async def _on_connection_established(self, data: Dict[str, Any]):
        """Handle a connection established event.

        Args:
            data: The data received with the event.
        """
        print("Connection: Connection established")

    ###
    # async def connect(self) -> None:
    #     """Connect to the socket."""
    #     try:
    #         self._ws = await self.aiohttp_session.ws_connect(  # type: ignore
    #             self.url, max_msg_size=0, autoclose=False, timeout=30
    #         )
    #         # self.connected = True
    #     except aiohttp.ClientError as err:
    #         raise ConnectionError("Error connecting to Pusher") from err

    # async def disconnect(self) -> None:
    #     """Disconnect."""
    #     if self._ws is not None:
    #         await self._ws.close()
    #         self._ws = None
    #         # self.connected = False

    # async def reconnect(self) -> None:
    #     """Reconnect."""
    #     await self.disconnect()
    #     await self.connect()

    # async def send(self, message: Any) -> None:
    #     """Send a message."""
    #     if self.connected:
    #         await self._ws.send_str(message)  # type: ignore
    #     else:
    #         raise ConnectionError("Not connected to the server.")

    # async def receive(self) -> Any:
    #     """Receive a message."""
    #     if self.connected:
    #         msg = await self._ws.receive_str()  # type: ignore
    #         return msg
    #     else:
    #         raise ConnectionError("Not connected to the server.")


async def test_connection():
    # pylint: disable=missing-function-docstring

    connection_url = "wss://ws-eu.pusher.com/app/e529828bbaae823d57d5?protocol=7&client=Aiopusher&version=0.1.0"
    connection = Connection(connection_url)

    # Connect to the server
    await connection.connect()


asyncio.run(test_connection())
