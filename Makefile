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

migrate:
	alembic upgrade head

migrations-generate:
	alembic revision --autogenerate -m "$(m)"

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
	$(DOCKER_COMPOSE) exec -T db  psql -U postgres -d coffee_shop < sql/test_data.sql


help:
	@echo "Available commands:"
	@echo "  make build             - Create images"
	@echo "  make up                - Start containers"
	@echo "  make down              - Stop containers"
	@echo "  make logs              - Show containers logs "
	@echo "  make logs-api          - Show api containers logs"
	@echo "  make logs-celery       - Show celery worker logs"
	@echo "  make restart           - Restart containers"
	@echo "  make shell             - Run bash in API container"
	@echo "  make migrate           - Run migrations"
	@echo "  make migrations-generate m='Message'  - Make migrations"
	@echo "  make clean             - Delete temp Python files"
	@echo "  make rebuild           - rebuild containers"
	@echo "  make status            - Check container status" 
	@echo "  make populate          - Populate database with test data" 