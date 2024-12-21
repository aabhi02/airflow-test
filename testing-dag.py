from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'abhishek',
    'retries': 5,
    'retry_deply': timedelta(minutes=2)
}

with DAG(
    dag_id="test1",
    description="tseing dag",
    schedule_interval='@daily',
    start_date=datetime(2024,12,22,1)
) as dag:
    task1 = BashOperator(
        task_id = "task1",
        bash_command = "echo nkn banthu!!"
    )


    task1
