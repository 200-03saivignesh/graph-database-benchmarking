from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import time

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")

print("Connecting to Neo4j...")
print("URI:", URI)
print("Database:", DATABASE)

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# ==========================
# DATASET
# ==========================

DATASET = "cit-HepPh.txt"

FILE_PATH = os.path.join(
    "data",
    DATASET
)

# ==========================
# SETTINGS
# ==========================

MAX_RELATIONSHIPS = 100000
BATCH_SIZE = 500

# ==========================
# CYPHER QUERY
# ==========================

QUERY = """
UNWIND $rows AS row

MERGE (p1:Paper {id: row.source})
MERGE (p2:Paper {id: row.target})

MERGE (p1)-[:CITES]->(p2)
"""

# ==========================
# CHECK DATASET
# ==========================

if not os.path.exists(FILE_PATH):

    print("ERROR: Dataset not found")
    print(FILE_PATH)

    print("\nAvailable files:")

    for f in os.listdir("data"):
        print("-", f)

    driver.close()
    exit()

print("\nLoading dataset:")
print(FILE_PATH)

# ==========================
# LOAD DATA
# ==========================

batch = []
total = 0

start = time.time()

with open(FILE_PATH, "r", encoding="utf-8") as file:

    for line in file:

        if line.startswith("#"):
            continue

        parts = line.strip().split()

        if len(parts) != 2:
            continue

        source, target = parts

        batch.append({
            "source": source,
            "target": target
        })

        total += 1

        if len(batch) >= BATCH_SIZE:

            with driver.session(database=DATABASE) as session:

                session.run(
                    QUERY,
                    rows=batch
                ).consume()

            print(f"Inserted {total} relationships")

            batch.clear()

        if total >= MAX_RELATIONSHIPS:
            break

# ==========================
# INSERT REMAINING DATA
# ==========================

if batch:

    with driver.session(database=DATABASE) as session:

        session.run(
            QUERY,
            rows=batch
        ).consume()

end = time.time()

print("\n----------------------------")
print("Neo4j Loading Completed")
print("Total relationships:", total)
print("Time:", round(end - start, 2), "seconds")

driver.close()