# 🚀 Airflow Project Guide

## Mục lục
- [Thiết lập biến môi trường](#thiết-lập-biến-môi-trường)
- [Đăng nhập Web UI](#đăng-nhập-web-ui)
- [Kích hoạt môi trường ảo](#kích-hoạt-môi-trường-ảo)
- [Cấu hình tên images](#cấu-hình-tên-images)
- [Docker Commands](#docker-commands)
- [Kiểm tra trạng thái container & service](#kiểm-tra-trạng-thái-container--service)
- [Kiểm tra cơ sở dữ liệu PostgreSQL](#kiểm-tra-cơ-sở-dữ-liệu-postgresql)
- [Kiểm tra và xử lý mạng](#kiểm-tra-và-xử-lý-mạng)
- [Các lệnh Docker phổ biến](#các-lệnh-docker-phổ-biến)
- [Các tuỳ chọn hữu ích cho docker run](#các-tuỳ-chọn-hữu-ích-cho-docker-run)
- [Git Commands](#git-commands)
- [Tạo file .env theo hệ điều hành](#tạo-file-env-theo-hệ-điều-hành)
- [Backup/Restore Database](#backuprestore-database)
- [Xoá image rác (None)](#xoá-image-rác-none)
- [Sinh fernet_key cho Airflow](#sinh-fernet_key-cho-airflow)
- [Tạo chứng chỉ tự ký (SSL)](#tạo-chứng-chỉ-tự-ký-ssl)

# 📚 Airflow Project Documentation

## 📌 Tổng quan & Hướng dẫn

- [📖 Tổng quan Airflow](README_overview_airflow.md)
- [🛠️ Hướng dẫn sử dụng Airflow](README_airflow_guide.md)
- [🔌 Topology & CICD](README_airflow_topology_cicd.md)
- [🧱 DAGs, Dockerfile & CI/CD](README_dags_dockerfile_cicd.md)
- [⚙️ Scripts, ENV & NGINX](README_scripts_env_nginx.md)
- [⚙️ Hướng dẫn thiết lập môi trường Airflow cho phát triển](setup_airflow_dev_guide.md)
- [📘 Airflow Production & Development Setup Guide](docs/Airflow_Production_and_Development_Setup_Guide.md)
- [📁 scripts/, nginx.conf & .env Usage (mount folder)](mount_folder.md)

## CMD/CLI
- [🛠 Lệnh quản lý Airflow (CLI)](Airflow_cli_cmd.md)

## 🔐 FERNET Key & Bảo mật

- [🔑 Hướng dẫn tạo FERNET Key](Airflow_FERNET_KEY_Guide.md)
- [🔐 Tích hợp FERNET vào Secret Manager](Airflow_FERNET_KEY_Secret_Integration.md)

## 🚀 CI/CD & Triển khai

- [🎯 CI/CD theo môi trường](ci_cd_env.md)
- [🚀 Auto reload DAG & Plugin dev](auto_reload_dev.md)
- [🚢 Production CI/CD Reload](Airflow_Prod_Ci_Reload.md)
- [🔐 CICD & Secret Integration](Airflow_CICD_Secrets_Integration.md)
- [🔁 CI/CD mẫu với GitHub Actions](ci_cd_template_withGithud.md)
- [Secrets CI/CD cần thiết](Secrets_CI_CD_need.md)

## ☁️ Cloud & Observability

- [🌐 Cloud GCP & AWS Integration](cloud_gcp_aws.md)
- [📈 Kết nối Prometheus/Grafana](prometheus_grafana.md)

## 🧪 Logging & Config

- [🧰 Thiết lập Logging nâng cao](setup_airflow_logging_config.md)
- [🔧 Fix lỗi config logging module](fix_logging_config_module_not_found.md)
- [🐞 Fix lỗi snapshot Docker layer](fix-docker-snapshot-error.md)
- [🔁 Config & Khởi động lại service](config_and_restart.md)

## 📦 Helm & SSL

- [⛵ Cấu hình Helm Chart](helm_chart.md)
- [🔐 Cấu hình SSL/HTTPS với OpenSSL](SSL_OpenSSL.md)

## ✅ Thủ thuật
- [Tự động reload DAGs/Plugin khi phát triển](plugin_reload_dev.md)
- [Hướng Dẫn Xử Lý Lỗi Airflow Init, Logging và FERNET_KEY](airflow_logging_fernet_guide.md)

## Troubleshooting
- [🔧 troubleshooting](troubleshooting.md)


## 📂 Tổng hợp (Index)

- [📋 Guide tổng hợp](Guide.md)
---

## Thiết lập biến môi trường

```powershell
$env:AIRFLOW_HOME="D:\WorkSpace\Python\airflow-project"
```

---

## Đăng nhập Web UI

- URL: [http://localhost:8080/login](http://localhost:8080/login)
- Username: `tanp`
- Password: `Abcd1234`

---

## Kích hoạt môi trường ảo

- **Windows:**
    ```bash
    env\Scripts\activate
    ```
- **macOS/Linux (dùng venv):**
    ```bash
    source venv/bin/activate
    ```
- **macOS/Linux (dùng conda):**
    ```bash
    conda activate airflow_env
    ```

---

## Cấu hình tên images

**Ví dụ:** airflow-nptan:1.0.0 trong `docker-compose.yml`

**Mục tiêu:**
- ✅ Build image có tên: `airflow-nptan:1.0.0`
- ✅ Các service Airflow (webserver, scheduler, worker,…) đều dùng chung image này
- ✅ Giảm size & số lượng image trong docker images

**Chỉnh trong phần `x-airflow-common`:**
```yaml
x-airflow-common:
  &airflow-common
  image: airflow-nptan:1.0.0  # 👈 Tên image mong muốn
  build:
    context: .
    dockerfile: ./airflow.Dockerfile
```

**Dọn dẹp Docker:**
```bash
docker system prune -f  # Xoá toàn bộ container, network, image không dùng
```

---

## 🐳 Docker Commands

### A. Build image
```bash
docker compose build
```

### B. Khởi chạy container
```bash
docker compose up -d
```
>>> kiểm tra log sau khi build

```bash
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler
```


### C. Dừng container
```bash
docker compose down
```

### D. Xoá volume database
```bash
docker volume rm postgres-db-volume
```

### E. Dừng container và xoá volume
```bash
docker compose down -v
```

### F. Khởi tạo Airflow lần đầu
```bash
docker compose up airflow-init
```

### G. Tạo mạng Docker bridge
```bash
docker network create --driver=bridge airflow-external-bridge
```

### H. Truy cập vào container (scheduler)
```bash
docker exec -it airflow-project-airflow-scheduler-1 bash
```

### I. Xoá các images airflow cũ

```bash
docker rmi airflow_bvb-airflow-webserver \
           airflow_bvb-airflow-scheduler \
           airflow_bvb-airflow-worker \
           airflow_bvb-airflow-init \
           airflow_bvb-flower
```

## Fix "image already exists"

###  Truy dấu container/image đang giữ tag

```bash
docker images | grep airflow-nptan
docker ps -a | grep airflow
```

### I (*) 🔥 Lệnh xóa sạch dữ liệu Và build lại

```bash
# Dừng và xóa toàn bộ container, volume
docker compose down -v --remove-orphans

# (Tuỳ chọn) Xóa image nếu muốn build lại từ đầu
docker image rm airflow-nptan:1.0.0

# Sau đó rebuild
docker compose build --no-cache
docker compose up -d
```

### I (**) 📌 Nếu chỉ muốn xóa riêng volume PostgreSQL 

```bash
docker volume rm airflow_npt_postgres-db-volume
```
Kiểm tra

```bash
docker volume ls
```
### 🔥 I (***): Xoá cache build (rất quan trọng):

```bash
docker builder prune -a
```
### ⛔️ Cảnh báo: Lệnh này sẽ xoá toàn bộ cache build của Docker, nên cần xác nhận bằng y.

--

Stop
```bash
docker stop $(docker ps -q)
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
Láy địa chỉ IP

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_postgres_name>
```

### access db

```bash
psql -U airflow -d airflow
```
---

## Tạo schema task_flow for plugin

### 🔹 1. Kiểm tra xem schema đã được tạo chưa
```sql
SELECT schema_name FROM information_schema.schemata;
```
📌 Nếu task_flow không xuất hiện, có thể lệnh CREATE SCHEMA đã bị lỗi hoặc chưa được thực thi đúng.

### 🔹 2. Kiểm tra quyền trên PostgreSQL
Một số tài khoản PostgreSQL không có quyền tạo schema. Hãy kiểm tra bằng:
```sql
SHOW ROLE;
```
📌 Nếu bạn không phải là superuser, cần cấp quyền:
```sql
GRANT CREATE ON DATABASE airflow TO airflow;
```
Chạy lệnh:
```sql
CREATE SCHEMA task_flow;
```

### 🔹 3. Kiểm tra lỗi khi tạo schema
Nếu schema không được tạo, hãy kiểm tra lỗi bằng:
```sql
SELECT * FROM pg_catalog.pg_namespace;
```
📌 Nếu có lỗi liên quan đến quyền hoặc xung đột với schema cũ, cần kiểm tra log PostgreSQL.


## Kiểm tra init

```bash
docker logs airflow_npt-airflow-init-1
```

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

---

# 🐳 Các lệnh Docker phổ biến

### `docker ps`
Liệt kê các container đang chạy.
- `-a`: Hiển thị tất cả container (đang chạy và đã dừng)
- `-q`: Chỉ hiện ID của container

### `docker pull`
Tải một image từ Docker Hub.
```bash
docker pull nginx
docker pull mysql
```

### `docker build`
Build một image từ Dockerfile.
```bash
docker build -t your_name_container .
```

### `docker run`
Chạy container từ image có sẵn.
```bash
docker run -it image_name bash
```

### `docker logs`
Xem log từ container.
```bash
docker logs --follow your_name_container
```

### `docker volume ls`
Liệt kê các volume được sử dụng bởi Docker.

### `docker rm`
Xóa một hoặc nhiều container.
```bash
docker rm <container_id_or_name>
```

### `docker rmi`
Xóa một hoặc nhiều image.
```bash
docker rmi <image_id>
```

### `docker stop`
Dừng một hoặc nhiều container.
```bash
docker stop <container_id_or_name>
```
Bạn cũng có thể dùng `docker kill` để buộc dừng container.

---

## ⚙️ Các tuỳ chọn hữu ích cho `docker run`

- `-d`, `--detach`: Chạy container ngầm
- `--entrypoint`: Ghi đè lệnh mặc định trong image
- `-e`, `--env`: Thiết lập biến môi trường (key=value)
- `--env-file`: Truyền biến môi trường từ file
- `--ip`: Gán địa chỉ IP cho container
- `--name`: Đặt tên cho container
- `-p`, `--publish`: Ánh xạ cổng container với host (VD: `-p 80:80`)
- `-P`, `--publish-all`: Mở tất cả các cổng
- `--rm`: Xóa container sau khi thoát
- `-t`, `--tty`: Gán terminal ảo
- `-i`, `--interactive`: Mở STDIN
- `-v`, `--volume`: Gắn volume vào container
    ```bash
    docker run --volume /volume_name image_name bash
    ```
- `-w`, `--workdir`: Chỉ định thư mục làm việc trong container
    ```bash
    docker run --workdir /app image_name bash
    ```

---

## 🧩 Git Commands

### Các lệnh cơ bản
```bash
git status
git add .
git add <file_name>
git commit -m "Mô tả chi tiết về thay đổi"
git push origin <branch_name>
```

### Cấu hình Git ban đầu
```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
git remote add origin <url_repository_git>
```

---

## Tạo file .env theo hệ điều hành

### macOS
```bash
cp .env.mac .env
```

### Windows (PowerShell)
```powershell
Copy-Item .env.windows -Destination .env
```

---

## Backup/Restore Database

### Backup dữ liệu database PostgreSQL từ container
```bash
docker exec -t airflow-project-postgres-1 \
  pg_dump -U airflow -d airflow > ./db_backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### Lưu database bên ngoài để không mất dữ liệu khi build lại
```bash
mkdir -p ./pgdata
```
Trong docker-compose:
```yaml
volumes:
  - ./pgdata:/var/lib/postgresql/data
```

### Backup volume data PostgreSQL ra ngoài (export volume ra .tar)
```bash
docker run --rm \
  -v airflow_bvb_postgres-db-volume:/volume \
  -v $(pwd)/db_backup:/backup \
  alpine \
  tar czf /backup/postgres_data_backup.tar.gz -C /volume .
```

### Restore volume trên máy dev khác
```bash
# Tạo volume mới (nếu chưa có)
docker volume create airflow_bvb_postgres-db-volume

# Restore vào volume mới
docker run --rm \
  -v airflow_bvb_postgres-db-volume:/volume \
  -v $(pwd)/db_backup:/backup \
  alpine \
  tar xzf /backup/postgres_data_backup.tar.gz -C /volume
```

---

## Xoá image rác (None)

### Xoá các images <none> (dangling images)
```bash
docker rmi $(docker images -f "dangling=true" -q) --force
```

### Xoá toàn bộ images không cần thiết (unused images)
```bash
docker image prune --all --force
```

### Tag lại image nếu cần giữ
```bash
docker tag <IMAGE_ID> <REPOSITORY>:<TAG>
# Ví dụ:
docker tag e6f415a2ae43 airflow-custom:latest
```

### Hạn chế tạo dangling images khi build
```bash
docker build -t my-image:latest .
```

---

## Sinh fernet_key cho Airflow

⚠️ Trên `airflow.cfg`, nếu `fernet_key` để trống, hãy sinh một khoá mới:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Tạo chứng chỉ tự ký (self-signed SSL)

```bash
mkdir -p nginx/ssl

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ./nginx/ssl/localhost.key \
  -out ./nginx/ssl/localhost.crt \
  -subj "/C=VN/ST=Dev/L=Localhost/O=MyCompany/OU=Dev/CN=localhost"
```

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-04-19