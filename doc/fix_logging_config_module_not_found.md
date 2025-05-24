# Hướng Dẫn Khắc Phục Lỗi `No module named 'config'` Khi Dùng Logging Config Tùy Chỉnh Trong Apache Airflow

## 📌 Mục tiêu

Fix lỗi:

```
ModuleNotFoundError: No module named 'config'
```

khi khai báo `LOGGING_CONFIG` bên ngoài `airflow_local_settings.py`.

---

## 🧠 Nguyên Nhân

Python KHÔNG coi thư mục `/opt/airflow/config` là package `config` nếu bạn chỉ mount vào và set `PYTHONPATH`.

---

## ✅ Điều kiện cần

1. Trong thư mục `config/` bắt buộc phải có `__init__.py`
2. Thư mục `config` phải nằm TRÊN PYTHONPATH — không phải chính `config/`

> Nếu `PYTHONPATH=/opt/airflow/config` thì **không thể** import `airflow_local_settings` vì `config` KHÔNG phải là module cha.

---

## ✅ Cách Fix Đúng

### 🛠️ Bước 1: Chuyển PYTHONPATH lên cấp cha

Trong `docker-compose.yaml`:

```yaml
environment:
  PYTHONPATH: /opt/airflow:$PYTHONPATH
```

Thay vì:

```yaml
PYTHONPATH: /opt/airflow/config
```

---

### 🛠️ Bước 2: Đảm bảo cấu trúc thư mục

Trong project:

```
.
├── dags/
├── config/
│   ├── __init__.py
│   └── airflow_local_settings.py
└── docker-compose.yaml
```

Mount trong Docker Compose:

```yaml
volumes:
  - ./config:/opt/airflow/config
```

---

### 🛠️ Bước 3: Kiểm tra lại bên trong container

```bash
docker run --rm -it \
  -v "$(pwd)/config:/opt/airflow/config" \
  -e PYTHONPATH="/opt/airflow" \
  python:3.12 bash
```

Test:

```bash
python -c "from airflow_local_settings import LOGGING_CONFIG; print(LOGGING_CONFIG['version'])"
```

✅ Nếu in ra `1` là OK.

---

## 🔁 Gợi ý thêm

Nếu bạn cần chuyển thành module riêng, bạn cũng có thể:

```bash
mv config airflow_config_module
touch airflow_config_module/__init__.py
```

Và dùng:

```env
AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS=airflow_config_module.airflow_local_settings.LOGGING_CONFIG
PYTHONPATH=/opt/airflow:$PYTHONPATH
```

---

## 🏁 Ghi chú

- File `__init__.py` bắt buộc cho tất cả thư mục chứa `.py` cần được import.
- Đảm bảo bạn không thêm trực tiếp thư mục chứa module (`config`) vào `PYTHONPATH` nếu bạn muốn import dưới dạng `config.xyz`.

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25
