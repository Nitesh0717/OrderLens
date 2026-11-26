import pandas as pd

def test_customers():
    df = pd.read_csv("data/processed/customers.csv")
    assert df["customer_id"].is_unique
    assert df["email"].notna().all()

def test_products():
    df = pd.read_csv("data/processed/products.csv")
    assert df["product_id"].is_unique
    assert (df["price"] > 0).all()

def test_orders():
    df = pd.read_csv("data/processed/orders.csv")
    assert df["order_id"].is_unique
    assert (df["quantity"] > 0).all()
    assert (df["total_amount"] >= 0).all()
    assert df["order_date"].notna().all()
