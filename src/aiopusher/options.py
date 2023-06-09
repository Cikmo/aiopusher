"""A module containing the options for the client."""

from dataclasses import dataclass
from typing import Optional

from .auth.options import ChannelAuthenticationOptions, UserAuthenticationOptions


@dataclass
class PusherClientOptions:
    """A typed dict of the options."""

    channel_authorization: Optional[ChannelAuthenticationOptions] = None
    user_authorization: Optional[UserAuthenticationOptions] = None

    cluster: Optional[str] = None

    ws_host: str = "ws.pusherapp.com" if cluster is None else f"ws-{cluster}.pusher.com"
    ws_port: int = 443
    force_tls: bool = True
