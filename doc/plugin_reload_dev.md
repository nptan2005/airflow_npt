# Tự động reload DAGs/Plugin khi phát triển

## Cách dùng:
- Mount toàn bộ thư mục DAGs và plugins vào container
- Đảm bảo biến `DAG_DIR_LIST_INTERVAL` có giá trị nhỏ (ví dụ: 10s hoặc 30s)

## Lưu ý:
- Không cần restart container khi cập nhật DAG
- Với plugin, đôi khi cần restart container nếu cập nhật class/plugin loader

