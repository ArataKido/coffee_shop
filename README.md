# Coffee Shop API

API для управления кофейней с функциями управления меню, заказами и корзиной.

## Требования

- Docker и Docker Compose

## Запуск с использованием Docker

### Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/coffee_shop_API.git
cd coffee_shop_API

# Запустить контейнеры
docker-compose up -d
```

Приложение будет доступно по адресу http://localhost:8001

### Сервисы

- **API**: http://localhost:8001 - FastAPI приложение
- **Flower**: http://localhost:5566 - Мониторинг задач Celery

### Управление контейнерами

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов API
docker-compose logs -f api

# Просмотр логов Celery Worker
docker-compose logs -f celery_worker

# Перестройка образов (при изменении зависимостей)
docker-compose build --no-cache
```

### Миграции базы данных

Миграции запускаются автоматически при старте API. Для ручного запуска:

```bash
# Вход в контейнер
docker-compose exec api bash

# Запуск миграций
alembic upgrade head

# Создание новой миграции
alembic revision --autogenerate -m "Your migration message"
```

## Разработка

При разработке вы можете изменять код в директории `app/`, и изменения будут применяться автоматически благодаря режиму `--reload` в Uvicorn.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Celery
- Redis
- JWT Authentication
- WebSocket
- Docker

## Environment Variables

Переменные окружения настроены в docker-compose.yml:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/coffee_shop
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
```

## API Documentation

После запуска приложения, вы можете получить доступ к:
- Swagger UI документации по адресу `/docs`
- ReDoc документации по адресу `/redoc` 