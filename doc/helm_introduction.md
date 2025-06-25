# 📦 Giới Thiệu Về Helm

## Helm là gì?

[Helm](https://helm.sh) là một công cụ quản lý **package** dành cho **Kubernetes**, giúp bạn:
- Triển khai ứng dụng phức tạp nhanh chóng.
- Tái sử dụng cấu hình.
- Cấu hình linh hoạt giữa môi trường (dev/staging/prod).
- Quản lý version giống như apt, yum, pip...

> Helm được ví như **"apt/yum của Kubernetes"**, còn Chart là **"gói phần mềm"**.

---

## ⚙️ Các thành phần chính của Helm

| Thành phần      | Mô tả                                                                             |
| --------------- | --------------------------------------------------------------------------------- |
| **Chart**       | Bộ định nghĩa template cho 1 ứng dụng, có thể custom theo giá trị (`values.yaml`) |
| **Release**     | Bản triển khai cụ thể của Chart trên 1 cluster Kubernetes                         |
| **Repository**  | Kho lưu trữ các Helm Chart, giống như PyPI/NPM                                    |
| **Values.yaml** | File cấu hình mặc định hoặc tuỳ chỉnh theo môi trường                             |

---

## 🎯 Lợi ích khi dùng Helm

✅ **Tự động hoá** triển khai ứng dụng (đúng cấu trúc Kubernetes).  
✅ **Giảm lặp lại cấu hình**, dễ bảo trì nhiều môi trường.  
✅ **Rollback dễ dàng** khi có sự cố (giữ lại phiên bản release).  
✅ **Tích hợp CI/CD** và GitOps thuận tiện.  
✅ Dễ dàng **chia sẻ cấu hình chuẩn** với team khác.

---

## 🛠️ Helm dùng cho ai?

- DevOps/SRE triển khai & vận hành hệ thống trên K8s.
- Developer xây dựng microservices cần tái sử dụng cấu hình.
- Tổ chức cần quản lý hàng trăm ứng dụng/dịch vụ trên Kubernetes.
- Tự động hoá việc build → test → deploy trong CI/CD pipeline.

---

## 🔗 So sánh với Docker Compose

| Tiêu chí         | Docker Compose                | Helm (Kubernetes)                           |
| ---------------- | ----------------------------- | ------------------------------------------- |
| Mức độ           | Cấp container                 | Cấp cluster (pod/service/volume/...)        |
| Hệ điều hành     | Chạy trực tiếp trên Docker    | Chạy trên Kubernetes                        |
| Quản lý version  | Không hỗ trợ version release  | Có Helm release version                     |
| Môi trường cloud | Không hỗ trợ cloud-native tốt | Tích hợp tốt AWS/GCP/Azure, autoscale, etc. |
| CI/CD            | Cần thêm tool                 | Dễ tích hợp ArgoCD/GitHub Actions/...       |

---

## 🧪 Demo lệnh Helm cơ bản

```bash
# Thêm repo
helm repo add apache-airflow https://airflow.apache.org

# Cài đặt Chart
helm install airflow apache-airflow/airflow -f values.yaml -n airflow

# Xem release đang chạy
helm list -n airflow

# Xoá release
helm uninstall airflow -n airflow


# 📚 Tài liệu tham khảo
	•	https://helm.sh/docs/
	•	https://artifacthub.io
	•	https://github.com/helm/charts

# 📦 Helm Chart Nâng Cao + CI/CD + GitOps (ArgoCD)


## 1. 🎯 Helm Chart Nâng Cao

### 1.1 Cấu trúc thư mục Chart

```bash
my-airflow-chart/
├── Chart.yaml            # Metadata chart
├── values.yaml           # Thông số mặc định
├── templates/           # Tập tin K8s (yaml, jinja)
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── secrets.yaml          # Tuùy chọn cho secrets
```
Hoặc
```bash
my-airflow-chart/
├── Chart.yaml              # Metadata chart (name, version, dependencies...)
├── values.yaml             # Thông số mặc định (dùng cho dev/local)
├── values-prod.yaml        # Thông số cho môi trường production
├── values-staging.yaml     # Thông số cho staging
├── templates/              # Template K8s (yaml, jinja)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── _helpers.tpl        # Template helper (dùng lại biến, định nghĩa hàm)
├── charts/                 # Subcharts nếu dùng (ví dụ: redis, postgres)
├── files/                  # File tĩnh (script, sql, ...)
└── README.md               # Hướng dẫn sử dụng chart
```


### Triển khai

Cải đặt helm
>>> Hướng dẫn cài Minikube với Docker driver
```bash
brew install minikube
minikube start --driver=docker
```
Lệnh trên sẽ dùng Docker Desktop làm backend cho Minikube.
Bạn không cần cài thêm Hyperkit hay VirtualBox.

Sau khi start xong, bạn có thể kiểm tra:

```bash
kubectl get nodes
```


Cài kubectl

```bash
brew install kubectl
```
Cài Helm

```bash
brew install helm
```
### Chuyển từ Docker Compose sang Helm
a. Về image Docker
Bạn có thể tái sử dụng image đã build (nếu đã push lên Docker Hub hoặc registry riêng).
Nếu image chỉ build local, bạn cần push lên registry (Docker Hub, GitHub Container Registry, hoặc minikube registry).

Ví dụ push lên Docker Hub:
```bash
docker tag my-image:latest yourdockerhub/my-image:latest
docker push yourdockerhub/my-image:latest
```
Sau đó, trong values.yaml của Helm, chỉ cần trỏ tới image này:

``` yaml
airflow:
  image:
    repository: yourdockerhub/my-image
    tag: latest
```

. Có cần build lại không?
Không cần build lại nếu image đã có trên registry và không thay đổi code.
Nếu bạn thay đổi code, hãy build lại image rồi push lại lên registry.

. Helm có dùng lại Dockerfile không?
Helm không build image. Helm chỉ dùng image đã có sẵn trên registry.
Dockerfile vẫn cần thiết để bạn build image, nhưng Helm chỉ kéo image về để chạy pod.

## *** Trường hợp image trên máy local

### Cách 1: Dùng minikube image load
Build image trên máy local:
```bash
docker build -t my-airflow:latest .
```
Load image vào Minikube:
```bash
minikube image load my-airflow:latest
```
Cấu hình values.yaml của Helm trỏ tới image local:
```yaml
airflow:
  image:
    repository: my-airflow
    tag: latest
```
Lưu ý: Không cần prefix docker.io/ hoặc username, chỉ cần đúng tên image đã load.

Triển khai Helm như bình thường:
```bash
helm upgrade --install airflow . -f values.yaml -n airflow --create-namespace
```

### Cách 2: Dùng Minikube Docker daemon
Chạy lệnh sau để các lệnh docker build dùng luôn Docker daemon của Minikube:
```bash
eval $(minikube docker-env)
```

Build image:
```bash
docker build -t my-airflow:latest .
```

Lúc này image sẽ nằm trong Minikube, không phải Docker Desktop.

Cấu hình values.yaml như trên.

Lưu ý chung:
Không cần push lên registry nếu chỉ chạy local với Minikube.
Nếu chuyển sang cluster thật (cloud), bạn bắt buộc phải push image lên registry (Docker Hub, GCR, ECR, ...).
Tóm tắt cấu hình values.yaml cho image local:
Tài liệu tham khảo:

Minikube: Load images
Airflow Helm Chart: Image config

----
### apply pvc
```bash
kubectl apply -f airflow-dags-pvc.yaml
kubectl apply -f airflow-logs-pvc.yaml
kubectl apply -f airflow-plugins-pvc.yaml
kubectl apply -f airflow-config-pvc.yaml

helm upgrade --install airflow . -f [values.yaml](http://_vscodecontentref_/9) -n airflow --create-namespace

### 1.2 Biến môi trường (giá trị tổng quát trong values.yaml)

```yaml
airflow:
  executor: CeleryExecutor
  config:
    AIRFLOW__WEBSERVER__EXPOSE_CONFIG: True
    AIRFLOW__CORE__FERNET_KEY: "your_key_here"
  image:
    repository: your-registry/airflow-nptan
    tag: 1.0.0
```

### 1.3 Sử dụng templates linh hoạt

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "airflow.fullname" . }}-webserver
spec:
  replicas: {{ .Values.airflow.web.replicas | default 1 }}
