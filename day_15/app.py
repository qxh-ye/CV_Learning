from flask import Flask
from flask import Response
from ultralytics import YOLO
from flask import request, redirect
import cv2
import time

app = Flask(__name__)
cap = cv2.VideoCapture(0)
prev_time = time.time()
fps = 0
frame_count = 0
# 类别
DETECT_CLASSES = [0]    # 0 = person
# 置信度

CONF = 0.35
model = YOLO("yolov8n.pt")

def generate_frames():
    global prev_time, frame_count, fps
    while True:
        success, frame = cap.read()

        if not success:
            break
        else:
            results = model(
                frame,
                conf=CONF,
                classes=DETECT_CLASSES
            )
            current_time = time.time()
            frame_count += 1
            if current_time - prev_time >= 1.0:
                fps = frame_count / (current_time - prev_time)
                frame_count = 0
                prev_time = current_time
            cv2.putText(
                frame,
                f"FPS:{fps:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            frame = results[0].plot()

            ret, buffer = cv2.imencode(".jpg", frame)       # 把opencv图片编码成jpg格式
            frame = buffer.tobytes()        # 转换成bytes字节流
            yield(
                b"--frame\r\n"      # 新的一帧开始了     
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

@app.route("/set_conf", methods=["POST"])
def set_conf():
    global CONF
    new_conf = request.form.get("conf")
    # Web输入保护
    try:
        new_conf = float(new_conf)
        if 0 <= new_conf <= 1:
            CONF = new_conf
        else:
            print("CONF 必须在0~1之间")
    except:
        print("CONF 输入错误")

    return redirect("/")

@app.route("/set_class", methods=["POST"])
def set_class():
    global DETECT_CLASSES
    cls = request.form.get("cls")
    if cls == "all":
        DETECT_CLASSES = None
    else:
        DETECT_CLASSES = [int(cls)]
    return redirect("/")

@app.route("/")
def home():
    return f"""
    <h1>YOLO Video Stream</h1>
    <form action="/set_conf" method="post">
        <label>CONF:</label>
        <input type="text" name="conf" value="{CONF}">
        <button type="submit">Update</button>
    </form>
    <form action="/set_class" method="post">
        <input type="text" name="cls" placeholder="0 person / 2 car / all">
        <button type="submit">Update Class</button>
    </form>
    <p>Current CONF: {CONF}</p>
    <p>Current Classes: {DETECT_CLASSES}</p>
    <p>Frame Count: {frame_count}</p>
    <p>Status: Running</p>
    <p>Model: YOLOv8n</p>
    <p>Mode: Web Video Stream</p>
    <img src="/video">
    """

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8080
    )