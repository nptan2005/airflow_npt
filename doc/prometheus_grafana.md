# 📊 Tích hợp Prometheus & Grafana với Apache Airflow

## 1. Cài Prometheus Exporter
Sử dụng `prometheus_flask_exporter`:

```bash
pip install prometheus_flask_exporter
```

## 2. Thêm vào `airflow_local_settings.py`
```python
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
metrics = GunicornPrometheusMetrics(app)
```

## 3. Cập nhật Prometheus config
```yaml
scrape_configs:
  - job_name: 'airflow'
    static_configs:
      - targets: ['airflow-webserver:8080']
```

## 4. Import Dashboard Airflow (Grafana)
- Truy cập Grafana
- Import dashboard ID: **10667** (Apache Airflow)

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25