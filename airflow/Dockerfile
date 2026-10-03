FROM apache/airflow:3.1.0-python3.12

# dbt and the ingest dependencies live in their own virtualenv,
# so they cannot conflict with Airflow's own packages
RUN python -m venv /opt/airflow/pipeline-venv \
 && /opt/airflow/pipeline-venv/bin/pip install --no-cache-dir \
      dbt-postgres "psycopg[binary]" python-dotenv
