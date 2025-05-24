# 📊 Tổng Quan Apache Airflow

---

## 1️⃣ Tổng quan

**Apache Airflow** là nền tảng mã nguồn mở để lập lịch và giám sát workflow theo cách lập trình.  
Bạn định nghĩa các DAGs (Directed Acyclic Graphs) — chuỗi các task phụ thuộc logic — bằng Python.

> 🧠 "Viết DAG như viết code, không cần cấu hình phức tạp."

---

## 2️⃣ Tính năng nổi bật

| Tính năng            | Mô tả                                        |
| -------------------- | -------------------------------------------- |
| 🧩 Modular            | Mở rộng bằng plugin, viết operator tùy chỉnh |
| 🛠 Lập lịch linh hoạt | Dựa trên cron hoặc thời gian tùy chỉnh       |
| 📊 Web UI mạnh mẽ     | Theo dõi DAG, log, retry task...             |
| 💥 Retry, Alert, SLA  | Tự động retry, gửi email khi task fail       |
| 🧵 Parallel execution | Chạy task song song qua Celery, Kubernetes   |
| 🔐 RBAC UI            | Phân quyền người dùng rõ ràng                |

---

## 3️⃣ Ứng dụng thực tế

| Lĩnh vực           | Ứng dụng                             |
| ------------------ | ------------------------------------ |
| 🎯 Dữ liệu lớn      | ETL, chuẩn hóa dữ liệu, Spark/Hadoop |
| 🧪 Khoa học dữ liệu | Training ML model định kỳ            |
| 🛒 E-commerce       | Tự động hóa báo cáo bán hàng         |
| 📬 Marketing        | Gửi email hàng loạt theo lịch        |
| 🧾 Kế toán          | Đối soát dữ liệu, chạy batch jobs    |

---

## 4️⃣ Khả năng mở rộng

| Mode               | Đặc điểm                                             |
| ------------------ | ---------------------------------------------------- |
| SequentialExecutor | Chạy tuần tự – chỉ dùng khi test                     |
| LocalExecutor      | Chạy song song trong 1 máy                           |
| CeleryExecutor     | Scale bằng nhiều worker, sử dụng Redis/RabbitMQ      |
| KubernetesExecutor | Tự động spawn pod cho từng task – lý tưởng cho cloud |

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

| Thành phần  | Mô tả                              | Tính năng chính                           |
| ----------- | ---------------------------------- | ----------------------------------------- |
| Webserver   | Giao diện người dùng (Flask)       | Xem DAG, trigger, log                     |
| Scheduler   | Lập lịch DAG theo thời gian        | Theo dõi trạng thái & lên lịch task       |
| Worker      | Thực thi task DAG                  | Có thể scale hàng chục                    |
| Broker      | Giao tiếp giữa Scheduler và Worker | Redis hoặc RabbitMQ                       |
| Metadata DB | Lưu trạng thái, DAG, task...       | Cực kỳ quan trọng, không được mất dữ liệu |
| Flower      | Monitor queue Celery               | Xem queue, retry, trạng thái worker       |

✅ Kiến trúc này phù hợp để scale từ local lên production cloud (GCP, AWS, Azure).

---

# ⚙️ Mô hình triển khai Apache Airflow theo Docker & Microservices + CI/CD

## 🧭 Mục tiêu

- ✅ Tự động build, push, deploy images
- ✅ Tách biệt từng thành phần trong container
- ✅ Có thể scale riêng các worker, proxy, etc.
- ✅ Tự động kiểm thử DAG trước khi đưa vào production

---

## 🧱 Mô hình tổng quan hệ thống

