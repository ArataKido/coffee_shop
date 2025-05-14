.PHONY: build up down logs restart shell migrate

# Переменные
DOCKER_COMPOSE = docker compose

# Сборка и запуск
build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

logs-api:
	$(DOCKER_COMPOSE) logs -f api

logs-celery:
	$(DOCKER_COMPOSE) logs -f celery_worker

restart:
	$(DOCKER_COMPOSE) restart

# Доступ к контейнерам
shell:
	$(DOCKER_COMPOSE) exec api bash

# Работа с базой данных
migrate:
	$(DOCKER_COMPOSE) exec api alembic upgrade head

migrations-generate:
	$(DOCKER_COMPOSE) exec api alembic revision --autogenerate -m "$(m)"

# Общие команды
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".DS_Store" -delete

# Полная перестройка с нуля
rebuild: down
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

# Проверка статуса
status:
	$(DOCKER_COMPOSE) ps

populate:
	@echo "Populating database with test data..."
	$(DOCKER_COMPOSE) exec -it api psql -U posgtres -d coffee_shop < sql/test_data.sql


help:
	@echo "Доступные команды:"
	@echo "  make build             - Собрать образы"
	@echo "  make up                - Запустить контейнеры"
	@echo "  make down              - Остановить контейнеры"
	@echo "  make logs              - Показать логи всех контейнеров"
	@echo "  make logs-api          - Показать логи API"
	@echo "  make logs-celery       - Показать логи Celery Worker"
	@echo "  make restart           - Перезапустить контейнеры"
	@echo "  make shell             - Запустить bash в контейнере API"
	@echo "  make migrate           - Применить миграции"
	@echo "  make migrations-generate m='Сообщение'  - Создать миграцию"
	@echo "  make clean             - Удалить временные файлы Python"
	@echo "  make rebuild           - Полная перестройка с нуля"
	@echo "  make status            - Проверить статус контейнеров" 