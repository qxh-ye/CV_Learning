import threading

from day_17.camera.camera_worker import camera_worker
from day_17.inference.yolo_worker import yolo_worker
from day_17.utils.logger import get_logger
from day_17.config import CAMERA_CONFIGS
from day_17.core.camera_context import CameraContext

logger = get_logger("manager")

class CameraManager:
    def __init__(self):
        self.camera_threads = []
        self.yolo_threads = []
        self.contexts = []

    def start(self):
        for camera_config in CAMERA_CONFIGS:
            context = CameraContext(camera_config=camera_config)
            self.contexts.append(context)

            logger.info(
                f"Creating stream: "
                f"{camera_config['id']} "
                f"{camera_config['name']} "
            )

            camera_thread = threading.Thread(
                target=camera_worker,
                args=(context,),
                daemon=True
            )

            yolo_thread = threading.Thread(
                target=yolo_worker,
                args=(context,),
                daemon=True
            )

            camera_thread.start()
            yolo_thread.start()

            self.camera_threads.append(camera_thread)
            self.yolo_threads.append(yolo_thread)

    def get_context(self, stream_id=0):
        for context in self.contexts:
            if context.camera_config["id"] == stream_id:
                return context
        return None

    def get_all_contexts(self):
        return self.contexts

    def add_camera(self, camera_config):
        if self.get_context(camera_config["id"]) is not None:
            raise ValueError(
                f"Camera id {camera_config['id']} already exists"
            )
        context = CameraContext(camera_config=camera_config)
        self.contexts.append(context)

        logger.info(
            f"Adding stream: "
            f"{camera_config['id']} "
            f"{camera_config['name']}"
        )

        camera_thread = threading.Thread(
            target=camera_worker,
            args=(context,),
            daemon=True
        )

        yolo_thread = threading.Thread(
            target=yolo_worker,
            args=(context,),
            daemon=True
        )

        camera_thread.start()
        yolo_thread.start()

        self.camera_threads.append(camera_thread)
        self.yolo_threads.append(yolo_thread)

        return context

    def remove_camera(self, stream_id):
        context = self.get_context(stream_id)
        if context is None:
            raise ValueError(
                f"Camera {stream_id} not found"
            )
        context.running = False
        context.source_status = "stopped"
        self.contexts.remove(context)

        logger.info(
            f"Remove stream: {stream_id}"
        )
        return context


