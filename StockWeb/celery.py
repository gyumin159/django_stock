from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StockWeb.settings')

app = Celery('StockWeb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Asia/Seoul'

app.autodiscover_tasks()

# celery -A StockWeb worker -l info --pool=solo
