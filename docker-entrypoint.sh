#!/bin/bash
set -e

# making dir for logs if they do not exist
mkdir -p /app/logs

# Waiting till the redis is available  PostgreSQL
if [ "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Waiting till the redis is available Redis
if [ "$REDIS_URL" ]; then
    echo "Waiting for Redis..."
    while ! nc -z redis 6379; do
        sleep 0.1
    done
    echo "Redis started"
fi

# Auto applying migrations for API
if [ "$1" = "api" ]; then
    echo "Applying database migrations..."
    alembic upgrade head
    echo "Starting API server..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi

exec "$@" 