from typing import Any, Awaitable, Callable, Dict, Tuple, Union

from .connection import Connection

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


# async def test_channel():
#     connection_url = "wss://ws-eu.pusher.com/app/xxx?protocol=7&client=Aiopusher&version=0.1.0"
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
