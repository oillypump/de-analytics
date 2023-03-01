from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "ryano",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id='our_first_dag1',
    default_args=default_args,
    description='this is our first dag',
    start_date=datetime(2023, 2, 23, 2),
    schedule_interval='@daily'

) as dag:
    task1 = BashOperator(
        task_id="first_task1",
        bash_command="echo hello world"
    )

    task1
