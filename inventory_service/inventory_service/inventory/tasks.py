# inventory_service/inventory/tasks.py
import datetime

import jwt
from celery import shared_task
from celery import Celery
import json
import pika
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import requests
from requests import RequestException

from .models import ProcessedOrderItem
from .repositories import InventoryRepository


@shared_task
def publish_inventory_event(warehouse_id, goods_id, quantity, action, order_id=None, order_item_id=None):
    """Publishes inventory events to RabbitMQ."""
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='inventory_events', exchange_type='topic')

    message = {
        'warehouse_id': warehouse_id,
        'goods_id': goods_id,
        'quantity': quantity,
        'action': action,
        'order_id': order_id,
        'order_item_id': order_item_id
    }

    channel.basic_publish(exchange='inventory_events', routing_key='inventory.updated', body=json.dumps(message))
    connection.close()


@shared_task
def check_stock_levels():
    """Example periodic task to check stock levels."""
    from .repositories import InventoryRepository
    repository = InventoryRepository()
    low_stock_items = repository.get_low_stock_items()

    for item in low_stock_items:
        publish_inventory_event.delay(item.warehouse.id, item.goods.id, item.quantity, 'low_stock')

    return f"Checked {len(low_stock_items)} low stock items."


# Cache the service token and its expiration
_service_token = None
_token_expiry = None


def get_service_token():
    """
    Fetch a new service token for the inventory service account from the auth service.
    Cache the token and its expiry time to avoid redundant requests.
    """
    global _service_token, _token_expiry

    # If the token is still valid, return it
    if _service_token and _token_expiry and _token_expiry > datetime.datetime.now():
        return _service_token

    try:
        # Request a token from the auth service
        response = requests.post(
            f"{settings.AUTH_SERVICE_URL}/api/auth/service-token/",
            json={"service_name": "inventory"}
        )
        response.raise_for_status()

        data = response.json()
        _service_token = data["token"]
        decoded_payload = jwt.decode(
            _service_token,
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        )
        _token_expiry = datetime.datetime.utcfromtimestamp(decoded_payload["exp"])

        return _service_token
    except RequestException as e:
        print(f"Error fetching service token: {e}")
        raise
    except KeyError:
        print("Malformed response from auth service while fetching token.")
        raise


def consume_order_events():
    """
    Consume order events from RabbitMQ and process them in the inventory service.
    """
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="order_events", exchange_type="topic")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="order_events", queue=queue_name, routing_key="order.#")

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f" [x] Received order event in inventory service: {message}")

        if "action" not in message or "order_id" not in message:
            print("Invalid message format.")
            return

        action = message["action"]
        order_id = message["order_id"]

        try:
            headers = {"Authorization": f"Bearer {get_service_token()}"}
            response = requests.get(
                f"{settings.ORDER_SERVICE_URL}/api/orders/{order_id}/", headers=headers
            )
            response.raise_for_status()
            order_data = response.json()

            if action == "created":
                handle_order_created(order_data, order_id)
            elif action == "cancel":
                handle_order_cancel(order_data, order_id)
            else:
                print(f"Unknown action: {action}")

        except RequestException as e:
            print(f"Error fetching order details: {e}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for order events. To exit press CTRL+C")
    channel.start_consuming()


def handle_order_created(order_data, order_id):
    """
    Handle the 'created' action for an order.
    """
    if "order_items" in order_data:
        for index, item in enumerate(order_data["order_items"]):
            # Generate a fallback order_item_id using the index if not provided
            order_item_id = item.get("id", None)
            if order_item_id is None:
                # Generate a fallback ID (e.g., based on order ID and index)
                order_item_id = int(f"{order_id}{index + 1}")

            # Check if the order item has already been processed
            if ProcessedOrderItem.objects.filter(order_item_id=order_item_id).exists():
                print(f"Order item {order_item_id} already processed.")
                continue

            try:
                inventory_repository = InventoryRepository()
                inventory_repository.deduct_inventory(
                    item["warehouse_id"], item["goods_id"], item["quantity"]
                )
                publish_inventory_event.delay(
                    warehouse_id=item["warehouse_id"],
                    goods_id=item["goods_id"],
                    quantity=item["quantity"],
                    action="reserve",
                    order_id=order_id,
                    order_item_id=order_item_id,
                )

                # Mark the order item as processed
                ProcessedOrderItem.objects.create(order_item_id=order_item_id)
            except ObjectDoesNotExist:
                print(
                    f"Inventory for goods {item['goods_id']} in warehouse {item['warehouse_id']} not found."
                )
                publish_inventory_event.delay(
                    warehouse_id=item["warehouse_id"],
                    goods_id=item["goods_id"],
                    quantity=item["quantity"],
                    action="reserve_failed",
                    order_id=order_id,
                    order_item_id=order_item_id,
                )
            except ValueError as e:
                print(f"Error reserving inventory: {e}")
                publish_inventory_event.delay(
                    warehouse_id=item["warehouse_id"],
                    goods_id=item["goods_id"],
                    quantity=item["quantity"],
                    action="reserve_failed",
                    order_id=order_id,
                    order_item_id=order_item_id,
                )
    else:
        print("No order items found")


def handle_order_cancel(order_data, order_id):
    """
    Handle the 'cancel' action for an order.
    """
    if "order_items" in order_data:
        for item in order_data["order_items"]:
            try:
                inventory_repository = InventoryRepository()
                inventory_repository.add_inventory(
                    item["warehouse_id"], item["goods_id"], item["quantity"]
                )
                publish_inventory_event.delay(
                    warehouse_id=item["warehouse_id"],
                    goods_id=item["goods_id"],
                    quantity=item["quantity"],
                    action="add",
                    order_id=order_id,
                    order_item_id=item.get("id"),
                )

                # Mark as processed
                ProcessedOrderItem.objects.create(order_item_id=item.get("id"))
            except ObjectDoesNotExist:
                print(
                    f"Inventory for goods {item['goods_id']} in warehouse {item['warehouse_id']} not found."
                )
            except ValueError as e:
                print(f"Error adding inventory: {e}")


