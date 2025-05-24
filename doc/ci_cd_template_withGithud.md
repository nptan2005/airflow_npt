# 🔁 CI/CD mẫu với GitHub Actions

```yaml
name: Deploy Airflow

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: docker/setup-buildx-action@v2

    - name: Build & Push image
      uses: docker/build-push-action@v4
      with:
        context: .
        tags: your_user/airflow-nptan:latest
        push: true

    - name: Trigger Deploy Server (SSH)
      uses: appleboy/ssh-action@v1
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USER }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd airflow-deploy
          docker compose pull
          docker compose up -d
```
