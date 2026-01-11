import argparse
import json
import pathlib

from elasticsearch import Elasticsearch

QUERIES = pathlib.Path(__file__).parent.resolve().joinpath("queries")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to the query JSON file - 01 is for 01.json")
    parser.add_argument("--explain", action="store_true", help="Enable query profiling")
    args = parser.parse_args()

    es = Elasticsearch(
        ["http://127.0.0.1:9200"],
        basic_auth=("elastic", "password"),
        verify_certs=False,
        ssl_show_warn=False,
    )

    file = QUERIES.joinpath(f"{args.file}.json")
    with open(file, "r") as f:
        query = json.load(f)

    print(f"Executing query from {file}.")
    resp = es.search(index="finance", body=query)
    print(json.dumps(resp.body, indent=2, default=str))

    if args.explain:
        query["profile"] = True
        print("\n" + "=" * 60)
        print("PROFILE:\n")
        resp = es.search(index="finance", body=query)
        if "profile" in resp.body:
            print(json.dumps(resp.body["profile"], indent=2, default=str))

if __name__ == "__main__":
    main()
