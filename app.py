import asyncio

from flask import Flask, Response, render_template, request
import threading
import ws_server as ws


app = Flask("web-stream")


@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")


def start_ws_server(loop):
    asyncio.set_event_loop(loop)
    server = ws.Server()
    start_server = ws.websockets.serve(server.ws_handler, "0.0.0.0", 5000)
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    threading.Thread(target=start_ws_server, args=(loop,)).start()
    app.run(threaded=True, host="0.0.0.0", port=8000)
