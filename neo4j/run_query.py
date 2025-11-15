import argparse
import pathlib

from tabulate import tabulate

from neo4j import Driver, GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

QUERIES = pathlib.Path(__file__).parent.resolve().joinpath("queries")

def run_query(driver: Driver, cypher_file: str) -> None:

    with open(QUERIES.joinpath(f"{cypher_file}.cypher"), "r", encoding="utf-8") as f:
        query = f.read().strip()

    with driver.session() as session:
        result = session.run(query)
        records = list(result)

        if not records:
            return

        headers = records[0].keys()
        rows = [tuple(r.values()) for r in records]

        print(f"Executing query from: {cypher_file}\n")
        print(tabulate(rows, headers=headers, tablefmt="pretty", numalign="right", stralign="left"))
        print(f"{len(rows)} rows returned.\n")


def main():
    parser = argparse.ArgumentParser(description="Run Cypher query from file")
    parser.add_argument("--file", required=True, help="Path to .cypher file (e.g. 01)")
    args = parser.parse_args()

    driver = GraphDatabase.driver(URI, auth=AUTH)
    run_query(driver, args.file)
    driver.close()


if __name__ == "__main__":
    main()
