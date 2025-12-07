from app.neo4j_connection import driver

# ----------------------------
# Car functions
# ----------------------------
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


# ----------------------------
# User functions
# ----------------------------
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
