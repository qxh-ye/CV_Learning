import cv2
import time

from day_17.config import CAMERA_ID, SLEEP_TIME
from day_17.utils.shared_data import frame_queue, status_data
from day_17.utils.logger import get_logger

logger = get_logger("camera")

def camera_worker():
    cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
    logger.info("Camera worker started")
    while True:
        ret, frame = cap.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
            continue
        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except:
                pass
        frame_queue.put(frame)
        status_data["frame_queue_size"] = frame_queue.qsize()
        time.sleep(SLEEP_TIME)