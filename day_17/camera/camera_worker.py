import time

from day_17.config import SLEEP_TIME, VIDEO_TYPE, RECONNECT_DELAY
from day_17.utils.shared_data import frame_queue, status_data
from day_17.utils.logger import get_logger
from day_17.utils.video_utils import get_video_source, open_video_capture

logger = get_logger("camera")


def camera_worker():

    cap = open_video_capture()
    status_data["source_status"] = "running"
    while True:
        if not cap.isOpened():
            status_data["source_status"] = "error"
            error_msg = (f"Failed to open {VIDEO_TYPE} source:{get_video_source()}")
            logger.error(error_msg)
            status_data["last_error"] = error_msg
            status_data["reconnect_count"] += 1
            time.sleep(RECONNECT_DELAY)
            cap = open_video_capture()

            continue

        ret, frame = cap.read()
        if not ret:
            status_data["source_status"] = "reconnecting"
            error_msg = ("Failed to read frame, reconnecting video source...")
            logger.error(error_msg)
            status_data["last_error"] = error_msg
            status_data["reconnect_count"] += 1

            cap.release()
            time.sleep(RECONNECT_DELAY)
            cap = open_video_capture()
            if cap.isOpened():
                status_data["source_status"] = "running"

        while not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except Exception as e:
                logger.error(f"Queue error: {e}")
                break
        frame_queue.put(frame)
        status_data["last_error"] = ""

        status_data["frame_queue_size"] = frame_queue.qsize()
        time.sleep(SLEEP_TIME)