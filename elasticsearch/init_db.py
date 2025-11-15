import random
import time
import uuid

import faker

import elasticsearch as es
from elasticsearch.helpers import bulk

Faker = faker.Faker("de_DE")


if __name__ == "__main__":
    esearch = es.Elasticsearch(
        hosts=["http://127.0.0.1:9200"],
        basic_auth=("elastic", "password"),
        verify_certs=False,
        ssl_show_warn=False,
    )
    while not esearch.ping():
        print("Waiting for Elasticsearch to be available...")
        time.sleep(2)

    index_name = "finance"
    if not esearch.indices.exists(index=index_name):
        esearch.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    "customer_id": {"type": "keyword"},
                    "customer_name": {"type": "text"},
                    "account_id": {"type": "keyword"},
                    "account_type": {"type": "keyword"},
                    "balance": {"type": "float"},
                    "branch": {"type": "keyword"},
                    "transaction_id": {"type": "keyword"},
                    "transaction_date": {"type": "date"},
                    "transaction_type": {"type": "keyword"},
                    "amount": {"type": "float"},
                    "loan_id": {"type": "keyword"},
                    "loan_amount": {"type": "float"},
                    "loan_status": {"type": "keyword"},
                }
            },
        )
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

    customers: list[tuple[str, str]] = [
        (str(uuid.uuid4()), f"{Faker.first_name()} {Faker.last_name()}")
        for _ in range(200)
    ]
    cities = [Faker.city() for _ in range(5)]
    branches = []
    for c in cities:
        for d in ["north", "south", "east", "west", "central"]:
            branches.append(f"{c} {d.title()} branch")

    a_types = ["savings", "checking", "credit"]

    accounts = []
    for c in customers:
        b = random.choice(branches)
        for _ in range(random.randint(1, 3)):
            account_id = random.randint(10000000, 99999999)
            account_type = random.choice(a_types)
            accounts.append((c[0], c[1], account_id, account_type, b))

    trns = []
    for _ in range(5000):
        a = random.choice(accounts)
        customer_id, customer_name, account_id, account_type, branch = a
        doc = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "account_id": str(account_id),
            "account_type": account_type,
            "balance": round(random.uniform(1000, 100000), 2),
            "branch": branch,
            "transaction_id": str(uuid.uuid4()),
            "transaction_date": Faker.date_between(start_date='-1y', end_date='today'),
            "transaction_type": random.choice(["deposit", "withdrawal", "transfer", "payment"]),
            "amount": round(random.uniform(10, 5000), 2),
            "loan_id": str(uuid.uuid4()),
            "loan_amount": round(random.uniform(5000, 50000), 2),
            "loan_status": random.choice(["approved", "pending", "rejected", "active"]),
        }
        trns.append(doc)

    bulk(esearch, ({'_index': index_name, '_source': doc} for doc in trns))
