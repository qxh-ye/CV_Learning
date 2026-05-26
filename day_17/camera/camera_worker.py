import cv2
import time

from day_17.config import VIDEO_SOURCE, SLEEP_TIME
from day_17.utils.shared_data import frame_queue, status_data
from day_17.utils.logger import get_logger

logger = get_logger("camera")

def camera_worker():
    logger.info(f"Opening video source: {VIDEO_SOURCE}")
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        logger.error(f"Failed to open video source:{VIDEO_SOURCE}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.warning("Failed to read frame, reconnecting video source...")

            status_data["reconnect_count"] += 1

            cap.release()
            time.sleep(1)

            cap = cv2.VideoCapture(VIDEO_SOURCE)

            if not cap.isOpened():
                logger.error(f"Failed to open video source:{VIDEO_SOURCE}")
                time.sleep(1)
            continue
        while not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except:
                break
        frame_queue.put(frame)
        status_data["frame_queue_size"] = frame_queue.qsize()
        time.sleep(SLEEP_TIME)