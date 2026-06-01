#!/bin/bash

cd /mnt/hgfs/demo

./day_17/scripts/stop.sh
sleep 2
./day_17/scripts/start_gunicorn.sh

echo "Gunicorn YOLO service restarted"
