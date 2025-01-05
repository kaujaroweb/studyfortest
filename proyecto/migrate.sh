#!/bin/bash

# Default email if DJANGO_SUPERUSER_EMAIL is not set
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"kaujaroweb@gmail.com"}

# Change to the application directory
cd /app/

# Use Python from the virtual environment to run migrations
/opt/venv/bin/python manage.py migrate --noinput

# Create superuser if it doesn't exist
/opt/venv/bin/python manage.py createsuperuser --email $DJANGO_SUPERUSER_EMAIL --noinput || true
