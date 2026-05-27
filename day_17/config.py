# config.py  负责统一管理参数
# ==================================
# Video Source Config
# ==================================
VIDEO_SOURCE = "videos/test.mp4"
VIDEO_TYPE = "video"
RTSP_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/102"
RECONNECT_DELAY = 1

# ===================================
# YOLO Config
# ===================================
MODEL_PATH = "models/yolov8n.pt"
CONF = 0.5
IMG_SIZE = 640
DETECT_INTERVAL = 1

# ===================================
# Queue Config
# ===================================
FRAME_QUEUE_SIZE = 5
RESULT_QUEUE_SIZE = 5

# ===================================
# System Config
# ===================================
SLEEP_TIME = 0.01

