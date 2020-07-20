#!/usr/bin/env bash

source /home/.jywcode/lianjia/backend/venv/bin/activate
cd /home/.jywcode/lianjia/backend
celery -A backend.celery worker -l info