# [Lệnh quản lý Airflow (CLI)](Airflow_cli_cmd.md)

Cơ bản:
```bash
airflow db init               # Khởi tạo database lần đầu
airflow db upgrade            # Cập nhật schema database
airflow users create          # Tạo user đăng nhập
airflow webserver             # Chạy web UI
airflow scheduler             # Chạy scheduler
```

DAG management:
```bash
airflow dags list                     # Liệt kê các DAG
airflow dags trigger <dag_id>         # Kích hoạt DAG thủ công
airflow dags pause <dag_id>           # Dừng chạy DAG theo schedule
airflow dags unpause <dag_id>         # Cho phép DAG chạy theo schedule
```

Task management:
```bash
airflow tasks list <dag_id>                           # Liệt kê task trong DAG
airflow tasks test <dag_id> <task_id> <exec_date>     # Test task cục bộ
```

Monitoring & Debug:
```bash
airflow info                  # Xem thông tin cấu hình
airflow config get-value core dags_folder
airflow plugins list          # Liệt kê plugin đã được load
```
