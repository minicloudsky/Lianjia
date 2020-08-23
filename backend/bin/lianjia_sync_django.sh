#!/usr/bin/env bash


PROJECT_PATH=/home/.jywcode/lianjia/backend

source /home/.jywcode/lianjia/backend/venv/bin/activate
python $PROJECT_PATH/manage.py  makemigrations
python $PROJECT_PATH/manage.py  migrate
python $PROJECT_PATH/manage.py  collectstatic