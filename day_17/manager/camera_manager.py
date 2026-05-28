import threading

from day_17.camera.camera_worker import camera_worker
from day_17.inference.yolo_worker import yolo_worker
from day_17.utils.logger import get_logger
from day_17.config import CAMERA_CONFIGS

logger = get_logger("manager")

class CameraManager:
    def __init__(self):
        self.camera_threads = []
        self.yolo_threads = []

    def start(self):
        for camera_config in CAMERA_CONFIGS:
            logger.info(
                f"Creating stream: "
                f"{camera_config['id']} "
                f"{camera_config['name']} "
            )

            camera_thread = threading.Thread(
                target=camera_worker,
                args=(camera_config,),
                daemon=True
            )

            yolo_thread = threading.Thread(
                target=yolo_worker,
                args=(camera_config,),
                daemon=True
            )

            camera_thread.start()
            yolo_thread.start()

            self.camera_threads.append(camera_thread)
            self.yolo_threads.append(yolo_thread)
