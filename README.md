# aiopusher

[![PyPI](https://img.shields.io/pypi/v/aiopusher)](https://pypi.org/project/aiopusher/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/aiopusher.svg)](https://pypi.org/project/aiopusher/)
[![check](https://github.com/Cikmo/aiopusher/actions/workflows/tests.yml/badge.svg)](https://github.com/Cikmo/aiopusher/actions/workflows/tests.yml/)

An async library for subscribing to the Pusher WebSocket protocol.

## Installation

You can install `aiopusher` via pip from PyPI:

```bash
pip install aiopusher
```

Or with [Poetry](https://python-poetry.org/):

```bash
poetry add aiopusher
```

## Usage

Here are some examples of using `aiopusher`:

```python
import asyncio
from aiopusher import Pusher

async def main():
    async with Pusher('<your-app-key>') as client:
        channel = await client.subscribe('<channel-name>')
        channel.bind('<event-name>', lambda data: print(data))

        # Run forever (or until manually stopped)
        while True:
            await asyncio.sleep(1)

asyncio.run(main())
```

Or, if you don't want to use context manager, you can use `connect` and `disconnect` methods

```python
async def main():
    client =  Pusher('<your-app-key>')
    await client.connect()

    channel = await client.subscribe('<channel-name>')
    channel.bind('<event-name>', lambda data: print(data))

    while True:
        await asyncio.sleep(1)
    
    await client.disconnect() # Yes, I know this cannot technically be reached
```

You can also use decorators to bind events

```python
import asyncio
from aiopusher import Pusher

client = Pusher('<your-app-key>')

@client.event('<channel-name>', '<event-name>')
async def handle_event(data):
    print(data)

async def main():
    await client.connect()

    # Run forever (or until manually stopped)
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
```

Connect to different endpoints

```python
import asyncio
from aiopusher import Pusher

async def main():
    options = {
        host: 'api.example.com', # default: 'ws.pusherapp.com'
        "userAuthentication": {
            "endpoint": "/auth",
            "transport": "ajax",
        }
    }

    async with Pusher('<your-app-key>', options) as client:
        channel = await client.subscribe('<channel-name>')
        channel.bind('<event-name>', lambda data: print(data))

        # Run forever (or until manually stopped)
        while True:
            await asyncio.sleep(1)

asyncio.run(main())
```

You can also make a singleton client, which can be accessed from anywhere in your code

```python
import asyncio
from aiopusher import Pusher, SingletonClient

async def main():
    client = Pusher('<your-app-key>')
    SingletonClient.set_client(client)
    await client.connect()

    channel = await SingletonClient.get_client().subscribe('<channel-name>')
    channel.bind('<event-name>', lambda data: print(data))

    while True:
        await asyncio.sleep(1)
```

---

## Contributing

If you want to contribute to this project, please read [CONTRIBUTING.md](CONTRIBUTING.md).
