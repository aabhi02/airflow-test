from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'abhishek',
    'retries': 5,
    'retry_deply': timedelta(minutes=2)
}


def testing():
    print("nkn banthu!!")


with DAG(
    dag_id="test1",
    description="tseing dag",
    schedule_interval='@daily',
    start_date=datetime(2024,12,21,1)
) as dag:
    task1 = PythonOperator(
        task_id = "task1",
        python_callable=testing
    )


    task1
