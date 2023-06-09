"""Options for the user authentication."""

from dataclasses import dataclass


@dataclass
class UserAuthenticationOptions:
    """Options for the user authentication."""

    endpoint: str = "/user-auth"


@dataclass
class ChannelAuthenticationOptions:
    """Options for the channel authentication."""

    endpoint: str = "/channel-auth"
