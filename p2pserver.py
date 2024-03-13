import os
import asyncio
import websockets
import json

P2P_PORT = int(os.environ.get('P2P_PORT', 5001))
PEERS = os.environ.get('PEERS', '').split(',')

class P2PServer:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.sockets = []

    async def listen(self):
        server = await websockets.serve(self.handle_socket, 'localhost', P2P_PORT)
        print(f"Listening for peer to peer connection on port: {P2P_PORT}")
        await self.connect_to_peers()
        await server.wait_closed()

    async def handle_socket(self, socket, path):
        self.sockets.append(socket)
        print("Socket connected")
        await self.message_handler(socket)
        await self.send_chain(socket)

    async def connect_to_peers(self):
        for peer in PEERS:
            try:
                async with websockets.connect(peer) as socket:
                    self.sockets.append(socket)
                    print(f"Connected to peer: {peer}")
                    await self.handle_socket(socket, None)
            except websockets.exceptions.ConnectionClosedError:
                print(f"Failed to connect to peer: {peer}")

    async def message_handler(self, socket):
        try:
            async for message in socket:
                data = json.loads(message)
                print(f"Received data: {data}")
                self.blockchain.replace_chain(data)
        except websockets.exceptions.ConnectionClosed:
            self.sockets.remove(socket)
            print("Socket closed")

    async def send_chain(self, socket):
        await socket.send(json.dumps(self.blockchain.chain))

    def sync_chain(self):
        for socket in self.sockets:
            asyncio.create_task(self.send_chain(socket))

if __name__ == "__main__":
    blockchain = ... 
    p2p_server = P2PServer(blockchain)
    asyncio.get_event_loop().run_until_complete(p2p_server.listen())