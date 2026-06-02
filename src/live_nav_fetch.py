import requests
import pandas as pd
import os

RAW_PATH = "data/raw/"

def fetch_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["data"])
        df.to_csv(os.path.join(RAW_PATH, f"{scheme_code}_nav.csv"), index=False)
        print(f"Saved NAV for {scheme_code}")
    else:
        print(f"Failed to fetch NAV for {scheme_code}")

if __name__ == "__main__":
    # Example scheme codes
    scheme_codes = ["118834", "100027"]
    for code in scheme_codes:
        fetch_nav(code)
