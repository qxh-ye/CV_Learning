# Multi-Camera YOLO Monitoring System

## 项目简介

基于 Flask + YOLOv8 + OpenCV 构建的多路视频实时监控平台。

项目支持多路视频流管理、YOLO实时目标检测、Dashboard监控面板、动态摄像头管理、告警系统以及 Linux 部署。

该项目主要用于学习和实践：

* YOLO工程化部署
* 多线程视频处理
* Flask Web开发
* Linux服务部署
* Gunicorn + Nginx反向代理

---

## 技术栈

* Python
* Flask
* OpenCV
* Ultralytics YOLOv8
* Threading
* Queue
* Gunicorn
* Nginx
* Linux

---

## 核心功能

### 视频监控

* 多路视频流管理
* YOLO实时目标检测
* MJPEG视频流推送
* 视频循环播放
* 自动重连机制

### 系统监控

* FPS监控
* 推理耗时统计
* CPU监控
* 内存监控
* Health状态检查

### 告警系统

支持：

* LOW_FPS
* HIGH_MEMORY_USAGE
* HIGH_CPU_USAGE
* TOO_MANY_RECONNECT

支持告警历史记录查询。

### 动态摄像头管理

运行过程中支持：

* 添加摄像头
* 删除摄像头

无需重启服务。

---

## 项目结构

```text
day_17/
├── camera/
├── core/
├── inference/
├── manager/
├── templates/
├── utils/
├── logs/
├── models/
├── videos/
├── scripts/
│
├── app.py
├── config.py
├── requirements_min.txt
└── README.md
```

---

## REST API

| 接口                  | 功能        |
| ------------------- | --------- |
| GET /               | Dashboard |
| GET /video/<id>     | 视频流       |
| GET /status/<id>    | 摄像头状态     |
| GET /summary        | 系统统计      |
| GET /cameras        | 摄像头列表     |
| GET /warnings       | 告警历史      |
| POST /camera/add    | 添加摄像头     |
| POST /camera/remove | 删除摄像头     |

---

## 快速启动

### Windows

```bash
python -m day_17.app
```

访问：

```text
http://127.0.0.1:5000
```

### Linux

创建虚拟环境：

```bash
python3 -m venv venv

source venv/bin/activate
```

安装依赖：

```bash
pip install -r day_17/requirements_min.txt
```

启动项目：

```bash
python -m day_17.app
```

---

## Gunicorn 部署

启动：

```bash
./day_17/scripts/start_gunicorn.sh
```

重启：

```bash
./day_17/scripts/restart_gunicorn.sh
```

停止：

```bash
./day_17/scripts/stop.sh
```

查看状态：

```bash
./day_17/scripts/status.sh
```

---

## Nginx 反向代理

项目部署于 Ubuntu 环境。

使用：

```text
Nginx → Gunicorn → Flask → YOLO Service
```

访问地址：

```text
http://10.10.10.132
```

无需手动输入：

```text
:5000
```

实现通过 Nginx 将 80 端口反向代理到 Gunicorn 的 5000 端口。

---

## 性能测试

| 摄像头数量 | 平均FPS |
| ----- | ----- |
| 1 路   | 20    |
| 2 路   | 11    |
| 3 路   | 9     |
| 4 路   | 7     |

测试环境：

* Ubuntu
* Python 3.10
* YOLOv8n

---

## 项目亮点

* 多线程视频处理架构
* Queue实时处理机制
* 动态摄像头管理
* 告警系统
* 日志系统
* Linux部署
* Gunicorn部署
* Nginx反向代理
* REST API设计

---

## Future Work

* WebSocket实时推送
* RTSP摄像头支持优化
* Docker部署
* 告警持久化存储
* 目标跟踪（ByteTrack）
* 数据库集成

---

## 项目成果

项目已完成：

* 多路视频监控
* 动态摄像头管理
* 实时目标检测
* Dashboard监控面板
* 告警中心
* Linux部署
* Gunicorn部署
* Nginx反向代理

具备基本的视频监控平台能力，可作为 AI/CV 工程方向实习项目展示。
