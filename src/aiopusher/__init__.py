"""aiopusher is an async client for Pusher."""


from typing_extensions import Self


def __version__():
    return "0.1.0"


class Blah:
    """Blah blah blah."""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Blah({self.name})"

    def return_self(self) -> Self:
        """Return self."""
        return self


one = Blah("one")

two = one.return_self().return_self()
