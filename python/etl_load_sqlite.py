import argparse
import os
import sqlite3
import pandas as pd

CSV_FILES = [
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
]

TABLE_MAP = {
    "olist_customers_dataset.csv": "customers",
    "olist_sellers_dataset.csv": "sellers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation",
}

def read_csv_safely(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

def main():
    p = argparse.ArgumentParser(description="Load Olist CSVs into SQLite.")
    p.add_argument("--data-dir", required=True)
    p.add_argument("--db", required=True)
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.db), exist_ok=True)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), "..", "sql", "00_schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())
    conn.commit()

    for csv_name in CSV_FILES:
        csv_path = os.path.join(args.data_dir, csv_name)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Missing file: {csv_path}")

        df = read_csv_safely(csv_path)
        table = TABLE_MAP[csv_name]
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"Loaded {csv_name} -> {table} ({len(df):,} rows)")

    conn.close()
    print(f"Done. DB created at: {args.db}")

if __name__ == "__main__":
    main()
