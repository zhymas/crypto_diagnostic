from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import websockets

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.binance_task = asyncio.create_task(self.binance_listener(), name="binance_listener")

    async def disconnect(self, close_code):
        if hasattr(self, 'binance_task'):
            self.binance_task.cancel()
            try:
                await self.binance_task
            except asyncio.CancelledError:
                pass
        await self.close()

    async def receive(self, text_data):
        print(f'received message: {text_data}')
        await self.send(text_data=json.dumps({"message": "Received message"}))

    async def binance_listener(self):
        binance_url = "wss://fstream.binance.com/ws/btcusdt@aggTrade"
        while True:
            try:
                async with websockets.connect(binance_url) as websocket:
                    while True:

                        try:
                            data = await websocket.recv()
                            print(f'received data: {data}')
                            info = json.loads(data)
                            await self.send(text_data=json.dumps(info))
                            await asyncio.sleep(1)
                        except websockets.exceptions.ConnectionClosed:
                            print("Connection closed, attempting to reconnect...")
                            break

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(5) 
                    