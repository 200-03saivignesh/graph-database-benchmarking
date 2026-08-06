from gqlalchemy import Memgraph
from dotenv import load_dotenv
import os

load_dotenv()

HOST = "3.24.177.132"
PORT = 7687
USERNAME = os.getenv("MEMGRAPH_USERNAME")
PASSWORD = os.getenv("MEMGRAPH_PASSWORD")


print("Connecting to Memgraph...")

connection = Memgraph(
    HOST,
    PORT,
    USERNAME,
    PASSWORD,
    encrypted=True
)

result = connection.execute_and_fetch(
    "RETURN 1 AS test"
)

print(next(result))
print("Memgraph connection successful!")