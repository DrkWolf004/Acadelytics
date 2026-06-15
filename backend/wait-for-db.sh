#!/bin/bash
set -e

echo "Esperando a que PostgreSQL esté disponible en $DB_HOST:5432..."
while ! nc -z "$DB_HOST" 5432; do
  sleep 1
done
echo "PostgreSQL está disponible"

exec gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
