#!/bin/bash
set -e

# Создаем директорию для логов, если она не существует
mkdir -p /app/logs

# Ждем доступности PostgreSQL
if [ "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Ждем доступности Redis
if [ "$REDIS_URL" ]; then
    echo "Waiting for Redis..."
    while ! nc -z redis 6379; do
        sleep 0.1
    done
    echo "Redis started"
fi

# Применяем миграции при запуске API
if [ "$1" = "api" ]; then
    echo "Applying database migrations..."
    alembic upgrade head
    echo "Starting API server..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
fi

# Запускаем переданную команду
exec "$@" 