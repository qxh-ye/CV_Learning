# Linux 运行说明

## 1. 进入项目根目录

```bash
cd demo

## 2. 创建虚拟环境
python3 -m venv venv

## 3. 激活虚拟环境
source venv/bin/activate

## 4. 安装依赖
pip install -r day_17/requirements_min.txt

## 5. 启动项目
python -m day_17.app

## 6. 访问服务
http://服务器名IP:5000

## 7. 查看日志
tail -f day_17/logs/system.log 

