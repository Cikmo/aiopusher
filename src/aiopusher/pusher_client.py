"""Defines the PusherClient class."""

from dataclasses import dataclass, fields
from typing import Optional, Any


@dataclass
class PusherClientOptions:
    """A typed dict of the options."""

    host: str = "ws.pusherapp.com"
    port: int = 443


class PusherClient:
    """Pusher client."""

    def __init__(
        self,
        app_key: str,
        *,
        options: Optional[PusherClientOptions] = None,
        **kwargs: Any,
    ):
        """Initialise the PusherClient.

        Args:
            app_key: The Pusher app key.
            options: The PusherClientOptions. Defaults to None. Mutually
                exclusive with kwargs.
            **kwargs: The PusherClientOptions as keyword arguments. Defaults to None.
                Mutually exclusive with options.

        Raises:
            ValueError: If both options and kwargs are given. Only one way of
                providing options is allowed.
        """

        # Rejecting scenario when both options and kwargs are given
        # to avoid potential unexpected behaviour (e.g. kwargs overwriting options or vice versa)
        if kwargs:
            if options is not None:
                raise ValueError(
                    "Cannot provide both options object and keyword arguments."
                    " Please use one or the other."
                )

            # Ensuring that all the kwargs provided are actually valid
            # options that can be used with this class
            for key in kwargs:
                if key not in [field.name for field in fields(PusherClientOptions)]:
                    raise ValueError(
                        f"Invalid keyword argument {key}. Please see"
                        " PusherClientOptions for valid options."
                    )

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
