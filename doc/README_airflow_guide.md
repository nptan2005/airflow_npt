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

## ⚙️ Công cụ production nên dùng:

- ✅ Docker Compose (dev/staging)
- ✅ Kubernetes (Helm chart Airflow)
- ✅ AWS ECS / GCP GKE / Azure AKS
- ✅ Redis Cluster, PostgreSQL RDS
- ✅ Giám sát: Prometheus, Grafana, Sentry

---

## 🧠 So sánh Docker Compose vs Cài Service Truyền Thống

| Tiêu chí          | Docker Compose   | Cài nhiều service |
| ----------------- | ---------------- | ----------------- |
| Dễ quản lý        | ✅                | ❌                 |
| Backup đơn giản   | ✅ Volume/pg_dump | ❌ Khó hơn         |
| Scale linh hoạt   | ✅ `--scale`      | ❌ Thủ công        |
| Tách biệt service | ✅                | ❌                 |
| Dev → Prod dễ     | ✅ Build/Push/Tag | ❌                 |

---

## ✅ Tag và Push Image

```bash
docker tag airflow-nptan:1.0.0 your_dockerhub_user/airflow-nptan:1.0.0
docker push your_dockerhub_user/airflow-nptan:1.0.0
```

---

## 📂 Tài liệu khác

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Helm Chart Airflow](https://github.com/apache/airflow/tree/main/chart)

---

**✍️ Tác giả:** nptan2005   
**📅 Created:** 2025-04-19
