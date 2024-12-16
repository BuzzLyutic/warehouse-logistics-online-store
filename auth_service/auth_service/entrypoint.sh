#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create roles in the database
echo "Creating initial roles and permissions..."
python manage.py create_roles

# Start Gunicorn server
echo "Starting Gunicorn..."
gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000