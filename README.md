# Giới thiệu:

## Mục đích dự án:
Dự án này xử lý việc lên lịch, thực thi và lưu trữ dữ liệu sau khi xử lý. Nó tích hợp với cơ sở dữ liệu Oracle, các server SFTP và dịch vụ email.

Project sử dụng Sử dụng airflow, được mở rộng bằng các thư viên python (schedule service) do tôi viết và áp dụng vài tổ chức đã làm trước đây.

## tác giả:
**email:** *nptan2005@gmail.com*

# 📊 Tổng Quan Apache Airflow

---

## 1️⃣ Tổng quan

**Apache Airflow** là một nền tảng mã nguồn mở dùng để lập lịch và giám sát luồng công việc (workflow) theo cách lập trình được.  
Airflow cho phép bạn định nghĩa các DAGs (Directed Acyclic Graphs) — một chuỗi các task có quan hệ phụ thuộc logic — bằng Python.

> 🧠 "Viết DAG như viết code, không cần cấu hình phức tạp."

---

## 2️⃣ Tính năng nổi bật


| Tính năng             | Mô tả                                             |
|-----------------------|--------------------------------------------------|
| 🧩 Modular            | Có thể mở rộng bằng plugin, viết operator tùy chỉnh |
| 🛠 Lập lịch linh hoạt | Dựa trên cron hoặc thời gian tùy chỉnh           |
| 📊 Web UI mạnh mẽ     | Theo dõi DAG, log, retry task...                 |
| 💥 Retry, Alert, SLA  | Tự động retry, gửi email khi task fail          |
| 🧵 Parallel execution | Chạy task song song qua Celery, Kubernetes      |
| 🔐 RBAC UI            | Phân quyền người dùng rõ ràng                   |


---

## 3️⃣ Ứng dụng thực tế


| Lĩnh vực         | Ứng dụng                                    |
|------------------|---------------------------------------------|
| 🎯 Dữ liệu lớn   | ETL, chuẩn hóa dữ liệu, Spark/Hadoop        |
| 🧪 Khoa học dữ liệu | Training ML model định kỳ                |
| 🛒 E-commerce     | Tự động hóa báo cáo bán hàng               |
| 📬 Marketing      | Gửi email hàng loạt theo lịch              |
| 🧾 Kế toán        | Đối soát dữ liệu, chạy batch jobs          |


---

## 4️⃣ Khả năng mở rộng

|---------------------|------------------------------------------------------|
| Mode                | Đặc điểm                                             |
|---------------------|------------------------------------------------------|
| SequentialExecutor  | Chạy tuần tự – chỉ dùng khi test                     |
|---------------------|------------------------------------------------------|
| LocalExecutor       | Chạy song song trong 1 máy                           |
|---------------------|------------------------------------------------------|
| CeleryExecutor      | Scale bằng nhiều worker, sử dụng Redis/RabbitMQ      |
|---------------------|------------------------------------------------------|
| KubernetesExecutor  | Tự động spawn pod cho từng task – lý tưởng cho cloud |
|---------------------|------------------------------------------------------|


---

## 5️⃣ Kiến trúc & các thành phần chính

```plaintext
                         +-----------------------+
                         |   Web Server (UI)     |
                         |   Flask + Gunicorn    |
                         +-----------+-----------+
                                     |
                                     v
                              Scheduler (Trigger DAG)
                                     |
                                     v
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
         Worker 1               Worker 2               Worker N
          (task)                 (task)                 (task)
              |                      |                      |
              +----------------------+----------------------+
                                     |
                           Redis/RabbitMQ (Broker)
                                     |
                          PostgreSQL/MySQL (Metadata DB)
```

### 📦 Mô tả chi tiết:


