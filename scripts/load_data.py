from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import time


load_dotenv()


URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


print("URI:", URI)
print("USERNAME:", USERNAME)


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# =========================
# GRAPH 3 DATASET
# =========================

DATASET = "wiki-Vote.txt/Wiki-Vote.txt"

FILE_PATH = os.path.join(
    "data",
    DATASET
)


# =========================
# GRAPH SIZE
# =========================

MAX_RELATIONSHIPS = 50000

BATCH_SIZE = 500


# =========================
# CYPHER
# =========================

QUERY = """
UNWIND $rows AS row

MERGE (p1:Paper {id: row.source})
MERGE (p2:Paper {id: row.target})

MERGE (p1)-[:CITES]->(p2)
"""


# =========================
# CHECK DATASET
# =========================

if not os.path.exists(FILE_PATH):

    print("Dataset not found:")
    print(FILE_PATH)

    print("\nAvailable files:")

    for f in os.listdir("data"):
        print("-", f)

    driver.close()
    exit()


print("Loading dataset:")
print(FILE_PATH)


# =========================
# LOAD GRAPH
# =========================

batch = []

total = 0

start = time.time()


with open(
    FILE_PATH,
    "r",
    encoding="utf-8"
) as file:


    for line in file:


        if line.startswith("#"):
            continue


        parts = line.strip().split()


        if len(parts) != 2:
            continue


        source = parts[0]
        target = parts[1]


        batch.append(
            {
                "source": source,
                "target": target
            }
        )


        total += 1


        if len(batch) >= BATCH_SIZE:

            with driver.session() as session:

                session.run(
                    QUERY,
                    rows=batch
                ).consume()


            print(
                f"Inserted {total} relationships"
            )


            batch.clear()



        if total >= MAX_RELATIONSHIPS:
            break



# remaining batch

if batch:

    with driver.session() as session:

        session.run(
            QUERY,
            rows=batch
        ).consume()



end = time.time()


print("-------------------------")
print("Graph 3 loading completed")
print("Total relationships:", total)
print(
    "Time:",
    round(end-start, 2),
    "seconds"
)


driver.close()