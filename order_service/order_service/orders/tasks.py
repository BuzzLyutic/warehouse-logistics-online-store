import jwt
from celery import shared_task
from celery.signals import worker_ready
from django.conf import settings
import requests
import json
import pika
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from requests import RequestException
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order
from .serializers import OrderSerializer


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
            json={"service_name": "order"}
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

@shared_task
def publish_order_processing_event(order_id, action):
    """Publishes an event to RabbitMQ to trigger order processing."""
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='order_events', exchange_type='topic')

    message = {
        'order_id': order_id,
        'action': action
    }

    channel.basic_publish(exchange='order_events', routing_key='order.created', body=json.dumps(message))
    connection.close()

@shared_task(bind=True, max_retries=3)
def process_order_task(self, order_id):
    """
    Processes an order:
    1. Reserve inventory (by publishing event and waiting for inventory service to process it)
    2. Create shipment request
    """
    try:
        order = Order.objects.get(id=order_id)

        # Create shipment request after inventory is reserved (or failed to be reserved)
        publish_order_processing_event(order_id, "created")
        create_shipment_request.delay(order_id)

    except ObjectDoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise self.retry(exc=e, countdown=60)

@shared_task
def create_shipment_request(order_id):
    """Sends a request to create a shipment."""
    try:
        order = Order.objects.get(id=order_id)
        access_token = get_service_token()

        shipment_url = f'{settings.SHIPMENT_SERVICE_URL}/api/shipments/'
        shipment_payload = {
            'shipment_id': f"SHIP-{order.id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'order_id': str(order.id),
            'carrier_name': 'Example Carrier',
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(shipment_url, data=json.dumps(shipment_payload), headers=headers)
        response.raise_for_status()
        order.process_order()
        order.save()

    except requests.exceptions.RequestException as e:
        print(f"Error creating shipment: {e}")
        # Handle the error appropriately
        # You may want to retry, log the error, or take other actions


@shared_task(bind=True, max_retries=3)
def fulfill_order_task(self, order_id):
    """Fulfills an order."""
    try:
        order = Order.objects.get(id=order_id)
        # Logic to fulfill order such as calling shipment service if needed
        # For now just change the order status
        order.fulfill_order()
        order.save()
    except ObjectDoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def cancel_order_task(self, order_id):
    """Cancels an order and sends a request to add inventory back."""
    try:
        order = Order.objects.get(id=order_id)
        order_data = OrderSerializer(order).data

        # For each item in the order, send a request to add back stock
        if 'order_items' in order_data:
            for item in order_data['order_items']:
                publish_order_processing_event(order_id, "cancel")
        else:
            print("No order items found")
            return

        order.cancel_order()
        order.save()
    except ObjectDoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def update_order_status_from_shipment(self, order_id, shipment_status):
    """Updates the order status based on shipment updates received."""
    try:
        order = Order.objects.get(id=order_id)

        if shipment_status == 'Delivered':
            order.fulfill_order()
        elif shipment_status in ["In Transit", "At Local Distribution Center", "Out for Delivery"]:
            order.ship_order()
        else:
            print(f"Unhandled shipment status received: {shipment_status}")
        order.save()
    except ObjectDoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise self.retry(exc=e, countdown=60)


def consume_inventory_events():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='inventory_events', exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='inventory_events', queue=queue_name, routing_key='inventory.#')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f" [x] Received inventory event: {message}")
        # Process the inventory event
        # Example: If low stock, maybe cancel related orders or notify admins

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for inventory events. To exit press CTRL+C')
    channel.start_consuming()


@shared_task(bind=True, queue='shipment_status_updates')
def consume_shipment_status_updates(self):
    """Consumes shipment status updates from RabbitMQ and updates orders."""
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='shipment_events', exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='shipment_events', queue=queue_name, routing_key='shipment.status_update')

    def callback(ch, method, properties, body):
        shipment_data = json.loads(body)
        order_id = shipment_data['order_id']
        shipment_status = shipment_data['status']
        # Update the order status
        update_order_status_from_shipment(order_id, shipment_status)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for shipment status updates. To exit press CTRL+C')
    channel.start_consuming()


@worker_ready.connect
def start_consuming(sender=None, **kwargs):
    consume_shipment_status_updates.delay()