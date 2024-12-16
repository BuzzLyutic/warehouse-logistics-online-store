#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py run_inventory_reservation_consumer &

# Start Gunicorn server
echo "Starting Gunicorn..."
gunicorn inventory_service.wsgi:application --bind 0.0.0.0:8000
