# 🔁 Auto Reload DAG & Plugin trong quá trình phát triển

## DAG
DAGs được reload tự động nếu bạn mount volume `./dags:/opt/airflow/dags`

### Đảm bảo config:
```yaml
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: "5"
```
(giá trị nhỏ giúp phát hiện nhanh thay đổi DAG)

## Plugin
Airflow không reload plugin tự động.

### Giải pháp:
1. Mount volume: `./plugins:/opt/airflow/plugins`
2. Restart container `airflow-scheduler` và `airflow-webserver`:
```bash
docker compose restart airflow-scheduler airflow-webserver
```

## Gợi ý dev nhanh hơn:
Dùng lệnh alias:
```bash
alias af-reload='docker compose restart airflow-scheduler airflow-webserver'
```
---


**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25