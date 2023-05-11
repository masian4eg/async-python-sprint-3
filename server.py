import asyncio
import logging

import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Server:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logger.info(f"{ws.remote_address} connects.")

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logger.info(f"{ws.remote_address} disconnects.")

    async def send_message(self, message: str = ""):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        await self.distribute(ws)
        # try:
        #     await self.distribute(ws)
        # finally:
        #     await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_message(message)

    # async def serve(self):
    #     await websockets.serve(self.ws_handler, self.host, self.port)
    #
    # def listen(self):
    #     event_loop = asyncio.get_event_loop()
    #     event_loop.run_until_complete(self.serve())
    #     event_loop.run_forever()


if __name__ == "__main__":
    server = Server()
    # server.listen()
    start_server = websockets.serve(server.ws_handler, "127.0.0.1", 8000)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server)
    event_loop.run_forever()
