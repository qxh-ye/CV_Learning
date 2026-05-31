# config.py  负责统一管理参数
import os
# ==================================
# Video Source Config
# ==================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_SOURCE = os.path.join(BASE_DIR, "videos", "test.mp4")
VIDEO_TYPE = "video"
RTSP_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/102"
RECONNECT_DELAY = 1
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 1))
STREAM_ID = 0
CAMERA_CONFIGS = [
    {
        "id": 0,
        "name": "test_camera0",
        "source": VIDEO_SOURCE,
	    "type": "video"
    }
]

# ===================================
# YOLO Config
# ===================================
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8n.pt")
CONF = float(os.getenv("conf", 0.5))
IMG_SIZE = int(os.getenv("IMG_SIZE", 320))
DETECT_INTERVAL = 2

# ===================================
# Queue Config
# ===================================
FRAME_QUEUE_SIZE = 5
RESULT_QUEUE_SIZE = 5

# ===================================
# System Config
# ===================================
SLEEP_TIME = 0.01
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False") == "True"


