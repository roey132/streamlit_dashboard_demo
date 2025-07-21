import os
import time
from datetime import datetime, timedelta, timezone
import boto3
import pandas as pd

# === Configuration ===
DATABASE = "batch_data_demo"
OUTPUT_S3 = "s3://batch-data-demo-euc1/athena-queries/"
REGION = "eu-central-1"
QUERY_PATH = "app/athena_query.sql"


def load_sql_query(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def get_recent_successful_query(execution_window_minutes=120):
    client = boto3.client('athena', region_name=REGION)
    recent_threshold = datetime.now(timezone.utc) - timedelta(minutes=execution_window_minutes)

    executions = client.list_query_executions(MaxResults=50)['QueryExecutionIds']
    for exec_id in executions:
        result = client.get_query_execution(QueryExecutionId=exec_id)['QueryExecution']
        status = result['Status']
        submission_time = status['SubmissionDateTime']

        if (
            status['State'] == 'SUCCEEDED' and
            submission_time >= recent_threshold and
            result['ResultConfiguration']['OutputLocation'].startswith(OUTPUT_S3)
        ):
            return exec_id
    return None


def run_or_reuse_athena_query(query: str) -> pd.DataFrame:
    client = boto3.client('athena', region_name=REGION)

    existing_id = get_recent_successful_query()
    if existing_id:
        csv_path = f"{OUTPUT_S3}{existing_id}.csv"
        print("Reusing existing query result:", existing_id)
        return pd.read_csv(csv_path)

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT_S3}
    )
    execution_id = response['QueryExecutionId']

    while True:
        result = client.get_query_execution(QueryExecutionId=execution_id)
        state = result['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)

    if state != 'SUCCEEDED':
        raise Exception(f"Athena query failed: {state}")

    csv_path = f"{OUTPUT_S3}{execution_id}.csv"
    print("Query completed successfully:", execution_id)
    return pd.read_csv(csv_path)
