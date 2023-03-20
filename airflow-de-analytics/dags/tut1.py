from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "ryano",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="demo1",
    default_args=default_args,
    start_date=datetime(2023, 2, 28),
    schedule='@daily'
) as dag:

    # Tasks are represented as operators
    hello = BashOperator(
        task_id="hello",
        bash_command="echo hello"
    )

    @task
    def airflow():
        print("airflow")

    # # Set dependencies between tasks
    hello >> airflow()
