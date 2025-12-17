from app.neo4j_connection import driver


def push_car_to_neo4j(car):
    """
    Insert or update a Car node in Neo4j.
    car: SQLAlchemy Car object
    """
    query = """
    MERGE (c:Car {id: $id})
    SET c.make = $make,
        c.model = $model,
        c.year = $year
    """
    with driver.session() as session:
        session.run(query,
                    id=car.id,
                    make=car.make,
                    model=car.model,
                    year=car.year)


def get_all_cars_from_neo4j():
    query = "MATCH (c:Car) RETURN c"
    with driver.session() as session:
        result = session.run(query)
        return [record["c"] for record in result]



def push_user_to_neo4j(user):
    """
    Insert or update a User node in Neo4j.
    user: SQLAlchemy User object
    """
    query = """
    MERGE (u:User {id: $id})
    SET u.username = $username,
        u.email = $email
    """
    with driver.session() as session:
        session.run(query,
                    id=user.id,
                    username=user.username,
                    email=user.email)


def get_all_users_from_neo4j():
    query = "MATCH (u:User) RETURN u"
    with driver.session() as session:
        result = session.run(query)
        return [record["u"] for record in result]

def get_user_from_neo4j(user_id: int):
    query = "MATCH (u:User {id: $id}) RETURN u"
    with driver.session() as session:
        result = session.run(query, id=user_id).single()
        return result["u"] if result else None

def get_cars_filtered(year=None, make=None, model=None):
    conditions = []
    params = {}

    if year:
        conditions.append("c.year = $year")
        params["year"] = year

    if make:
        conditions.append("c.make = $make")
        params["make"] = make

    if model:
        conditions.append("c.model = $model")
        params["model"] = model

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"MATCH (c:Car) {where_clause} RETURN c"

    with driver.session() as session:
        result = session.run(query, **params)
        return [record["c"] for record in result]
