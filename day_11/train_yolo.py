from ultralytics import YOLO
model = YOLO("yolov8n.pt")

model.train(
    data="my_first_project/data.yaml",
    epochs=100,
    imgsz=640,
    batch=4
)