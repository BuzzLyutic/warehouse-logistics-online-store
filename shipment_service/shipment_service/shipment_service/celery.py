from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shipment_service.settings')

app = Celery('shipment_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from the local app
app.autodiscover_tasks()
