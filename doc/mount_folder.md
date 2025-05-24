# [📁 scripts/, nginx.conf & .env Usage](scripts_folder.md)

## 1. scripts/

Chứa các shell/Python script hỗ trợ Airflow như:
- `init.sh`: Tạo user, migrate db, khởi tạo lần đầu
- `backup.sh`: Sao lưu dữ liệu PostgreSQL hoặc DAGs
- `restore.sh`: Khôi phục dữ liệu từ bản sao lưu
- `healthcheck.sh`: Kiểm tra tình trạng container
- `generateKey.py`: Sinh key mã hoá, dùng trong DAG

> 📌 Đảm bảo file `.sh` có quyền chạy:
```bash
chmod +x scripts/*.sh
```

---

## 2. nginx.conf

Cấu hình NGINX làm reverse proxy cho Airflow Webserver:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Mount file vào container:
```yaml
services:
  access-hot-proxy:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
```

---

## 3. File `.env`

Quản lý biến môi trường riêng biệt theo từng máy hoặc môi trường:

Ví dụ `.env.mac`:
```env
AIRFLOW_IMAGE_NAME=apache/airflow:2.10.5-python3.12
AIRFLOW_UID=501
AIRFLOW_GID=20
_AIRFLOW_WWW_USER_USERNAME=tanp
_AIRFLOW_WWW_USER_PASSWORD=Vccb1234
```

Sử dụng `.env` trong `docker-compose.yml`:
```yaml
env_file: .env
```

Copy file:
```bash
cp .env.mac .env  # macOS
# hoặc
Copy-Item .env.windows -Destination .env  # Windows PowerShell
```


# 📂 DAGs, Dockerfile, và CI/CD cho Airflow

## 1. DAGs – Tập tin điều khiển workflow

Thư mục `dags/` chứa các file `.py` định nghĩa workflow và các task của bạn.

Ví dụ DAG cơ bản:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("sample_dag", start_date=datetime(2023, 1, 1), schedule_interval="@daily") as dag:
    def task_fn():
        print("Hello from Airflow!")

    t1 = PythonOperator(
        task_id="say_hello",
        python_callable=task_fn
    )
```

---

## 2. Dockerfile – Định nghĩa image của bạn

Ví dụ Dockerfile chuẩn:
```Dockerfile
ARG AIRFLOW_IMAGE_NAME
FROM ${AIRFLOW_IMAGE_NAME}

USER root

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

USER airflow
COPY airflow.requirements.txt .
RUN pip install --no-cache-dir -r airflow.requirements.txt
```

---

## 3. CI/CD – Tự động hoá build & deploy

Ví dụ GitHub Actions workflow:
```yaml
name: Build & Push Airflow Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USER }}
        password: ${{ secrets.DOCKER_PASS }}

    - name: Build & Push Image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: your_dockerhub_user/airflow-nptan:latest
```

---

# 🔌 Airflow Plugins & Command-line Management

## 1. Airflow Plugins

Airflow hỗ trợ plugin để mở rộng tính năng — như thêm operators, sensors, hooks, macros, và Flask views.

Cấu trúc thư mục plugins/:
```
plugins/
├── __init__.py
├── custom_operator.py
├── custom_hook.py
├── my_plugin.py
```

Ví dụ plugin operator:
```python
# plugins/custom_operator.py
from airflow.models import BaseOperator

class HelloOperator(BaseOperator):
    def execute(self, context):
        print("Xin chào từ plugin!")
```

Đăng ký plugin:
```python
# plugins/my_plugin.py
from airflow.plugins_manager import AirflowPlugin
from .custom_operator import HelloOperator

class MyAirflowPlugin(AirflowPlugin):
    name = "my_custom_plugin"
    operators = [HelloOperator]
```

---

## 2. Lệnh quản lý Airflow (CLI)

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
