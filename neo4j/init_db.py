import random

from faker import Faker

from neo4j import GraphDatabase

fake = Faker("en_GB")

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)

def clear_db(tx):
    tx.run("MATCH (n) DETACH DELETE n")

def create_data(tx):
    supplier_dict = {}
    country_list = list(set(fake.country() for _ in range(10)))
    for _ in range(50):
        supplier_name = fake.company()
        supplier_country = random.choice(country_list)
        tx.run("""
            MERGE (s:Supplier {name: $name, country: $country})
        """, name=supplier_name, country=supplier_country)
        supplier_dict[supplier_name] = None

    warehouse_dict = {}
    direction_list = ["North", "South", "East", "West", "Central"]
    city_list = [fake.city() for _ in range(30)]
    for city in city_list[:20]:
        random.shuffle(direction_list)
        warehouse_name = f"{city} Warehouse {direction_list[0]}"
        tx.run("""
            MERGE (w:Warehouse {name: $name, city: $city})
        """, name=warehouse_name, city=city)
        warehouse_dict[warehouse_name] = None
        if random.random() < 0.3:
            warehouse_name2 = f"{city} Warehouse {direction_list[1]}"
            tx.run("""
                MERGE (w:Warehouse {name: $name, city: $city})
            """, name=warehouse_name2, city=city)
            warehouse_dict[warehouse_name2] = None

    store_dict = {}
    for _ in range(50):
        city = random.choice(city_list)
        while (store_name := f"{city} {random.choice(direction_list)} Store") in store_dict:
            continue
        tx.run("""
            MERGE (s:Store {name: $name, city: $city})
        """, name=store_name, city=city)
        store_dict[store_name] = []

    categories_dict = {
        "Electronics": [
            ("MacBook Pro M3 13", 1499.0),
            ("MacBook Pro M3 14", 1799.0),
            ("MacBook Pro M3 16", 2199.0),
            ("MacBook Air M3 13", 1299.0),
            ("MacBook Pro M4 13", 1599.0),
            ("MacBook Pro M4 14", 1899.0),
            ("MacBook Pro M4 16", 2299.0),
            ("MacBook Air M4 13", 1399.0),
            ("Dell XPS 13", 1200.0),
            ("Dell XPS 15", 1500.0),
            ("Dell XPS 17", 1800.0),
            ("Lenovo ThinkPad X1 Carbon", 1600.0),
            ("Lenovo ThinkPad X1 Yoga", 1700.0),
            ("HP Spectre x360 13", 1300.0),
            ("HP Spectre x360 15", 1500.0),
            ("HP Envy 13", 1100.0),
            ("HP Envy 15", 1300.0),
            ("iPhone 15", 999.0),
            ("iPhone 15 Pro", 1199.0),
            ("iPhone 15 Pro Max", 1399.0),
            ("iPhone 15 Mini", 899.0),
            ("Samsung Galaxy S23", 950.0),
            ("Samsung Galaxy S23+", 1050.0),
            ("Samsung Galaxy S23 Ultra", 1250.0),
            ("Samsung Galaxy Note 23", 1100.0),
            ("Google Pixel 8", 800.0),
            ("Google Pixel 8 Pro", 1000.0),
            ("OnePlus 11", 750.0),
            ("OnePlus 11 Pro", 900.0),
            ("iPad Pro 11", 950.0),
            ("iPad Pro 12.9", 1200.0),
            ("iPad Air 10.9", 700.0),
            ("iPad Mini 8.3", 600.0),
            ("Samsung Galaxy Tab S8", 800.0),
            ("Samsung Galaxy Tab S8+", 950.0),
            ("Samsung Galaxy Tab S8 Ultra", 1100.0),
            ("AirPods Pro 2", 300.0),
            ("AirPods Max", 600.0),
            ("Apple Watch Series 9", 450.0),
            ("Apple Watch Ultra 2", 900.0),
            ("Galaxy Buds Pro 2", 200.0),
            ("Galaxy Watch 6", 350.0),
            ("Galaxy Watch 6 Classic", 400.0),
            ("Surface Pro 9", 1200.0),
            ("Surface Laptop 5", 1300.0),
            ("Surface Go 3", 600.0),
            ("Canon EOS R5", 4000.0),
            ("Canon EOS R6", 2500.0),
            ("Nikon Z7 II", 3000.0),
            ("Nikon Z6 II", 2000.0),
        ],
        "Food": [
            ("Organic Apples", 3.0),
            ("Bananas", 2.0),
            ("Whole Wheat Bread", 2.5),
            ("Almond Milk", 2.0),
            ("Free-Range Eggs", 3.5),
            ("Greek Yogurt", 1.5),
            ("Quinoa", 4.0),
            ("Chia Seeds", 5.0),
            ("Avocado", 2.0),
            ("Kale", 2.5),
            ("Salmon Fillet", 8.0),
            ("Chicken Breast", 6.0),
            ("Brown Rice", 2.0),
            ("Black Beans", 1.5),
            ("Hummus", 2.0),
            ("Olive Oil", 6.0),
            ("Dark Chocolate", 3.0),
            ("Granola Bars", 2.5),
            ("Mixed Nuts", 4.0),
            ("Coconut Water", 2.0),
            ("Turmeric Powder", 3.0),
            ("Cinnamon Sticks", 2.0),
            ("Honey", 4.0),
            ("Peanut Butter", 3.0),
            ("Maple Syrup", 5.0),
        ],
        "Sports": [
            ("Soccer Ball", 25.0),
            ("Basketball", 30.0),
            ("Tennis Racket", 60.0),
            ("Running Shoes", 80.0),
            ("Yoga Mat", 20.0),
            ("Dumbbell Set", 50.0),
            ("Fitness Tracker", 100.0),
            ("Cycling Helmet", 40.0),
            ("Golf Clubs", 300.0),
            ("Baseball Glove", 35.0),
            ("Volleyball", 25.0),
            ("Swim Goggles", 15.0),
            ("Hiking Backpack", 60.0),
            ("Treadmill", 700.0),
            ("Exercise Bike", 500.0),
            ("Jump Rope", 10.0),
            ("Boxing Gloves", 40.0),
            ("Skateboard", 60.0),
            ("Ski Goggles", 50.0),
            ("Snowboard", 250.0),
            ("Tread Shoes", 90.0),
            ("Cricket Bat", 70.0),
            ("Badminton Set", 30.0),
            ("Rowing Machine", 600.0),
            ("Pull-Up Bar", 35.0),
        ],
        "Home": [
            ("Sofa", 400.0),
            ("Dining Table", 350.0),
            ("Queen Bed Frame", 300.0),
            ("Office Chair", 120.0),
            ("Bookshelf", 80.0),
            ("Lamp", 40.0),
            ("Area Rug", 90.0),
            ("Curtains", 30.0),
            ("Coffee Table", 100.0),
            ("TV Stand", 110.0),
            ("Dresser", 150.0),
            ("Nightstand", 60.0),
            ("Wall Art", 50.0),
            ("Throw Pillows", 25.0),
            ("Kitchen Island", 200.0),
            ("Bar Stools", 70.0),
            ("Floor Lamp", 60.0),
            ("Ceiling Fan", 120.0),
            ("Mirror", 80.0),
            ("Storage Ottoman", 90.0),
            ("Desk Organizer", 20.0),
            ("Bedside Lamp", 35.0),
            ("Picture Frame", 15.0),
            ("Vase", 25.0),
            ("Candle Set", 20.0),
        ],
        "Clothing": [
            ("T-Shirt", 20.0),
            ("Jeans", 50.0),
            ("Sneakers", 80.0),
            ("Jacket", 70.0),
            ("Dress", 60.0),
            ("Sweater", 40.0),
            ("Skirt", 35.0),
            ("Boots", 90.0),
            ("Hat", 25.0),
            ("Scarf", 20.0),
        ],
        "Stationery": [
            ("Ballpoint Pen", 1.5),
            ("Gel Pen", 2.0),
            ("Mechanical Pencil", 2.5),
            ("Notebook", 3.0),
            ("Sticky Notes", 1.0),
            ("Highlighter", 1.5),
            ("Eraser", 0.8),
            ("Ruler", 1.2),
            ("Stapler", 4.0),
            ("Paper Clips", 0.5),
            ("Correction Tape", 2.0),
            ("Scissors", 3.0),
            ("Glue Stick", 1.2),
            ("Binder", 2.5),
            ("Desk Organizer", 5.0),
            ("File Folder", 1.0),
            ("Push Pins", 0.7),
            ("Whiteboard Marker", 1.8),
            ("Calculator", 10.0),
            ("Drawing Pad", 4.0),
        ]
    }
    for category, items in categories_dict.items():
        for product_name, product_price in items:
            tx.run("""
                MERGE (p:Product {name: $name, category: $category, price: $price})
            """, name=product_name, category=category, price=product_price)

    for supplier in supplier_dict:
        supplier_dict[supplier] = random.choice(list(categories_dict.keys()))

    for warehouse in warehouse_dict:
        warehouse_dict[warehouse] = random.sample(list(categories_dict.keys()), k=random.randint(3, 5))

    for warehouse, categories in warehouse_dict.items():
        for category in categories:
            suppliers_for_category = [s for s, cat in supplier_dict.items() if cat == category]
            selected_suppliers = random.sample(suppliers_for_category, k=int(len(suppliers_for_category) / 3))
            for supplier in selected_suppliers:
                tx.run("""
                    MATCH (s:Supplier {name: $supplier})
                    MATCH (w:Warehouse {name: $warehouse})
                    MERGE (s)-[:SUPPLIES]->(w)
                """, supplier=supplier, warehouse=warehouse)

    for category, products in categories_dict.items():
        warehouses_for_category = [w for w, cats in warehouse_dict.items() if category in cats]
        for product_name, _ in products:
            selected_warehouses = random.sample(warehouses_for_category, k=random.randint(1, int(len(warehouses_for_category)/3 + 1)))
            for warehouse in selected_warehouses:
                quantity = random.randint(100, 1000)
                tx.run("""
                    MATCH (w:Warehouse {name: $warehouse})
                    MATCH (p:Product {name: $product})
                    MERGE (w)-[:STOCKS {quantity: $quantity}]->(p)
                """, warehouse=warehouse, product=product_name, quantity=quantity)

    for store, categories in store_dict.items():
        selected_categories = random.sample(list(categories_dict.keys()), k=random.randint(2, 4))
        store_dict[store] = selected_categories

    for store, categories in store_dict.items():
        warehouses_for_store = [w for w, wcats in warehouse_dict.items() if any(cat in wcats for cat in categories)]
        connected_warehouses = random.sample(warehouses_for_store, k=min(random.randint(3, 7), int(len(warehouses_for_store) / 3 * 2)))
        for warehouse in connected_warehouses:
            distance = round(random.uniform(50.0, 1000.0), 1)
            time = round(distance / random.uniform(60, 120) * 60, 1)
            tx.run("""
                MATCH (w:Warehouse {name: $warehouse})
                MATCH (s:Store {name: $store})
                MERGE (w)-[:ROUTE {distance: $distance, time: $time}]->(s)
            """, warehouse=warehouse, store=store, distance=distance, time=time)

    for store, categories in store_dict.items():
        product_list = []
        for category in categories:
            product_list += random.sample(categories_dict[category], k=int(len(categories_dict[category]) / 2))
        for product in product_list:
            quantity = random.randint(10, 50)
            tx.run("""
                MATCH (s:Store {name: $store})
                MATCH (p:Product {name: $product})
                MERGE (s)-[:ORDERS {quantity: $quantity}]->(p)
            """, store=store, product=product[0], quantity=quantity)

def main():
    with driver.session() as session:
        session.execute_write(clear_db)
        session.execute_write(create_data)

if __name__ == "__main__":
    main()
