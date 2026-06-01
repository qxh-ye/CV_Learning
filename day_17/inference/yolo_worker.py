# inference/yolo_worker.py
import time
from ultralytics import YOLO

from day_17.config import MODEL_PATH, CONF, IMG_SIZE, SLEEP_TIME, DETECT_INTERVAL
from day_17.utils.logger import get_logger



def get_latest_frame(context):
    frame = None

    while not context.frame_queue.empty():
        frame = context.frame_queue.get()

    return frame


logger = get_logger("yolo")
def yolo_worker(context):
    camera_config = context.camera_config
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
    frame_id = 0
    while context.running:
        if context.frame_queue.empty():
            time.sleep(SLEEP_TIME)
            continue
        frame = get_latest_frame(context)

        if frame is None:
            time.sleep(SLEEP_TIME)
            continue

        frame_id += 1
        if frame_id % DETECT_INTERVAL != 0:
            time.sleep(SLEEP_TIME)
            continue

        start = time.time()

        try:
            results = model(
                frame,
                conf=CONF,
                imgsz=IMG_SIZE,
                verbose=False
            )
            end = time.time()
            context.inference_time = round(
                (end - start) * 1000,
                2
            )
            annotated_frame = results[0].plot()
            context.infer_frames += 1
        except Exception as e:
            logger.error(f"YOLO inference failed: {e}")
            time.sleep(SLEEP_TIME)
            continue

        while not context.result_queue.empty():
            try:
                context.result_queue.get(False)
            except Exception as e:
                logger.error(f"Result queue error: {e}")
                break
        context.result_queue.put(annotated_frame)

        now = time.time()
        delta = now - last_time
        if delta > 0:
            context.fps = round(1 / delta, 2)

        last_time = now
        if context.detect_count % 30 == 0:
            logger.info(
                f"[Stream {camera_config['id']}] "
                f"[{camera_config['name']}] "
                f"fps={context.fps} |"
                f"frame_queue={context.frame_queue.qsize()} |"
                f"result_queue={context.result_queue.qsize()} |"
                f"detect_count={context.detect_count}"
            )

        context.detect_count += 1
        context.last_detect_time = time.time()
        context.frame_queue_size = context.frame_queue.qsize()
        context.result_queue_size = context.result_queue.qsize()

    logger.info(
        f"[Stream {context.camera_config['id']}] "
        f"[{context.camera_config['name']}] "
        "yolo worker stopped"
    )
