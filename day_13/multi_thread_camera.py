import cv2
import threading
import time
from queue import Queue
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

frame_queue = Queue(maxsize=5)
result_queue = Queue(maxsize=5)
track_history = {}
track_lost_count = {}

cap = cv2.VideoCapture(0)
running = True
def camera_worker():
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_queue.full():
            frame_queue.get()
        frame_queue.put(frame)
            # print("生产 frame")

detect_intarval = 2
frame_id = 0
last_result_frame = None

def yolo_worker():
    global frame_id, last_result_frame
    while running:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame_id += 1
            if frame_id % detect_intarval == 0:     # 隔2帧检测一次
                results = model.track(
                    frame,
                    persist=True,  # 记住上一帧目标
                    conf=0.35,
                    classes=[0],
                    imgsz=320
                )

                current_ids = set()

                result = results[0]
                result_frame = results[0].plot()
                boxes = result.boxes

                for box in boxes:
                    if box.id is not None:
                        track_id = int(box.id[0])
                        current_ids.add(track_id)       # 当前帧

                        x1, y1, x2, y2 = box.xyxy[0]
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)
                        cv2.circle(
                            result_frame,
                            (center_x, center_y),
                            8,
                            (255, 0, 0),
                            -1          # 实心  2：空心
                        )
                        if track_id not in track_history:
                            track_history[track_id] = []
                        track_history[track_id].append((center_x, center_y))

                        if len(track_history[track_id]) > 30:
                            track_history[track_id].pop(0)

                        points = track_history[track_id]
                        for i in range(1, len(points)):
                            cv2.line(
                                result_frame,
                                points[i - 1],         # 起点
                                points[i],             # 终点
                                (0, 0, 255),
                                5
                            )

                        print(track_id)
                for tid in list(track_history.keys()):
                    if tid not in current_ids:
                        track_lost_count[tid] = track_lost_count.get(tid, 0) + 1

                        if track_lost_count[tid] > 30:
                            del track_history[tid]
                            del track_lost_count[tid]
                    else:
                        track_lost_count[tid] = 0

                last_result_frame = result_frame
            else:
                if last_result_frame is not None:
                    result_frame = last_result_frame
                else:
                    result_frame = frame

            if not result_queue.full():
                    result_queue.put(result_frame)



t1 = threading.Thread(target=camera_worker)
t1.start()
t2 = threading.Thread(target=yolo_worker)
t2.start()


fps = 0
fps_display = 0
frame_count = 0
last_fps_time = time.time()
while True:
    if not result_queue.empty():
        frame = result_queue.get()
        cv2.putText(
            frame,
            f"Queue:{frame_queue.qsize()}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Interval: {detect_intarval}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"imgse: 320",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        frame_count += 1
        current_time = time.time()
        if current_time - last_fps_time >= 1.0:
            fps_display = frame_count / (current_time - last_fps_time)
            frame_count = 0
            last_fps_time = current_time


        cv2.putText(
            frame,
            f"FPS: {fps_display:.2f}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("camera", frame)
    key = cv2.waitKey(1)
    if key == ord("s"):
        cv2.imwrite("screenshot.jpg", frame)
        print("截图已保存")
    if key == ord("q"):
        running = False
        break
t1.join()
t2.join()
cap.release()
cv2.destroyAllWindows()
