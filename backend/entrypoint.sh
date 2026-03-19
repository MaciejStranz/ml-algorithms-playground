#!/bin/sh
set -e

echo "Waiting for database..."

until python -c "
import os
import psycopg2

psycopg2.connect(
    dbname=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT', '5432'),
)
print('Database is ready')
"; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Synchronizing datasets..."
python manage.py sync_datasets

echo "Synchronizing algorithms..."
python manage.py sync_algorithms

echo "Starting backend..."
exec "$@"
