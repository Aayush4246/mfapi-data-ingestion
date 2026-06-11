"""
ETL Pipeline Script — Bluestock MF Capstone
Author: Ayush Kumar Singh
Date: 12 June 2026
Description:
Extracts raw mutual fund data, transforms it (cleaning, validation),
and loads processed outputs for downstream analytics.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# 1️⃣ Define folder paths
# -----------------------------
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 2️⃣ Extract — Load all CSVs
# -----------------------------
def load_raw_data():
    datasets = {}
    for file in RAW_DIR.glob("*.csv"):
        df = pd.read_csv(file)
        print(f"Loaded {file.name} → shape={df.shape}")
        datasets[file.stem] = df
    return datasets

# -----------------------------
# 3️⃣ Transform — Clean datasets
# -----------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    # Handle missing values (forward + backward fill)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

# -----------------------------
# 4️⃣ Load — Save cleaned outputs
# -----------------------------
def save_processed(datasets: dict):
    for name, df in datasets.items():
        out_path = PROCESSED_DIR / f"{name}_clean.csv"
        df.to_csv(out_path, index=False)
        print(f"Saved cleaned file → {out_path}")

# -----------------------------
# 5️⃣ Data Quality Summary
# -----------------------------
def generate_quality_report(datasets: dict):
    report = []
    for name, df in datasets.items():
        summary = {
            "dataset": name,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum())
        }
        report.append(summary)
    report_df = pd.DataFrame(report)
    report_df.to_csv(REPORTS_DIR / "data_quality_report.csv", index=False)
    print("✅ Data quality report generated → reports/data_quality_report.csv")

# -----------------------------
# 6️⃣ Main ETL Execution
# -----------------------------
def main():
    print("🚀 Starting ETL pipeline...")
    raw_datasets = load_raw_data()
    cleaned_datasets = {name: clean_data(df) for name, df in raw_datasets.items()}
    save_processed(cleaned_datasets)
    generate_quality_report(cleaned_datasets)
    print("🎯 ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
