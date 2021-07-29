import os

from celery import Celery

celery = Celery(__name__, include=["app.account.tasks"])

celery.conf.database_engine_options = {"echo": True}
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
