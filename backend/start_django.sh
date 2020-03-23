#!/bin/bash
set -e

python manage.py collectstatic --noinput

if [ "$ENV" = 'PRODACTION' ]; then
    echo "PRODACTION" 
    exec gunicorn project.wsgi:application -w 2 -b :8000
else
    echo "DEVELOP"
    exec python manage.py runserver 0.0.0.0:8000
fi
