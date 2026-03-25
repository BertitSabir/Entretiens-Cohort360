.PHONY: help install test coverage format lint typecheck migrate makemigrations run seed pre-commit

help:
	@echo "Available commands:"
	@echo "  make install         Create venv and install dev dependencies"
	@echo "  make test            Run tests"
	@echo "  make coverage        Run tests with coverage (min 80%)"
	@echo "  make format          Format code with ruff"
	@echo "  make lint            Lint and auto-fix with ruff"
	@echo "  make typecheck       Type check with ty"
	@echo "  make makemigrations  Generate migrations"
	@echo "  make migrate         Apply migrations"
	@echo "  make run             Run development server"
	@echo "  make seed            Seed demo data"
	@echo "  make pre-commit      Run pre-commit on staged files"

install:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements-dev.txt

install-hooks:
	pre-commit install

test:
	pytest

coverage:
	pytest --cov=medical --cov-report=term-missing --cov-fail-under=80

format:
	ruff format .

lint:
	ruff check . --fix

typecheck:
	ty check .

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver

seed:
	python manage.py seed_demo --patients 2500 --medications 150

pre-commit:
	pre-commit run
