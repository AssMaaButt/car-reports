from neo4j import GraphDatabase
import os


NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test12345")


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def close_driver():
    driver.close()
