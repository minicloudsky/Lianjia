
#! /usr/bin/python
source /home/.jywcode/lianjia/backend/venv/bin/activate

gunicorn -w 2 --forwarded-allow-ips=* --bind=0.0.0.0:7600 backend.wsgi:application --chdir /home/.jywcode/lianjia/backend
 --access-logfile /tmp/lianjia-access.log --error-logfile /tmp/lianjia-error.log