```plaintext
[GitHub/GitLab] → CI/CD Pipeline → Build/Push Image → Deploy (docker-compose/K8s)
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

| Thành phần             | Vai trò                     |
| ---------------------- | --------------------------- |
| **GitHub CI/CD**       | Kiểm thử, build, push image |
| **Docker Compose/K8s** | Triển khai Airflow stack    |
| **Nginx proxy**        | Reverse proxy, SSL          |
| **Webserver**          | Giao diện quản trị          |
| **Scheduler**          | Lập lịch DAG                |
| **Worker(s)**          | Thực thi task (scale)       |
| **Redis**              | Queue broker                |
| **PostgreSQL**         | Lưu trạng thái DAG/task     |

---



## 🔐 Secrets CI/CD cần thiết

| Tên biến      | Mô tả                     |
| ------------- | ------------------------- |
| `DOCKER_USER` | Docker Hub username       |
| `DOCKER_PASS` | Docker Hub password/token |
| `SSH_KEY`     | Private key deploy server |
| `HOST`        | IP/FQDN của máy chủ       |
| `USER`        | User SSH                  |

---

## 🔄 DAG Sync mô hình production

1. Mount volume từ NFS chứa DAG
2. Đồng bộ DAG từ Git về container bằng `git pull` + cron
3. Dùng `airflow-dags-git-sync` hoặc sidecar container (K8s)

---

✅ Mô hình này phù hợp với production cần:
- Chạy nhiều DAG phức tạp
- Theo dõi lịch sử, log chi tiết
- Có quy trình CI/CD mạnh mẽ
- Tối ưu hiệu năng và khả năng mở rộng

---

# [📘 Airflow Production & Development Setup Guide](docs/Airflow_Production_and_Development_Setup_Guide.md)

## 1. Docker Compose (Development Mode)

Docker Compose là cách nhanh gọn để khởi chạy toàn bộ Airflow stack trên 1 máy dev (macOS, Windows, Linux).

### Cấu trúc điển hình gồm:
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-worker` (scale được)
- `airflow-init`
- `flower` (monitor worker)
- `postgres` (metadata DB)
- `redis` (Celery broker)
- `nginx` (proxy/nginx optional)



## 2. Production Deployment (Recommended)

| Service       | Nên tách ra? | Ghi chú               |
| ------------- | ------------ | --------------------- |
| Webserver     | ✅            | Cho UI riêng          |
| Scheduler     | ✅            | Đảm bảo trigger       |
| Worker(s)     | ✅✅✅          | Nên scale             |
| Redis         | ✅            | Broker                |
| PostgreSQL    | ✅            | Metadata DB           |
| Nginx / Proxy | ✅            | TLS, route            |
| Flower        | ✅            | Giám sát task         |
| DAG Storage   | ✅ (optional) | S3/NFS để đồng bộ DAG |

---

## 3. Công cụ production nên dùng

- Docker Compose (dev/staging)
- Kubernetes (Helm chart Airflow)
- AWS ECS / GCP GKE / Azure AKS
- Redis Cluster, PostgreSQL RDS
- Giám sát: Prometheus, Grafana, Sentry

---

## 4. So sánh Docker Compose vs Cài Service Truyền Thống

| Tiêu chí          | Docker Compose   | Cài nhiều service |
| ----------------- | ---------------- | ----------------- |
| Dễ quản lý        | ✅                | ❌                 |
| Backup đơn giản   | ✅ Volume/pg_dump | ❌ Khó hơn         |
| Scale linh hoạt   | ✅ `--scale`      | ❌ Thủ công        |
| Tách biệt service | ✅                | ❌                 |
| Dev → Prod dễ     | ✅ Build/Push/Tag | ❌                 |

---

# [📁 scripts/, nginx.conf & .env Usage](mount_folder.md)

## 1. scripts/

Chứa các shell/Python script hỗ trợ Airflow như:
- `init.sh`: Tạo user, migrate db, khởi tạo lần đầu
- `backup.sh`: Sao lưu dữ liệu PostgreSQL hoặc DAGs
- `restore.sh`: Khôi phục dữ liệu từ bản sao lưu
- `healthcheck.sh`: Kiểm tra tình trạng container
- `generateKey.py`: Sinh key mã hoá, dùng trong DAG

---

## 2. nginx.conf

Cấu hình NGINX làm reverse proxy cho Airflow Webserver:


## 3. File `.env`

Quản lý biến môi trường riêng biệt theo từng máy hoặc môi trường:


---

# [📂 DAGs, Dockerfile, và CI/CD cho Airflow](mount_folder.md)

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

