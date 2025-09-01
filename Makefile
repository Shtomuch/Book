.PHONY: help install run test migrate docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  run          Run the application locally"
	@echo "  test         Run tests"
	@echo "  migrate      Run database migrations"
	@echo "  docker-up    Start Docker containers"
	@echo "  docker-down  Stop Docker containers"
	@echo "  clean        Clean up cache files"

install:
	poetry install

run:
	poetry run uvicorn src.main:app --reload

test:
	poetry run pytest

migrate:
	poetry run alembic upgrade head

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache