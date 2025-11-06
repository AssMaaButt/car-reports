# app/tasks/celery_app.py
from app import create_app
from celery import Celery
from celery.schedules import crontab

app = create_app()

def make_celery(app):
    """Initialize Celery with Flask app context."""
    celery = Celery(
        app.import_name,
        broker=app.config.get("CELERY_BROKER_URL"),
        backend=app.config.get("CELERY_RESULT_BACKEND")
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Periodic task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        sync_from_back4app.s(),
        name="daily-sync"
    )

# Celery task
@celery.task(name="sync_from_back4app")
def sync_from_back4app():
    from app.tasks.fetch_and_store_cars_task import fetch_and_store_cars
    return fetch_and_store_cars()
