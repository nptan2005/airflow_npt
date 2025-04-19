# 🚀 Airflow Project Guide

## 🌍 Environment Setup

### 1. Thiết lập biến môi trường

```powershell
$env:AIRFLOW_HOME="D:\WorkSpace\Python\airflow-project"
```

---

## 🔐 Đăng nhập Web UI

- URL: [http://localhost:8080/login](http://localhost:8080/login)
- Username: `tanp`
- Password: `Vccb1234`

---

## 💻 Kích hoạt môi trường ảo

- **Windows:**

```bash
env\Scripts\activate
```

- **macOS:**

```bash
conda activate ./venv
```

## Cấu hình tên images

#### * Cách cấu hình image: Ví du: airflow-nptan:1.0.0 trong docker-compose.yml*
####🎯 Mục tiêu:
	*	✅ Build image có tên: airflow-nptan:1.0.0
	*	✅ Các service Airflow (webserver, scheduler, worker,…) đều dùng chung image này
	*	✅ Giảm size & số lượng image trong docker images
### ✅ A. Gán image: trong x-airflow-common:

- *Trong phần x-airflow-common, chỉnh:*
```yaml
x-airflow-common:
  &airflow-common
  image: airflow-nptan:1.0.0  # 👈 Đây là tên image bạn muốn
  build:
    context: .
    dockerfile: ./airflow.Dockerfile
```

## 🐳 Docker Commands

### A. Build:
```bash
docker compose build
```

> (Chưa có lệnh cụ thể – bạn có thể bổ sung nếu cần)

### B. Khởi chạy container

```bash
docker compose up -d
```

### C. Dừng container

```bash
docker compose down
```

##### Remove volumn

```bash
docker volume rm postgres-db-volume
```

##### down container và xoá volumn

```base
docker compose down -v
```

### D. Khởi tạo Airflow lần đầu

```bash
docker-compose up airflow-init
```

### E. Tạo mạng Docker bridge

```bash
docker network create --driver=bridge airflow-external-bridge
```

### F. Truy cập vào container (scheduler)

```bash
docker exec -it airflow-project-airflow-scheduler-1 bash
```

### G. Clear up images:

```bash
docker rmi airflow_bvb-airflow-webserver \
           airflow_bvb-airflow-scheduler \
           airflow_bvb-airflow-worker \
           airflow_bvb-airflow-init \
           airflow_bvb-flower
```

---

## 🧪 Kiểm tra trạng thái container & service

### Liệt kê container

```bash
docker ps -a
```

### Kiểm tra logs webserver

```bash
docker logs airflow-project-airflow-webserver-1
```

---

## 🗄️ Kiểm tra cơ sở dữ liệu PostgreSQL

```bash
docker exec -it airflow-project-postgres-1 \
  psql -U airflow -d airflow -c '\l'
```

---

## 🌐 Kiểm tra và xử lý mạng

### Inspect network

```bash
docker network inspect airflow-project_default
```

### Ping IP từ container

```bash
docker exec -it airflow-project-airflow-webserver-1 ping 172.26.1.32
```

### SSH & mở cổng truy cập database

```bash
ssh airflow@172.26.1.32
sudo ufw allow from 172.26.0.0/16 to any port 5432
netstat -tuln | grep 5432
```

### Dọn dẹp network không dùng

```bash
docker network prune
```

### Chạy Airflow webserver dưới dạng background

```bash
airflow webserver -d
```



# 🐳 Docker Commands & Useful Options

## 📌 Commonly Used Docker Commands

### 🔍 `docker ps`
Liệt kê các container đang chạy.

**Tùy chọn**:
- `-a`, `--all`: Hiển thị tất cả container (đang chạy và đã dừng).
- `-q`, `--quiet`: Chỉ hiện ID của container.

---

### 📥 `docker pull`
Tải một image từ Docker Hub.

**Ví dụ**:
```bash
docker pull nginx
docker pull mysql
```

---

### 🛠️ `docker build`
Build một image từ Dockerfile.

**Ví dụ**:
```bash
docker build -t your_name_container .
```

---

### 🚀 `docker run`
Chạy container từ image có sẵn.

**Ví dụ**:
```bash
docker run image_name -it bash
```

---

### 📄 `docker logs`
Xem log từ container.

**Ví dụ**:
```bash
docker logs --follow your_name_container
```

---

### 💾 `docker volume ls`
Liệt kê các volume được sử dụng bởi Docker.

---

### 🗑️ `docker rm`
Xóa một hoặc nhiều container.

**Ví dụ**:
```bash
docker rm <container_id_or_name>
```

---

### 🗑️ `docker rmi`
Xóa một hoặc nhiều image.

**Ví dụ**:
```bash
docker rmi <image_id>
```

---

### ⛔ `docker stop`
Dừng một hoặc nhiều container.

**Ví dụ**:
```bash
docker stop <container_id_or_name>
```

Bạn cũng có thể dùng `docker kill` để buộc dừng container.

---

## ⚙️ Useful Options for `docker run`

- `--detach`, `-d`: Chạy container ngầm.
- `--entrypoint`: Ghi đè lệnh mặc định trong image.
- `--env`, `-e`: Thiết lập biến môi trường (key=value).
- `--env-file`: Truyền biến môi trường từ file.
- `--ip`: Gán địa chỉ IP cho container.
- `--name`: Đặt tên cho container.
- `--publish`, `-p`: Ánh xạ cổng container với host (VD: `-p 80:80`).
- `--publish-all`, `-P`: Mở tất cả các cổng.
- `--rm`: Xóa container sau khi thoát.
- `--tty`, `-t`: Gán terminal ảo.
- `--interactive`, `-i`: Mở STDIN.
- `--volume`, `-v`: Gắn volume vào container.

```bash
docker run --volume /volume_name image_name bash
```

- `--workdir`, `-w`: Chỉ định thư mục làm việc trong container.

```bash
docker run --workdir /app image_name bash
```



---

## 🧩 Git Commands

### A. Các lệnh cơ bản

```bash
git status
git add .
git add <file_name>
git commit -m "Mô tả chi tiết về thay đổi"
git push origin <branch_name>
```

### B. Cấu hình Git ban đầu

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
git remote add origin <url_repository_git>
```

---

## 🔗 Tạo file .env theo hệ điều hành

### macOS

```bash
cp .env.mac .env
```

### Windows (PowerShell)

```powershell
Copy-Item .env.windows -Destination .env
```

### Backup dữ liệu database postgre - container 

```bash
docker exec -t airflow-project-postgres-1 \
  pg_dump -U airflow -d airflow > ./db_backups/backup_$(date +%Y%m%d_%H%M%S).sql
```


### Trường hợp muốn lưu database bên ngoài để ko mất dữ liệu mỗi khi build

```base
mkdir -p ./pgdata
```

```powershell
volumes:
  - ./pgdata:/var/lib/postgresql/data
```

### Backup volumn data postgre ra ngoài
#####📦 1. Export volume ra .tar:
```base
docker run --rm \
  -v airflow_bvb_postgres-db-volume:/volume \
  -v $(pwd)/db_backup:/backup \
  alpine \
  tar czf /backup/postgres_data_backup.tar.gz -C /volume .
```
#####🔁 3. Restore trên máy dev khác:

```base
# Tạo volume mới (nếu chưa có)
docker volume create airflow_bvb_postgres-db-volume

# Restore vào volume mới
docker run --rm \
  -v airflow_bvb_postgres-db-volume:/volume \
  -v $(pwd)/db_backup:/backup \
  alpine \
  tar xzf /backup/postgres_data_backup.tar.gz -C /volume
```