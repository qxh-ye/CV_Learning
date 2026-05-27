# utils/shared_data.py  存放共享数据
import queue
from day_17.config import FRAME_QUEUE_SIZE, RESULT_QUEUE_SIZE

frame_queue = queue.Queue(maxsize=FRAME_QUEUE_SIZE)
result_queue = queue.Queue(maxsize=RESULT_QUEUE_SIZE)

status_data = {
    "fps": 0,
    "frame_queue_size": 0,
    "result_queue_size": 0,
    "detect_count": 0,
    "last_detect_time": 0,
    "reconnect_count": 0,
    "last_error": "",
    "source_status": "init"
}