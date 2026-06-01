#!/bin/bash

pkill -9  -f "gunicorn.*day_17.app:app"

pkill -9 -f "python -m day_17.app"

echo "Service stopped"
