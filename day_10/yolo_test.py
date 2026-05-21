from ultralytics import YOLO
model = YOLO("yolov8n.pt")

results = model("data/test.jpg")
result = results[0]
boxes = result.boxes
print(boxes)
print(boxes.xyxy)
print(boxes.cls)
print(boxes.conf)