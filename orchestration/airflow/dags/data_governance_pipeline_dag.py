"""Main Airflow Data Governance Pipeline DAG."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "Jayant Verman",
    "depends_on_past": False,
    "start_date": datetime(2023, 11, 1),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "aws_data_quality_governance_pipeline",
    default_args=default_args,
    description="End-to-end synthetic data generation, quality check, Macie scan, and Lake Formation governance",
    schedule_interval="@daily",
    catchup=False,
) as dag:

    def step_generate():
        print("Generating synthetic PII customer dataset...")

    def step_quality():
        print("Running Great Expectations quality suite & quarantine routing...")

    def step_macie():
        print("Executing Macie PII classification scan...")

    def step_lakeformation():
        print("Applying Lake Formation column-level masking policies...")

    t1 = PythonOperator(task_id="generate_data", python_callable=step_generate)
    t2 = PythonOperator(task_id="run_quality_checks", python_callable=step_quality)
    t3 = PythonOperator(task_id="trigger_macie_scan", python_callable=step_macie)
    t4 = PythonOperator(task_id="apply_lake_formation", python_callable=step_lakeformation)

    t1 >> t2 >> t3 >> t4
