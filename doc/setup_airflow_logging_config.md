
# Hướng dẫn cấu hình Logging Custom trong Apache Airflow

## ✅ Mục tiêu
Cho phép Airflow sử dụng file `airflow_local_settings.py` tùy chỉnh logging cấu hình thay vì mặc định.

---

## 🗂️ Cấu trúc thư mục

Đảm bảo file của bạn nằm trong đúng thư mục và được ánh xạ qua volume:

```
project_root/
├── config/
│   ├── airflow_local_settings.py
│   └── __init__.py
```

---

## 🔧 Nội dung `airflow_local_settings.py`

```python
import os

BASE_LOG_FOLDER = os.environ.get("LOG_PATH", "/opt/airflow/logs")
PROCESSOR_LOG_FOLDER = os.path.join(BASE_LOG_FOLDER, "scheduler")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'airflow': {
            'format': '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
        },
        'task': {
            'format': '[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow',
            'stream': 'ext://sys.stdout',
        },
        'task_file_handler': {
            'class': 'airflow.utils.log.file_task_handler.FileTaskHandler',
            'formatter': 'task',
            'base_log_folder': BASE_LOG_FOLDER,
            'filename_template': '{{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log',
        },
        'processor': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'airflow',
            'filename': os.path.join(PROCESSOR_LOG_FOLDER, 'dag_processor.log'),
            'when': 'midnight',
            'backupCount': 30,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'airflow': {
            'handlers': ['console', 'processor'],
            'level': os.environ.get("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
        'airflow.task': {
            'handlers': ['console', 'task_file_handler'],
            'level': os.environ.get("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
        'airflow.processor': {
            'handlers': ['processor'],
            'level': os.environ.get("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
    }
}
```

---

## 🔄 Cấu hình `docker-compose.yaml`

Trong phần `environment` của các service:

```yaml
environment:
  ...
  AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS: "airflow_local_settings.LOGGING_CONFIG"
  PYTHONPATH: /opt/airflow/config
```

---

## 🔁 Câu lệnh khởi động lại Airflow

```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

---

## ✅ Kiểm tra thành công

```bash
docker logs airflow_npt-airflow-init-1
```

Không còn lỗi `ImportError: No module named 'config'` hoặc `airflow_local_settings`.

---

## 📌 Ghi chú

- Đảm bảo `__init__.py` tồn tại trong thư mục chứa `airflow_local_settings.py`.
- Biến `PYTHONPATH` cần bao gồm thư mục đó (`/opt/airflow/config`).

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25
