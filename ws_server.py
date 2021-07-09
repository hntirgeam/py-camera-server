import asyncio
import base64
import statistics
import time

import cv2
import imutils
import websockets
from imutils.video import WebcamVideoStream
from websockets import WebSocketServerProtocol

vs = WebcamVideoStream(src=2).start()


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)

    async def send_to_clients(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws, uri):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws):
        print("distribute")
        print()
        try:
            while 1:
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                if not frame.any():
                    continue
                await asyncio.sleep(0.072)
                frame = cv2.imencode(".jpg", frame)[1].tobytes()
                message = "data:image/jpeg;base64,{}".format(base64.b64encode(frame).decode("utf-8"))

                await self.send_to_clients(message)
        except Exception as e:
            print("Disconnected")
            self.unregister(ws)

