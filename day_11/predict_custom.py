from ultralytics import YOLO

model = YOLO(
    "runs/detect/train-5/weights/best.pt"
)

results = model("images/test/pre1.jpg", conf=0.35)
results[0].show()