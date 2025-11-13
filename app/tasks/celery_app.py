# app/tasks/celery_app.py
from datetime import timedelta
from celery import Celery
from celery.signals import worker_ready
from celery_singleton import clear_locks

from app import create_app

# ----------------------------
# 1. Initialize Flask app
# ----------------------------
flask_app = create_app()

# ----------------------------
# 2. Initialize Celery
# ----------------------------
celery = Celery(
    "celery",
    broker=flask_app.config.get("CELERY_BROKER_URL"),
    backend=flask_app.config.get("CELERY_RESULT_BACKEND"),
    broker_connection_retry_on_startup=True,
    include=[
        "app.tasks.fetch_and_store_cars_task",
    ],
)

# Ensure tasks run within Flask app context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# ----------------------------
# 3. Define tasks
# ----------------------------
@celery.task(name="sync_from_back4app")
def sync_from_back4app():
    from .fetch_and_store_cars_task import fetch_and_store_cars
    return fetch_and_store_cars()

# ----------------------------
# 4. Set up periodic tasks (timedelta style)
# ----------------------------
celery.conf.beat_schedule = {
    "daily_sync_from_back4app": {
        "task": "sync_from_back4app",
        "schedule": timedelta(minutes=1),  
    }
}

# ----------------------------
# 5. Unlock singleton locks on worker start
# ----------------------------
@worker_ready.connect
def unlock_all(**kwargs):
    clear_locks(celery)
