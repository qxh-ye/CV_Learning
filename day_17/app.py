import logging
import time

from flask import Flask, Response, jsonify, render_template
import cv2

from day_17.utils.shared_data import result_queue, status_data
from day_17.utils.logger import get_logger
from day_17.config import SLEEP_TIME, STREAM_ID, CAMERA_CONFIG
from day_17.config import HOST, PORT, DEBUG
from day_17.utils.video_utils import get_video_source
from day_17.manager.camera_manager import CameraManager


app = Flask(__name__)
logger = get_logger("app")
logging.getLogger("werkzeug").setLevel(logging.ERROR)

@app.route("/")
def index():
    return render_template("index.html", video_source=get_video_source())



def generate_frames():
    while True:
        if result_queue.empty():
            time.sleep(SLEEP_TIME)
            continue

        frame = result_queue.get()

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

@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    now = time.time()

    last_detect = status_data["last_detect_time"]
    if now - last_detect > 5:
        return {
            "status": "error",
            "message": "YOLO worker timeout"
        }
    return {
        "status": "ok"
    }

@app.route("/status")
def status():
    return jsonify({
        "fps": status_data["fps"],
        "frame_queue_size": status_data["frame_queue_size"],
        "result_queue_size": status_data["result_queue_size"],
        "detect_count": status_data["detect_count"],
        "last_detect_time": status_data["last_detect_time"],
        "reconnect_count": status_data["reconnect_count"],
        "last_error": status_data["last_error"],
        "source_status": status_data["source_status"],
        "stream_id": STREAM_ID,
        "camera_name": CAMERA_CONFIG["name"]
    })



if __name__ == "__main__":
    manager = CameraManager()
    manager.start()

    app.run(host=HOST, port=PORT, debug=DEBUG)






