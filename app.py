import cv2
from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO, socketio
import os
import time
import base64

# camera_id = int(os.getenv("CAMERA_ID", 0))

# capture = cv2.VideoCapture(camera_id)

# if not capture.isOpened():
#     import sys, errno
#     print(f"Camera on /dev/video{camera_id} is not working or cannot be opened by cv2.")
#     sys.exit(errno.EINTR)

# capture.set(cv2.CAP_PROP_SATURATION, 28)
# capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

app = Flask("web-stream")
# socketio = SocketIO(app)

# def generate_image():
#     _, img = capture.read()
#     frame = cv2.imencode('.jpg', img)[1].tobytes()

#     frame = base64.b64encode(frame).decode('utf-8')
#     return "data:image/jpeg;base64,{}".format(frame)

# import asyncio
# import websockets


# async def produce(message, host, port):
#     async with websockets.connect(f"ws://{host}:{port}") as ws:
#         await ws.send()
#         await ws.receive()

# async def send_data():
#     while 1:
#         frame = generate_image()
#         await produce
#         # socketio.emit('server2web', {'image': frame}, namespace='/web')

#         # time.sleep(0.1)


# @socketio.on('cv2server')
# def handle_cv_message(message):
#     socketio.emit('server2web', message, namespace='/web')

from threading import Thread

# @app.route('/start_video')
# def start_video():
#     Thread(target=send_data).start()
#     return Response("200")


@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")


# @socketio.on('connect', namespace='/web')
# def connect_web():
#     print('[INFO] Web client connected: {}'.format(request.sid))


# @socketio.on('disconnect', namespace='/web')
# def disconnect_web():
#     print('[INFO] Web client disconnected: {}'.format(request.sid))


# @app.route("/")
# def index():
#     return '<html><img src="/video" /></html>'


# @app.route("/video")
# def video_feed():
#     return Response(generate_image(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0")
