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

- 实时摄像头检测
- Web视频流
- FPS显示
- Queue解耦
- 多线程实时系统
- Web状态接口
- 系统日志输出

---

## 项目结构

```text
day_17/
│
├── app.py
├── config.py
├── requirements.txt
│
├── camera/
├── inference/
├── utils/
├── templates/
├── static/
└── models/