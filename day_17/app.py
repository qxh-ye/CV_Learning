import logging
import time
import os
import psutil

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
manager.start()
process = psutil.Process(os.getpid())
process.cpu_percent(interval=None)


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

@app.route("/logs")
def get_logs():
    log_path = os.path.join(
        os.path.dirname(__file__),
        "logs",
        "system.log"
    )
    if not os.path.exists(log_path):
        return jsonify({
            "logs": []
        })
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-30:]
    return jsonify({
        "logs": lines
    })

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

    uptime = int(time.time() - context.start_time)

    memory_mb = round(process.memory_info().rss / 1024 / 1024, 2)
    current_cpu = psutil.cpu_percent(interval=None)
    context.system_cpu = round(
        context.system_cpu * 0.8 + current_cpu * 0.2
    )
    current_process_cpu = process.cpu_percent(interval=None)
    context.process_cpu = round(
        context.process_cpu * 0.8 + current_process_cpu * 0.2
    )

    average_read_fps = round(
        context.read_frames / uptime,
        2
    )if uptime > 0 else 0

    average_infer_fps = round(
        context.infer_frames / uptime,
        2
    )if uptime > 0 else 0

    detect_rate = round(
        context.detect_count / context.infer_frames,
        2
    )if context.infer_frames > 0 else 0

    if context.source_status != "running":
        health_status = "ERROR"
    elif context.last_error:
        health_status = "WARNING"
    elif average_infer_fps < 5:
        health_status = "WARNING"
    else:
        health_status = "OK"

    if context.last_detect_time:
        last_detect_time_text = time.strftime(
            "%H:%M:%S",
            time.localtime(context.last_detect_time)
        )
    else:
        last_detect_time_text = "None"

    uptime_minute = round(uptime / 60, 2)

    detect_per_second = round(
        context.detect_count / uptime,
        2
    )if uptime > 0 else 0

    warning_message = ""

    if average_infer_fps < 10:
        warning_message = "LOW_FPS"
    if context.reconnect_count > 5:
        warning_message = "TOO_MANY_RECONNECT"
    if memory_mb > 1000:
        warning_message = "HIGH_MEMORY_USAGE"

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
        "camera_name": context.camera_config["name"],
        "uptime": uptime,
        "process_cpu": context.process_cpu,
        "system_cpu": context.system_cpu,
        "memory_mb": memory_mb,
        "inference_time": context.inference_time,
        "read_frames": context.read_frames,
        "average_read_fps": average_read_fps,
        "infer_frames": context.infer_frames,
        "average_infer_fps": average_infer_fps,
        "detect_rate": detect_rate,
        "health_status": health_status,
        "last_detect_time_text": last_detect_time_text,
        "start_datetime": context.start_datetime,
        "uptime_minute": uptime_minute,
        "detect_per_second": detect_per_second,
        "warning_message": warning_message
    })



if __name__ == "__main__":
    manager = CameraManager()


    app.run(host=HOST, port=PORT, debug=DEBUG)






