from ultralytics import YOLO
import cv2
import time
from datetime import datetime

# 1. 加载模型
model = YOLO("yolov8n.pt")

# 2. 打开摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("摄像头打开失败，请检查摄像头编号或权限")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 25
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("fps:", fps)
print("width:", width)
print("height:", height)

# 保存
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter(
#     "data/output_result.avi",
#     fourcc,
#     fps,
#     (width, height)
# )

# 3. 创建窗口
cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
frame_id = 0
last_boxes = []
smooth_fps = 0
fps_display = 0
last_fps_time = time.time()
danger_area = (100, 100, 500, 400)
line_y = 250
in_count = 0
out_count = 0


cross_count = 0
track_history = {}
while True:
    # 4. 读取摄像头画面
    ret, frame = cap.read()
    if not ret:
        break
    frame_id += 1
    frame = cv2.resize(frame, (640, 480))
    start_time = time.time()
    # 5. YOLO检测
    if frame_id % 3 == 0:           # 每3帧检测一次
        results = model.track(frame, conf=0.35, classes=[0], persist=True)
        result = results[0]
        last_boxes = result.boxes

    person_count = 0
    dx1, dy1, dx2, dy2 = danger_area
    # 6. 遍历检测框
    for box in last_boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        # 中心点
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        # 越线显示
        if center_y > line_y:
            cv2.putText(
                frame,
                "CROSS LINE!",
                (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 255),
                3
            )

        in_area = (
                dx1 <= center_x <= dx2 and dy1 <= center_y <= dy2
        )
        if in_area:
            cv2.putText(
                frame,
                "INTRUSION!",
                (20, 170),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(
                f"alarm_images/alarm_{timestamp}.jpg",
                frame
            )
        track_id = int(box.id[0]) if box.id is not None else -1
        if track_id != -1:
            if track_id not in track_history:
                track_history[track_id] = center_y
            old_y = track_history[track_id]
            # 上 -> 下
            if old_y < line_y and center_y >= line_y:
                cross_count += 1
                print("进入+1，当前进入人数：", in_count)
            # 下 -> 上
            if old_y > line_y and center_y <= line_y:
                out_count += 1
                print("离开+1，当前离开人数：", out_count)
            track_history[track_id] = center_y

        cls_id = int(box.cls[0])
        class_name = result.names[cls_id]
        conf = float(box.conf[0])
        label = f"ID:{track_id}{class_name}: {conf:.2f}"

        if class_name == "person":
            person_count += 1
        # 画框
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # 防止文字越界
        text_y = y1 - 10
        if text_y < 20:
            text_y = y1 + 20
        # 绘制标签
        cv2.putText(
            frame,
            label,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    # 7. 显示人数
    cv2.putText(
        frame,
        f"Person Count:{person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )
    # 8. FPS
    end_time = time.time()
    time_diff = end_time - start_time
    if time_diff > 0:
        current_fps = 1 / time_diff
    else:
        current_fps = 0
    if end_time - last_fps_time >= 0.5:
        fps_display = current_fps
        last_fps_time = end_time

    cv2.putText(
        frame,
        f"FPS: {fps_display:.2f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # 9. 报警
    if person_count >= 2:
        cv2.putText(
            frame,
            "WARNING!",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
    # out.write(frame)
    # 警戒区域

    cv2.rectangle(
        frame,
        (dx1, dy1),
        (dx2, dy2),
        (0, 0, 255),
        2
    )
    cv2.putText(
        frame,
        "Danger Area",
        (dx1, dy1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.line(
        frame,
        (0, line_y),
        (640, line_y),
        (255, 0, 255),
        3
    )
    cv2.putText(
        frame,
        f"Cross Count:{cross_count}",
        (20, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        2
    )
    cv2.putText(
        frame,
        f"IN：{in_count}",
        (20, 280),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        2
    )
    cv2.putText(
        frame,
        f"OUT: {out_count}",
        (20, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        2
    )

    # 10. 显示画面
    cv2.imshow("camera", frame)

    # q 退出
    key = cv2.waitKey(10)
    if key == ord("q"):
        break
    #
# 11. 释放资源
cap.release()
# out.release()
cv2.destroyAllWindows()