# config.py  负责统一管理参数
import os
# ==================================
# Video Source Config
# ==================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_SOURCE_0 = os.path.join(BASE_DIR, "videos", "test.mp4")
VIDEO_SOURCE_1 = os.path.join(BASE_DIR, "videos", "test2.mp4")
VIDEO_SOURCE_2 = os.path.join(BASE_DIR, "videos", "test3.mp4")
VIDEO_TYPE = "video"
RTSP_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/102"
RECONNECT_DELAY = 1
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 1))
STREAM_ID = 0
CAMERA_CONFIGS = [
    {
        "id": 0,
        "name": "test_camera0",
        "source": VIDEO_SOURCE_0,
	    "type": "video"
    },
    {
        "id": 1,
        "name": "test_camera1",
        "source": VIDEO_SOURCE_1,
	    "type": "video"
    },
    {
        "id": 2,
        "name": "test_camera2",
        "source": VIDEO_SOURCE_2,
	    "type": "video"
    }
]

# ===================================
# YOLO Config
# ===================================
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8n.pt")
CONF = float(os.getenv("conf", 0.5))
IMG_SIZE = int(os.getenv("IMG_SIZE", 320))
DETECT_INTERVAL = 3

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

# ===================================
# Warning Config
# ===================================
MEMORY_WARNING_MB = 1000
CPU_WARNING_PERCENT = 80
FPS_WARNING = 5
RECONNECT_WARNING_COUNT = 5




