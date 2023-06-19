"""Defines the PusherClient class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from typing_extensions import Self

from . import __version__

logger = logging.getLogger(__name__)

__all__ = ["PusherClient", "PusherClientOptions"]


@dataclass
class PusherClientOptions:
    """Pusher client options."""

    # pylint: disable=too-many-instance-attributes

    cluster: str | None = None
    secure: bool = True
    secret: str | None = None
    auth_endpoint: str | None = None
    auth_endpoint_headers: dict[str, str] | None = None
    user_data: dict[str, str] | None = None
    log_level: int = logging.INFO
    daemon: bool = True
    reconnect_interval: int = 10
    custom_host: str | None = None
    port: int | None = None
    auto_sub: bool = False
    http_proxy_host: str | None = None
    http_proxy_port: int = 0
    http_no_proxy: str | None = None
    http_proxy_auth: str | None = None

    @classmethod
    def from_dict(cls, options: dict[str, Any]) -> Self:
        """Return PusherClientOptions from a dict.

        Args:
            options: The options. See :class:`PusherClientOptions`.

        Returns:
            Self: The PusherClientOptions.
        """
        return cls(**options)


class PusherClient:
    """The PusherClient class."""

    # pylint: disable=too-many-instance-attributes
    # For now, we'll do it this way. Perhaps later we'll move some of these to
    # some option classes or something.

    host = "ws.pusherapp.com"
    client_id = "Aiopusher"
    protocol = 6

    def __init__(
        self,
        app_key: str,
        *,
        options: PusherClientOptions | None = None,
    ):
        """Initialise the PusherClient.

        Args:
            app_key: The Pusher app key.
            options: The PusherClientOptions. Defaults to None.
        """

        if options is None:
            options = PusherClientOptions()

        # If a cluster is specified, use it to build the host. Otherwise, use the default.
        if options.cluster:
            self.host = f"ws-{options.cluster}.pusher.com"

        self.app_key = app_key
        self.secret = options.secret or ""
        self.auth_endpoint = options.auth_endpoint
        self.auth_endpoint_headers = options.auth_endpoint_headers or {}

        self.user_data = options.user_data or {}

        self.channels: dict[str, Any] = {}  # TODO: Channel type pylint: disable=fixme
        self.url = self._build_url(options.secure, options.port, options.custom_host)

        # TODO: Implement Connection class pylint: disable=fixme
        # reconnect_handler = self._reconnect_handler if options.auto_sub else None

        # self.connection = Connection(self._connection_handler, self.url,
        #                              reconnect_handler=reconnect_handler,
        #                              log_level=log_level,
        #                              daemon=daemon,
        #                              reconnect_interval=reconnect_interval,
        #                              socket_kwargs=dict(http_proxy_host=http_proxy_host,
        #                                                 http_proxy_port=http_proxy_port,
        #                                                 http_no_proxy=http_no_proxy,
        #                                                 http_proxy_auth=http_proxy_auth,
        #                                                 ping_timeout=100),
        #                              **thread_kwargs)

    @property
    def app_key_as_bytes(self) -> bytes:
        """The app key as bytes."""
        return (
            self.app_key
            if isinstance(self.app_key, bytes)
            else self.app_key.encode("UTF-8")
        )

    @property
    def secret_as_bytes(self) -> bytes:
        """The app secret as bytes."""
        return (
            self.secret
            if isinstance(self.secret, bytes)
            else self.secret.encode("UTF-8")
        )

    async def connect(self) -> None:
        """Connect to Pusher."""

    async def disconnect(self) -> None:
        """Disconnect from Pusher."""

    async def subscribe(self, channel_name: str) -> None:
        """Subscribe to a channel."""

    async def unsubscribe(self, channel_name: str) -> None:
        """Unsubscribe from a channel."""

    async def _reconnect_handler(self):
        """Handle a reconnect."""
        # for channel_name, channel in self.channels.items():
        #     data = {'channel': channel_name}

        #     if channel.auth:
        #         data['auth'] = channel.auth

        #     self.connection.send_event('pusher:subscribe', data)

    def _build_url(
        self,
        secure: bool = True,
        port: int | None = None,
        custom_host: str | None = None,
    ):
        """Build the connection URL."""

        # Example URL: ws://ws-ap1.pusher.com:80/app/APP_KEY?client=js&version=7.0.3&protocol=5

        path = (
            f"/app/{self.app_key}?client={self.client_id}"
            f"&version={__version__}&protocol={self.protocol}"
        )

        proto = "wss" if secure else "ws"

        host = custom_host or self.host
        if not port:
            port = 443 if secure else 80

        return f"{proto}://{host}:{port}{path}"
