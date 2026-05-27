import cv2
import time

from day_17.config import VIDEO_SOURCE, SLEEP_TIME, VIDEO_TYPE, RECONNECT_DELAY, RTSP_URL
from day_17.utils.shared_data import frame_queue, status_data
from day_17.utils.logger import get_logger

logger = get_logger("camera")

def open_video_capture():

    source = get_video_source()
    logger.info(f"Opening {VIDEO_TYPE} source: {source}")

    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return cap

def get_video_source():
    if VIDEO_TYPE == "rtsp":
        return RTSP_URL

    return VIDEO_SOURCE

def camera_worker():
    logger.info(f"Opening {VIDEO_TYPE} source: {VIDEO_SOURCE}")

    cap = open_video_capture()

    while True:
        if not cap.isOpened():
            logger.error(f"Failed to open {VIDEO_TYPE} source:{get_video_source()}")
            status_data["reconnect_count"] += 1
            time.sleep(RECONNECT_DELAY)
            cap = open_video_capture()
            continue

        ret, frame = cap.read()
        if not ret:
            logger.warning("Failed to read frame, reconnecting video source...")

            status_data["reconnect_count"] += 1

            cap.release()
            time.sleep(RECONNECT_DELAY)

            cap = open_video_capture()

        while not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except Exception as e:
                logger.error(f"Queue error: {e}")
                break
        frame_queue.put(frame)

        status_data["frame_queue_size"] = frame_queue.qsize()
        time.sleep(SLEEP_TIME)