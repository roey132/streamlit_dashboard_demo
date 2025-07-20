import boto3
import pandas as pd
import time
import os

def run_athena_query(query: str, database: str, output_location: str, region: str = 'eu-central-1') -> pd.DataFrame:
    client = boto3.client('athena', region_name=region)

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': output_location}
    )

    execution_id = response['QueryExecutionId']

    # Wait for the query to complete
    while True:
        result = client.get_query_execution(QueryExecutionId=execution_id)
        status = result['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)

    if status != 'SUCCEEDED':
        raise Exception(f"Athena query failed: {status}")

    # Construct result file path
    result_file = f"{output_location}{execution_id}.csv"
    df = pd.read_csv(result_file)
    return df
