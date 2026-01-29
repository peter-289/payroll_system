#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! pg_isready -h db -p 5432 -U payroll_user -d payroll_db; do
  sleep 1
done

echo "Database is ready!"
echo "Running database migrations..."
cd /app && python -m alembic upgrade head

echo "Creating admin user..."
python scripts/create_admin.py

echo "Starting application..."
exec gunicorn -w 4 -b 0.0.0.0:8000 --timeout 60 --access-logfile - --error-logfile - app.main:app
