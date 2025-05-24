# Hướng dẫn thay đổi config khi dev với Airflow + Docker Compose

## 1. Thay đổi config trong container

### a. Hiệu chỉnh trực tiếp trong container
	1.	Vào container:
```bash
docker exec -it <container_name> /bin/bash
```
	2.	Chẳng hạn:
```bash
vi /opt/airflow/config/airflow.cfg
```
	3.	Restart service:
```bash
docker restart <container_name>
```
### b. Hiệu chỉnh config file không build lại
	•	Airflow đã mount volume:
```yaml
volumes:
  - ./config:/opt/airflow/config
```
	•	Chỉ cần sửa file local, sau đó restart container:

docker-compose restart airflow-webserver

## 2. Thay đổi config HAProxy, NGINX

### a. HAProxy
	•	File mount:
```bash
volumes:
  - ./haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
```
	•	Bước:
```bash
nano ./haproxy/haproxy.cfg
```
	•	Restart:
```bash
docker-compose restart haproxy
```
### b. NGINX
	•	File mount:
```yaml
volumes:
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
```
	•	Restart:
```bash
docker-compose restart acess-host-proxy
```
## 3. Khi tạo plugin mới
	•	Airflow mount plugins:
```yaml
volumes:
  - ./plugins:/opt/airflow/plugins
```
	•	Sau khi tạo file plugin python mới:
```bash
nano plugins/my_plugin.py
```
	•	Chỉ cần restart webserver + scheduler (ko rebuild image):
```bash
docker-compose restart airflow-webserver airflow-scheduler
```
## 4. Thay đổi cấu hình airflow

### a. airflow.cfg
	•	Đã mount:
```yaml
volumes:
  - ./config:/opt/airflow/config
```
	•	Sửa config/airflow.cfg hoặc set biến ENV trong docker-compose.yml

### b. .env file
	•	Thay đổi file .env:
```bash
nano .env
```
	•	Sau đó:
```bash
docker-compose down
docker-compose up -d
```
## 5. Thay đổi logging
	•	File logging:
```bash
config/airflow_local_settings.py
```
	•	Ensure:
```yaml
environment:
  AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS: config.airflow_local_settings.LOGGING_CONFIG
```
	•	Sau khi thay đổi:
```bash
docker-compose restart airflow-webserver airflow-scheduler airflow-worker
```

⸻

## Ghi nhớ:
	•	Không cần rebuild image khi thay đổi file mount (plugins, config, .env, logging)
	•	Cần rebuild image khi thay Dockerfile, poetry.lock, airflow.requirements.txt
```bash
docker-compose build
```

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25