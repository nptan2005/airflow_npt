from airflow import DAG
from pd_to_excel_plugin.excel_export_operator import ExcelExportOperator
from datetime import datetime
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),
}

dag = DAG(
    dag_id='test_export_plugin_task',
    default_args=default_args,
    schedule_interval=None,  # Chạy thủ công hoặc theo lịch
)

# Tạo DataFrame mẫu để xuất
sample_dataframe = pd.DataFrame({
    'Column A': [1, 2, 3],
    'Column B': ['A', 'B', 'C']
})

# Sử dụng operator tùy chỉnh trong DAG
export_task = ExcelExportOperator(
    task_id='test_export_plugin_task',
    dataframe=sample_dataframe,
    output_path="/opt/airflow/out_data",
    file_name_prefix="sample_export",
    dag=dag,
)
