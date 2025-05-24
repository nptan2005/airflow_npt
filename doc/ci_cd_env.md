# 🚀 CI/CD nâng cao theo môi trường

## 1. Cấu trúc repo đề xuất:
```
.github/workflows/
    dev.yml
    staging.yml
    prod.yml

environments/
    dev/.env
    staging/.env
    prod/.env
```

## 2. GitHub Action mẫu
```yaml
name: Deploy to Dev

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker compose -f docker-compose.yml --env-file environments/dev/.env up -d --build
```

## 3. Biến môi trường riêng theo env
Sử dụng biến môi trường `.env` khác nhau:
- `dev/.env`
- `prod/.env`

Bạn có thể dùng lệnh:
```bash
docker compose --env-file environments/dev/.env up
```

---

**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25