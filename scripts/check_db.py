from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

with driver.session() as session:

    nodes = session.run(
        "MATCH (n) RETURN count(n) AS count"
    ).single()["count"]

    relations = session.run(
        "MATCH ()-[r:CITES]->() RETURN count(r) AS count"
    ).single()["count"]

    print("Nodes:", nodes)
    print("Relationships:", relations)

driver.close()