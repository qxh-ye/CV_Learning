import cv2
from day_17.config import VIDEO_SOURCE, RTSP_URL, VIDEO_TYPE, BUFFER_SIZE
from day_17.utils.logger import get_logger

logger = get_logger("video")

def get_video_source():
    if VIDEO_TYPE == "rtsp":
        return RTSP_URL

    return VIDEO_SOURCE

def open_video_capture():

    source = get_video_source()
    logger.info(f"Opening {VIDEO_TYPE} source: {source}")

    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, BUFFER_SIZE)

    return cap