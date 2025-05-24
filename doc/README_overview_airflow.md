# 📊 Tổng Quan Apache Airflow

---

## 1️⃣ Tổng quan

**Apache Airflow** là một nền tảng mã nguồn mở dùng để lập lịch và giám sát luồng công việc (workflow) theo cách lập trình được.  
Airflow cho phép bạn định nghĩa các DAGs (Directed Acyclic Graphs) — một chuỗi các task có quan hệ phụ thuộc logic — bằng Python.

> 🧠 "Viết DAG như viết code, không cần cấu hình phức tạp."

---

## 2️⃣ Tính năng nổi bật

```plaintext
| Tính năng            | Mô tả                                               |
| -------------------- | --------------------------------------------------- |
| 🧩 Modular            | Có thể mở rộng bằng plugin, viết operator tùy chỉnh |
| 🛠 Lập lịch linh hoạt | Dựa trên cron hoặc thời gian tùy chỉnh              |
| 📊 Web UI mạnh mẽ     | Theo dõi DAG, log, retry task...                    |
| 💥 Retry, Alert, SLA  | Tự động retry, gửi email khi task fail              |
| 🧵 Parallel execution | Chạy task song song qua Celery, Kubernetes          |
| 🔐 RBAC UI            | Phân quyền người dùng rõ ràng                       |
```

---

## 3️⃣ Ứng dụng thực tế

```plaintext
| Lĩnh vực           | Ứng dụng                             |
| ------------------ | ------------------------------------ |
| 🎯 Dữ liệu lớn      | ETL, chuẩn hóa dữ liệu, Spark/Hadoop |
| 🧪 Khoa học dữ liệu | Training ML model định kỳ            |
| 🛒 E-commerce       | Tự động hóa báo cáo bán hàng         |
| 📬 Marketing        | Gửi email hàng loạt theo lịch        |
| 🧾 Kế toán          | Đối soát dữ liệu, chạy batch jobs    |
```

---

## 4️⃣ Khả năng mở rộng

```plaintext
| Mode               | Đặc điểm                                             |
| ------------------ | ---------------------------------------------------- |
| SequentialExecutor | Chạy tuần tự – chỉ dùng khi test                     |
| LocalExecutor      | Chạy song song trong 1 máy                           |
| CeleryExecutor     | Scale bằng nhiều worker, sử dụng Redis/RabbitMQ      |
| KubernetesExecutor | Tự động spawn pod cho từng task – lý tưởng cho cloud |
```

---

## 5️⃣ Kiến trúc & các thành phần chính

```plaintext
                         +-----------------------+
                         |   Web Server (UI)     |
                         |   Flask + Gunicorn    |
                         +-----------+-----------+
                                     |
                                     v
                              Scheduler (Trigger DAG)
                                     |
                                     v
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
         Worker 1               Worker 2               Worker N
          (task)                 (task)                 (task)
              |                      |                      |
              +----------------------+----------------------+
                                     |
                           Redis/RabbitMQ (Broker)
                                     |
                          PostgreSQL/MySQL (Metadata DB)
```

### 📦 Mô tả chi tiết:

```plaintext
| Thành phần  | Mô tả                              | Tính năng chính                           |
| ----------- | ---------------------------------- | ----------------------------------------- |
| Webserver   | Giao diện người dùng (Flask)       | Xem DAG, trigger, log                     |
| Scheduler   | Lập lịch DAG theo thời gian        | Theo dõi trạng thái & lên lịch task       |
| Worker      | Thực thi task DAG                  | Có thể scale hàng chục                    |
| Broker      | Giao tiếp giữa Scheduler và Worker | Redis hoặc RabbitMQ                       |
| Metadata DB | Lưu trạng thái, DAG, task...       | Cực kỳ quan trọng, không được mất dữ liệu |
| Flower      | Monitor queue Celery               | Xem queue, retry, trạng thái worker       |
```

---

✅ Với kiến trúc này, Airflow rất phù hợp để scale từ máy local lên production cloud (GCP, AWS, Azure).

**✍️ Tác giả:** nptan2005  
**📅 Created:** 2025-04-19
