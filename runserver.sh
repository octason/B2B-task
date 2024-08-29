#!/bin/bash

source /venv/bin/activate

# It's the easiest way to wait for mysql container to start

sleep 5
python manage.py makemigrations
python manage.py migrate

gunicorn --env DJANGO_SETTINGS_MODULE=b2b_wallet_project.settings b2b_wallet_project.wsgi:application authbind -b 0.0.0.0:8000 --log-level debug -w 2 -t 500