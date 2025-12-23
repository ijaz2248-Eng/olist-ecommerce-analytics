import argparse
import os
import sqlite3

def main():
    p = argparse.ArgumentParser(description="Create reporting views in SQLite.")
    p.add_argument("--db", required=True)
    args = p.parse_args()

    if not os.path.exists(args.db):
        raise FileNotFoundError(f"DB not found: {args.db}")

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    views_path = os.path.join(os.path.dirname(__file__), "..", "sql", "02_clean_views.sql")
    with open(views_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()
    print("Reporting views created.")

if __name__ == "__main__":
    main()
