from v4l2py import Device
from flask import Flask, Response
import os

camera_id = int(os.getenv("CAMERA_ID", 0))

if not os.path.exists(f"/dev/video{camera_id}"):
    import sys, errno
    print(f"Camera on /dev/video{camera_id} does not exist.")
    sys.exit(errno.EINTR)

if not Device.from_id(camera_id).video_capture:
    import sys, errno
    print(f"Camera on /dev/video{camera_id} cannot be opened by v4l2py.")
    sys.exit(errno.EINTR)

app = Flask("web-stream")


def generate_image():
    with Device.from_id(camera_id) as cam:
        cam.video_capture.set_format(1280, 980, "MJPG")
        for frame in cam:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


@app.route("/")
def index():
    return '<html><img src="/video" /></html>'


@app.route("/video")
def video_feed():
    return Response(generate_image(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0")
