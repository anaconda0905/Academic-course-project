# import os
# from celery import Celery
#
# # set the default Django settings module for the 'celery' program.
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AoneBrains.settings')
#
# app = Celery('AoneBrains')
#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks(settings.INSTALLED_APPS)
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AoneBrains.settings')

CELERY_BROKER = getattr(
    settings,
    'CELERY_BROKER',
    'redis://localhost:6379/5')

app = Celery('AoneBrains', broker=CELERY_BROKER)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
