#!/bin/bash

cd ~/cv_project

source venv/bin/activate

nohup python -m day_17.app > day_17/logs/app.log 2>&1 &

echo "Multi Camera YOLO started in background"
