#!/bin/bash
# 假设代码目录在 /data/backend 中 并且 python 的需要环境是 venv
source /data/backend/venv/bin/activate
cd /data/backend/crontab

python3 sync_alerts.py