|--------------|--------------------------------------|-------------------------------------------|
| Thành phần   | Mô tả                                | Tính năng chính                           |
|--------------|--------------------------------------|-------------------------------------------|
| Webserver    | Giao diện người dùng (Flask)         | Xem DAG, trigger, log                     | 
|--------------|--------------------------------------|-------------------------------------------|
| Scheduler    | Lập lịch DAG theo thời gian          | Theo dõi trạng thái & lên lịch task       |
|--------------|--------------------------------------|-------------------------------------------|
| Worker       | Thực thi task DAG                    | Có thể scale hàng chục                    |
|--------------|--------------------------------------|-------------------------------------------|
| Broker       | Giao tiếp giữa Scheduler và Worker   | Redis hoặc RabbitMQ                       |
|--------------|--------------------------------------|-------------------------------------------|
| Metadata DB  | Lưu trạng thái, DAG, task...         | Cực kỳ quan trọng, không được mất dữ liệu |
|--------------|--------------------------------------|-------------------------------------------|
| Flower       | Monitor queue Celery                 | Xem queue, retry, trạng thái worker       |
|--------------|--------------------------------------|-------------------------------------------|


---

✅ Với kiến trúc này, Airflow rất phù hợp để scale từ máy local lên production cloud (GCP, AWS, Azure).

-----------------------------------------------------------------------------

# ⚙️ README: Mô hình triển khai Apache Airflow theo Docker & Microservices + CI/CD

---

## 🧭 Mục tiêu

Mô hình hoá hệ thống Airflow linh hoạt, hiện đại theo kiến trúc **microservices**, kết hợp với CI/CD để:

- ✅ Tự động build, push, deploy images
- ✅ Tách biệt từng thành phần trong container
- ✅ Có thể scale riêng các worker, proxy, etc.
- ✅ Tự động kiểm thử DAG trước khi đưa vào production

---

## 🧱 Mô hình tổng quan hệ thống

```plaintext
                              [ GitHub / GitLab ]
                                       |
                                       v
                             +------------------+
                             |   CI/CD Pipeline |
                             | (GitHub Actions) |
                             +------------------+
                                       |
        -------------------------------------------------------
        |                      |                              |
        v                      v                              v
 [Docker Build]       [Unit test DAGs]             [Push image airflow-nptan:tag]
        |
        v
[docker-compose-prod.yaml / Kubernetes Helm chart]
        |
        v
    +------------------------+      +--------------------+
    |  airflow-webserver     | <--> |  nginx proxy (TLS) |
    +------------------------+      +--------------------+
        |
        v
+--------------------------+
|  airflow-scheduler       |
+--------------------------+
        |
        v
+--------------------------+
| Redis / RabbitMQ Broker  |
+--------------------------+
        |
        v
+--------------------------+
|  airflow-worker(s)       | <---- scale horizontally
+--------------------------+
        |
        v
+--------------------------+
| PostgreSQL (metadata DB) |
+--------------------------+
```

---

## 🧩 Thành phần & vai trò

| Thành phần         | Vai trò |
|--------------------|--------|
| **GitHub CI/CD**   | Kiểm thử, build, push image |
| **Docker Compose / K8s** | Triển khai Airflow stack |
| **Nginx proxy**    | Reverse proxy, SSL |
| **Webserver**      | Giao diện quản trị |
| **Scheduler**      | Lập lịch DAG |
| **Worker(s)**      | Thực thi task (scale) |
| **Redis**          | Queue broker |
| **PostgreSQL**     | Lưu trạng thái DAG/task |

---

## 🔁 CI/CD mẫu với GitHub Actions

```yaml
name: Deploy Airflow

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: docker/setup-buildx-action@v2

    - name: Build & Push image
      uses: docker/build-push-action@v4
      with:
        context: .
        tags: your_user/airflow-nptan:latest
        push: true

    - name: Trigger Deploy Server (SSH)
      uses: appleboy/ssh-action@v1
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USER }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd airflow-deploy
          docker compose pull
          docker compose up -d
```

---

## 🔐 Secrets CI/CD cần thiết

