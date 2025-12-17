# app/mcp/server.py

from mcp.server.fastmcp import FastMCP
from app.db import get_db
from app.tasks.fetch_and_store_cars_task import fetch_and_store_cars_with_neo4j
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger("MCP")


mcp = FastMCP("car-report-mcp")

@mcp.tool()
def collect_and_store_cars():
    """
    Fetch cars from Back4App and store in Postgres + Neo4j
    """
    db = next(get_db())
    result = fetch_and_store_cars_with_neo4j(db)
    return result

if __name__ == "__main__":
    print("Starting FastMCP server...", flush=True)
    mcp.run()  

    
    while True:
        time.sleep(10)
