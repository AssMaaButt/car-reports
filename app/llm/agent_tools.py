from app.neo4j_repo import (
    get_user_from_neo4j,
    get_all_cars_from_neo4j,
    get_cars_filtered
)

def fetch_logged_in_user(user_id: int):
    user = get_user_from_neo4j(user_id)
    if not user:
        return {"error": "User not found in Neo4j"}
    return dict(user)

def fetch_all_cars():
    cars = get_all_cars_from_neo4j()
    return [dict(c) for c in cars]

def fetch_filtered_cars(year: int = None, make: str = None, model: str = None):
    cars = get_cars_filtered(year, make, model)
    return [dict(c) for c in cars]
