from arango import ArangoClient
from dotenv import load_dotenv
import os
import time


# ==========================
# LOAD ENV
# ==========================

load_dotenv()


ARANGO_URL = os.getenv("ARANGO_URL")
USERNAME = os.getenv("ARANGO_USERNAME")
PASSWORD = os.getenv("ARANGO_PASSWORD")


print("Connecting to ArangoDB...")
print("URL:", ARANGO_URL)
print("USERNAME:", USERNAME)


# ==========================
# CONNECTION
# ==========================

client = ArangoClient(hosts=ARANGO_URL)

db = client.db(
    "_system",
    username=USERNAME,
    password=PASSWORD
)


print("Connected to ArangoDB")


# ==========================
# COLLECTIONS
# ==========================

VERTEX_COLLECTION = "papers"
EDGE_COLLECTION = "cites"


# Remove old collections if they exist

if db.has_collection(EDGE_COLLECTION):
    db.delete_collection(EDGE_COLLECTION)

if db.has_collection(VERTEX_COLLECTION):
    db.delete_collection(VERTEX_COLLECTION)


# Create collections

papers = db.create_collection(
    VERTEX_COLLECTION
)

cites = db.create_collection(
    EDGE_COLLECTION,
    edge=True
)


print("Collections created")


# ==========================
# DATASET
# ==========================

FILE_PATH = "data/cit-HepPh.txt"

MAX_RELATIONSHIPS = 100000
BATCH_SIZE = 500


# ==========================
# LOAD DATA
# ==========================

batch_vertices = {}
batch_edges = []

total = 0

start = time.time()


print("Loading dataset:")
print(FILE_PATH)


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


        batch_vertices[source] = {
            "_key": source
        }

        batch_vertices[target] = {
            "_key": target
        }


        batch_edges.append(
            {
                "_from": f"{VERTEX_COLLECTION}/{source}",
                "_to": f"{VERTEX_COLLECTION}/{target}"
            }
        )


        total += 1


        if len(batch_edges) >= BATCH_SIZE:


            papers.insert_many(
                list(batch_vertices.values()),
                overwrite=True
            )


            cites.insert_many(
                batch_edges
            )


            print(
                f"Inserted {total} relationships"
            )


            batch_vertices.clear()
            batch_edges.clear()


        if total >= MAX_RELATIONSHIPS:
            break



# Remaining data

if batch_edges:

    papers.insert_many(
        list(batch_vertices.values()),
        overwrite=True
    )

    cites.insert_many(
        batch_edges
    )


end = time.time()


print("-------------------------")
print("ArangoDB Loading Completed")
print("Total relationships:", total)
print(
    "Time:",
    round(end-start,2),
    "seconds"
)