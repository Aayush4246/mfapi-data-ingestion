import pandas as pd
import os

RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"

def load_csvs():
    files = [f for f in os.listdir(RAW_PATH) if f.endswith(".csv")]
    datasets = {}
    for f in files:
        df = pd.read_csv(os.path.join(RAW_PATH, f))
        print(f"{f}: shape={df.shape}, columns={df.columns.tolist()}")
        datasets[f] = df
    return datasets

if __name__ == "__main__":
    data = load_csvs()
    # Save processed versions
    for name, df in data.items():
        df.to_csv(os.path.join(PROCESSED_PATH, f"cleaned_{name}"), index=False)
