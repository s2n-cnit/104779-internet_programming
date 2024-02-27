import asyncio

import websockets

CONNECTIONS = set()


async def echo(websocket):
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
    async for message in websocket:
        websockets.broadcast(CONNECTIONS, message)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
