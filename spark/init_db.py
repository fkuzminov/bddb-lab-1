import datetime
import os
import random

import faker
import pandas as pd

Faker = faker.Faker("de_DE")

cities = [Faker.city() for _ in range(15)]


if __name__ == "__main__":
    os.makedirs("./data", exist_ok=True)
    branches = []
    for idx, city in enumerate(cities):
        for n in range(random.randint(1, 4)):
            branches.append(
                {
                    "id": len(branches) + 1,
                    "branch_name": f"Bank D {city} Filiale {n+1}",
                    "city": city,
                }
            )

    pd.DataFrame(branches).to_parquet("./data/branches.parquet", index=False)

    employees = []
    positions = [
        ("Manager", lambda: random.randint(3, 6), lambda: round(random.randint(60000, 90000), -2)),
        ("Accountant", lambda: random.randint(5, 10), lambda: round(random.randint(48000, 70000), -2)),
        ("Loan Officer", lambda: random.randint(3, 6), lambda: round(random.randint(50000, 70000), -2)),
        ("Customer Service", lambda: random.randint(8, 15), lambda: round(random.randint(40000, 60000), -2)),
        ("Security", lambda: random.randint(2, 3), lambda: round(random.randint(40000, 50000), -2)),
        ("IT Specialist", lambda: random.randint(2, 4), lambda: round(random.randint(55000, 75000), -2)),
        ("Director", lambda: 1, lambda: round(random.randint(90000, 120000), -2)),
    ]
    for branch in branches:
        for position, count_func, salary_func in positions:
            for _ in range(count_func()):
                employees.append(
                    {
                        "id": len(employees) + 1,
                        "full_name": Faker.name(),
                        "branch_id": branch["id"],
                        "position": position,
                        "salary": salary_func(),
                    }
                )

    pd.DataFrame(employees).to_parquet("./data/employees.parquet", engine="pyarrow", index=False)

    customers, accounts = [], []
    account_types = ["Checking", "Savings", "Credit"]
    customer_accounts = dict[int, datetime.date]()
    for branch in branches:
        for _ in range(random.randint(50, 100)):
            customer_id = len(customers) + 1
            customers.append(
                {
                    "id": customer_id,
                    "full_name": Faker.name(),
                    "city": branch["city"],
                    "registration_date": (
                        registration_date := Faker.date_between(start_date='-5y', end_date='today')
                    ).isoformat(),
                }
            )
            if random.random() > 0.96:
                continue

            same_city_branched = [b for b in branches if b["city"] == branch["city"] and b["id"] != branch["id"]]

            for _ in range(random.randint(1, 3)):
                account_id = len(accounts) + 1
                accounts.append(
                    {
                        "id": account_id,
                        "customer_id": customer_id,
                        "account_type": random.choice(account_types),
                        "balance": round(random.uniform(100.0, 100000.0), 2),
                        "branch_id": branch["id"],
                    }
                )
                customer_accounts[account_id] = registration_date

            if same_city_branched and random.random() > 0.95:
                other_branch = random.choice(same_city_branched)
                account_id = len(accounts) + 1
                accounts.append(
                    {
                        "id": account_id,
                        "customer_id": customer_id,
                        "account_type": random.choice(account_types),
                        "balance": round(random.uniform(100.0, 100000.0), 2),
                        "branch_id": other_branch["id"],
                    }
                )
                customer_accounts[account_id] = registration_date

    pd.DataFrame(customers).to_parquet("./data/customers.parquet", engine="pyarrow", index=False)
    pd.DataFrame(accounts).to_parquet("./data/accounts.parquet", engine="pyarrow", index=False)

    transactions = []
    transaction_types = ["Deposit", "Withdrawal", "Transfer", "Payment"]
    for account in accounts:
        if random.random() > 0.96:
            continue

        for _ in range(random.randint(20, 100)):
            account_id = account["id"]
            customer_reg_date = customer_accounts[account_id]
            transactions.append(
                {
                    "id": len(transactions) + 1,
                    "account_id": account_id,
                    "amount": round(random.uniform(10.0, 10000.0), 2),
                    "transaction_date": Faker.date_between(
                        start_date=customer_reg_date, end_date=datetime.date.today()
                    ).isoformat(),
                    "transaction_type": random.choice(transaction_types),
                }
            )

    pd.DataFrame(transactions).to_parquet("./data/transactions.parquet", engine="pyarrow", index=False)
    loans = []
    loan_statuses = ["Active", "Closed", "Defaulted"]
    for customer in customers:
        for _ in range(random.randint(0, 4)):
            loans.append(
                {
                    "id": len(loans) + 1,
                    "customer_id": customer["id"],
                    "loan_amount": round(random.uniform(1000.0, 50000.0), 2),
                    "interest_rate": round(random.uniform(2.0, 10.0), 2),
                    "start_date": Faker.date_between(start_date='-5y', end_date='-6m').isoformat(),
                    "status": random.choice(loan_statuses),
                }
            )
    pd.DataFrame(loans).to_parquet("./data/loans.parquet", engine="pyarrow", index=False)
