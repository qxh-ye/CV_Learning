from ultralytics import YOLO
import cv2

# 1. 加载模型
model = YOLO("yolov8n.pt")

# 2. YOLO检测
results = model("data/test.jpg")

# 3. 读取原图
img = cv2.imread("data/test.jpg")

# 4. 获取第一张结果
result = results[0]

# 5. 获取 boxes
boxes = result.boxes

# 6. 遍历所有检测框
for box in boxes:
    # 获取坐标
    x1, y1, x2, y2 = box.xyxy[0]
    # 转 int
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # 获取类别编号
    cls_id = int(box.cls[0])

    # 获取类别名称
    class_name = result.names[cls_id]

    # 获取置信度
    conf = float(box.conf[0])

    # 组合显示文字
    label = f"{class_name}: {conf:.2f}"

    # 画矩形框
    cv2.rectangle(
        img,
        (x1, y1),           # 左上角
        (x2, y2),           # 右下角
        (0, 255, 0),        # 颜色(BGR)
        2                   # 线宽
    )
    text_y = y1 - 10
    if text_y < 20:
        text_y = y1 + 30
    # 绘制文字
    cv2.putText(
        img,
        label,
        (x1, text_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,           # 字体
        0.7,                                # 字体大小
        (0, 255, 0),
        2
    )

# 7. 显示图片
cv2.imshow("result", img)

cv2.waitKey(0)
cv2.destroyAllWindows()