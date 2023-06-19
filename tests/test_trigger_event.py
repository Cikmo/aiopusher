"""Test trigger event to pusher channel"""

from .pusher_trigger_event import trigger_event


def test_trigger_event():
    """Test trigger event to pusher channel"""
    channel = "my-channel"
    event = "my-event"
    data = {"message": "hello world"}
    trigger_event(channel, event, data)
