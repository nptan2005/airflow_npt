# Tạo SSL Key dùng cho phát triển (OPEN SSL)

## Bước 1: Tạo private key
### Chạy lệnh sau để tạo một private key:
```bash
openssl genrsa -out private.key 2048
```
## Bước 2: Tạo chứng chỉ tự ký (self-signed certificate)
### Sử dụng private key để tạo chứng chỉ tự ký:
```bash
openssl req -new -x509 -key private.key -out certificate.crt -days 365
```

### Bạn sẽ được yêu cầu nhập các thông tin cơ bản như:

- Country Name (Tên quốc gia, ví dụ: VN)

- State or Province Name (Tên tỉnh, ví dụ: Ho Chi Minh)

- Organization Name (Tên tổ chức, ví dụ: MyCompany)

- Common Name (Tên miền, ví dụ: example.com)

## Bước 3: Kết hợp key và chứng chỉ thành file server.pem
### Ghép private key và chứng chỉ vào một file server.pem:
```bash
cat private.key certificate.crt > server.pem
```

### File server.pem mẫu sẽ trông như sau:
```plaintext
-----BEGIN PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCATsw...
(your private key content here)
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIBqTCCARICAQEwDQYJKoZIhvcNAQELBQAw...
(your certificate content here)
-----END CERTIFICATE-----
```


**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-04-19