#!/bin/bash
set -e

export $(grep -v '^#' .env | xargs)

echo "waiting PostgreSQL..."
while ! nc -z db $POSTGRES_PORT; do
  sleep 0.5
done
echo "PostgreSQL is working"


echo "Migrating..."
python manage.py migrate --noinput


echo "Collecting statics..."
python manage.py collectstatic --noinput


echo "Run Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers=4 \
    --threads=2 \
    --worker-class=gthread
