from airflow import DAG
from airflow.models import Variable
from airflow.providers.common.sql.hooks.sql import BaseHook
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


# Hàm xuất dữ liệu từ bất kỳ database nào ra Excel
def export_to_excel(**kwargs):
    setup_logging()
    logging.info("Bắt đầu xuất dữ liệu từ cơ sở dữ liệu sang Excel...")

    try:
        # Lấy cấu hình từ Airflow Variables
        db_type = Variable.get("export_excel_db_type", default_var="postgresql")  # Loại database
        db_conn_id = Variable.get("pg_mms_slave_conn_id", default_var="mms_slave_db_conn")  # Tên kết nối trong Airflow
        query = Variable.get("export_query", default_var="SELECT * FROM public.transaction_model LIMIT 1000;")
        output_path = Variable.get("export_output_path", default_var="/opt/airflow/out_data")
        file_name_prefix = Variable.get("export_prefix", default_var="exported_data")

        # Thêm subfix ngày giờ vào tên file
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name_prefix}_{current_time}.xlsx"
        full_file_path = f"{output_path}/{file_name}"

        logging.info(f"Đường dẫn file xuất: {full_file_path}")

        # Kết nối đến cơ sở dữ liệu
        logging.info(f"Kết nối cơ sở dữ liệu với conn_id: {db_conn_id} (loại {db_type})")
        db_hook = BaseHook.get_hook(db_conn_id)  # BaseHook hỗ trợ các loại DB khác nhau
        conn = db_hook.get_conn()
        cursor = conn.cursor()

        # Thực thi câu lệnh SQL
        logging.info("Thực thi query...")
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Chuyển dữ liệu thành DataFrame
        df = pd.DataFrame(rows, columns=column_names)
        logging.info(f"Đã đọc được {len(df)} dòng dữ liệu.")

        # Xuất dữ liệu ra file Excel
        df.to_excel(full_file_path, index=False, engine='openpyxl')
        logging.info(f"✅ File Excel đã được xuất ra tại: {full_file_path}")
    except Exception as e:
        logging.error(f"Lỗi xảy ra: {e}")
        raise


# Cấu hình DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),  # Ngày bắt đầu DAG
}

dag = DAG(
    dag_id='export_to_excel',
    default_args=default_args,
    schedule_interval=None,  # Chỉ chạy DAG theo yêu cầu
)

# Task PythonOperator
export_task = PythonOperator(
    task_id='export_to_excel_task',
    python_callable=export_to_excel,
    provide_context=True,
    dag=dag,
)
