# Graph Database Benchmarking Project

## Overview

This project benchmarks multiple graph database platforms using the same citation network dataset.

The goal is to compare graph database performance for different workloads including lookup operations, graph traversals, and aggregation queries.


## Databases Tested

- Neo4j
- Memgraph
- ArangoDB
- CognoDB


## Dataset

Dataset used:

- cit-HepPh (High Energy Physics Citation Network)

Dataset details:

- Type: Citation network graph
- Relationships loaded: 100,000
- Format: Edge list


## Dataset Loading

The dataset was loaded into each graph database using custom Python scripts.

Loading scripts:

```text
scripts/load_neo4j.py
scripts/load_memgraph.py
scripts/load_arango.py
scripts/load_data.py
```
Each database was successfully populated with the same dataset for fair comparison.


## Benchmark Methodology

Each database was tested using the following queries:

- Point Lookup
- 1-Hop Traversal
- 2-Hop Traversal
- 3-Hop Traversal
- Aggregation Query


For every query:

- 20 executions were performed
- p50 latency was measured
- p95 latency was measured
- Results were recorded in milliseconds (ms)




## Benchmark Results

The benchmark results are shown below:

| Database | Point Lookup p50 (ms) | Point Lookup p95 (ms) | 1-Hop p50 (ms) | 1-Hop p95 (ms) | 2-Hop p50 (ms) | 2-Hop p95 (ms) | 3-Hop p50 (ms) | 3-Hop p95 (ms) | Aggregation p50 (ms) | Aggregation p95 (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Neo4j Cloud | 62.23 | 78.09 | 62.38 | 70.01 | 62.34 | 75.91 | 62.39 | 70.16 | 55.06 | 59.09 |
| Memgraph Cloud | 1085.27 | 1093.82 | 1082.40 | 1088.73 | 1087.29 | 1094.80 | 1084.63 | 1092.60 | 1095.15 | 1099.68 |
| ArangoDB Cloud | 264.73 | 272.98 | 265.47 | 318.99 | 265.76 | 307.14 | 265.20 | 307.11 | 279.35 | 403.38 |
| CognoDB Cloud | 257.48 | 269.47 | 261.22 | 263.45 | 261.01 | 267.33 | 261.17 | 273.71 | 260.95 | 264.55 |

The complete benchmark results are available in:

```text
results/benchmark_results.csv

## Technologies Used

- Python
- Neo4j Python Driver
- GQLAlchemy
- ArangoDB Python Driver
- pandas
- matplotlib
- python-dotenv

## Project Structure

```text
graph-task/
│
├── data/
│   └── cit-HepPh.txt
│
├── scripts/
│   ├── check_db.py
│   ├── load_data.py
│   ├── load_neo4j.py
│   ├── load_memgraph.py
│   ├── load_arango.py
│   ├── test_connection.py
│   ├── test_memgraph.py
│   ├── benchmark_neo4j.py
│   ├── benchmark_memgraph.py
│   ├── benchmark_arango.py
│   ├── benchmark_cognodb.py
│   └── create_graphs.py
│
├── results/
│   ├── benchmark_results.csv
│   └── graphs/
│       ├── p50_latency.png
│       └── p95_latency.png
│
├── .env
├── requirements.txt
└── README.md
## Conclusion

The benchmarking experiment compares graph database performance under similar workloads using the same dataset and query patterns.

Neo4j showed the lowest latency in this benchmark environment, while ArangoDB, CognoDB, and Memgraph provided competitive graph traversal capabilities with different performance characteristics.

The results demonstrate how database architecture and query engines influence graph workload performance.
