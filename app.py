import cv2
from flask import Flask, Response
from imutils.video import VideoStream
import time

import os
camera_id = int(os.getenv("CAMERA_ID", 0))

import statistics

cap = cv2.VideoCapture(camera_id)

app = Flask(__name__)

vs = VideoStream(src=camera_id).start()

def generate():
    t_time = []
    while True:
        start = time.time()
        ret, img = cap.read()
        flag, encodedImage = cv2.imencode(".jpeg", img)
        stop = time.time()

        t_time.append(stop - start)
        print(1 / statistics.mean(t_time))

        if len(t_time) > 10000:
            t_time.clear()
        
        if not flag:
            continue
        # time.sleep(0.001)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0")