```

## 2. 🚀 Tích Hợp CI/CD với GitHub Actions + Helm

### 2.1 workflows/.github/workflows/deploy.yml

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout source
      uses: actions/checkout@v3

    - name: Set up Kubeconfig
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.26.0'

    - name: Set up Helm
      uses: azure/setup-helm@v3

    - name: Helm Upgrade
      run: |
        helm upgrade --install airflow ./helm-chart \
          -f ./helm-chart/values.yaml \
          --namespace airflow --create-namespace
```

## 3. 🚀 GitOps với ArgoCD + Helm

### 3.1 Cài đặt ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 3.2 Khai báo Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: airflow
  namespace: argocd
spec:
  destination:
    namespace: airflow
    server: https://kubernetes.default.svc
  project: default
  source:
    repoURL: https://github.com/nptan2005/airflow_npt
    targetRevision: HEAD
    path: helm-chart
    helm:
      valueFiles:
        - values.yaml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 4. 🔄 Auto Sync DAG / Plugin (phát triển)

### 4.1 Mount DAG/plugin từ host:

```yaml
  volumes:
    - name: dags
      hostPath:
        path: /mnt/data/airflow/dags
  containers:
    volumeMounts:
      - name: dags
        mountPath: /opt/airflow/dags
```

### 4.2 Sử dụng Git-sync:

```bash
gitSync:
  enabled: true
  repo: https://github.com/nptan2005/airflow_npt_dags
  branch: main
  depth: 1
  wait: 30
```

## 5. 🔧 Tips

✅ Dùng nhiều file values-*.yaml tùy theo môi trường (dev/staging/prod)

✅ Dùng CI/CD để render values tuỳ biến theo secret manager (Vault, GCP, AWS)

## 📅 Tài liệu

https://airflow.apache.org/docs/helm-chart/stable

https://argo-cd.readthedocs.io

https://helm.sh/docs

