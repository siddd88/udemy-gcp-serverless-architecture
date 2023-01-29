import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator, DataprocDeleteBatchOperator, DataprocGetBatchOperator
)
from airflow.utils.dates import days_ago

PROJECT_ID = "{your-project-id}"
REGION = "us-central1"
PHS_CLUSTER = "pyspark-phs"

PYTHON_FILE_LOCATION = "gs://{bucket-name}/top_stackoverflow_tags.py"

PHS_CLUSTER_PATH = "projects/{your-project-id}/regions/us-central1/clusters/pyspark-phs"

SPARK_BIGQUERY_JAR_FILE = "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar"

default_args = {
    "start_date": days_ago(1),
    "project_id": PROJECT_ID,
    "region": REGION,
}

with models.DAG(
    "dataproc_serverless_pyspark",  
    default_args=default_args,  
    schedule_interval=datetime.timedelta(days=1), 
) as dag:

    create_batch = DataprocCreateBatchOperator(
        task_id="create_batch",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": PYTHON_FILE_LOCATION,
                "jar_file_uris": [SPARK_BIGQUERY_JAR_FILE],
            },
            "environment_config": {
                "peripherals_config": {
                    "spark_history_server_config": {
                        "dataproc_cluster": PHS_CLUSTER_PATH,
                    },
                },
            },
        },
        batch_id="batch-create-phs",
    )
    get_batch = DataprocGetBatchOperator(
        task_id="get_batches",
        batch_id="batch-create-phs",
    )
    delete_batch = DataprocDeleteBatchOperator(
        task_id="delete_created_batch",
        batch_id="batch-create-phs",
    )
    create_batch >> get_batch >> delete_batch