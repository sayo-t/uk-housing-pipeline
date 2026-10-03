from datetime import datetime, timedelta, timezone

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PY = "/opt/airflow/pipeline-venv/bin/python"
DBT = "/opt/airflow/pipeline-venv/bin/dbt"

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="uk_housing_pipeline",
    description="Ingest HM Land Registry Price Paid data, transform with dbt, test.",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    schedule="@monthly",
    catchup=False,
    default_args=default_args,
    params={"year": "2025"},
    tags=["housing", "dbt"],
) as dag:

    ingest = BashOperator(
        task_id="ingest_price_paid",
        bash_command=(
            "cd /opt/airflow/project && "
            f"{PY} ingest/load_price_paid.py {{{{ params.year }}}}"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd /opt/airflow/project/dbt && {DBT} run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd /opt/airflow/project/dbt && {DBT} test --profiles-dir .",
    )

    ingest >> dbt_run >> dbt_test
