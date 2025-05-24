# Triển khai Production với Apache Airflow

## 1. Kiến trúc triển khai Production (gợi ý)
	•	Airflow chạy bằng Docker Compose hoặc Kubernetes
	•	Sử dụng CeleryExecutor / KubernetesExecutor
	•	Tách biệt từng service:
	•	Webserver
	•	Scheduler
	•	Worker
	•	Flower
	•	PostgreSQL / Redis / MinIO (nếu có)
	•	Reverse proxy (nginx / haproxy)
	•	Backup volume định kỳ
	•	Giám sát bằng Prometheus, Grafana

## 2. GitHub Actions CI/CD Workflow (Gợi ý đơn giản)
```yaml
name: Airflow CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r airflow.requirements.txt

      - name: Lint code
        run: |
          pip install flake8
          flake8 dags plugins

      - name: Run tests (nếu có)
        run: |
          pytest tests/
```
## 3. Auto Reload DAGs / Plugins khi phát triển

### Cách 1: Mount volume vào container
```yaml
volumes:
  - ./dags:/opt/airflow/dags
  - ./plugins:/opt/airflow/plugins
```
### Cách 2: Restart container khi cần (plugin mới)
```bash
docker compose restart airflow-webserver airflow-scheduler
```
### Cách 3: Sử dụng watcher
```bash
watchmedo auto-restart --directory=dags/ --pattern=*.py --recursive -- airflow scheduler
```
## 4. Production best practices
	•	Luôn dùng CeleryExecutor (hoặc KubernetesExecutor)
	•	Không mount source code trực tiếp khi production
	•	Đóng gói DAG/plugin vào image để build
	•	Sử dụng secrets (Vault, AWS Secret Manager…) cho FERNET_KEY và mật khẩu
	•	Luôn backup volume (Postgres, logs, etc)
	•	Log gửi về các hệ thống tập trung như Elasticsearch, Loki
	•	Tách biệt image dev/prod

⸻

Có thể tạo thêm file .env.prod, .env.dev và dùng docker compose --env-file để chạy theo môi trường.
```bash
docker compose --env-file .env.prod up -d
```


**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25