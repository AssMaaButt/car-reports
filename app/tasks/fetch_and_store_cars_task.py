import os
import requests
from datetime import datetime
from app.models.car import Car
from app.neo4j_repo import push_car_to_neo4j, push_user_to_neo4j
from sqlalchemy.orm import Session
from app.models.user import User

def fetch_and_store_cars(db):
    """
    Fetch data from Back4App and upsert into local DB.
    Keeps only cars with year in [2012, 2022].
    """

    
    BACK4APP_APP_ID = os.getenv("BACK4APP_APP_ID")
    BACK4APP_REST_KEY = os.getenv("BACK4APP_REST_KEY")
    BACK4APP_URL = os.getenv(
        "BACK4APP_URL",
        "https://parseapi.back4app.com/classes/Car_Model_List"
    )

    headers = {
        "X-Parse-Application-Id": BACK4APP_APP_ID,
        "X-Parse-REST-API-Key": BACK4APP_REST_KEY,
    }

    limit = 1000
    skip = 0
    total_inserted = 0

    while True:
        params = {"limit": limit, "skip": skip}
        resp = requests.get(BACK4APP_URL, headers=headers, params=params, timeout=30)

        if resp.status_code != 200:
            print(f"Back4App fetch failed: {resp.text}")
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

            car = db.query(Car).filter_by(external_id=external_id).first() if external_id else None

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
                    db.add(car)
            else:
                new_car = Car(make=make or "Unknown", model=model, year=year, external_id=external_id)
                db.add(new_car)
                total_inserted += 1

        db.commit()
        if len(results) < limit:
            break
        skip += limit

    print(f"fetch_and_store_cars: inserted={total_inserted}")
    return {"inserted": total_inserted}

def fetch_and_store_cars_with_neo4j(db: Session):
    """
    Calls the existing fetch_and_store_cars to update Postgres,
    then pushes each car to Neo4j.
    """
    result = fetch_and_store_cars(db) 

    
    cars = db.query(Car).all()  

    for car in cars:
        try:
            push_car_to_neo4j(car)
        except Exception as e:
            print(f"Failed to push car {car.id} to Neo4j: {e}")

    users = db.query(User).all()
    for user in users:
        push_user_to_neo4j(user)

    return result