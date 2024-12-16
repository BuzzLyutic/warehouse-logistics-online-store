# inventory/management/commands/run_inventory_reservation_consumer.py
from django.core.management.base import BaseCommand
# from inventory.tasks import consume_inventory_reservation_events

from inventory.tasks import consume_order_events


class Command(BaseCommand):
    help = 'Starts the inventory reservation events consumer'

    def handle(self, *args, **options):
        consume_order_events()
