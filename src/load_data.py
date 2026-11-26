import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

for table in ["customers", "products", "orders"]:
    df = pd.read_csv(Path("data/processed") / f"{table}.csv")
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"{table}: {len(df)} records loaded")

print("Database loading completed!")
