# 🚀 README: DAGs, Dockerfile, và CI/CD cho Airflow

---

## 📂 1. DAGs – Tập tin điều khiển workflow

### 📁 Thư mục: `dags/`

Chứa các file `.py` định nghĩa workflow và các task của bạn trong Airflow.

### ✅ Cấu trúc DAG cơ bản:

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

### 💡 Lưu ý:
- Tên file `.py` không được chứa ký tự đặc biệt
- Luôn đặt DAG trong `with DAG(...)` block
- Gán `dag_id` duy nhất cho mỗi DAG

---

## 🐳 2. Dockerfile – Định nghĩa image của bạn

### ✅ Dockerfile chuẩn cho Airflow mở rộng:

```Dockerfile
ARG AIRFLOW_IMAGE_NAME
FROM ${AIRFLOW_IMAGE_NAME}

USER root

RUN apt-get update &&     apt-get install -y openjdk-11-jdk &&     apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

USER airflow
COPY airflow.requirements.txt .
RUN pip install --no-cache-dir -r airflow.requirements.txt
```

> 💡 Image base: `apache/airflow:2.10.5-python3.12`

---

## 🔄 3. CI/CD – Tự động hoá build & deploy

### 🎯 Mục tiêu CI/CD:
- Tự động build Docker image
- Push lên Docker Hub
- Deploy Airflow stack

---

### ✅ Ví dụ GitHub Actions workflow (`.github/workflows/airflow.yml`):

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

### ✅ Secrets bạn cần set trong GitHub:
- `DOCKER_USER`
- `DOCKER_PASS`

---

## 🧠 Gợi ý CI/CD nâng cao:
| Mục tiêu                  | Công cụ                       |
| ------------------------- | ----------------------------- |
| Chạy test DAG             | `pytest`, `airflow dags test` |
| Lint Python               | `flake8`, `black`             |
| Triển khai lên production | SSH deploy, AWS ECS, K8s, GKE |

---

## ✅ Tổng kết

| Thành phần | Mục tiêu                 | Ghi chú                               |
| ---------- | ------------------------ | ------------------------------------- |
| DAGs       | Lập lịch và chạy task    | Nên kiểm tra bằng `airflow dags test` |
| Dockerfile | Xây dựng môi trường      | Tách biệt rõ ràng các lib cần thiết   |
| CI/CD      | Tự động hoá build/deploy | Sử dụng GitHub Actions là dễ nhất     |

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-04-19
