import time
import cv2
from day_17.config import SLEEP_TIME, VIDEO_TYPE, RECONNECT_DELAY
from day_17.utils.logger import get_logger
from day_17.utils.video_utils import get_video_source, open_video_capture

logger = get_logger("camera")


def camera_worker(context):
    camera_config = context.camera_config

    cap = open_video_capture(camera_config=camera_config)
    context.source_status = "running"
    while context.running:
        if not cap.isOpened():
            context.source_status = "error"
            error_msg = (
                f"[Stream {camera_config['id']}] "
                f"[{camera_config['name']}] "
                f"Failed to open {VIDEO_TYPE} source:{get_video_source(camera_config=camera_config)}"
            )
            logger.error(error_msg)
            context.last_error = error_msg
            context.reconnect_count += 1
            time.sleep(RECONNECT_DELAY)
            cap = open_video_capture(camera_config=camera_config)

            continue

        ret, frame = cap.read()
        if not ret:
            if camera_config.get("type", "video") == "video":
                logger.warning(
                    f"[Stream {camera_config['id']}] "
                    f"[{camera_config['name']}] "
                    f"Video ended, restart from first frame"
                )
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                context.source_status = "running"
                context.last_error = ""
                time.sleep(SLEEP_TIME)
                continue

            context.source_status = "reconnecting"
            error_msg = (
                f"[Stream {camera_config['id']}] "
                f"[{camera_config['name']}] "
                f"Failed to read frame, reconnecting video source..."
            )
            logger.warning(error_msg)
            context.last_error = error_msg
            context.reconnect_count += 1

            cap.release()
            time.sleep(RECONNECT_DELAY)
            cap = open_video_capture(camera_config=camera_config)
            if cap.isOpened():
                context.source_status = "running"
            else:
                context.source_status = "error"
            continue

        if ret:
            context.read_frames += 1

        while not context.frame_queue.empty():
            try:
                context.frame_queue.get_nowait()
            except Exception as e:
                logger.error(f"Queue error: {e}")
                break
        context.frame_queue.put(frame)
        context.last_error = ""

        context.frame_queue_size = context.frame_queue.qsize()
        time.sleep(SLEEP_TIME)

    logger.info(
        f"[Stream {context.camera_config['id']}] "
        f"[{context.camera_config['name']}] "
        "camera worker stopped"
    )