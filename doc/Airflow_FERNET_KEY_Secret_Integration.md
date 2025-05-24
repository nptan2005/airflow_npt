
# 🔐 Quản lý FERNET_KEY bảo mật với Vault, AWS Secrets Manager và GCP Secret Manager

## 📌 Mục tiêu

- Quản lý `FERNET_KEY` an toàn, tránh lưu trực tiếp trong mã nguồn.
- Dễ chia sẻ trong nhóm phát triển, không lộ key.
- Tích hợp dễ dàng với Airflow khi deploy lên cloud hoặc môi trường production.

---

## 🔑 1. Với HashiCorp Vault

### ⚙️ Bước 1: Lưu `FERNET_KEY` vào Vault

```bash
vault kv put secret/airflow fernet_key="C1Cg8QaV6rUzSZlQ9OCAFHVv-IWMBQuSvnfcMfnuEAg="
```

### ⚙️ Bước 2: Cấu hình Airflow Docker để lấy key từ Vault

Trong Dockerfile:

```Dockerfile
RUN apt-get update && apt-get install -y curl jq

# Script để đọc FERNET_KEY từ Vault
COPY get_fernet_key.sh /opt/airflow/scripts/get_fernet_key.sh
RUN chmod +x /opt/airflow/scripts/get_fernet_key.sh
```

`get_fernet_key.sh`:

```bash
#!/bin/bash
FERNET_KEY=$(curl -s --header "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/secret/data/airflow | jq -r '.data.data.fernet_key')
export AIRFLOW__CORE__FERNET_KEY=$FERNET_KEY
exec "$@"
```

### ⚙️ Bước 3: Gọi script trong entrypoint
```yaml
entrypoint: ["/opt/airflow/scripts/get_fernet_key.sh"]
```

---

## ☁️ 2. AWS Secrets Manager

### ⚙️ Bước 1: Lưu key

```bash
aws secretsmanager create-secret     --name airflow/fernet_key     --secret-string "C1Cg8QaV6rUzSZlQ9OCAFHVv-IWMBQuSvnfcMfnuEAg="
```

### ⚙️ Bước 2: Lấy FERNET_KEY trong Docker

```bash
FERNET_KEY=$(aws secretsmanager get-secret-value --secret-id airflow/fernet_key --query SecretString --output text)
export AIRFLOW__CORE__FERNET_KEY=$FERNET_KEY
```

Thêm đoạn script trên vào entrypoint hoặc `docker-entrypoint.sh` của bạn.

---

## 🌐 3. Google Cloud Secret Manager

### ⚙️ Bước 1: Lưu secret

```bash
echo -n "C1Cg8QaV6rUzSZlQ9OCAFHVv-IWMBQuSvnfcMfnuEAg=" |   gcloud secrets create airflow-fernet-key --data-file=-
```

### ⚙️ Bước 2: Gán quyền

```bash
gcloud secrets add-iam-policy-binding airflow-fernet-key   --member="serviceAccount:your-service-account@project.iam.gserviceaccount.com"   --role="roles/secretmanager.secretAccessor"
```

### ⚙️ Bước 3: Load trong container

```bash
FERNET_KEY=$(gcloud secrets versions access latest --secret="airflow-fernet-key")
export AIRFLOW__CORE__FERNET_KEY=$FERNET_KEY
```

---

## ✅ Khuyến nghị

- Không commit key vào mã nguồn.
- Dùng `.env` (trong dev), hoặc Secret Manager (prod).
- Tự động hoá load `FERNET_KEY` qua shell script ở `entrypoint`.

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25
