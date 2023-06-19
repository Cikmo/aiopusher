"""Trigger event to pusher channel

This module is used to trigger event to pusher channel for testing purpose.
A pusher account is required to run this module, and the credentials should be
set in a `.test.env` file in the tests directory with the following format:

```
PUSHER_APP_ID=your_app_id
PUSHER_KEY=your_key
PUSHER_SECRET=your_secret
PUSHER_CLUSTER=your_cluster
```

If you are running the tests in a CI environment like GitHub Actions, you can
set the environment variable `DONT_USE_ENV_FILE` to `True` to use the credentials
set in the environment variables directly, and skip the `.test.env` file.
"""

from __future__ import annotations

import os
from typing import Any

import pusher  # type: ignore - Pusher is not a typed library
from dotenv import load_dotenv

# load environment variables. If DONT_USE_ENV_FILE is set to True, then the
# environment variables will be loaded from the environment variables directly
use_env_file = os.getenv("DONT_USE_ENV_FILE")
if not use_env_file or use_env_file.lower() != "true":
    load_dotenv(dotenv_path="tests/.test.env")


pusher_client = pusher.Pusher(
    app_id=os.getenv("PUSHER_APP_ID"),
    key=os.getenv("PUSHER_KEY"),
    secret=os.getenv("PUSHER_SECRET"),
    cluster=os.getenv("PUSHER_CLUSTER"),
    ssl=True,
)


def trigger_event(channel: str, event: str, data: dict[str, Any]):
    """trigger event to pusher channel"""
    pusher_client.trigger(channel, event, data)  # type: ignore
