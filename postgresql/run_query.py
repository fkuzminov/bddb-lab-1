import argparse
import os
import pathlib

import psycopg2
from tabulate import tabulate


QUERIES = pathlib.Path(__file__).parent.resolve().joinpath("queries")


def get_dns() -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    port = os.getenv("POSTGRES_PORT", 5432)
    dbname = os.getenv("POSTGRES_DB", "students")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def main():
    parser = argparse.ArgumentParser(description="Run PostgreSQL query from file")
    parser.add_argument("--file", required=True, help="Query file name (e.g., 01)")
    parser.add_argument("--explain", action="store_true", help="Run EXPLAIN ANALYZE on the query")
    args = parser.parse_args()

    query_file = QUERIES.joinpath(f"q{args.file}.sql")

    with open(query_file, "r", encoding="utf-8") as f:
        query = f.read().strip()

    conn = psycopg2.connect(dsn=get_dns())
    cursor = conn.cursor()

    print(f"Executing query from: {query_file.name}\n")
    cursor.execute(query)

    results = cursor.fetchall()

    if results:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(results, headers=headers, tablefmt="pretty"))
        print(f"\n{len(results)} rows returned.\n")
    else:
        print("No results returned.\n")

    if args.explain:
        print("=" * 60)
        print("EXPLAIN ANALYZE:\n")
        cursor.execute(f"EXPLAIN ANALYZE {query}")
        explain_results = cursor.fetchall()
        for row in explain_results:
            print(row[0])

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()