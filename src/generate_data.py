import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

BASE = Path("data/raw")
BASE.mkdir(parents=True, exist_ok=True)

cities = ["Lucknow", "Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Pune", "Jaipur"]
categories = ["Electronics", "Fashion", "Home", "Books", "Sports"]

customers = []
for i in range(1, 501):
    customers.append({
        "customer_id": i,
        "customer_name": f"Customer_{i}",
        "email": f"customer{i}@example.com",
        "city": random.choice(cities),
        "created_at": datetime(2024, 1, 1) + timedelta(days=random.randint(0, 700))
    })

products = []
for i in range(1, 101):
    products.append({
        "product_id": i,
        "product_name": f"Product_{i}",
        "category": random.choice(categories),
        "price": round(random.uniform(100, 25000), 2)
    })

orders = []
for i in range(1, 10001):
    customer_id = random.randint(1, 500)
    product_id = random.randint(1, 100)
    quantity = random.randint(1, 5)
    order_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 699))
    price = products[product_id - 1]["price"]

    orders.append({
        "order_id": i,
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": order_date,
        "total_amount": round(price * quantity, 2)
    })

pd.DataFrame(customers).to_csv(BASE / "customers.csv", index=False)
pd.DataFrame(products).to_csv(BASE / "products.csv", index=False)
pd.DataFrame(orders).to_csv(BASE / "orders.csv", index=False)

print("Dataset generated successfully!")
print(f"Customers: {len(customers)} | Products: {len(products)} | Orders: {len(orders)}")
