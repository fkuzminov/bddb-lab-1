import os
import random
from datetime import datetime, time, timedelta

import faker
from pymongo import MongoClient, database

Faker = faker.Faker("en_GB")

CATEGORIES = {
    "Electronics": ["Smartphones", "Laptops", "Tablets", "Headphones"],
    "Clothing": ["Men's Clothing", "Women's Clothing", "Kids' Clothing", "Shoes"],
    "Home & Garden": ["Furniture", "Kitchen", "Garden Tools", "Decor"],
    "Sports": ["Fitness", "Outdoor", "Team Sports", "Water Sports"],
    "Beauty": ["Skincare", "Makeup", "Hair Care", "Fragrances"]
}
COUNTRIES = ["GE", "SK", "IT", "SL", "NL", "PL", "CZ", "ES", "HU", "RO", "BG", "HR", "FI", "SE", "NO", "DK"]
SHIPMENT_STATUSES = ["pending", "shipped", "delivered", "cancelled"]


def get_mongo_connection() -> database.Database:
    host = os.getenv("MONGO_HOST", "127.0.0.1")
    port = int(os.getenv("MONGO_PORT", 27017))
    db_name = os.getenv("MONGO_DB", "ecommerce")
    client = MongoClient(host, port)
    return client[db_name]


def clear_collections(db: database.Database):
    collections = [
        "products", "categories", "customers", "orders", "order_items", "suppliers", "shipments", "product_suppliers"
    ]
    for collection_name in collections:
        db[collection_name].delete_many({})


def create_categories(db: database.Database) -> dict[str, str]:
    category_ids = {}
    categories_collection = db.categories

    for main_category, subcategories in CATEGORIES.items():
        main_cat_doc = {
            "category_name": main_category,
            "parent_id": None
        }
        result = categories_collection.insert_one(main_cat_doc)
        main_cat_id = result.inserted_id
        category_ids[main_category] = main_cat_id

        for subcategory in subcategories:
            sub_cat_doc = {
                "category_name": subcategory,
                "parent_id": main_cat_id
            }
            result = categories_collection.insert_one(sub_cat_doc)
            category_ids[subcategory] = result.inserted_id

    return category_ids


def create_suppliers(db: database.Database) -> list[str]:
    suppliers_collection = db.suppliers
    supplier_ids = []

    for _ in range(50):
        supplier_doc = {
            "name": Faker.company(),
            "country": random.choice(COUNTRIES)
        }
        result = suppliers_collection.insert_one(supplier_doc)
        supplier_ids.append(result.inserted_id)
    return supplier_ids


def create_products(db: database.Database, category_ids: dict[str, str]) -> dict[str, float]:
    products_collection = db.products
    product_ids = {}
    all_subcategories = [sub for subs in CATEGORIES.values() for sub in subs]
    subcategory_ids = [category_ids[name] for name in all_subcategories]

    for _ in range(1000):
        product_doc = {
            "name": Faker.catch_phrase(),
            "category_id": random.choice(subcategory_ids),
            "price": (price := round(random.uniform(10.0, 1000.0), 2)),
            "stock": random.randint(0, 1000),
        }
        result = products_collection.insert_one(product_doc)
        product_ids[result.inserted_id] = price
    return product_ids


def create_product_suppliers(db: database.Database, product_ids: dict[str, float], supplier_ids: list) -> None:
    product_suppliers_collection = db.product_suppliers
    cnt = 0
    for product_id in product_ids:
        num_suppliers = random.randint(1, 3)
        selected_suppliers = random.sample(supplier_ids, num_suppliers)
        for supplier_id in selected_suppliers:
            product_suppliers_collection.insert_one(
                {"supplier_id": supplier_id, "product_id": product_id}
            )
            cnt += 1


def create_customers(db: database.Database) -> list[str]:
    customers_collection = db.customers
    customer_ids = []

    for _ in range(5000):
        reg_date = Faker.date_between(start_date='-4y', end_date='today')

        customer_doc = {
            "full_name": Faker.name(),
            "email": Faker.email(),
            "registration_date": datetime.combine(reg_date, time.min),
            "country": random.choice(COUNTRIES)
        }
        result = customers_collection.insert_one(customer_doc)
        customer_ids.append(result.inserted_id)
    return customer_ids


def create_orders_and_items(db: database.Database, customer_ids: list, product_ids: dict[str, float]) -> dict[str, datetime.date]:
    orders_collection = db.orders
    order_items_collection = db.order_items
    order_ids = {}
    orders = 0
    for _ in range(10000):
        order_date = Faker.date_between(start_date='-4y', end_date='today')
        order_doc = {
            "customer_id": random.choice(customer_ids),
            "order_date": datetime.combine(order_date, time.min)
        }
        order_result = orders_collection.insert_one(order_doc)
        order_id = order_result.inserted_id
        order_ids[order_id] = order_date

        selected_products = random.sample(list(product_ids.keys()), random.randint(1, 10))
        total_amount = 0.0

        for product_id in selected_products:
            unit_price = product_ids[product_id]
            quantity = random.randint(1, 3)

            order_item_doc = {
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price
            }
            order_items_collection.insert_one(order_item_doc)
            total_amount += unit_price * quantity
            orders += 1
        orders_collection.update_one(
            {"_id": order_id},
            {"$set": {"total_amount": round(total_amount, 2)}}
        )
    return order_ids


def create_shipments(db, order_ids: dict[str, datetime.date]) -> None:
    shipments_collection = db.shipments

    for order_id, order_date in order_ids.items():
        shipment_date = order_date + timedelta(days=random.randint(4, 21))

        shipment_doc = {
            "order_id": order_id,
            "shipment_date": datetime.combine(shipment_date, time.min),
            "status": random.choice(SHIPMENT_STATUSES)
        }
        shipments_collection.insert_one(shipment_doc)


def main():
    db = get_mongo_connection()
    clear_collections(db)

    category_ids = create_categories(db)
    supplier_ids = create_suppliers(db)
    product_ids = create_products(db, category_ids)
    create_product_suppliers(db, product_ids, supplier_ids)
    customer_ids = create_customers(db)

    order_ids = create_orders_and_items(db, customer_ids, product_ids)
    create_shipments(db, order_ids)
    db.orders.create_index("customer_id")
    db.order_items.create_index("order_id")
    db.order_items.create_index("product_id")
    db.product_suppliers.create_index([("product_id", 1), ("supplier_id", 1)])


if __name__ == "__main__":
    main()
