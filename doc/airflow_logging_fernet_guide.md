# Hướng Dẫn Xử Lý Lỗi Airflow Init, Logging và FERNET_KEY

## 📌 Mục lục
- [1. Xử lý lỗi `airflow-init`](#1-xử-lý-lỗi-airflow-init)
- [2. Cấu hình `FERNET_KEY`](#2-cấu-hình-fernet_key)
- [3. Tạm thời bỏ logging tuỳ chỉnh](#3-tạm-thời-bỏ-logging-tuỳ-chỉnh)
- [4. Setup logging tuỳ chỉnh đúng cách](#4-setup-logging-tuỳ-chỉnh-đúng-cách)
- [5. Script test logging trong container](#5-script-test-logging-trong-container)

---

## 1. Xử lý lỗi `airflow-init`

Nếu gặp lỗi:
```
service "airflow-init" didn't complete successfully: exit 1
```
Thực hiện:
```bash
docker compose down -v
docker volume rm airflow_npt_postgres-db-volume
docker rmi airflow-nptan:1.0.0
docker compose build --no-cache
docker compose up -d
```

---

## 2. Cấu hình `FERNET_KEY`

Tạo FERNET_KEY mới:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Cập nhật `.env`:
```env
FERNET_KEY=your_generated_key_here
```

---

## 3. Tạm thời bỏ logging tuỳ chỉnh

Trong `.env` hoặc `docker-compose.yaml`, comment dòng sau:
```yaml
# AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS: config.airflow_local_settings.LOGGING_CONFIG
```

Sau đó restart:
```bash
docker compose down
docker compose up -d
```

---

## 4. Setup logging tuỳ chỉnh đúng cách

### Bước 1: Tạo file `config/airflow_local_settings.py`

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
        'stderr': {
            'class': 'airflow.utils.log.logging_mixin.RedirectStdHandler',
            'formatter': 'airflow',
            'stream': 'sys.stderr',
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
        'airflow.task_runner': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
    }
}
```

### Bước 2: Đảm bảo `PYTHONPATH` chứa `/opt/airflow`
```yaml
    PYTHONPATH: /opt/airflow:/opt/airflow/config:...
```

### Bước 3: Gán cấu hình vào Airflow
```yaml
AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS: config.airflow_local_settings.LOGGING_CONFIG
```

---

## 5. Script test logging trong container

```bash
docker run --rm -it   -v "$(pwd)/config:/opt/airflow/config"   -e PYTHONPATH="/opt/airflow:/opt/airflow/config"   python:3.12 bash

# Trong container:
python -c "from config.airflow_local_settings import LOGGING_CONFIG; print(LOGGING_CONFIG['version'])"
```

Nếu không lỗi: setup thành công.