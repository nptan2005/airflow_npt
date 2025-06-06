from airflow import DAG
from pd_to_excel_plugin.export_operator import ExportOperator
from datetime import datetime
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),
}

dag = DAG(
    dag_id='test_export_plugin_task',
    default_args=default_args,
    schedule=None,  # Chạy thủ công hoặc theo lịch
)

# Tạo DataFrame mẫu để xuất
sample_dataframe = [pd.DataFrame({
    'Column A': [1, 2, 3],
    'Column B': ['A', 'B', 'C']
}),
pd.DataFrame({
    'Column A': [1, 2, 3],
    'Column B': ['A', 'B', 'C']
})
]


# Sử dụng operator tùy chỉnh trong DAG
export_task = ExportOperator(
    task_id='test_export_plugin_task',
    dataframe_array=sample_dataframe,
    name_arr=['DATA','TEST'],
    output_path="/opt/airflow/data",
    file_name_prefix="sample_export",
    file_extension = 'xlsx',
    template = None,
    dag=dag,
)
