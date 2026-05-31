#!/bin/bash

cd ~/cv_project

./scripts/stop.sh
sleep 2
./scripts/start_gunicorn.sh

echo "Gunicorn YOLO service restarted"
