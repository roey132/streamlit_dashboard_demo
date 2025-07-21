import os
import time
from app.data_loader import run_or_reuse_athena_query
from app.dashboard import render_dashboard

import streamlit as st

# === Load SQL Query ===
QUERY_PATH = "app/athena_query.sql"

def load_sql_query(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()

# === Run Application ===
def main():
    st.set_page_config(page_title="Earthquake Dashboard", layout="wide")

    message = st.empty()
    message.info("⏳ Loading data from AWS Athena...")

    try:
        query = load_sql_query(QUERY_PATH)
        df = run_or_reuse_athena_query(query)
        message.success("✅ Data loaded successfully.")
        time.sleep(2)  # show success briefly
        message.empty()
        render_dashboard(df)
    except Exception as e:
        message.error("❌ Failed to load data.")
        st.exception(e)
if __name__ == "__main__":
    main()
