"""
Load Cleaned Data into SQLite — Bluestock MF Capstone
Author: Ayush Kumar Singh
Date: 12 June 2026
Description:
Takes cleaned CSVs from data/processed/, creates a star schema in SQLite,
and loads the data for downstream SQL analytics.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# -----------------------------
# 1️⃣ Define paths
# -----------------------------
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/db")
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "bluestock_mf.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

# -----------------------------
# 2️⃣ Define schema
# -----------------------------
schema_sql = """
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code TEXT,
    date TEXT,
    nav REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    date TEXT,
    transaction_type TEXT,
    amount REAL,
    state TEXT,
    age_group TEXT,
    gender TEXT,
    FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code TEXT,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    expense_ratio REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    amfi_code TEXT,
    year INTEGER,
    aum REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);
"""

# -----------------------------
# 3️⃣ Load schema safely
# -----------------------------
def create_schema():
    with engine.connect() as conn:
        for statement in schema_sql.strip().split(";"):
            if statement.strip():
                conn.execute(text(statement))
    print("✅ SQLite schema created successfully.")

# -----------------------------
# 4️⃣ Load cleaned CSVs
# -----------------------------
def load_csvs():
    for file in PROCESSED_DIR.glob("*.csv"):
        df = pd.read_csv(file)
        table_name = file.stem.replace("_clean", "")
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"📦 Loaded {file.name} → table={table_name}")

# -----------------------------
# 5️⃣ Example analytical queries
# -----------------------------
def run_queries():
    queries = {
        "Top 5 funds by AUM": """
            SELECT amfi_code, MAX(aum) AS max_aum
            FROM fact_aum
            GROUP BY amfi_code
            ORDER BY max_aum DESC
            LIMIT 5;
        """,
        "Average NAV per month": """
            SELECT amfi_code, AVG(nav) AS avg_nav, SUBSTR(date,1,7) AS month
            FROM fact_nav
            GROUP BY amfi_code, month;
        """,
        "SIP YoY growth": """
            SELECT SUBSTR(date,1,4) AS year, SUM(amount) AS total_sip
            FROM fact_transactions
            WHERE transaction_type='SIP'
            GROUP BY year;
        """
    }

    with engine.connect() as conn:
        for name, q in queries.items():
            result = conn.execute(text(q)).fetchall()
            print(f"\n🔍 {name}:\n{result}")

# -----------------------------
# 6️⃣ Main execution
# -----------------------------
def main():
    print("🚀 Starting Day 2 pipeline...")
    create_schema()
    load_csvs()
    run_queries()
    print("🎯 Day 2 pipeline completed successfully.")

if __name__ == "__main__":
    main()
