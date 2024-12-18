from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago

# Function to check XCom value from job1 and decide the next step
def check_xcom_value(ti):
    # Pull the value pushed by the Spark job (job1)
    value = ti.xcom_pull(task_ids='job1')  # Pull XCom value from job1
    if value is None:
        print("No value found in XCom.")
        return 'skip_job2'  # If no value is found, skip job2
    
    filename = value.get('filename', '')  # Retrieve 'filename' key from XCom value
    cur_date = '2024-12-18'  # You can dynamically get the current date if needed
    
    print(f"The value from XCom is: {filename}")
    
    # Check if the value is a non-empty string and contains cur_date
    if filename and cur_date in filename:
        return 'job2'  # If condition is met, run job2
    else:
        return 'skip_job2'  # Skip job2 if condition is not met

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'spark_jobs_with_xcom_check',
    default_args=default_args,
    description='Run Spark jobs with XCom check',
    schedule_interval=None,  # Trigger manually or based on your needs
)

# Task 1: Job 1 (Spark Job 1)
job1_task = PythonOperator(
    task_id='job1',
    python_callable=lambda: print("Running job1..."),  # Simulate the job1 logic
    dag=dag,
)

# Task 2: Job 2 (Spark Job 2) - This will only run if the condition is met in the check_xcom_value task
job2_task = PythonOperator(
    task_id='job2',
    python_callable=lambda: print("Running job2..."),  # Simulate the job2 logic
    dag=dag,
)

# Task 3: Task to skip job2 if condition is not met
skip_job2_task = PythonOperator(
    task_id='skip_job2',
    python_callable=lambda: print("Skipping job2 task because condition was not met."),
    dag=dag,
)

# Task to check the XCom value and decide the next step (branching logic)
check_xcom_task = BranchPythonOperator(
    task_id='check_xcom_value',
    python_callable=check_xcom_value,
    provide_context=True,
    dag=dag
)

# Set the task dependencies
job1_task >> check_xcom_task  # Run check_xcom_task after job1
check_xcom_task >> [job2_task, skip_job2_task]  # If condition is met, run job2, else skip job2
