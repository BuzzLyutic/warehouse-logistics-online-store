# Dockerfile

# Use official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Copy entrypoint script
COPY entrypoint.sh /app/

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Collect static files (if any)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start Gunicorn and Celery worker
CMD ["sh", "/app/entrypoint.sh"]
# CMD celery -A inventory_service worker --loglevel=info --concurrency=4 -n inventory_worker.%h