from ultralytics import YOLO
import cv2
import time
# 1. 加载模型
model = YOLO("yolov8n.pt")

# 2. 打开视频
cap = cv2.VideoCapture("data/people_animal.mp4")

cv2.namedWindow("video", cv2.WINDOW_NORMAL)         # 创建一个可调整窗口
cv2.resizeWindow("video", 800, 600)                 # 设置窗口大小
# 3. 循环读取视频帧
while True:
    ret, frame = cap.read()     # 逐帧读取视频
    start_time = time.time()
    # 视频结束
    if not ret:
        break
    # 4. YOLO检测
    results = model(frame)  # results = model(frame, conf=0.35, classes=[0]
    result = results[0]

    # 5. 获取boxes
    boxes = result.boxes

    # 6. 遍历目标
    person_count = 0

    for box in boxes:
        # 坐标
        x1, y1, x2, y2 = box.xyxy[0]
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # 类别
        cls_id = int(box.cls[0])
        class_name = result.names[cls_id]
        if class_name == "person":
            person_count += 1

        # 置信度
        conf = float(box.conf[0])

        label = f"{class_name}: {conf:.2f}"

        # 画框
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        # 防止文字越界
        text_y = y1 - 10
        if text_y < 20:
            text_y = y1 + 30
        # 写文字
        cv2.putText(
            frame,
            label,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Person Count: {person_count}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        if person_count >= 2:
            cv2.putText(
                frame,
                "WARNING: Too many people!",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
    # 7. 显示视频
    cv2.imshow("video", frame)
    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
# 8. 释放资源
cap.release()
cv2.destroyAllWindows()