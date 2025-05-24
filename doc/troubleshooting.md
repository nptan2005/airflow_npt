---

## 📄 `docs/troubleshooting.md`

```markdown
# Xử lý sự cố Airflow
```

## 1. Lỗi CSRF token khi đăng nhập
```text
Bad Request - The CSRF session token is missing.

```

### Cách khắc phục:
	•	Truy cập đúng domain (không nên dùng IP trực tiếp nếu dùng HTTPS + Cookie Secure)
	•	Nếu dùng nginx/haproxy, đảm bảo X-Forwarded-* headers được pass qua
	•	Kiểm tra .env có AIRFLOW__WEBSERVER__COOKIE_SECURE=False nếu không dùng HTTPS

## 2. Lỗi không tìm thấy logging config

```text
ImportError: Unable to load custom logging from config.airflow_local_settings.LOGGING_CONFIG
```

### Nguyên nhân:
	•	Module config chưa có __init__.py
	•	PYTHONPATH chưa bao gồm /opt/airflow/config

### Khắc phục:

```python
# Tạo file __init__.py
touch config/__init__.py
```

