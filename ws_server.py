import asyncio
import base64
import statistics
import time

import cv2
import imutils
import websockets
from imutils.video import WebcamVideoStream
from websockets import WebSocketServerProtocol
import os

camera_id = int(os.getenv("CAMERA_ID", 2))

vs = WebcamVideoStream(src=camera_id).start()

if not vs.grabbed:
    import sys, errno

    print(f"Camera on /dev/video{camera_id} is not working or cannot be opened.")
    sys.exit(errno.EINTR)


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
        prev_msg = None
        while 1:
            if self.clients:
                frame = vs.read()

                if not frame.any():
                    continue

                frame = cv2.imencode(".jpg", frame)[1].tobytes()
                message = "data:image/jpeg;base64,{}".format(base64.b64encode(frame).decode("utf-8"))

                if prev_msg:
                    if message == prev_msg:
                        pass
                    else:
                        await self.send_to_clients(message)

                prev_msg = message
