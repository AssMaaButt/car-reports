from datetime import timedelta
import os
from celery import Celery
from celery.signals import worker_ready
from celery_singleton import clear_locks
from app.neo4j_repo import push_car_to_neo4j


# Import SQLAlchemy session and your task
from app.db import SessionLocal
from app.tasks.fetch_and_store_cars_task import fetch_and_store_cars

# ----------------------------
# 1. Initialize Celery
# ----------------------------
celery = Celery(
    "celery",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    broker_connection_retry_on_startup=True,
    include=[
        "app.tasks.fetch_and_store_cars_task",
    ],
)

# ----------------------------
# 2. Define tasks
# ----------------------------
@celery.task(name="sync_from_back4app")
def sync_from_back4app():
    """
    Calls fetch_and_store_cars function with a DB session.
    """
    db = SessionLocal()
    try:
        from app.tasks.fetch_and_store_cars_task import fetch_and_store_cars_with_neo4j
        return fetch_and_store_cars_with_neo4j(db)
    finally:
        db.close()

# ----------------------------
# 3. Set up periodic tasks
# ----------------------------
celery.conf.beat_schedule = {
    "daily_sync_from_back4app": {
        "task": "sync_from_back4app",
        "schedule": timedelta(minutes=10),  # Adjust as needed
    }
}

# ----------------------------
# 4. Unlock singleton locks on worker start
# ----------------------------
@worker_ready.connect
def unlock_all(**kwargs):
    clear_locks(celery)
