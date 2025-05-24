# 🛠 README: Scripts, nginx.conf & .env Usage

## 📁 1. scripts/

Thư mục `scripts/` thường chứa các file shell hoặc Python hỗ trợ hệ thống Airflow như:

| Script           | Mục đích                               |
| ---------------- | -------------------------------------- |
| `init.sh`        | Tạo user, migrate db, khởi tạo lần đầu |
| `backup.sh`      | Sao lưu dữ liệu PostgreSQL hoặc DAGs   |
| `restore.sh`     | Khôi phục dữ liệu từ bản sao lưu       |
| `healthcheck.sh` | Dùng để kiểm tra tình trạng container  |
| `generateKey.py` | Sinh key mã hoá, dùng trong DAG        |

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

| Thành phần | Vai trò                     | Khuyến nghị               |
| ---------- | --------------------------- | ------------------------- |
| scripts/   | Tự động hóa quản lý Airflow | Tách biệt logic rõ ràng   |
| nginx.conf | Reverse proxy + SSL         | Mount vào container       |
| .env       | Biến môi trường cấu hình    | Dùng theo từng môi trường |

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-04-19
