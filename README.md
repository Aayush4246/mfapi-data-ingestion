# Mutual Fund NAV Project

## Structure
- `data/raw/` → raw CSVs and API responses
- `data/processed/` → cleaned datasets
- `src/` → ingestion, API fetch, validation scripts
- `notebooks/` → exploratory analysis
- `reports/sql/` → SQL checks
- `dashboard/` → visualizations

## Workflow
1. Run `src/live_nav_fetch.py` to fetch NAV data.
2. Run `src/data_ingestion.py` to ingest and clean CSVs.
3. Explore datasets in `notebooks/exploration.ipynb`.
4. Validate AMFI codes with `src/validate_amfi.py`.
5. Commit and push to GitHub.

