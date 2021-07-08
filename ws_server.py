import asyncio
import websockets
from websockets import WebSocketServerProtocol
import cv2
import base64
import time
import websockets
import asyncio
import statistics
import imutils
from imutils.video import WebcamVideoStream


vs = WebcamVideoStream(src=0).start()


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
        t_i = []
        while 1:
            start = time.time()
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            frame = cv2.imencode(".jpg", frame)[1].tobytes()
            message = "data:image/jpeg;base64,{}".format(base64.b64encode(frame).decode("utf-8"))

            await self.send_to_clients(message)
            stop = time.time()

            t_i.append(1 / (stop - start))

            print(statistics.mean(t_i))


server = Server()

start_server = websockets.serve(server.ws_handler, "0.0.0.0", 5000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
