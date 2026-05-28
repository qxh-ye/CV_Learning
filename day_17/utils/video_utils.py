import cv2
from day_17.config import RTSP_URL, VIDEO_TYPE, BUFFER_SIZE
from day_17.utils.logger import get_logger

logger = get_logger("video")

def get_video_source(camera_config):
    if VIDEO_TYPE == "rtsp":
        return RTSP_URL

    return camera_config["source"]

def open_video_capture(camera_config):

    source = get_video_source(camera_config=camera_config)
    logger.info(
        f"[Stream {camera_config['id']}] "
        f"[{camera_config['name']}] "
        f"Opening {VIDEO_TYPE} source: {source}"
    )

    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)

    return cap