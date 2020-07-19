from __future__ import absolute_import, unicode_literals

import os
from multiprocessing import current_process

from celery import Celery
from django.conf import settings

current_process()._config = {'semprefix': '/mp'}
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
redis_url = 'aliyun.yawujia.cn'
app = Celery('backend', backend='redis://{}:6379/3'.format(redis_url))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# from celery.signals import worker_process_init
#
#
# @worker_process_init.connect
# def fix_multiprocessing(**kwargs):
#     from multiprocessing import current_process
#     try:
#         current_process()._config
#     except AttributeError:
#         current_process()._config = {'semprefix': '/mp'}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
