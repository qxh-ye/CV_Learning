#!/bin/bash

echo "=============Gunicorn=============="
ps -ef | grep day_17.app | grep -v grep

echo
echo "==============Nginx================"
systemctl is-active nginx

echo
echo "==============Port================="
ss -tlnp | grep 5000
