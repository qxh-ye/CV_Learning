#!/bin/bash

pkill -9  -f "python -m day_17.app"

pkill -9  -f "gunicorn.*day_17.app:app"

echo "Service stopped"
