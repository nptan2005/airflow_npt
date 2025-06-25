# Hướng Dẫn Triển Khai Airflow với Helm

## 1. Chuẩn Bị
- Cài đặt Helm: https://helm.sh/docs/intro/install/
- Có sẵn Kubernetes cluster (GKE, EKS, AKS, minikube,...)
- Namespace (tuỳ chọn): `airflow`

## 2. Cài Helm Chart

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create namespace airflow
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  -f values.yaml