## [2. Lệnh quản lý Airflow (CLI)](Airflow_cli_cmd.md)

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

---

# 🚀 Giao diện Web Airflow – Tổng Quan

Truy cập web UI qua:  
👉 http://localhost:8080 (mặc định)  
Đăng nhập bằng tài khoản bạn đã cấu hình:

```bash
Username: tanp
Password: Abcd1234
```

## Các thành phần chính trên Web UI

| Mục                     | Mô tả                                       |
| ----------------------- | ------------------------------------------- |
| DAGs                    | Danh sách các DAG trong thư mục dags/       |
| Tree View               | Biểu đồ DAG dạng cây theo ngày chạy         |
| Graph View              | DAG hiển thị dạng node – hình dung pipeline |
| Code                    | Xem source code Python của DAG              |
| Trigger DAG             | Kích hoạt DAG thủ công                      |
| Pause/Unpause           | Bật/tắt chạy DAG theo schedule              |
| Admin → Connections     | Quản lý kết nối đến DB, API, SFTP,…         |
| Admin → Variables       | Biến môi trường toàn cục cho DAG            |
| Admin → Pools           | Giới hạn số task chạy song song             |
| Browse → Task Instances | Theo dõi từng lần chạy của task             |
| Browse → Logs           | Xem log task chạy thất bại/thành công       |
| Browse → DAG Runs       | Danh sách các lần chạy của mỗi DAG          |

---

# ☁️📈 Apache Airflow – Tích hợp với Cloud, Datalake & Machine Learning

## 1. Khả năng tích hợp với Databricks, Cloud, Data Lake

Airflow hỗ trợ kết nối và orchestration với các nền tảng cloud/data lake qua providers:

| Dịch vụ      | Mô tả hỗ trợ                        |
| ------------ | ----------------------------------- |
| Databricks   | Hook, operator để submit job lên DB |
| AWS          | S3, EMR, Lambda, ECS, Glue...       |
| GCP          | BigQuery, Cloud Composer, GKE       |
| Azure        | Data Lake, Synapse, ML Service      |
| Snowflake    | Query trực tiếp, run warehouse      |
| HDFS / MinIO | Lưu trữ DAG hoặc batch đầu vào      |

---

## 2. Tích hợp & bổ trợ cho Machine Learning

Airflow là orchestrator tốt cho MLOps pipeline:
- Thu thập dữ liệu
- Tiền xử lý
- Train model
- Evaluate
- Deploy

Dùng tốt với MLflow, Metaflow, TensorFlow, scikit-learn…

Ví dụ:
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

---

## 3. Ưu nhược điểm của Airflow

| Ưu điểm                    | Nhược điểm                             |
| -------------------------- | -------------------------------------- |
| ✅ Quản lý DAG bằng Python  | ❌ Không tối ưu cho real-time streaming |
| ✅ Web UI đẹp, dễ dùng      | ❌ Khởi động chậm nếu DAG lớn           |
| ✅ Hỗ trợ retry, SLA, alert | ❌ Không tốt cho task cực ngắn          |
| ✅ Rất nhiều provider cloud | ❌ Cần cấu hình nhiều nếu dùng K8s      |
| ✅ Orchestrate logic mạnh   | ❌ Không có model registry built-in     |

---

## 4. So sánh với các framework khác

| Tool               | Open Source | Điểm mạnh                  | Yếu điểm / Hạn chế                 |
| ------------------ | ----------- | -------------------------- | ---------------------------------- |
| Airflow            | ✅           | Linh hoạt, phổ biến        | Không real-time                    |
| Prefect            | ✅           | Dễ dùng, DAG như Python    | Giao diện miễn phí còn hạn chế     |
| Dagster            | ✅           | Typed DAG, Data-aware      | Mới hơn, ít cộng đồng hơn          |
| Luigi              | ✅           | Nhẹ, ít phụ thuộc          | Không có web UI, đã cũ             |
| Azure Data Factory | ❌           | Tích hợp Azure tốt         | Không mở rộng, phụ thuộc Microsoft |
| GCP Composer       | ❌           | Quản lý airflow trên cloud | Chi phí cao, ít tuỳ biến           |
| AWS Step Functions | ❌           | Tích hợp Lambda/S3 tốt     | Không viết code thuần Python       |

