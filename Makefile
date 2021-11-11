#!/bin/bash

SQLALCHEMY_DATABASE_URI_TESTING="sqlite+aiosqlite:///./instance/testing.db"
CELERY_BROKER_URL_TESTING="sqla+sqlite:///instance/testing-worker.db"
CELERY_RESULT_BACKEND_TESTING="db+sqlite:///instance/testing-worker.db"

show-routes:
	@python app/cli.py route show

requirements-dev:
	@pip install --upgrade pip
	@pip install setuptools wheel
	@pip install -r requirements/development.txt
	@pip install -e .

requirements:
	@pip install --upgrade pip
	@pip install setuptools wheel
	@pip install -r requirements/production.txt

runserver-dev:
	@uvicorn app.main:app --reload

runserver:
	@uvicorn app.main:app

runcelery:
	@celery -A app.worker.celery worker -E -B --loglevel=INFO --pool=prefork

runcelery-test:
	@export TESTING=1 && \
	export CELERY_BROKER_URL=$(CELERY_BROKER_URL_TESTING) && \
	export CELERY_RESULT_BACKEND=$(CELERY_RESULT_BACKEND_TESTING) && \
	celery -A app.worker.celery worker -E -B --loglevel=INFO --pool=prefork

runflower:
	@celery -A app.worker.celery flower --port=5555

outdated:
	@pip list --outdated

test:
	@export SQLALCHEMY_DATABASE_URI=$(SQLALCHEMY_DATABASE_URI_TESTING) && \
	export TESTING=1 && \
	export CELERY_BROKER_URL=$(CELERY_BROKER_URL_TESTING) && \
	export CELERY_RESULT_BACKEND=$(CELERY_RESULT_BACKEND_TESTING) && \
	py.test --disable-pytest-warnings

test-matching:
	@export SQLALCHEMY_DATABASE_URI=$(SQLALCHEMY_DATABASE_URI_TESTING) && \
	export TESTING=1 && \
	export CELERY_BROKER_URL=$(CELERY_BROKER_URL_TESTING) && \
	export CELERY_RESULT_BACKEND=$(CELERY_RESULT_BACKEND_TESTING) && \
	py.test -sk $(test)


test-matching-log:
	@export SQLALCHEMY_DATABASE_URI=$(SQLALCHEMY_DATABASE_URI_TESTING) && \
	export TESTING=1 && \
	export CELERY_BROKER_URL=$(CELERY_BROKER_URL_TESTING) && \
	export CELERY_RESULT_BACKEND=$(CELERY_RESULT_BACKEND_TESTING) && \
	py.test -sk $(test) --log-cli-level=INFO

coverage:
	@export SQLALCHEMY_DATABASE_URI=$(SQLALCHEMY_DATABASE_URI_TESTING) && \
	export TESTING=1 && \
	export CELERY_BROKER_URL=$(CELERY_BROKER_URL_TESTING) && \
	export CELERY_RESULT_BACKEND=$(CELERY_RESULT_BACKEND_TESTING) && \
	py.test --cov=app --cov-report=term-missing --cov-fail-under=80 tests/

migration-up:
	@alembic upgrade head

migration-down:
	@alembic downgrade -1

flake8:
	@flake8 --show-source app tests alembic

check-import:
	@isort app tests alembic --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --check-only

fix-import:
	isort app tests alembic --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses

check-black:
	@black app tests alembic --line-length 79 --check

fix-black:
	black app tests alembic --line-length 79

check-bandit:
	@bandit -r -f custom -x tests app tests alembic

check-safety:
	safety check --file=requirements/production.txt

check-dead-fixtures:
	@pytest --dead-fixtures

lint: fix-import fix-black flake8

check-lint: check-import check-black check-bandit flake8 check-dead-fixtures