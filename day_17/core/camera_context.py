import time
from queue import Queue

class CameraContext:
    def __init__(self, camera_config):
        self.camera_config = camera_config
        self.frame_queue = Queue(maxsize=5)
        self.result_queue = Queue(maxsize=5)

        self.frame_queue_size = 0
        self.result_queue_size = 0

        self.detect_count = 0
        self.reconnect_count = 0

        self.source_status = "init"
        self.last_detect_time = 0
        self.last_error = ""

        self.fps = 0

        self.start_time = time.time()

