from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="sample_dag",
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"),
    catchup=False,
    schedule="0 0 * * *",
    tags=["sample"],
) as dag:
    start_task = EmptyOperator(task_id="start_task")

    bash_task = BashOperator(
        task_id="bash_example",
        bash_command="echo 'Hello from BashOperator!'",
    )

    end_task = EmptyOperator(task_id="end_task")

    start_task >> bash_task >> end_task