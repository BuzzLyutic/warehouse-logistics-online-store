# orders/management/commands/run_inventory_consumer.py
from django.core.management.base import BaseCommand
from orders.tasks import consume_inventory_events

class Command(BaseCommand):
    help = 'Starts the inventory events consumer'

    def handle(self, *args, **options):
        consume_inventory_events()