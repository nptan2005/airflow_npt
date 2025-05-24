# Khắc phục lỗi Docker: `parent snapshot ... does not exist`

**Ngày**: 2025-05-24

## 🧩 Mô tả lỗi

Khi build hoặc chạy Docker Compose, bạn gặp lỗi:

```
failed to solve: image "...": already exists
...
apply layer error ... parent snapshot sha256:... does not exist: not found
```

## 🧾 Nguyên nhân

- Image bị lỗi do cache hỏng.
- Parent snapshot (lớp cha) đã bị xoá hoặc mất.
- Build conflict vì image có cùng tên/tag.

## ✅ Cách xử lý

### Bước 1: Xoá image cũ và cache

```bash
docker image rm airflow-nptan:1.0.0
docker builder prune --force
```

Nếu vẫn lỗi, xoá toàn bộ cache và volume (⚠️ sẽ mất dữ liệu chưa mount):

```bash
docker system prune --all --volumes --force
```

---

### Bước 2: Build lại hoàn toàn

```bash
docker compose build --no-cache
```

---

### Bước 3: Khởi động lại container

```bash
docker compose up -d
```

---

## 🎯 Gợi ý

- Nếu bạn thử nghiệm nhiều, hãy đổi tag mỗi lần build:

  ```yaml
  image: airflow-nptan:1.0.1
  ```

- Xoá container lỗi liên quan đến `airflow_npt`:

  ```bash
  docker ps -a | grep airflow_npt | awk '{print $1}' | xargs docker rm -f
  ```

---

## 📌 Tổng kết

Lỗi `parent snapshot does not exist` thường liên quan đến cache bị hỏng. Việc xoá cache và rebuild image là cách hiệu quả để khắc phục.


**✍️ Tác giả:** nptan2005
**📅 Created:** 2025-05-25

