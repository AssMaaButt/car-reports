# app/tasks/fetch_and_store_cars_task.py
import requests
from datetime import datetime
from flask import current_app
from app.models.car import Car
from app import db

def fetch_and_store_cars():
    """
    Fetch data from Back4App and upsert into local DB.
    Keeps only cars with year in [2012, 2022].
    """
    app = current_app._get_current_object()
    headers = {
        "X-Parse-Application-Id": app.config.get("BACK4APP_APP_ID"),
        "X-Parse-REST-API-Key": app.config.get("BACK4APP_REST_KEY"),
    }
    url = app.config.get("BACK4APP_URL", "https://parseapi.back4app.com/classes/Car_Model_List")

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
            external_id = item.get("objectId") or item.get("id") or item.get("ObjectId")
            make = item.get("make") or item.get("Make") or item.get("manufacturer")
            model = item.get("model") or item.get("Model")
            raw_year = item.get("year") or item.get("Year")

            try:
                year = int(raw_year) if raw_year else None
            except Exception:
                year = None

            if year and not (2012 <= year <= 2022):
                continue

            car = Car.query.filter_by(external_id=external_id).first() if external_id else None

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
                new_car = Car(make=make or "Unknown", model=model, year=year, external_id=external_id)
                db.session.add(new_car)
                total_inserted += 1

        db.session.commit()
        if len(results) < limit:
            break
        skip += limit

    app.logger.info("fetch_and_store_cars: inserted=%d", total_inserted)
    return {"inserted": total_inserted}
