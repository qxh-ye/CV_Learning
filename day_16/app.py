from flask import Flask, Response, jsonify
from ultralytics import YOLO
import cv2
import threading
import queue
import time

frame_queue = queue.Queue(maxsize=5)        # 原始摄像头帧
result_queue = queue.Queue(maxsize=5)       # YOLO处理结果

app = Flask(__name__)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
model = YOLO("yolov8n.pt")

fps = 0
frame_count = 0
last_fps_time = time.time()



def camera_worker():
    while True:
        success, frame = cap.read()
        if not success:
            time.sleep(0.01)
            continue
        if frame_queue.full():
            frame_queue.get()
        frame_queue.put(frame)


def yolo_worker():

    while True:
        if frame_queue.empty():
            time.sleep(0.01)
            continue
        frame = frame_queue.get()
        results = model(
            frame,
            conf=0.35,
            classes=[0],
            imgsz=320
        )
        result_frame = results[0].plot()
        while result_queue.qsize() > 0:
            result_queue.get()
        result_queue.put(result_frame)


def generate_frame():
    global fps, frame_count, last_fps_time
    while True:
        if result_queue.empty():
            time.sleep(0.01)
            continue
        frame = result_queue.get()
        frame_count += 1
        current_time = time.time()
        if current_time - last_fps_time >= 1.0:
            fps = frame_count / (current_time - last_fps_time)
            frame_count = 0
            last_fps_time = current_time
        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )
        frame = buffer.tobytes()
        yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
        )



camera_thread = threading.Thread(target=camera_worker)
camera_thread.daemon = True
camera_thread.start()
yolo_thread = threading.Thread(target=yolo_worker)
yolo_thread.daemon = True
yolo_thread.start()

@app.route("/")
def home():

    return """

    <html>

    <body>

        <h1>Day16 Multi Thread YOLO</h1>

        <p id="fps">FPS:</p>

        <p id="frame_queue">
        Frame Queue:
        </p>

        <p id="result_queue">
        Result Queue:
        </p>

        <img src="/video">

        <script>

        async function updateStatus() {

            const response =
            await fetch('/status');

            const data =
            await response.json();

            document.getElementById(
                "fps"
            ).innerText =
            "FPS: " + data.fps;

            document.getElementById(
                "frame_queue"
            ).innerText =
            "Frame Queue: "
            + data.frame_queue;

            document.getElementById(
                "result_queue"
            ).innerText =
            "Result Queue: "
            + data.result_queue;
        }

        setInterval(
            updateStatus,
            1000
        );

        </script>

    </body>

    </html>

    """

@app.route("/video")
def video():
    return Response(
        generate_frame(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/status")
def status():
    return jsonify({
        "frame_queue": frame_queue.qsize(),
        "result_queue": result_queue.qsize(),
        "fps": round(fps, 2)
    })


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)