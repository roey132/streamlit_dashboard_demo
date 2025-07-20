import os
from app.data_loader import run_athena_query
from app.dashboard import render_dashboard

import streamlit as st

# === Configuration ===
DATABASE = "batch_data_demo"  # <-- replace with your Athena database name
OUTPUT_S3 = "s3://batch-data-demo-euc1/athena-queries/"  # <-- must exist and be writable
REGION = "eu-central-1"

# === Load SQL Query ===
QUERY_PATH = "app/athena_query.sql"

def load_sql_query(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()

# === Run Application ===
def main():
    st.set_page_config(page_title="Earthquake Dashboard", layout="wide")
    st.info("⏳ Loading data from AWS Athena...")

    try:
        query = load_sql_query(QUERY_PATH)
        df = run_athena_query(query, DATABASE, OUTPUT_S3, REGION)
        st.success("✅ Data loaded successfully.")
        render_dashboard(df)
    except Exception as e:
        st.error("❌ Failed to load data.")
        st.exception(e)

if __name__ == "__main__":
    main()
