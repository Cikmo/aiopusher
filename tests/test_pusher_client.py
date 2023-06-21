"""Test PusherClient class."""
# pylint: disable=missing-function-docstring

from __future__ import annotations

from typing import Any

import pytest

from aiopusher import __version__ as aiopusher_version
from aiopusher.pusher_client import PusherClient, PusherClientOptions

DEFAULT_HOST = "ws.pusherapp.com"
CUSTOM_HOST = "example.com"
CLUSTER = "us2"
HOST_WITH_CLUSTER = f"ws-{CLUSTER}.pusher.com"
TEST_KEY = "my_key"
CLIENT_ID = "Aiopusher"


@pytest.fixture(name="default_pusher_client")
def fixture_default_pusher_client():
    return PusherClient(TEST_KEY)


@pytest.fixture(name="pusher_client_with_options")
def fixture_pusher_client_with_options():
    return PusherClient(TEST_KEY, options=PusherClientOptions(cluster=CLUSTER))


@pytest.fixture(name="pusher_client_custom_host")
def fixture_pusher_client_custom_host():
    return PusherClient(TEST_KEY, options=PusherClientOptions(custom_host=CUSTOM_HOST))


def test_init_default_options(default_pusher_client: PusherClient):
    """Tests initialization with default options."""
    assert default_pusher_client.host == DEFAULT_HOST
    assert default_pusher_client.CLIENT_ID == CLIENT_ID
    assert default_pusher_client.app_key == TEST_KEY


def test_init_with_options(pusher_client_with_options: PusherClient):
    """Tests initialization with specific options."""
    assert pusher_client_with_options.host == HOST_WITH_CLUSTER
    assert pusher_client_with_options.CLIENT_ID == CLIENT_ID
    assert pusher_client_with_options.app_key == TEST_KEY


@pytest.mark.parametrize(
    "options_dict, expected_attributes",
    [
        (
            {"cluster": CLUSTER, "secure": True, "secret": "my_secret"},
            {"cluster": CLUSTER, "secure": True, "secret": "my_secret"},
        ),
        ({}, {}),
    ],
)
def test_init_options_from_dict(
    options_dict: dict[str, Any], expected_attributes: dict[str, Any]
):
    """Test initialization of PusherClientOptions from a dictionary."""
    pusher_client_options = PusherClientOptions.from_dict(options_dict)

    for key, value in expected_attributes.items():
        assert getattr(pusher_client_options, key) == value


def test_init_custom_host(pusher_client_custom_host: PusherClient):
    """Tests initialization with a custom host."""
    assert pusher_client_custom_host.DEFAULT_HOST == DEFAULT_HOST
    assert pusher_client_custom_host.options.custom_host == CUSTOM_HOST


@pytest.mark.parametrize(
    "custom_host, secure, port, expected_url",
    [
        (
            None,
            True,
            None,
            f"wss://{DEFAULT_HOST}:443/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
        (
            None,
            False,
            None,
            f"ws://{DEFAULT_HOST}:80/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
        (
            CUSTOM_HOST,
            True,
            None,
            f"wss://{CUSTOM_HOST}:443/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
        (
            CUSTOM_HOST,
            False,
            None,
            f"ws://{CUSTOM_HOST}:80/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
        (
            None,
            True,
            8080,
            f"wss://{DEFAULT_HOST}:8080/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
        (
            CUSTOM_HOST,
            False,
            8080,
            f"ws://{CUSTOM_HOST}:8080/app/{TEST_KEY}?client={PusherClient.CLIENT_ID}"
            f"&version={aiopusher_version}&protocol={PusherClient.PROTOCOL}",
        ),
    ],
)
def test_build_url(
    custom_host: str | None, secure: bool, port: int | None, expected_url: str
):
    """Test _build_url method. Check that the url is built correctly based on
    the custom_host, secure and port options.
    """
    options = PusherClientOptions(custom_host=custom_host, secure=secure, port=port)
    client = PusherClient(TEST_KEY, options=options)
    assert client._build_url() == expected_url  # type: ignore # pylint: disable=protected-access
