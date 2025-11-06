from app import create_app
from app.tasks.fetch_and_store_cars import make_celery
from celery.schedules import crontab

app = create_app()
celery = make_celery(app)

# Periodic task setup
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule: daily at 2:00 AM (example)
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        sync_from_back4app.s(),
        name="daily-sync"
    )

@celery.task(name="sync_from_back4app")
def sync_from_back4app():
    from app.tasks.fetch_and_store_cars import fetch_and_store_cars
    return fetch_and_store_cars()
