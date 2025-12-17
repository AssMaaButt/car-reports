from datetime import timedelta
import os
from celery import Celery
from celery.signals import worker_ready
from celery_singleton import clear_locks
from app.neo4j_repo import push_car_to_neo4j
import asyncio
from app.mcp.client import call_collect_and_store_cars


celery = Celery(
    "celery",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    broker_connection_retry_on_startup=True,
)

@celery.task(name="sync_from_back4app")
def sync_from_back4app():
    """
    Calls the MCP tool 'collect_and_store_cars' via running MCP server.
    """
    try:
        result = asyncio.run(call_collect_and_store_cars())
        return result
    except Exception as e:
        return {"error": str(e)}


celery.conf.beat_schedule = {
    "daily_sync_from_back4app": {
        "task": "sync_from_back4app",
        "schedule": timedelta(minutes=10), 
    }
}

@worker_ready.connect
def unlock_all(**kwargs):
    clear_locks(celery)
