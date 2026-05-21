from ultralytics import YOLO
import cv2
import time

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



fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(
    "data/output_result.avi",
    fourcc,
    fps,
    (width, height)
)

# 3. 创建窗口
cv2.namedWindow("camera", cv2.WINDOW_NORMAL)

while True:
    # 4. 读取摄像头画面
    ret, frame = cap.read()
    if not ret:
        break
    start_time = time.time()
    # 5. YOLO检测
    results = model(frame, conf=0.35, classes=[0])
    result = results[0]
    boxes = result.boxes

    person_count = 0
    # 6. 遍历检测框
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        cls_id = int(box.cls[0])
        class_name = result.names[cls_id]
        conf = float(box.conf[0])
        label = f"{class_name}: {conf:.2f}"

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
    fps = 1 / (end_time - start_time)
    cv2.putText(
        frame,
        f"FPS: {fps:.2f}",
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
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
    out.write(frame)
    # 10. 显示画面
    cv2.imshow("camera", frame)

    # q 退出
    key = cv2.waitKey(10)
    if key == ord("q"):
        break
    #
# 11. 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()