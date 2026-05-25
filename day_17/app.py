import time

from flask import Flask, Response, jsonify, render_template
import cv2
import threading

from day_17.camera.camera_worker import camera_worker
from day_17.inference.yolo_worker import yolo_worker
from day_17.utils.shared_data import result_queue, status_data
from day_17.utils.logger import get_logger
from day_17.config import SLEEP_TIME


logger = get_logger("app")
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



def generate_frame():
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
        generate_frame(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/status")
def status():
    return jsonify(status_data)



if __name__ == "__main__":
    logger.info("Starting camera thread")
    threading.Thread(target=camera_worker, daemon=True).start()

    logger.info("Starting yolo thread")
    threading.Thread(target=yolo_worker, daemon=True).start()

    logger.info("Starting Flask server")



    app.run(host="0.0.0.0", port=5000, debug=False, )






