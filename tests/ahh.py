import pusher

pusher_client = pusher.Pusher(
    app_id="1616087",
    key="e529828bbaae823d57d5",
    secret="483d418d625fec4cca56",
    cluster="eu",
    ssl=True,
)

pusher_client.trigger("my-channel", "my-event", {"message": "hello world"})
