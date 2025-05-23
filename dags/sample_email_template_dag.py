from __future__ import annotations

import pendulum
import pandas as pd # Cần cài đặt pandas nếu chưa có: pip install pandas

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin # Để log trong PythonOperator

# Import EmailTemplateSender từ plugin của bạn
# Đảm bảo 'plugins' nằm trong PYTHONPATH của Airflow
# Hoặc plugin được cài đặt đúng cách để Airflow có thể tìm thấy module này.
try:
    from email_template_manager_plugin.email_service import EmailTemplateSender, EmailStr
except ImportError:
    LoggingMixin().log.warning(
        "Could not import EmailTemplateSender from plugin. "
        "Ensure 'email_template_manager_plugin' is in plugins folder and accessible."
    )
    # Cung cấp một class giả để DAG có thể parse mà không lỗi hoàn toàn
    class EmailTemplateSender:
        def __init__(self, *args, **kwargs): pass
        def send_email_with_template(self, *args, **kwargs): 
            LoggingMixin().log.error("EmailTemplateSender not loaded!")
            return False
        @property
        def last_operation_note(self): return "EmailTemplateSender not loaded!"
    EmailStr = str


# --- Các thông số cho DAG ---
SMTP_CONNECTION_ID = "smtp_default"  # ID của Airflow Connection cho SMTP server của bạn
EMAIL_TEMPLATE_NAME_IN_DB = "my_sample_report_template" # Tên template bạn đã tạo trong UI
RECIPIENT_EMAIL = "your_email@example.com" # Thay bằng email người nhận thực tế

# --- Hàm Python để thực thi bởi PythonOperator ---
def send_templated_email_task(**kwargs):
    log = LoggingMixin().log
    log.info(f"Bắt đầu tác vụ gửi email với template: {EMAIL_TEMPLATE_NAME_IN_DB}")

    # Khởi tạo EmailTemplateSender
    # Cần đảm bảo Airflow Connection 'SMTP_CONNECTION_ID' đã được cấu hình đúng trong Airflow UI
    # với host, port, login, password, và các tùy chọn SSL/TLS trong 'Extra'.
    email_sender = EmailTemplateSender(airflow_smtp_conn_id=SMTP_CONNECTION_ID, logger=log)

    # Chuẩn bị dữ liệu (context) để render vào template
    # Template của bạn (trong DB) nên có các placeholder như {header}, {body}, {textMessage}, {chartImg}
    # Ví dụ: "Xin chào {user_name}, đây là báo cáo ngày {report_date}."
    
    # Dữ liệu cho bảng (nếu template của bạn có phần {body} để hiển thị bảng)
    sample_data = {
        'Sản phẩm': ['A', 'B', 'C'],
        'Số lượng': [10, 20, 15],
        'Doanh thu': [1000, 2200, 1600]
    }
    df_sample = pd.DataFrame(sample_data)
    email_sender.data_frames_for_report = [df_sample] # Phải là một list các DataFrame

    # Header tùy chỉnh (nếu template có placeholder {header})
    email_sender.custom_header_text = "Báo cáo Tóm tắt Hàng ngày"

    # File đính kèm (tùy chọn)
    # Tạo một file text mẫu để đính kèm
    attachment_file_path = "/tmp/sample_attachment.txt" # Đường dẫn này cần tồn tại trên worker
    try:
        with open(attachment_file_path, "w") as f:
            f.write("Đây là nội dung file đính kèm mẫu.\n")
        email_sender.attachment_paths = [attachment_file_path]
    except Exception as e_attach:
        log.warning(f"Không thể tạo file đính kèm mẫu: {e_attach}")


    # Context để render vào các placeholder trong template
    email_context = {
        "user_name": "Người dùng Airflow",
        "report_date": pendulum.now().to_date_string(),
        "text_message": "Đây là thông điệp bổ sung được truyền vào template.",
        # 'title': 'Tiêu đề email tùy chỉnh từ context' # Có thể ghi đè subject từ template
    }

    # Gửi email
    success = email_sender.send_email_with_template(
        template_name=EMAIL_TEMPLATE_NAME_IN_DB,
        to_recipients=[EmailStr(RECIPIENT_EMAIL)], # Phải là list các EmailStr
        context=email_context,
        # override_subject="Tiêu đề Email Mẫu từ DAG" # Tùy chọn: ghi đè chủ đề từ template
    )

    if success:
        log.info(f"Gửi email thành công! Ghi chú: {email_sender.last_operation_note}")
    else:
        log.error(f"Gửi email thất bại. Ghi chú: {email_sender.last_operation_note}")
        # raise AirflowException(f"Gửi email thất bại: {email_sender.last_operation_note}")


# --- Định nghĩa DAG ---
with DAG(
    dag_id="sample_send_templated_email_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None, # Chạy thủ công
    tags=['email', 'template_plugin_sample'],
    doc_md=f"""
    ### DAG Gửi Email Mẫu Sử Dụng Plugin

    DAG này minh họa cách sử dụng `EmailTemplateSender` từ `email_template_manager_plugin`
    để gửi email với nội dung từ một template được lưu trong cơ sở dữ liệu Airflow.

    **Cần cấu hình trước khi chạy:**
    1.  **Airflow Connection**: Tạo một SMTP connection trong Airflow UI với ID là `{SMTP_CONNECTION_ID}`.
        Điền đầy đủ thông tin host, port, login, password.
        Trong trường `Extra`, bạn có thể thêm JSON: `{{{{ "use_ssl": true }}}}` hoặc `{{{{ "use_tls": true }}}}` nếu cần.
    2.  **Email Template**: Sử dụng UI "Email Management" > "Email Templates" (từ plugin) để tạo một template
        với "Template Name" là `{EMAIL_TEMPLATE_NAME_IN_DB}`.
        Nội dung HTML của template có thể chứa các placeholder như:
        `{{{{header}}}}`, `{{{{body}}}}` (cho bảng dữ liệu), `{{{{textMessage}}}}`, `{{{{chartImg}}}}`.
        Ví dụ một template đơn giản:
        ```html
        <h1>{{{{header}}}}</h1>
        <p>Xin chào {{{{user_name}}}},</p>
        <p>Đây là báo cáo cho ngày {{{{report_date}}}}.</p>
        <div>{{{{body}}}}</div>
        <p>{{{{textMessage}}}}</p>
        <div>{{{{chartImg}}}}</div>
        <p>Trân trọng,<br>Hệ thống Airflow</p>
        ```
    3.  **Email Người Nhận**: Cập nhật biến `RECIPIENT_EMAIL` trong code DAG bằng địa chỉ email thực tế.
    4.  **Thư viện Pandas**: Đảm bảo thư viện `pandas` đã được cài đặt trong môi trường Airflow của bạn (`pip install pandas`).
    """
) as dag: # Đảm bảo dấu ngoặc đóng của DAG ở đúng dòng
    task_send_email = PythonOperator(
        task_id="send_custom_templated_email",
        python_callable=send_templated_email_task,
    )