from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from pytz import timezone
import os 
import random

local_tz = timezone('Asia/Ho_Chi_Minh')

dag = DAG("my_dag", # Dag id
        start_date=datetime(2023, 1 ,1), # start date, the 1st of January 2021 
        schedule_interval='@daily',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
        description='A simple ML flow with DAG',
)

def _training_model():
    return random.randint(0, 10)

# Tasks are implemented under the dag object
training_model_A = PythonOperator(
    task_id="training_model_A",
    python_callable=_training_model,
    dag=dag
)
training_model_B = PythonOperator(
    task_id="training_model_B",
    python_callable=_training_model,
    dag=dag
)
training_model_C = PythonOperator(
    task_id="training_model_C",
    python_callable=_training_model,
    dag=dag
)

def _choosing_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    if max(accuracies) > 8:
        return 'accurate'
    return 'inaccurate'
    

choosing_best_model = BranchPythonOperator(
    task_id="choosing_best_model",
    python_callable=_choosing_best_model,
    dag=dag
)

accurate = BashOperator(
    task_id="accurate",
    bash_command="echo 'Prediction'"
)
inaccurate = BashOperator(
    task_id="inaccurate",
    bash_command=" echo 'Retraining'"
)
training_model_tasks = [
    PythonOperator(
        task_id=f"training_model_{model_id}",
        python_callable=_training_model,
        op_kwargs={
            "model": model_id
        }
    ) for model_id in ['A', 'B', 'C']
]
choosing_best_model = BranchPythonOperator(
    task_id="choosing_best_model",
    python_callable=_choosing_best_model
)

training_model_tasks >> choosing_best_model >> [accurate, inaccurate]


