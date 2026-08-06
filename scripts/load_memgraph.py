from gqlalchemy import Memgraph
from dotenv import load_dotenv
import os
import time


# ==========================
# LOAD ENV
# ==========================

load_dotenv()


HOST = "3.24.177.132"
PORT = 7687

USERNAME = os.getenv("MEMGRAPH_USERNAME")
PASSWORD = os.getenv("MEMGRAPH_PASSWORD")


print("Connecting to Memgraph...")
print("Host:", HOST)
print("Username:", USERNAME)


connection = Memgraph(
    HOST,
    PORT,
    USERNAME,
    PASSWORD,
    encrypted=True
)


# ==========================
# DATASET
# ==========================

FILE_PATH = "data/cit-HepPh.txt"

MAX_RELATIONSHIPS = 100000
BATCH_SIZE = 500


# ==========================
# CLEAR OLD DATA
# ==========================

print("Clearing old data...")

connection.execute(
    "MATCH (n) DETACH DELETE n"
)


# ==========================
# INSERT QUERY
# ==========================

QUERY = """
UNWIND $rows AS row

MERGE (p1:Paper {id: row.source})
MERGE (p2:Paper {id: row.target})

MERGE (p1)-[:CITES]->(p2)
"""


# ==========================
# CHECK FILE
# ==========================

if not os.path.exists(FILE_PATH):

    print("Dataset not found:")
    print(FILE_PATH)
    exit()


print("\nLoading dataset:")
print(FILE_PATH)


# ==========================
# LOAD DATA
# ==========================

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


            connection.execute(
                QUERY,
                {
                    "rows": batch
                }
            )


            print(
                f"Inserted {total} relationships"
            )


            batch.clear()


        if total >= MAX_RELATIONSHIPS:
            break



# Remaining batch

if batch:

    connection.execute(
        QUERY,
        {
            "rows": batch
        }
    )


end = time.time()


print("-------------------------")
print("Memgraph Loading Completed")
print("Total relationships:", total)
print(
    "Time:",
    round(end-start, 2),
    "seconds"
)