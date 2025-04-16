from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def export_to_excel():
    try:
        # Kết nối tới PostgreSQL bằng PostgresHook
        hook = PostgresHook(postgres_conn_id='atom_read_dw')
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Query dữ liệu từ PostgreSQL
        query = """
                SELECT a.id, a.txn_id
                    , TO_CHAR(TO_TIMESTAMP(a.created_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS created_time
                    , TO_CHAR(TO_TIMESTAMP(a.updated_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS updated_time
                    , a.mid, a.tid, a.serial_no, a.card_no
                    , a.batch_no, a.invoice_no, a.card_origin, a.bank_code, a.card_type, a.is_credit
                    , a.mcc_international
                    , a.pos_entry_mode, a.routing_bank_code
                    , a.transaction_type, a.request_amount, a.tip
                    , a.response_code, a.is_settle, a.is_void, a.is_refund, a.is_clear_batch

                    , a.system_trace_no
                    , a.retrieval_ref_no, a.auth_id_response

                    , a.msp_code, a.msp_price, a.fee_percentage, a.longitude, a.latitude
                    , a.primary_account, a.primary_account_name
                    --, a.*
                    , TO_TIMESTAMP(CAST(a.original_transaction_date AS INT))::DATE AS orig_txn_date
                    , TO_CHAR(TO_TIMESTAMP(a.settle_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS settle_time
                    , TO_CHAR(TO_TIMESTAMP(a.void_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS void_time
                    , TO_CHAR(TO_TIMESTAMP(a.reversal_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS reversal_time
                    FROM public.transaction_model a;
    """  
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Chuyển dữ liệu thành DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Xuất ra file Excel
        output_path = "/opt/airflow/out_data/exported_data.xlsx"  # Thay đường dẫn file phù hợp
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"File Excel đã được xuất ra tại: {output_path}")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),  # Ngày bắt đầu DAG
}

# Định nghĩa DAG
dag = DAG(
    dag_id='export_postgres_to_excel',
    default_args=default_args,
    schedule_interval=None,  # Chạy DAG theo yêu cầu
)

# Task PythonOperator
export_task = PythonOperator(
    task_id='export_to_excel_task',
    python_callable=export_to_excel,
    dag=dag,
)
