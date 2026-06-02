import pandas as pd

def validate_amfi(fund_master_path, nav_history_path):
    fm = pd.read_csv(fund_master_path)
    nh = pd.read_csv(nav_history_path)

    fm_codes = set(fm["amfi_code"].dropna())
    nh_codes = set(nh["amfi_code"].dropna())

    missing_in_nh = fm_codes - nh_codes
    missing_in_fm = nh_codes - fm_codes

    print("Codes in Fund Master but missing in NAV History:", missing_in_nh)
    print("Codes in NAV History but missing in Fund Master:", missing_in_fm)

if __name__ == "__main__":
    validate_amfi("data/raw/fund_master.csv", "data/raw/nav_history.csv")