| Tên biến | Mô tả |
|----------|------|
| `DOCKER_USER` | Docker Hub username |
| `DOCKER_PASS` | Docker Hub password/token |
| `SSH_KEY`     | Private key deploy server |
| `HOST`        | IP/FQDN của máy chủ |
| `USER`        | User SSH |

---

## 🔄 DAG Sync mô hình production

### Cách phổ biến:
1. Mount volume từ NFS chứa DAG
2. Đồng bộ DAG từ Git về container bằng `git pull` + cron
3. Dùng `airflow-dags-git-sync` hoặc sidecar container (K8s)

---

✅ Mô hình này phù hợp với production cần:
- Chạy nhiều DAG phức tạp
- Theo dõi lịch sử, log chi tiết
- Có quy trình CI/CD mạnh mẽ
- Tối ưu hiệu năng và khả năng mở rộng



-----------------------------------------------------------------------------
# 📘 Airflow Production & Development Setup Guide

## 📦 1. Docker Compose (Development Mode)

Docker Compose là cách nhanh gọn để khởi chạy toàn bộ Airflow stack trên 1 máy dev (macOS, Windows, Linux).

### ✅ Cấu trúc điển hình gồm:
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-worker` (scale được)
- `airflow-init`
- `flower` (monitor worker)
- `postgres` (metadata DB)
- `redis` (Celery broker)
- `nginx` (proxy/nginx optional)

### ✅ Image chuẩn:

```yaml
x-airflow-common:
  &airflow-common
  image: airflow-nptan:1.0.0
  build:
    context: .
    dockerfile: ./airflow.Dockerfile
```

### ✅ Clean container names:

```yaml
services:
  airflow-webserver:
    <<: *airflow-common
    container_name: airflow-webserver

  airflow-scheduler:
    <<: *airflow-common
    container_name: airflow-scheduler

  # ...với các service còn lại

  postgres:
    image: postgres:13
    container_name: airflow-postgres
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
```

⛔ Không áp dụng `<<: *airflow-common` cho `postgres`, `redis`, hoặc `nginx`.

---

## 🧩 2. Docker Named Volume: `postgres-db-volume`

Volume này được Docker quản lý và **không cần tạo thủ công**.

### ✅ Backup volume ra file `.tar.gz`:

```bash
docker run --rm   -v airflow_bvb_postgres-db-volume:/volume   -v $(pwd)/db_backup:/backup   alpine   tar czf /backup/postgres_data_backup.tar.gz -C /volume .
```

### ✅ Restore lại:

```bash
docker volume create airflow_bvb_postgres-db-volume

docker run --rm   -v airflow_bvb_postgres-db-volume:/volume   -v $(pwd)/db_backup:/backup   alpine   tar xzf /backup/postgres_data_backup.tar.gz -C /volume
```

---

## 🧠 3. Tại sao `container_name` khiến bạn không scale được?

```yaml
services:
  airflow-worker:
    container_name: airflow-worker
