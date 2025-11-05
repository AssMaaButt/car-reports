# app/tasks.py
# Celery helper + fetch logic for Back4App dataset
import requests
from datetime import datetime
from celery import Celery
from flask import current_app
from ..models.models import Car
from app import db

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config.get("CELERY_BROKER_URL"), backend=app.config.get("CELERY_RESULT_BACKEND"))
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def fetch_and_store_cars():
    """
    Synchronous helper to fetch data from Back4App and upsert into local DB.
    Keeps only cars with year in [2012, 2022]. Updates existing records (non-destructive).
    """
    app = current_app._get_current_object()
    headers = {
        "X-Parse-Application-Id": app.config.get("BACK4APP_APP_ID"),
        "X-Parse-REST-API-Key": app.config.get("BACK4APP_REST_KEY"),
    }
    url = app.config.get("BACK4APP_URL", "https://parseapi.back4app.com/classes/Car_Model_List")

    # Pagination: Back4App uses 'limit' and 'skip' typical of parse
    limit = 1000
    skip = 0
    total_inserted = 0
    while True:
        params = {"limit": limit, "skip": skip}
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            app.logger.error("Back4App fetch failed: %s", resp.text)
            break
        data = resp.json()
        results = data.get("results") or data.get("rows") or []
        if not results:
            break
        for item in results:
            # dataset fields may vary; attempt common keys
            external_id = item.get("objectId") or item.get("id") or item.get("ObjectId")
            make = item.get("make") or item.get("Make") or item.get("manufacturer")
            model = item.get("model") or item.get("Model")
            raw_year = item.get("year") or item.get("Year")
            try:
                year = int(raw_year) if raw_year else None
            except Exception:
                year = None
            # only keep 2012..2022
            if year and not (2012 <= year <= 2022):
                continue

            if external_id:
                car = Car.query.filter_by(external_id=external_id).first()
            else:
                car = None

            if car:
                updated = False
                if make and car.make != make:
                    car.make = make
                    updated = True
                if model and car.model != model:
                    car.model = model
                    updated = True
                if year and car.year != year:
                    car.year = year
                    updated = True
                if updated:
                    car.updated_at = datetime.utcnow()
                    db.session.add(car)
            else:
                # create new
                new_car = Car(make=make or "Unknown", model=model, year=year, external_id=external_id)
                db.session.add(new_car)
                total_inserted += 1
        db.session.commit()
        if len(results) < limit:
            break
        skip += limit
    app.logger.info("fetch_and_store_cars: inserted=%d", total_inserted)
    return {"inserted": total_inserted}
