from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def etl_postgres_to_oracle(**kwargs):
    # Lấy tham số từ dag_run.conf hoặc sử dụng giá trị mặc định
    config = kwargs['dag_run'].conf if 'dag_run' in kwargs else {}
    source_table = config.get('source_table', 'public.transaction_model')  # Giá trị mặc định
    target_table = config.get('target_table', 'oracle_target_table')       # Giá trị mặc định

    # Extract từ PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='mms_slave_db_conn')
    conn_postgres = postgres_hook.get_conn()
    cursor_postgres = conn_postgres.cursor()

    query = f"SELECT * FROM {source_table};"
    cursor_postgres.execute(query)
    rows = cursor_postgres.fetchall()
    column_names = [desc[0] for desc in cursor_postgres.description]
    df = pd.DataFrame(rows, columns=column_names)

    # Transform (tùy chọn)
    df['new_column'] = df['txn_id'].apply(lambda x: f"Transformed_{x}")

    # Load vào Oracle
    oracle_hook = OracleHook(oracle_conn_id='oracle_dw_conn')
    conn_oracle = oracle_hook.get_conn()
    cursor_oracle = conn_oracle.cursor()

    for _, row in df.iterrows():
        cursor_oracle.execute(
            f"INSERT INTO {target_table} (id, txn_id, new_column) VALUES (:1, :2, :3)",
            (row['id'], row['txn_id'], row['new_column'])
        )
    conn_oracle.commit()
    print(f"ETL hoàn tất từ {source_table} sang {target_table}!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),
}

with DAG(
    dag_id='etl_postgres_to_oracle',
    default_args=default_args,
    schedule_interval=None,  # Kích hoạt DAG thủ công
) as dag:
    etl_task = PythonOperator(
        task_id='etl_task',
        python_callable=etl_postgres_to_oracle,
        provide_context=True,  # Cho phép nhận context từ Airflow
    )
