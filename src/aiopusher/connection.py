"""Handles the websocket connection to the Pusher server."""

from __future__ import annotations

from typing import Any, Callable, Awaitable, Dict, Tuple, Union

import aiohttp
import asyncio
import json


class Connection:
    """Handles the websocket connection to the Pusher server."""

    def __init__(
        self, connection_url: str, aiohttp_session: aiohttp.ClientSession | None = None
    ) -> None:
        self.aiohttp_session = (
            aiohttp.ClientSession() if aiohttp_session is None else aiohttp_session
        )
        self.connection_url = connection_url

        self.connected = False
        self._ws: aiohttp.ClientWebSocketResponse | None = None

    async def connect(self) -> None:
        """Connect to the socket."""
        try:
            self._ws = await self.aiohttp_session.ws_connect(  # type: ignore
                self.connection_url, max_msg_size=0, autoclose=False, timeout=30
            )
            self.connected = True
        except aiohttp.ClientError as err:
            raise ConnectionError("Error connecting to Pusher") from err

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        if self._ws is not None:
            await self._ws.close()
            self._ws = None
            self.connected = False

    async def reconnect(self) -> None:
        """Reconnect the socket."""
        await self.disconnect()
        await self.connect()

    async def send(self, message: Any) -> None:
        """Send a message through the socket."""
        if self.connected:
            await self._ws.send_str(message)  # type: ignore
        else:
            raise ConnectionError("Not connected to the server.")

    async def receive(self) -> Any:
        """Receive a message from the socket."""
        if self.connected:
            msg = await self._ws.receive_str()  # type: ignore
            return msg
        else:
            raise ConnectionError("Not connected to the server.")


EventDataType = Dict[str, Union[str, int, float]]
ArgsType = Tuple[Any, ...]
KwargsType = Dict[str, Any]
CallbackType = Callable[..., Awaitable[None]]


class Channel:
    """Handles a specific channel of the websocket connection."""

    def __init__(self, channel_name: str, connection: Connection) -> None:
        self.channel_name = channel_name
        self.connection = connection
        self.subscribed = False
        self.event_callbacks: dict[
            str,
            list[
                tuple[
                    CallbackType,
                    ArgsType,
                    KwargsType,
                ]
            ],
        ] = {}

    def bind(
        self,
        event_name: str,
        callback: Callable[..., Awaitable[None]],
        *args: Any,
        **kwargs: Any,
    ):
        """Binds a callback function to an event."""
        self.event_callbacks[event_name].append((callback, args, kwargs))

    def _handle_event(self, event_name: str, data: EventDataType) -> None:
        if event_name in self.event_callbacks:
            for callback, args, kwargs in self.event_callbacks[event_name]:
                callback(data, *args, **kwargs)

    # async def listen(self) -> None:
    #     """Listen for messages on the channel."""
    #     if self.subscribed:
    #         print(f"Listening on channel {self.channel_name}...")
    #         while True:
    #             message = await self.connection.receive()
    #             message_dict = json.loads(message)
    #             event_name = message_dict.get("event")

    #             # If a callback is bound to this event, call it
    #             if event_name in self.event_callbacks:
    #                 callback_func = self.event_callbacks[event_name]
    #                 callback_func(event_name, message_dict)
    #     else:
    #         print("Not subscribed to the channel.")

    # - Move these methods to the PusherClient class
    # async def subscribe(self) -> None:
    #     """Subscribe to the channel."""

    #     # Prepare the subscription message. This would depend on the specifics
    #     # of the Pusher service and might need to be adapted.
    #     subscription_message = json.dumps(
    #         {"event": "pusher:subscribe", "data": {"channel": self.channel_name}}
    #     )

    #     # Send the subscription message
    #     try:
    #         await self.connection.send(subscription_message)
    #         self.subscribed = True
    #         print(f"Subscribed to channel {self.channel_name}")
    #     except ConnectionError as e:
    #         print(f"Failed to subscribe to channel: {e}")

    # async def unsubscribe(self) -> None:
    #     """Unsubscribe from the channel."""

    #     # Prepare the unsubscription message
    #     unsubscription_message = json.dumps(
    #         {"event": "pusher:unsubscribe", "data": {"channel": self.channel_name}}
    #     )

    #     # Send the unsubscription message
    #     try:
    #         await self.connection.send(unsubscription_message)
    #         self.subscribed = False
    #         print(f"Unsubscribed from channel {self.channel_name}")
    #     except ConnectionError as e:
    #         print(f"Failed to unsubscribe from channel: {e}")


# async def test_connection():
#     # pylint: disable=missing-function-docstring

#     connection_url = "wss://ws-eu.pusher.com/app/<key>?protocol=7&client=Aiopusher&version=0.1.0"
#     connection = Connection(connection_url)

#     # Connect to the server
#     try:
#         await connection.connect()
#         print("Connection successful!")
#     except ConnectionError as err:
#         print(f"Failed to connect: {err}")
#         return

#     # If connected, try sending and receiving a message
#     if connection.connected:
#         try:
#             message = "Hello, Pusher!"
#             await connection.send(message)
#             print(f"Sent message: {message}")

#             received_message = await connection.receive()
#             print(f"Received message: {received_message}")
#         except Exception as err:
#             print(f"Failed to send/receive message: {err}")

#         # Disconnect from the server
#         await connection.disconnect()
#         print("Disconnected.")


# def print_message(message):
#     print(f"Received message: {message}")


# async def test_channel():
#     connection_url = "wss://ws-eu.pusher.com/app/e529828bbaae823d57d5?protocol=7&client=js&version=4.4.0&flash=false"
#     connection = Connection(connection_url)
#     await connection.connect()

#     # Create a channel and subscribe to it
#     channel = Channel("my-channel", connection)
#     await channel.subscribe()

#     # Bind the print_message function to an event
#     channel.bind("my-event", print_message)

#     # Listen to the channel for messages
#     await channel.listen()

#     # Unsubscribe from the channel and disconnect
#     await channel.unsubscribe()
#     await connection.disconnect()


# # Run the test
# asyncio.run(test_channel())