```

→ Khi scale:

```bash
docker compose up --scale airflow-worker=2
```

→ Docker lỗi do **2 container trùng tên**.

### ✅ Giải pháp:
- ❌ Đừng dùng `container_name` nếu muốn scale
- ✅ Dùng `-p airflow` để đổi prefix project

---

## 🚀 4. Production Deployment (Recommended)

| Service         | Nên tách ra? | Ghi chú |
|----------------|--------------|--------|
| Webserver      | ✅           | Cho UI riêng |
| Scheduler      | ✅           | Đảm bảo trigger |
| Worker(s)      | ✅✅✅       | Nên scale |
| Redis          | ✅           | Broker |
| PostgreSQL     | ✅           | Metadata DB |
| Nginx / Proxy  | ✅           | TLS, route |
| Flower         | ✅           | Giám sát task |
| DAG Storage    | ✅ (optional)| S3/NFS để đồng bộ DAG |

---

## ⚙️ Công cụ production nên dùng:

- ✅ Docker Compose (dev/staging)
- ✅ Kubernetes (Helm chart Airflow)
- ✅ AWS ECS / GCP GKE / Azure AKS
- ✅ Redis Cluster, PostgreSQL RDS
- ✅ Giám sát: Prometheus, Grafana, Sentry

---

## 🧠 So sánh Docker Compose vs Cài Service Truyền Thống

| Tiêu chí          | Docker Compose         | Cài nhiều service |
|------------------|------------------------|-------------------|
| Dễ quản lý        | ✅                      | ❌ |
| Backup đơn giản   | ✅ Volume/pg_dump       | ❌ Khó hơn |
| Scale linh hoạt   | ✅ `--scale`            | ❌ Thủ công |
| Tách biệt service | ✅                      | ❌ |
| Dev → Prod dễ     | ✅ Build/Push/Tag       | ❌ |

---

## ✅ Tag và Push Image

```bash
docker tag airflow-nptan:1.0.0 your_dockerhub_user/airflow-nptan:1.0.0
docker push your_dockerhub_user/airflow-nptan:1.0.0
```
-----------------------------------------------------------------------------


# 🛠 README: Scripts, nginx.conf & .env Usage

## 📁 1. scripts/

Thư mục `scripts/` thường chứa các file shell hoặc Python hỗ trợ hệ thống Airflow như:

| Script              | Mục đích |
|---------------------|----------|
| `init.sh`           | Tạo user, migrate db, khởi tạo lần đầu |
| `backup.sh`         | Sao lưu dữ liệu PostgreSQL hoặc DAGs |
| `restore.sh`        | Khôi phục dữ liệu từ bản sao lưu |
| `healthcheck.sh`    | Dùng để kiểm tra tình trạng container |
| `generateKey.py`    | Sinh key mã hoá, dùng trong DAG |

> 📌 Tất cả file `.sh` cần được gán quyền chạy:
```bash
chmod +x scripts/*.sh
```

---

## 🌐 2. nginx.conf

Cấu hình NGINX làm **reverse proxy** cho Airflow Webserver:

### ✅ Ví dụ cấu hình:

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

### 📦 Mount file vào container:

```yaml
services:
  access-hot-proxy:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
```

> 🔐 Bạn có thể mở rộng với SSL (Let's Encrypt), hoặc định tuyến nhiều domain.

---

## 🔐 3. File `.env`

File `.env` dùng để **quản lý biến môi trường** riêng biệt theo từng máy hoặc môi trường:

### Ví dụ `.env.mac`:

```env
AIRFLOW_IMAGE_NAME=apache/airflow:2.10.5-python3.12
AIRFLOW_UID=501
AIRFLOW_GID=20
_AIRFLOW_WWW_USER_USERNAME=tanp
_AIRFLOW_WWW_USER_PASSWORD=Vccb1234
```

### 🔄 Sử dụng `.env` trong `docker-compose.yml`:

```yaml
env_file: .env
```

Hoặc dùng trong CLI:

```bash
cp .env.mac .env  # macOS
# hoặc
Copy-Item .env.windows -Destination .env  # Windows PowerShell
```

---

## ✅ Tổng kết

| Thành phần | Vai trò | Khuyến nghị |
|------------|---------|-------------|
| scripts/   | Tự động hóa quản lý Airflow | Tách biệt logic rõ ràng |
| nginx.conf | Reverse proxy + SSL         | Mount vào container |
| .env       | Biến môi trường cấu hình    | Dùng theo từng môi trường |

-----------------------------------------------------------------------------
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
| Mục tiêu                  | Công cụ |
|---------------------------|---------|
| Chạy test DAG             | `pytest`, `airflow dags test` |
| Lint Python               | `flake8`, `black`              |
| Triển khai lên production | SSH deploy, AWS ECS, K8s, GKE  |

---

## ✅ Tổng kết

| Thành phần | Mục tiêu | Ghi chú |
|------------|----------|--------|
| DAGs       | Lập lịch và chạy task | Nên kiểm tra bằng `airflow dags test` |
| Dockerfile | Xây dựng môi trường    | Tách biệt rõ ràng các lib cần thiết |
| CI/CD      | Tự động hoá build/deploy | Sử dụng GitHub Actions là dễ nhất |

-----------------------------------------------------------------------------
# 🔌 README: Airflow Plugins & Command-line Management

## 🔌 1. Airflow Plugins

Airflow hỗ trợ plugin để mở rộng tính năng — như thêm operators, sensors, hooks, macros, và Flask views.

### 📁 Cấu trúc thư mục plugins/:
``` 
plugins/
├── __init__.py
├── custom_operator.py
├── custom_hook.py
├── my_plugin.py
```
	🔁 Airflow sẽ tự động load tất cả các file .py trong plugins/ mỗi lần khởi động.

### ✅ Ví dụ 1: Plugin operator

```python
# plugins/custom_operator.py
from airflow.models import BaseOperator

class HelloOperator(BaseOperator):
    def execute(self, context):
        print("Xin chào từ plugin!")
```

### ✅ Ví dụ 2: Đăng ký plugin

```python
# plugins/my_plugin.py
from airflow.plugins_manager import AirflowPlugin
from .custom_operator import HelloOperator

class MyAirflowPlugin(AirflowPlugin):
    name = "my_custom_plugin"
    operators = [HelloOperator]
```

## ⚙️ 2. Lệnh quản lý Airflow (CLI)

### ✅ Cơ bản
```bash
airflow db init               # Khởi tạo database lần đầu
airflow db upgrade            # Cập nhật schema database
airflow users create          # Tạo user đăng nhập
airflow webserver             # Chạy web UI
airflow scheduler             # Chạy scheduler
```

### ✅ DAG management

```bash
airflow dags list                     # Liệt kê các DAG
airflow dags trigger <dag_id>        # Kích hoạt DAG thủ công
airflow dags pause <dag_id>          # Dừng chạy DAG theo schedule
airflow dags unpause <dag_id>        # Cho phép DAG chạy theo schedule
```

### ✅ Task management

```bash
airflow tasks list <dag_id>                           # Liệt kê task trong DAG
airflow tasks test <dag_id> <task_id> <exec_date>     # Test task cục bộ
```

### ✅ Monitoring & Debug

```bash
airflow info                  # Xem thông tin cấu hình
airflow config get-value core dags_folder
airflow plugins list          # Liệt kê plugin đã được load
```

## 🧠 Gợi ý khi dùng plugins:

| **Lưu ý**     | **Mẹo**                               |
|---------------|---------------------------------------|
| Load chậm?	| Kiểm tra log khi khởi động webserver  |
|---------------|---------------------------------------|
| Debug plugin	| Dùng airflow plugins list             |
|---------------|---------------------------------------|
| Reusable code	| Tách rõ file .py trong plugins/       |
|---------------|---------------------------------------|
| Reload plugin	| Phải restart webserver/scheduler      |
---------------------------------------------------------

-----------------------------------------------------------------------------

# 🚀 Giao diện Web Airflow – Tổng Quan

Truy cập web UI qua:
👉 http://localhost:8080 (mặc định)
Đăng nhập bằng tài khoản bạn đã cấu hình:

```bash
Username: tanp
Password: Vccb1234
```

## 🧭 Các thành phần chính trên Web UI

| **Mục**                 |	**Mô tả**
|-------------------------|-----------------------------------------------------------|
| DAGs	                  | Danh sách các DAG được phát hiện trong thư mục dags/
|-------------------------|-----------------------------------------------------------|
| Tree View	              | Biểu đồ DAG dạng cây: các task theo ngày chạy
|-------------------------|-----------------------------------------------------------|
| Graph View	          | DAG hiển thị theo dạng node – giúp dễ hình dung pipeline
|-------------------------|-----------------------------------------------------------|
| Code	                  | Xem source code Python của DAG
|-------------------------|-----------------------------------------------------------|
| Trigger DAG	          | Kích hoạt DAG thủ công
|-------------------------|-----------------------------------------------------------|
| Pause/Unpause	          | Bật/tắt chạy DAG theo schedule
|-------------------------|-----------------------------------------------------------|
| Admin → Connections     |	Quản lý kết nối đến DB, API, SFTP,…
|-------------------------|-----------------------------------------------------------|
| Admin → Variables	      | Biến môi trường toàn cục cho DAG
|-------------------------|-----------------------------------------------------------|
| Admin → Pools	          | Giới hạn số task chạy song song
|-------------------------|-----------------------------------------------------------|
| Browse → Task Instances |	Theo dõi từng lần chạy của task
|-------------------------|-----------------------------------------------------------|
| Browse → Logs	          | Xem log task chạy thất bại/thành công
|-------------------------|-----------------------------------------------------------|
| Browse → DAG Runs	      | Danh sách các lần chạy của mỗi DAG

### 🔧 1. Cấu hình Connections
    1.	Truy cập: Admin → Connections
	2.	Nhấn ➕ để tạo kết nối mới
	3.	Ví dụ tạo kết nối PostgreSQL:

| **Field**    | **Value**
|--------------|----------------------------------------|
| Conn Id	   | my_postgres
|--------------|----------------------------------------|
| Conn Type	   | Postgres
|--------------|----------------------------------------|
| Host	       | postgres (tên service trong compose)
|--------------|----------------------------------------|
| Schema	   | airflow
|--------------|----------------------------------------|
| Login	       | airflow
|--------------|----------------------------------------|
| Password	   | airflow
|--------------|----------------------------------------|
| Port	       | 5432
|--------------|----------------------------------------|

**🧪 Bạn có thể test bằng Python operator dùng:**
```python
PostgresHook(postgres_conn_id="my_postgres")
```

### 🧰 2. Cấu hình Variables (Admin → Variables)

Dùng để truyền biến toàn cục vào DAG:
	•	Ví dụ key: email_list
	•	Value: ["dev@example.com", "admin@example.com"]

Sau đó dùng trong DAG:

```python
from airflow.models import Variable

emails = Variable.get("email_list", deserialize_json=True)
```

### 🛑 3. Dừng/Chạy DAG

	*	🔘 Pause DAG: Dừng chạy theo lịch (schedule_interval)
	*	▶️ Unpause DAG: Bật lại tự động chạy
	*	🔄 Trigger DAG: Chạy thủ công 1 lần

### 🧪 4. Kiểm tra Log Task

	*	Vào Browse → DAG Runs → Task Instance
	*	Chọn 1 task → bấm “Log” để xem chi tiết
	*	Có thể thấy traceback khi task lỗi

### 🔐 5. Thêm người dùng

Từ terminal:
```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password yourpassword
```

## 📊 Tùy chỉnh Web UI thêm:

	•	Cài theme: pip install airflow-theme
	•	Sửa favicon/logo: Override Flask template (nâng cao)
	•	Thêm menu mới: viết plugin flask_blueprint (nâng cao)

## ✅ Kết luận

| **Việc cần làm**         |  	**Thực hiện ở đâu**
|--------------------------|----------------------------|
| Tạo DAG, Trigger DAG     | Trang DAGs
|--------------------------|----------------------------|
| Xem log, trạng thái task | Browse → Task Instances
|--------------------------|----------------------------|
| Quản lý DB/API…	       | Admin → Connections
|--------------------------|----------------------------|
| Lưu biến toàn cục	       | Admin → Variables
|--------------------------|----------------------------|
| Tạo người dùng	       | CLI hoặc Admin UI
|--------------------------|----------------------------|


-----------------------------------------------------------------------------


# ☁️📈 Apache Airflow – Tích hợp với Cloud, Datalake & Machine Learning

## 1️⃣ Khả năng tích hợp với Databricks, Cloud, Data Lake

Apache Airflow hỗ trợ kết nối và orchestration với các nền tảng cloud và data lake thông qua các **providers**:

| Dịch vụ         | Mô tả hỗ trợ                                 |
|------------------|---------------------------------------------|
| Databricks       | Hook, operator để submit job lên DB         |
| AWS              | S3, EMR, Lambda, ECS, Glue...               |
| GCP              | BigQuery, Cloud Composer, GKE               |
| Azure            | Data Lake, Synapse, ML Service              |
| Snowflake        | Query trực tiếp, run warehouse              |
| HDFS / MinIO     | Lưu trữ DAG hoặc batch đầu vào              |

## 2️⃣ Tích hợp & bổ trợ cho Machine Learning

Airflow là công cụ orchestrator, rất tốt để:
	•	Xây dựng MLOps pipeline
	•	Tự động hoá các bước ML:
	•	Thu thập dữ liệu
	•	Tiền xử lý
	•	Train model
	•	Evaluate
	•	Deploy

	✅ Dùng tốt với MLflow, Metaflow, hoặc trực tiếp với TensorFlow, scikit-learn…

## 3️⃣ Tích hợp TensorFlow

 có thể:
	•	Viết PythonOperator để gọi hàm train model
	•	Gọi shell script hoặc submit job lên Spark/TensorFlow Cluster
	•	Ghi log vào MLflow / Neptune / WandB

```python
def train_model():
    import tensorflow as tf
    model = tf.keras.Sequential([...])
    model.compile(...)
    model.fit(...)

PythonOperator(
    task_id="train_ai_model",
    python_callable=train_model
)
```
## 4️⃣ Ưu nhược điểm của Airflow:

| Ưu điểm                           | Nhược điểm                             |
|----------------------------------|----------------------------------------|
| ✅ Quản lý DAG bằng Python        | ❌ Không tối ưu cho real-time streaming |
| ✅ Web UI đẹp, dễ dùng            | ❌ Khởi động chậm nếu DAG lớn           |
| ✅ Hỗ trợ retry, SLA, alert      | ❌ Không tốt cho task cực ngắn          |
| ✅ Rất nhiều provider cloud       | ❌ Cần cấu hình nhiều nếu dùng K8s      |
| ✅ Rất mạnh về orchestrate logic | ❌ Không có model registry built-in     |

## 5️⃣ So sánh với các framework khác

| Tool              | Open Source | Điểm mạnh                | Yếu điểm / Hạn chế                  |
|-------------------|-------------|--------------------------|--------------------------------------|
| **Airflow**       | ✅           | Linh hoạt, phổ biến       | Không real-time                      |
| Prefect           | ✅           | Dễ dùng, DAG như Python   | Giao diện miễn phí còn hạn chế       |
| Dagster           | ✅           | Typed DAG, Data-aware     | Mới hơn, ít cộng đồng hơn            |
| Luigi             | ✅           | Nhẹ, ít phụ thuộc         | Không có web UI, đã cũ               |
| Azure Data Factory| ❌           | Tích hợp Azure tốt        | Không mở rộng, phụ thuộc Microsoft   |
| GCP Composer      | ❌           | Quản lý airflow trên cloud | Chi phí cao, ít tuỳ biến             |
| AWS Step Functions| ❌           | Tích hợp Lambda/S3 tốt    | Không viết code thuần Python         |

## ✅ Đề xuất

| Tình huống                    | Công cụ phù hợp    |
|-------------------------------|--------------------|
| Xây dựng ETL/ELT + ML         | **Airflow**        |
| Workflow đơn giản, realtime   | Prefect, Dagster   |
| Azure-only                    | Azure Data Factory |
| ML trên GCP                   | Airflow + BigQuery |
| MLOps + UI + Tracking         | Airflow + MLflow   |

-----------------------------------------------------------------------------
# Đánh giá về việc khắc phục nhược điểm data streaming của airflow
# 🔄 Apache Airflow + Streaming: Kafka & Giải pháp thay thế

## ❓ Vấn đề: Airflow không hỗ trợ Streaming Real-time

*Apache Airflow được thiết kế để xử lý các batch jobs, theo lịch trình định kỳ.*
***⚠️ Không phù hợp cho xử lý event-driven hoặc streaming real-time như:***
	•	Consume Kafka message mỗi giây
	•	Trigger DAG khi có dữ liệu đẩy tới
	•	Xử lý continuous stream từ IoT, logs…

## 1️⃣ Tích hợp Apache Kafka với Airflow

### ✅ Mục tiêu:
	•	Airflow xử lý batch từ Kafka mỗi X phút
	•	Hoặc Airflow trigger DAG khi detect file/message
### 📦 Cách tích hợp phổ biến:

Cách	             | Mô tả
---------------------|-------------------------------------------------------------------|
Kafka Consumer DAG	 | DAG chạy mỗi X phút, dùng hook để lấy batch từ Kafka
---------------------|-------------------------------------------------------------------|
Sensor + Kafka	     | Viết custom sensor, check Kafka message rồi trigger task
---------------------|-------------------------------------------------------------------|
Kafka → HTTP	     | Kafka push event đến API để trigger Airflow DAG (via REST API)
---------------------|-------------------------------------------------------------------|
Kafka → DB → Airflow | Kafka dump vào DB, Airflow dùng ExternalTaskSensor
---------------------|-------------------------------------------------------------------|

### 🔧 Ví dụ sử dụng Kafka Hook:

```python
from airflow.hooks.base_hook import BaseHook
from kafka import KafkaConsumer

def read_kafka():
    consumer = KafkaConsumer(
        'my-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'
    )
    for msg in consumer:
        print(msg.value)
```

## 2️⃣ Ưu – Nhược khi tích hợp Kafka

| Ưu điểm                          | Nhược điểm                             |
|----------------------------------|----------------------------------------|
| ✅ Có thể xử lý event theo batch | ❌ Không phải real-time thực sự        |
| ✅ Tận dụng hệ thống Airflow sẵn | ❌ Không scale tốt theo tốc độ Kafka   |
| ✅ Dễ debug với web UI/log       | ❌ Complex nếu dùng sensor liên tục     |

## 3️⃣ Giải pháp thay thế chuyên dụng streaming

| Công cụ          | Ưu điểm                                      | Nhược điểm                    |
|------------------|----------------------------------------------|-------------------------------|
| **Apache Flink** | Stream + batch, cực kỳ mạnh với CEP         | Học hơi khó, JVM-based        |
| Kafka Streams    | Nhẹ, chạy trong microservices Java           | Phụ thuộc Kafka platform      |
| Spark Structured Streaming | Giao diện dễ, scale tốt              | Delay cao nếu xử lý nhỏ       |
| NiFi             | GUI luồng dữ liệu trực quan, support Kafka   | Tính linh hoạt thấp hơn code  |
| Prefect + Kafka  | Event-based DAG hỗ trợ native                | Mới hơn, ít plugin cloud hơn  |

## 4️⃣ Đề xuất

| Mục đích                     | Nên dùng gì            |
|------------------------------|------------------------|
| ETL batch mỗi 15 phút        | Airflow + KafkaConsumer |
| Trigger DAG theo file/data   | Airflow + REST API      |
| Streaming real-time mạnh     | Kafka + Flink/Spark     |
| DAG trigger theo event       | Prefect or Dagster      |
| Tích hợp Kafka + tracking    | NiFi + Airflow / Flink  |

## ✅ Tổng kết

Airflow vẫn có thể tương tác với Kafka nhưng không nên dùng cho streaming real-time.
📌 Nếu workload của bạn yêu cầu < 5 phút/dữ liệu – dùng Prefect, Flink hoặc Spark Streaming là lựa chọn tốt hơn.

-----------------------------------------------------------------------------
# 📂 Tài liệu tham khảo

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Helm Chart Airflow](https://github.com/apache/airflow/tree/main/chart)

---

**✍️ Tác giả:** nptan2005  
**📅 Generated:** 2025-04-19
