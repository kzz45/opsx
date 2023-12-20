#!/bin/bash
# 假设代码目录在 /data/backend 中
cd /data/backend/crontab

source /data/backend/venv/bin/activate

export RUN_ENV="online"
python3 instance_task.py
