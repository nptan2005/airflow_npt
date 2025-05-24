from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id="atom_read_dw",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 4, 16),
    catchup=False,
) as dag:
    test_connection = PostgresOperator(
        task_id="test_connection",
        postgres_conn_id="external_postgres",  # Conn ID đã tạo trong Airflow
        sql="SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    )
