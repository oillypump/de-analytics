from datetime import timedelta, datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "ryano",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id='scrap_1',
    default_args=default_args,
    description='this is our first dag',
    start_date=datetime(2023, 2, 28),
    schedule_interval='@daily'

) as dag:
    
    @task
    def request_url():
        pass