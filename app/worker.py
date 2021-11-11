import os

from celery import Celery

celery = Celery(
    __name__,
    include=[
        "app.notification.tasks",
    ],
)

celery.conf.database_engine_options = {"echo": False}
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
