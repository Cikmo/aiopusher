"""Test PusherClient class."""
# pylint: disable=missing-function-docstring

from aiopusher.pusher_client import PusherClientOptions, PusherClient


def test_pusher_client_init():
    client = PusherClient("my_key")

    assert client.host == "ws.pusherapp.com"


def test_pusher_client_options_from_dict():
    options = {
        "cluster": "us2",
        "secure": True,
        "secret": "my_secret",
        "auth_endpoint": "my_endpoint",
        "auth_endpoint_headers": {"key": "value"},
        "user_data": {"key": "value"},
        "log_level": 10,
        "daemon": True,
        "reconnect_interval": 10,
        "custom_host": "my_host",
        "port": 8000,
        "auto_sub": False,
        "http_proxy_host": "proxy_host",
        "http_proxy_port": 8080,
        "http_no_proxy": "no_proxy",
        "http_proxy_auth": "proxy_auth",
    }

    pusher_client_options = PusherClientOptions.from_dict(options)

    for key, value in options.items():
        assert getattr(pusher_client_options, key) == value

    client = PusherClient("my_key", options=pusher_client_options)

    assert client.options.cluster == "us2"
