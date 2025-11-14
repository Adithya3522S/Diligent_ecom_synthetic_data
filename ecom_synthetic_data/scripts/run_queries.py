import sqlite3
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "ecom.db")
SQL_DIR = os.path.join(BASE, "sql")

def run_query(file):
    with open(os.path.join(SQL_DIR, file), "r") as f:
        query = f.read()

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    print("Running customer_orders.sql")
    print(run_query("customer_orders.sql"))

    print("\nRunning order_details.sql")
    print(run_query("order_details.sql"))

    print("\nRunning top_customers.sql")
    print(run_query("top_customers.sql"))

if __name__ == "__main__":
    main()
