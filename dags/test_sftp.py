from airflow.providers.sftp.operators.sftp import SFTPOperator

with DAG("sftp_dag", start_date=datetime(2025, 4, 16)) as dag:
    sftp_task = SFTPOperator(
        task_id="upload_file_sftp",
        sftp_conn_id="sftp_default",
        local_filepath="/path/to/local/file",
        remote_filepath="/path/to/remote/file",
        operation="put"
    )
