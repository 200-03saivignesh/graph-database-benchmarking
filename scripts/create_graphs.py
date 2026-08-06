import pandas as pd
import matplotlib.pyplot as plt
import os


df = pd.read_csv("results/benchmark_results.csv")


os.makedirs("results/graphs", exist_ok=True)


# p50 graph
plt.figure(figsize=(10,5))

for db in df["Database"].unique():
    temp = df[df["Database"] == db]
    plt.plot(
        temp["Query"],
        temp["p50_ms"],
        marker="o",
        label=db
    )

plt.xticks(rotation=45)
plt.ylabel("p50 Latency (ms)")
plt.title("Graph Database Benchmark - p50 Latency")
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/graphs/p50_latency.png"
)

plt.close()



# p95 graph
plt.figure(figsize=(10,5))

for db in df["Database"].unique():
    temp = df[df["Database"] == db]
    plt.plot(
        temp["Query"],
        temp["p95_ms"],
        marker="o",
        label=db
    )

plt.xticks(rotation=45)
plt.ylabel("p95 Latency (ms)")
plt.title("Graph Database Benchmark - p95 Latency")
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/graphs/p95_latency.png"
)

plt.close()


print("Graphs created successfully!")