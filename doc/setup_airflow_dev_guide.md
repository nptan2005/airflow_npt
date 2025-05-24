# Hướng dẫn thiết lập môi trường Airflow cho phát triển

## 1. Yêu cầu
- Docker + Docker Compose
- Python 3.12 (chỉ dùng để chạy lệnh bên ngoài container nếu cần)
- Hệ điều hành: macOS/Linux

## 2. Khởi tạo
```bash
# Clone source
git clone https://github.com/nptan2005/airflow_npt
cd airflow_npt


# Tạo virtualenv nếu cần
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 3. Tạo .env

```bash
cp .env.example .env
# Cập nhật các biến như FERNET_KEY, cấu hình resource...
```
## 4. Build image & Start container

```bash
docker-compose build
docker-compose up -d
```

## 4. Build image & Start container

```bash
docker-compose build
docker-compose up -d
```

## 5. Truy cập UI
	•	Web UI: http://localhost:8080
	•	Flower: http://localhost:5555