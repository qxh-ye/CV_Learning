# Day17 实时YOLO Web系统（工程化版）

## 项目介绍

基于：

- Flask
- YOLOv8
- OpenCV
- 多线程
- Queue

实现的实时视频分析系统。

支持：

- 实时视频检测
- Web视频流
- 多线程解耦
- Queue实时系统
- Logger日志系统
- Health健康检查
- Status状态监控
- 视频源重连
- 视频文件输入
- 工程化模块拆分

---

## 视频源配置说明

项目通过 `config.py` 中的 `VIDEO_TYPE` 控制视频输入源。

### USB摄像头

```python
VIDEO_TYPE = "camera"
VIDEO_SOURCE = 0

### 本地视频文件
VIDEO_TYPE = "video"
VIDEO_SOURCE = "videos/test.mp4"

### RTSP网络摄像头
VIDEO_TYPE = "rtsp"
RTSP_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/102"

## 最小依赖说明

项目核心依赖：

```text
flask
opencv-python
ultralytics
numpy


## 项目结构

```text
day_17/
│
├── camera/
│   ├── __init__.py
│   └── camera_worker.py
│
├── inference/
│   ├── __init__.py
│   └── yolo_worker.py
│
├── models/
│   └── yolov8n.pt
│
├── static/
│
├── templates/
│   └── index.html
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── shared_data.py
│
├── videos/
│   └── test.mp4
│
├── app.py
├── config.py
├── requirements.txt
└──README.md
