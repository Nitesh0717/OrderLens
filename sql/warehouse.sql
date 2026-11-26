CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(150),
    email VARCHAR(150),
    city VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES dim_customers(customer_id),
    product_id INTEGER REFERENCES dim_products(product_id),
    quantity INTEGER CHECK (quantity > 0),
    order_date TIMESTAMP,
    total_amount NUMERIC(12,2) CHECK (total_amount >= 0)
);
