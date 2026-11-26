import pandas as pd
from pathlib import Path
import logging

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def process_file(name, required_columns, key):
    df = pd.read_csv(RAW / f"{name}.csv")
    initial_count = len(df)

    df.columns = df.columns.str.strip().str.lower()

    rejected = pd.DataFrame()

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"{name}: Missing columns: {missing_columns}")

    df = df.drop_duplicates()

    invalid = df[key].isna()
    rejected = pd.concat([rejected, df[invalid]], ignore_index=True)
    df = df[~invalid]

    df[key] = pd.to_numeric(df[key], errors="coerce")
    invalid_key = df[key].isna()
    rejected = pd.concat([rejected, df[invalid_key]], ignore_index=True)
    df = df[~invalid_key]

    df[key] = df[key].astype(int)

    if name == "orders":
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        invalid = (
            df["quantity"].isna() |
            df["total_amount"].isna() |
            df["order_date"].isna() |
            (df["quantity"] <= 0) |
            (df["total_amount"] < 0)
        )
    elif name == "products":
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        invalid = df["price"].isna() | (df["price"] <= 0)
    elif name == "customers":
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        invalid = (
            df["customer_name"].isna() |
            df["email"].isna() |
            df["created_at"].isna()
        )

    rejected = pd.concat([rejected, df[invalid]], ignore_index=True)
    df = df[~invalid]

    df = df.drop_duplicates(subset=[key], keep="last")

    df.to_csv(PROCESSED / f"{name}.csv", index=False)
    rejected.to_csv(PROCESSED / f"{name}_rejected.csv", index=False)

    logging.info("%s | Input=%s | Valid=%s | Rejected=%s",
                 name, initial_count, len(df), len(rejected))

    print(f"{name}: {initial_count} input -> {len(df)} valid -> {len(rejected)} rejected")

def main():
    process_file(
        "customers",
        ["customer_id", "customer_name", "email", "city", "created_at"],
        "customer_id"
    )
    process_file(
        "products",
        ["product_id", "product_name", "category", "price"],
        "product_id"
    )
    process_file(
        "orders",
        ["order_id", "customer_id", "product_id", "quantity", "order_date", "total_amount"],
        "order_id"
    )
    print("ETL processing completed!")

if __name__ == "__main__":
    main()
