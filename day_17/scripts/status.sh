#!/bin/bash

echo "=============Gunicorn=============="
ps -ef | grep gunicorn | grep -v grep

echo
echo "=============Port 5000============="
ss -tlnp | grep 5000
