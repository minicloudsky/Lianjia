#!/usr/bin/env bash

source /home/.jywcode/lianjia/backend/venv/bin/activate

screen celery -A backend.celery worker -l info