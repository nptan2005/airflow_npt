# Tích Hợp Airflow Với CI/CD, Google KMS, Azure Key Vault và Auto-sync `.env`

## 1. CI/CD (GitHub Actions, GitLab CI)

### GitHub Actions - Ví dụ:
```yaml
name: Airflow CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      FERNET_KEY: ${{ secrets.FERNET_KEY }}
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t airflow-custom .
```

### GitLab CI/CD
```yaml
stages:
  - build

variables:
  FERNET_KEY: $FERNET_KEY

build:
  stage: build
  script:
    - docker build -t airflow-custom .
```

## 2. Google Cloud KMS

### Tạo KeyRing và CryptoKey
```bash
gcloud kms keyrings create airflow-keyring --location=global
gcloud kms keys create fernet-key \
  --location=global \
  --keyring=airflow-keyring \
  --purpose=encryption
```

### Mã hoá key:
```bash
echo -n "$FERNET_KEY" | gcloud kms encrypt \
  --keyring=airflow-keyring \
  --location=global \
  --key=fernet-key \
  --plaintext-file=- \
  --ciphertext-file=fernet-key.enc
```

### Giải mã để sử dụng (runtime):
```bash
gcloud kms decrypt \
  --keyring=airflow-keyring \
  --location=global \
  --key=fernet-key \
  --ciphertext-file=fernet-key.enc \
  --plaintext-file=-
```

## 3. Azure Key Vault
```bash
az keyvault create --name airflow-vault --resource-group airflow-rg --location eastus
az keyvault secret set --vault-name airflow-vault --name FERNET_KEY --value <your_fernet_key>
az keyvault secret show --name FERNET_KEY --vault-name airflow-vault --query value -o tsv
```

## 4. Auto-sync `.env` đa môi trường

### Sử dụng `direnv` (dev)
```bash
brew install direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
# Tạo `.envrc` tại project
echo "dotenv .env" > .envrc
direnv allow
```

### Tự động sync `.env` từ git hoặc secret manager:
- Dùng script shell/Python để lấy từ secret manager, export vào `.env` trước khi build hoặc start container.

---

✅ **Luôn đảm bảo `FERNET_KEY` nhất quán giữa tất cả node/container.**


**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25