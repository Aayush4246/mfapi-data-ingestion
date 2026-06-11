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





---

## 📊 Bluestock Mutual Fund Capstone Extension

This project evolved into a full analytics suite integrating:
- Automated ETL pipeline (`src/etl_pipeline.py`)
- Exploratory and performance analysis (`notebooks/03_eda_analysis.ipynb`, `04_performance_analytics.ipynb`)
- Predictive modeling and SIP forecasting (`05_advanced_analytics.ipynb`)
- Interactive dashboard (`src/dashboard.py`)
- Final report generation (`06_final_report.ipynb`)

### Key Outputs
- `data/processed/` → Cleaned datasets  
- `reports/fund_scorecard.csv` → Fund performance metrics  
- `reports/final_summary.csv` → Project summary  
- Streamlit dashboard → Real‑time visualization at `localhost:8501`

### Run Instructions
```bash
pip install -r requirements.txt
streamlit run src/dashboard.py


