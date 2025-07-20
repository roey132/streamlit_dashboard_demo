import os
from app.data_loader import run_athena_query

# === Configuration ===
QUERY_FILE = "app/athena_query.sql"
DATABASE = "batch_data_demo"  # Replace this
OUTPUT_S3 = "s3://batch-data-demo-euc1/athena-queries/"  # Must exist and end with /
REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-central-1")

# === Load SQL query ===
with open(QUERY_FILE, "r") as f:
    query = f.read()
print(query)
# === Run Query ===
print("Running Athena query...")
df = run_athena_query(query, DATABASE, OUTPUT_S3, REGION)
print(f"✅ Success! Loaded {len(df)} rows.")
print(df.head())  # Show preview

