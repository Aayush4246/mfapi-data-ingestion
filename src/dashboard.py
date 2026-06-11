"""
Bluestock MF Capstone — Day 5: Dashboard
Author: Ayush Kumar Singh
Date: 12 June 2026
"""

import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

# -----------------------------
# 1️⃣ Load data safely
# -----------------------------
DATA_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")

# Load mandatory files
nav_history = pd.read_csv(DATA_DIR / "nav_history_clean.csv")
fund_master = pd.read_csv(DATA_DIR / "fund_master_clean.csv")
scorecard = pd.read_csv(REPORTS_DIR / "fund_scorecard.csv")

# Auto‑detect transactions file
possible_files = [
    "investor_transactions_clean.csv",
    "transactions_clean.csv",
    "cleaned_nav_history.csv"
]
transactions = None
for f in possible_files:
    path = DATA_DIR / f
    if path.exists():
        transactions = pd.read_csv(path)
        st.sidebar.success(f"Loaded transactions file: {f}")
        break

if transactions is None:
    st.warning("⚠️ No transactions file found in data/processed/. Dashboard will skip SIP and demographics sections.")

# -----------------------------
# 2️⃣ Dashboard Layout
# -----------------------------
st.set_page_config(page_title="Bluestock MF Dashboard", layout="wide")

st.title("📊 Bluestock Mutual Fund Dashboard")
st.sidebar.header("Filters")

funds = nav_history["amfi_code"].unique()
selected_fund = st.sidebar.selectbox("Select Fund", funds)

# -----------------------------
# 3️⃣ NAV Trend
# -----------------------------
st.subheader("NAV Trend")
fund_data = nav_history[nav_history["amfi_code"] == selected_fund]
fig = px.line(fund_data, x="nav_date", y="nav_value", title=f"NAV Trend — {selected_fund}")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 4️⃣ SIP Inflows
# -----------------------------
if transactions is not None and "transaction_type" in transactions.columns:
    st.subheader("SIP Inflows")
    sip_txn = transactions[transactions["transaction_type"].str.lower() == "sip"]
    sip_txn["date"] = pd.to_datetime(sip_txn["date"], errors="coerce")
    sip_monthly = sip_txn.groupby(sip_txn["date"].dt.to_period("M"))["amount"].sum()
    st.line_chart(sip_monthly)

# -----------------------------
# 5️⃣ Fund Scorecard
# -----------------------------
st.subheader("Fund Scorecard")
st.dataframe(scorecard)

# -----------------------------
# 6️⃣ Investor Demographics
# -----------------------------
if transactions is not None and "age_group" in transactions.columns:
    st.subheader("Investor Demographics")
    col1, col2 = st.columns(2)

    with col1:
        sns.countplot(data=transactions, x="age_group")
        plt.title("Investor Age Group Distribution")
        st.pyplot(plt.gcf())
        plt.clf()

    with col2:
        sns.boxplot(data=transactions, x="age_group", y="amount")
        plt.title("SIP Amount by Age Group")
        st.pyplot(plt.gcf())
        plt.clf()

st.success("🎯 Dashboard ready — explore filters and charts interactively!")
