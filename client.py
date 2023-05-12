import asyncio
from asyncio import StreamWriter, StreamReader
from aioconsole import ainput
from settings import HOST, PORT


class Client:
    def __init__(self, server_host: str = HOST, server_port: int = PORT) -> None:
        self.server_host = server_host
        self.server_port = server_port

    async def client_connection(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(
            self.server_host, self.server_port)
        await asyncio.gather(
            self.send_to_server(),
            self.receive_messages()
        )

    async def receive_messages(self):
        server_message = None
        while server_message != "quit":
            server_message = await self.get_from_server()
            await asyncio.sleep(0.1)
            print(f"{server_message}")

    async def get_from_server(self) -> str:
        return str((await self.reader.read(255)).decode("utf8"))

    async def send_to_server(self) -> None:
        while True:
            response = await ainput(">>> ")
            self.writer.write(response.encode('utf-8'))
            await self.writer.drain()

class Authentication:
    def __init__(self, reader: StreamReader, writer: StreamWriter, reports: int = 0) -> None:
        self.reader = reader
        self.writer = writer
        self.reports = reports
        self.nickname = 'bot'
        self.public = False

    async def get_message(self) -> str:
        return str((await self.reader.read(255)).decode('utf8'))

    def send_message(self, message: bytes) -> None:
        return self.writer.write(message)


if __name__ == '__main__':
    client = Client()
    asyncio.run(client.client_connection())
