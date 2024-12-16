import random
from time import sleep
import jwt
import pika
from celery import shared_task
from django.conf import settings
import requests
import json
import datetime
from requests import RequestException
from .models import Shipment, ShipmentLog

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
            json={"service_name": "shipment"}
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
def notify_order_processing_service(shipment_id):
    """Publishes shipment status updates to RabbitMQ."""
    shipment = Shipment.objects.filter(shipment_id=shipment_id).first()
    if shipment:
        message = {
            'order_id': shipment.order_id,
            'shipment_id': shipment.shipment_id,
            'status': shipment.status,
        }
        # Publish to RabbitMQ
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange='shipment_events', exchange_type='topic')
        channel.basic_publish(exchange='shipment_events', routing_key='shipment.status_update', body=json.dumps(message))
        connection.close()
    else:
        print(f"Shipment with ID {shipment_id} not found. Cannot notify order service.")


@shared_task
def simulate_single_shipment_update(shipment_id, status, location):
    shipment = Shipment.objects(shipment_id=shipment_id).first()
    if shipment:
        log = ShipmentLog(
            timestamp=datetime.datetime.now(),
            location=location,
            status=status
        )
        shipment.logs.append(log)  # Append the log instance
        shipment.status = status
        shipment.updated_at = datetime.datetime.now()
        shipment.save()
        notify_order_processing_service.delay(shipment_id)

@shared_task
def simulate_shipment_updates(shipment_id):
    statuses = ["In Transit", "At Local Distribution Center", "Out for Delivery", "Delivered"]
    locations = ["Moscow", "Saint Petersburg", "Surgut", "Vladivostok"]

    for status in statuses:
        sleep(10)
        location = random.choice(locations)
        simulate_single_shipment_update.delay(shipment_id, status, location)

