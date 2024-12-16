# inventory/apps.py
import os

from django.apps import AppConfig
from django.conf import settings


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from .tasks import consume_order_events
        import threading

        if not settings.DEBUG and not os.environ.get('RUN_MAIN'):
            threading.Thread(target=consume_order_events, daemon=True).start()
