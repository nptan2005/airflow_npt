from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import logging

# Thiết lập logging
def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def etl_postgres_to_oracle(**kwargs):
    setup_logging()
    logging.info("Bắt đầu ETL...")

    try:
        # Lấy giá trị từ Airflow Variables
        postgres_conn_id = Variable.get("pg_mms_slave_conn_id", default_var="mms_slave_db_conn")
        oracle_conn_id = Variable.get("orl_dw_conn_id", default_var="oracle_dw_conn")
        source_table = Variable.get("pg_mms_txn_tbl", default_var="transaction_model")
        target_table = Variable.get("orl_des_txn_tbl", default_var="transaction_model")
        chunk_size = int(Variable.get("chunk_size", default_var="1000"))
        pg_schema = Variable.get("pg_mms_schema", default_var="public")
        oracle_schema = Variable.get("orl_dw_schema", default_var="dw")

        # Kết nối PostgreSQL
        logging.info(f"Kết nối PostgreSQL với conn_id: {postgres_conn_id}")
        postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
        conn_postgres = postgres_hook.get_conn()
        cursor_postgres = conn_postgres.cursor()
        query = f'SELECT * FROM "{pg_schema}"."{source_table}"'

        # Kết nối Oracle
        logging.info(f"Kết nối Oracle với conn_id: {oracle_conn_id}")
        oracle_hook = OracleHook(oracle_conn_id=oracle_conn_id)
        conn_oracle = oracle_hook.get_conn()
        cursor_oracle = conn_oracle.cursor()

        # Xoá dữ liệu bảng đích trên Oracle
        delete_sql = f'DELETE FROM {oracle_schema}.{target_table}'
        logging.info(f"Xoá dữ liệu trong bảng {target_table} trên Oracle.")
        cursor_oracle.execute(delete_sql)
        conn_oracle.commit()

        # Lấy dữ liệu từ PostgreSQL
        logging.info(f"Truy vấn dữ liệu từ bảng {source_table} trên PostgreSQL.")
        result_proxy = conn_postgres.execution_options(stream_results=True).execute(query)
        columns = result_proxy.keys()

        # Chuẩn bị câu lệnh INSERT cho Oracle
        insert_sql = f'''
            INSERT INTO {oracle_schema}.{target_table} ({', '.join(columns)})
            VALUES ({', '.join([':' + str(i + 1) for i in range(len(columns))])})
        '''
        logging.info(f"Câu lệnh INSERT động: {insert_sql}")

        # Đọc và chèn dữ liệu từng chunk
        rows = []
        total_inserted = 0
        for row in result_proxy:
            rows.append(row)
            if len(rows) >= chunk_size:
                cursor_oracle.executemany(insert_sql, rows)
                conn_oracle.commit()
                total_inserted += len(rows)
                logging.info(f"Đã chèn {total_inserted} dòng...")
                rows = []

        # Chèn các dòng còn lại
        if rows:
            cursor_oracle.executemany(insert_sql, rows)
            conn_oracle.commit()
            total_inserted += len(rows)

        logging.info(f"✅ Hoàn tất ETL. Tổng cộng đã chèn {total_inserted} dòng vào {target_table}.")
    except Exception as e:
        logging.error(f"Lỗi xảy ra trong ETL: {e}")
        raise
    finally:
        # Đóng kết nối
        cursor_postgres.close()
        cursor_oracle.close()

# Cấu hình DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),
}

with DAG(
    dag_id='etl_postgres_to_oracle_with_variables',
    default_args=default_args,
    schedule_interval=None,  # Chỉ chạy thủ công
) as dag:
    etl_task = PythonOperator(
        task_id='etl_task',
        python_callable=etl_postgres_to_oracle,
        provide_context=True
    )
