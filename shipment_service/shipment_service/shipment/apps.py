from django.apps import AppConfig
from mongoengine import connect


class ShipmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shipment"

    def ready(self):
        from . import tasks
        connect(
            db='shipment_db',
            host='mongodb://mongodb:27017/',
        )
