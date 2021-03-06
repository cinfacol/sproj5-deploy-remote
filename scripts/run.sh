#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput --clear
python manage.py makemigrations cart inventario perfiles products store
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi
