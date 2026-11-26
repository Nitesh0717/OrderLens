# OrderLens — Retail Data Pipeline & Analytics Engine

OrderLens is an end-to-end retail data engineering project that demonstrates data generation, ETL processing, data quality validation, PostgreSQL warehousing, SQL analytics and interactive dashboard visualization.

## Architecture

CSV Data Sources → ETL & Data Validation → PostgreSQL → Data Warehouse → SQL Analytics → Streamlit Dashboard

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQL
- SQLAlchemy
- Streamlit
- Plotly
- Pytest

## Features

- Synthetic retail dataset generation
- ETL data cleaning and validation
- Rejected-data handling
- PostgreSQL integration
- Star-schema style warehouse (fact and dimension tables)
- SQL-based business analytics
- Automated data quality tests
- Interactive revenue analytics dashboard

## Dataset

- 500 Customers
- 100 Products
- 10,000 Orders

## Dashboard Metrics

- Total Revenue
- Total Orders
- Average Order Value
- Customer Count
- Monthly Revenue Trends
- Revenue by Category
- Revenue by City
- Top 10 Customers

## Project Structure

    OrderLens/
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── src/
    ├── sql/
    ├── tests/
    ├── logs/
    ├── requirements.txt
    └── README.md

## Run the Project

### 1. Clone the repository

    git clone <your-repository-url>
    cd OrderLens

### 2. Create virtual environment

    python3 -m venv .venv
    source .venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Generate data

    python src/generate_data.py

### 5. Run ETL

    python src/etl.py

### 6. Load data

    python src/load_data.py

### 7. Run tests

    pytest -v

### 8. Launch dashboard

    streamlit run src/dashboard.py

## Analytics

The project analyzes retail revenue, monthly sales trends, product categories, customer performance and geographical revenue distribution using SQL and Python.

## Purpose

This project demonstrates practical data engineering fundamentals including ETL, data quality, relational databases, warehouse modeling, analytical SQL and data visualization.
