# inference/yolo_worker.py
import time
from ultralytics import YOLO

from day_17.config import MODEL_PATH, CONF, IMG_SIZE, SLEEP_TIME, STREAM_ID, CAMERA_CONFIG
from day_17.utils.shared_data import frame_queue, result_queue, status_data
from day_17.utils.logger import get_logger


def get_latest_frame():
    frame = None

    while not frame_queue.empty():
        frame = frame_queue.get()

    return frame


logger = get_logger("yolo")
def yolo_worker(camera_config):
    logger.info(
        f"[Stream {camera_config['id']}] "
        f"[{camera_config['name']}] "
        "Loading YOLO model"
    )
    model = YOLO(MODEL_PATH)
    logger.info(
        f"[Stream {camera_config['id']}] "
        f"[{camera_config['name']}] "
        "YOLO model loaded"
    )

    last_time = time.time()
    detect_count = 0

    while True:
        if frame_queue.empty():
            time.sleep(SLEEP_TIME)
            continue
        frame = get_latest_frame()
        if frame is None:
            time.sleep(SLEEP_TIME)
            continue
        try:
            results = model(
                frame,
                conf=CONF,
                imgsz=IMG_SIZE,
                verbose=False
            )
            annotated_frame = results[0].plot()
        except Exception as e:
            logger.error(f"YOLO inference failed: {e}")
            time.sleep(SLEEP_TIME)
            continue

        if result_queue.full():
            try:
                result_queue.get_nowwait()
            except:
                pass
        result_queue.put(annotated_frame)

        detect_count += 1
        if detect_count % 30 == 0:
            logger.info(
                f"[Stream {camera_config['id']}] "
                f"[{camera_config['name']}] "
                f"fps={status_data['fps']} |"
                f"frame_queue={frame_queue.qsize()} |"
                f"result_queue={result_queue.qsize()} |"
                f"detect_count={detect_count}"
            )
        status_data["last_detect_time"] = time.time()
        now = time.time()

        fps = 1 / (now - last_time)
        last_time = now

        status_data["fps"] = round(fps, 2)
        status_data["result_queue_size"] = result_queue.qsize()
        status_data["detect_count"] = detect_count

