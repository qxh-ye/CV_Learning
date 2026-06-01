#!/bin/bash 

cd /mnt/hgfs/demo

source ~/cv_project/venv/bin/activate

nohup gunicorn \
-w 1 \
-k gthread \
--threads 4 \
--timeout 0 \
-b 0.0.0.0:5000 \
day_17.app:app \
> day_17/logs/gunicorn.log 2>&1 &

echo "Gunicorn YOLO service started"
