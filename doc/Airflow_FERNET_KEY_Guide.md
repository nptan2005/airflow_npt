
# 🔐 Apache Airflow – FERNET_KEY Guide

## 1. FERNET_KEY là gì?

FERNET_KEY là khoá bí mật dùng bởi **Apache Airflow** để:
- Mã hoá/giải mã thông tin nhạy cảm như:
  - XCom
  - Connection password
  - Variable bí mật

---

## 2. Thuật toán mã hoá được sử dụng

Airflow sử dụng thư viện `cryptography.fernet.Fernet` (tuân theo [RFC 7519](https://tools.ietf.org/html/rfc7519)):

- **Thuật toán:** AES 128-bit (CBC mode) + HMAC SHA256
- **Key size:** 32 bytes (256-bit) được base64-encoded
- **Ví dụ key:** `C1Cg8QaV6rUzSZlQ9OCAFHVv-IWMBQuSvnfcMfnuEAg=`

> 📌 Mặc định Airflow **chỉ hỗ trợ Fernet**. Không hỗ trợ cấu hình AES-256 hay các thuật toán khác.

---

## 3. Có thể thay thế bằng AES-256 không?

Không trực tiếp.

- Airflow không cho phép cấu hình thuật toán mã hoá thay thế.
- Có thể tuỳ chỉnh mã hoá riêng qua:
  - Custom XCom backend
  - Custom connection class

⚠️ Tuy nhiên điều này yêu cầu override core hoặc viết plugin → **không khuyến khích nếu không cần thiết**.

---

## 4. Quản lý `FERNET_KEY` theo nhóm/dev team

### Cách 1: Dùng `.env` được đồng bộ
- Lưu `.env` vào Git hoặc chia sẻ qua file riêng.
- Sử dụng qua Docker Compose:

```bash
docker compose --env-file .env up -d
```

### Cách 2: Dùng Secret Manager (AWS/GCP/Vault)

#### AWS Secrets Manager

```bash
export FERNET_KEY=$(aws secretsmanager get-secret-value   --secret-id airflow/fernet_key   --query SecretString --output text)
```

#### GCP Secret Manager

```bash
export FERNET_KEY=$(gcloud secrets versions access latest   --secret="airflow-fernet")
```

#### Vault by HashiCorp

- Sử dụng bằng Env Injector hoặc Sidecar Container.
- Đặt key tại path `secret/data/airflow/fernet_key`

---

## 5. Tạo FERNET_KEY

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 6. Lưu ý khi dùng

- Key nên được tạo 1 lần duy nhất và giữ nguyên.
- Nếu thay đổi key giữa chừng → cần reset database hoặc sẽ lỗi giải mã.
- FERNET_KEY nên được đồng bộ giữa các môi trường staging, dev, prod nếu dùng chung DB.

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25
