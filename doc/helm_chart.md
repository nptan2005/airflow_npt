# 📦 Triển khai Apache Airflow với Helm Chart

## 1. Cài đặt Helm:
```bash
brew install helm
# Hoặc:
sudo apt install helm
```

## 2. Add repo Airflow
```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

## 3. Tạo giá trị tùy chỉnh `values.yaml`:
```yaml
executor: CeleryExecutor

dags:
  gitSync:
    enabled: true
    repo: https://github.com/your-org/dags.git

web:
  port: 8080
```

## 4. Cài đặt chart:
```bash
helm upgrade --install airflow apache-airflow/airflow -n airflow --create-namespace -f values.yaml
```

## 5. Xem trạng thái:
```bash
kubectl get pods -n airflow
```

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25