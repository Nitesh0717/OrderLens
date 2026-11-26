import pandas as pd
from pathlib import Path
from sqlalchemy import text
from db import engine

DATA = Path("data/processed")

customers = pd.read_csv(DATA / "customers.csv")
products = pd.read_csv(DATA / "products.csv")
orders = pd.read_csv(DATA / "orders.csv")

with engine.begin() as conn:
    conn.execute(text("DELETE FROM fact_orders"))
    conn.execute(text("DELETE FROM dim_products"))
    conn.execute(text("DELETE FROM dim_customers"))

    customers.to_sql("dim_customers", conn, if_exists="append", index=False)
    products.to_sql("dim_products", conn, if_exists="append", index=False)
    orders.to_sql("fact_orders", conn, if_exists="append", index=False)

print("Warehouse loading completed successfully!")
print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
