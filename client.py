import asyncio
import logging

import websockets
from websockets import WebSocketClientProtocol
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, server_host="127.0.0.1", server_port=8000):
        self.server_host = server_host
        self.server_port = server_port

    # async def handler(self, websocket: WebSocketClientProtocol) -> None:
    #     async for message in websocket:
    #         logger.info(f"Message: {message}")

    async def send(self):
        # msg = input("msg: ")
        # async with websockets.connect(f"ws://{self.server_host}:{self.server_port}") as socket:
        #     await socket.send(msg)
        #     await socket.recv()
        session = aiohttp.ClientSession()
        async with session.ws_connect(f"ws://{self.server_host}:{self.server_port}") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        await ws.send_str(msg.data + '/answer')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

    # def run(self):
    #     event_loop = asyncio.get_event_loop()
    #     event_loop.run_until_complete(self.send())
    #     event_loop.run_forever()


if __name__ == "__main__":
    client = Client()
    # client.run()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(client.send())
    event_loop.run_forever()
