import argparse
import json
import os
import pathlib

from pymongo import MongoClient


QUERIES = pathlib.Path(__file__).parent.resolve().joinpath("queries")


def get_mongo_connection():
    host = os.getenv("MONGO_HOST", "127.0.0.1")
    port = int(os.getenv("MONGO_PORT", 27017))
    db_name = os.getenv("MONGO_DB", "ecommerce")
    client = MongoClient(host, port)
    return client[db_name]


def main():
    parser = argparse.ArgumentParser(description="Run MongoDB query from file")
    parser.add_argument("--file", required=True, help="Query file name (e.g., 01)")
    args = parser.parse_args()

    query_file = QUERIES.joinpath(f"q{args.file}.js")

    with open(query_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    collection_name = args.collection
    pipeline = None

    if "db." in content and ".aggregate(" in content:
        # Extract collection name: db.collection.aggregate([...])
        if not collection_name:
            collection_name = content.split("db.")[1].split(".aggregate")[0]

        # Extract pipeline
        pipeline_start = content.index("[")
        pipeline_end = content.rindex("]") + 1
        pipeline_str = content[pipeline_start:pipeline_end]
        pipeline = json.loads(pipeline_str)
    else:
        print("Error: Could not parse MongoDB query")
        print("File should contain: db.collection.aggregate([...])")
        return

    db = get_mongo_connection()
    collection = db[collection_name]

    print(f"Executing query from: {query_file.name}")
    print(f"Collection: {collection_name}\n")

    results = list(collection.aggregate(pipeline))

    print(f"Results: {len(results)} documents\n")

    # Pretty print results
    for i, doc in enumerate(results, 1):
        print(f"Document {i}:")
        print(json.dumps(doc, indent=2, default=str))
        print()


if __name__ == "__main__":
    main()