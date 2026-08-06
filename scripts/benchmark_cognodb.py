import time
from statistics import median
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os


load_dotenv()


URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


print("Connecting to CognoDB...")
print("URI:", URI)


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)



def benchmark(query, runs=20):

    times = []

    with driver.session() as session:

        for _ in range(runs):

            start = time.perf_counter()

            session.run(query).consume()

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
    MATCH (n:Paper {id:'12345'})
    RETURN n
    """,


    "1-Hop Traversal":
    """
    MATCH (n:Paper {id:'12345'})-[:CITES]->(m)
    RETURN m
    """,


    "2-Hop Traversal":
    """
    MATCH (n:Paper {id:'12345'})-[:CITES*2]->(m)
    RETURN m
    """,


    "3-Hop Traversal":
    """
    MATCH (n:Paper {id:'12345'})-[:CITES*3]->(m)
    RETURN m
    """,


    "Aggregation":
    """
    MATCH ()-[r:CITES]->()
    RETURN count(r)
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


driver.close()