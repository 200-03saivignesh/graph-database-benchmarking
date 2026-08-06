import time
from statistics import median
from dotenv import load_dotenv
import os

from arango import ArangoClient


load_dotenv()


URL = os.getenv("ARANGO_URL")
USERNAME = os.getenv("ARANGO_USERNAME")
PASSWORD = os.getenv("ARANGO_PASSWORD")


print("Connecting to ArangoDB...")
print("URL:", URL)


client = ArangoClient(hosts=URL)

sys_db = client.db(
    "_system",
    username=USERNAME,
    password=PASSWORD
)

db = sys_db


def benchmark(query, runs=20):

    times = []

    for _ in range(runs):

        start = time.perf_counter()

        cursor = db.aql.execute(query)

        list(cursor)

        end = time.perf_counter()

        times.append(
            (end-start)*1000
        )


    times.sort()

    p50 = median(times)

    p95 = times[int(len(times)*0.95)-1]

    return p50, p95



queries = {

    "Point Lookup":
    """
    FOR p IN papers
    FILTER p._key == "12345"
    RETURN p
    """,


    "1-Hop Traversal":
    """
    FOR p IN papers
    FILTER p._key == "12345"
    FOR v,e IN 1..1 OUTBOUND p cites
    RETURN v
    """,


    "2-Hop Traversal":
    """
    FOR p IN papers
    FILTER p._key == "12345"
    FOR v,e IN 2..2 OUTBOUND p cites
    RETURN v
    """,


    "3-Hop Traversal":
    """
    FOR p IN papers
    FILTER p._key == "12345"
    FOR v,e IN 3..3 OUTBOUND p cites
    RETURN v
    """,


    "Aggregation":
    """
    FOR e IN cites
    COLLECT WITH COUNT INTO count
    RETURN count
    """
}



print()

print(
    f"{'Query':30} {'p50(ms)':>12} {'p95(ms)':>12}"
)

print("-"*60)


for name, query in queries.items():

    p50, p95 = benchmark(query)

    print(
        f"{name:30} {p50:12.2f} {p95:12.2f}"
    )