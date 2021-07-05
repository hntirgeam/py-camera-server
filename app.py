import cv2
from flask import Flask, Response
import os

camera_id = int(os.getenv("CAMERA_ID", 0))

capture = cv2.VideoCapture(camera_id)

if not capture.isOpened():
    import sys, errno
    print(f"Camera on /dev/video{camera_id} is not working or cannot be opened by cv2.")
    sys.exit(errno.EINTR)

capture.set(cv2.CAP_PROP_SATURATION, 28)
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

app = Flask("web-stream")


def generate_image():
    while True:
        _, img = capture.read()
        flag, encodedImage = cv2.imencode(".jpg", img)

        if not flag:
            continue

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + bytearray(encodedImage) + b"\r\n")


@app.route("/")
def index():
    return '<html><img src="/video" /></html>'


@app.route("/video")
def video_feed():
    return Response(generate_image(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0")
