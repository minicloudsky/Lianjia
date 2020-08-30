#!/usr/bin/env bash

source /home/.jywcode/lianjia/backend/venv/bin/activate
cd /home/.jywcode/lianjia/backend
nohup python run_spider.py & >> lianjia.out