---

## 5. Đề xuất

| Tình huống                  | Công cụ phù hợp    |
| --------------------------- | ------------------ |
| Xây dựng ETL/ELT + ML       | Airflow            |
| Workflow đơn giản, realtime | Prefect, Dagster   |
| Azure-only                  | Azure Data Factory |
| ML trên GCP                 | Airflow + BigQuery |
| MLOps + UI + Tracking       | Airflow + MLflow   |

---

# 🔄 Airflow + Streaming: Kafka & Giải pháp thay thế

## Vấn đề: Airflow không hỗ trợ Streaming Real-time

Airflow thiết kế cho batch jobs, không phù hợp cho event-driven/streaming real-time như:
- Consume Kafka message mỗi giây
- Trigger DAG khi có dữ liệu đẩy tới
- Xử lý continuous stream từ IoT, logs…

---

## 1. Tích hợp Apache Kafka với Airflow

- Airflow xử lý batch từ Kafka mỗi X phút
- Hoặc Airflow trigger DAG khi detect file/message

Các cách tích hợp:
| Cách                 | Mô tả                                               |
| -------------------- | --------------------------------------------------- |
| Kafka Consumer DAG   | DAG chạy mỗi X phút, dùng hook lấy batch từ Kafka   |
| Sensor + Kafka       | Viết custom sensor, check Kafka message rồi trigger |
| Kafka → HTTP         | Kafka push event đến API để trigger Airflow DAG     |
| Kafka → DB → Airflow | Kafka dump vào DB, Airflow dùng ExternalTaskSensor  |

Ví dụ sử dụng Kafka Hook:
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

---

## 2. Ưu – Nhược khi tích hợp Kafka

| Ưu điểm                         | Nhược điểm                          |
| ------------------------------- | ----------------------------------- |
| ✅ Có thể xử lý event theo batch | ❌ Không phải real-time thực sự      |
| ✅ Tận dụng hệ thống Airflow sẵn | ❌ Không scale tốt theo tốc độ Kafka |
| ✅ Dễ debug với web UI/log       | ❌ Complex nếu dùng sensor liên tục  |

---

## 3. Giải pháp thay thế chuyên dụng streaming

| Công cụ                    | Ưu điểm                                    | Nhược điểm                   |
| -------------------------- | ------------------------------------------ | ---------------------------- |
| Apache Flink               | Stream + batch, mạnh với CEP               | Học hơi khó, JVM-based       |
| Kafka Streams              | Nhẹ, chạy trong microservices Java         | Phụ thuộc Kafka platform     |
| Spark Structured Streaming | Giao diện dễ, scale tốt                    | Delay cao nếu xử lý nhỏ      |
| NiFi                       | GUI luồng dữ liệu trực quan, support Kafka | Tính linh hoạt thấp hơn code |
| Prefect + Kafka            | Event-based DAG hỗ trợ native              | Mới hơn, ít plugin cloud hơn |

---

## 4. Đề xuất

| Mục đích                   | Nên dùng gì             |
| -------------------------- | ----------------------- |
| ETL batch mỗi 15 phút      | Airflow + KafkaConsumer |
| Trigger DAG theo file/data | Airflow + REST API      |
| Streaming real-time mạnh   | Kafka + Flink/Spark     |
| DAG trigger theo event     | Prefect or Dagster      |
| Tích hợp Kafka + tracking  | NiFi + Airflow/Flink    |

---

## Tổng kết

Airflow có thể tương tác với Kafka nhưng không nên dùng cho streaming real-time.  
Nếu workload yêu cầu < 5 phút/dữ liệu – dùng Prefect, Flink hoặc Spark Streaming là lựa chọn tốt hơn.

---

# 📂 Tài liệu tham khảo

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Helm Chart Airflow](https://github.com/apache/airflow/tree/main/chart)
- [📘 Xem tài liệu chi tiết](doc/Guide.md)

---

**✍️ Tác giả:** nptan2005  
**📅 Created Date:** 2025-04-19