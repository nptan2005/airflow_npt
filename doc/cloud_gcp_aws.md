# ☁️ Hướng dẫn triển khai Airflow trên GCP / AWS

## GCP Composer
1. Tạo Composer Environment (Cloud Composer 2)
2. Upload DAGs vào GCS bucket
3. Sử dụng GCP Secret Manager cho key như `FERNET_KEY`

## AWS MWAA (Managed Workflows for Apache Airflow)
1. Tạo môi trường MWAA
2. Upload DAG vào S3 bucket
3. Config log CloudWatch + IAM Role
4. Sử dụng AWS Parameter Store cho `FERNET_KEY` hoặc secrets

## Cài Docker trên VM riêng (EC2, GCE)
1. Cấu hình HTTPS với Nginx hoặc Load Balancer
2. Dùng Cloud SQL / RDS cho DB
3. Mount volume qua EFS / Filestore

---

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25