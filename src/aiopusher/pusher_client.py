"""Defines the PusherClient class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Union, get_args, get_origin

from typing_extensions import Self

logger = logging.getLogger(__name__)


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
    port: int = 443
    reconnect_interval: int = 10
    custom_host: str | None = None
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
        # validate type of all options
        for key, value in options.items():
            if (type_hint := cls.__annotations__.get(key)) is not None:
                validate_type(value, type_hint)
        return cls(**options)


class PusherClient:
    """The PusherClient class."""

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

        self.app_key = app_key
        self.options = options

    # --- Boilerplate ---

    def __repr__(self) -> str:
        return f"PusherClient(app_key={self.app_key}, " f"options={repr(self.options)})"

    def __str__(self) -> str:
        return f"App key: {self.app_key}, " f"Options: {self.options.__dict__}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PusherClient):
            return NotImplemented
        return self.app_key == other.app_key and self.options == other.options

    def __hash__(self) -> int:
        return hash((self.app_key, self.options))

    # --- End of boilerplate ---

    async def connect(self) -> None:
        """Connect to Pusher."""

    async def disconnect(self) -> None:
        """Disconnect from Pusher."""

    async def subscribe(self, channel_name: str) -> None:
        """Subscribe to a channel."""

    async def unsubscribe(self, channel_name: str) -> None:
        """Unsubscribe from a channel."""


def validate_type(value: Any, type_hint: Any):
    """Validate the type of a value.

    Args:
        value (Any): The value to validate.
        type_hint (Any): The type hint to validate against.

    Raises:
        TypeError: If the type of the value does not match the type hint.
        TypeError: If the type hint is not a valid type hint.
    """
    if get_origin(type_hint) is Union:
        allowed_types = get_args(type_hint)
        if not isinstance(value, allowed_types):
            raise TypeError(f"Expected {allowed_types}, got {type(value)}")
    elif not isinstance(value, type_hint):  # pylint: disable=confusing-consecutive-elif
        raise TypeError(f"Expected {type_hint}, got {type(value)}")