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

| Thành phần               | Vai trò                     |
| ------------------------ | --------------------------- |
| **GitHub CI/CD**         | Kiểm thử, build, push image |
| **Docker Compose / K8s** | Triển khai Airflow stack    |
| **Nginx proxy**          | Reverse proxy, SSL          |
| **Webserver**            | Giao diện quản trị          |
| **Scheduler**            | Lập lịch DAG                |
| **Worker(s)**            | Thực thi task (scale)       |
| **Redis**                | Queue broker                |
| **PostgreSQL**           | Lưu trạng thái DAG/task     |

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

| Tên biến      | Mô tả                     |
| ------------- | ------------------------- |
| `DOCKER_USER` | Docker Hub username       |
| `DOCKER_PASS` | Docker Hub password/token |
| `SSH_KEY`     | Private key deploy server |
| `HOST`        | IP/FQDN của máy chủ       |
| `USER`        | User SSH                  |

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

---

**✍️ Tác giả:** nptan2005  
**📅 Created:** 2025-04-19
