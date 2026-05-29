import logging
import time

from flask import Flask, Response, jsonify, render_template
import cv2

from day_17.utils.logger import get_logger
from day_17.config import SLEEP_TIME
from day_17.config import HOST, PORT, DEBUG
from day_17.manager.camera_manager import CameraManager



app = Flask(__name__)
logger = get_logger("app")
logging.getLogger("werkzeug").setLevel(logging.ERROR)
manager = CameraManager()

@app.route("/")
def index():
    return render_template(
        "index.html",
        cameras=[
            context.camera_config
            for context in manager.contexts
        ]
    )

def generate_frames(stream_id):

    while True:
        context = manager.get_context(stream_id=stream_id)
        if context is None:
            time.sleep(SLEEP_TIME)
            continue

        if context.result_queue.empty():
            time.sleep(SLEEP_TIME)
            continue

        frame = context.result_queue.get()

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not ret:
           continue

        frame = buffer.tobytes()
        yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
        )

@app.route("/video/<int:stream_id>")
def video(stream_id):
    return Response(
        generate_frames(stream_id),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    context = manager.get_context(0)
    now = time.time()

    last_detect = context.last_detect_time
    if now - last_detect > 5:
        return {
            "status": "error",
            "message": "YOLO worker timeout"
        }
    return {
        "status": "ok"
    }

@app.route("/status/<int:stream_id>")
def status(stream_id):
    context = manager.get_context(stream_id=stream_id)

    if context is None:
        return jsonify({
            "status": "error",
            "message": "context not found"
        })

    return jsonify({
        "fps": context.fps,
        "frame_queue_size": context.frame_queue.qsize(),
        "result_queue_size": context.result_queue.qsize(),
        "detect_count": context.detect_count,
        "last_detect_time": context.last_detect_time,
        "reconnect_count": context.reconnect_count,
        "last_error": context.last_error,
        "source_status": context.source_status,
        "stream_id": context.camera_config["id"],
        "camera_name": context.camera_config["name"]
    })



if __name__ == "__main__":
    manager = CameraManager()
    manager.start()

    app.run(host=HOST, port=PORT, debug=DEBUG)






