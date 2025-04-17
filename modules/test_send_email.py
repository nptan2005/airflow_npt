from task_flow.task_engine.taskEmailSender import TaskEmailSender
from task_flow import (Task, TaskDispatcher,
                       TaskScheduler)
from task_flow.taskFactory import TaskFactory
from conn_kit.emailSender import EmailSender

test_sql_export_email = {
    "task_id": 1,
    "task_type": 'EXPORT',
    "task_name": "Export Sales Report",
    "config_key_name": "sales_report",
    "process_num": 3,
    "frequency": "DAILY",
    "day_of_week": 2,
    "day_of_month": 15,
    "is_export": "1",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
    "is_import": "0",
    "is_header": "1",
    "is_notification": "1",
    "is_attachment": "1",
    "script": "SELECT SYSDATE FROM dual",
    "connection_string": "DW",
    "output_name": "sales_report_output",
    "src_folder_name": "src_folder",
    "src_file_name": "sales_data",
    "src_file_type": "xlsx",
    "dst_folder_name": "dst_folder",
    "dst_file_name": "report",
    "dst_file_type": "xlsx",
    "email": "tannp@bvbank.net.vn",
    "run_time": "1600",  # Giả sử đây là kiểu chuỗi
    "task_time_out": 3600
}

# Sử dụng TaskFactory để chuẩn hóa dữ liệu
normalized_task_data = TaskFactory.normalize_task_data(test_sql_export_email)



# # Tạo đối tượng Task từ dữ liệu đã chuẩn hóa
task_object = TaskFactory.create_from_sql_result(normalized_task_data)


# with TaskDispatcher() as p:
#     p.enqueue(task_object)
#     p.run_tasks()

# Ví dụ sử dụng
# send_email_ssl('noreply@bvbank.net.vn', 'NO_PASSWORD', 'tannp@bvbank.net.vn', 'Test Email', 'Hello from Python!')

with EmailSender("EMAIL_DEFAULT", is_ssl=False, is_debug= False) as sender:
    sender.header = 'self.task.task_name'
    sender.send(
        subject=f'[Tst]', 
        receivers=['tannp@bvbank.net.vn'], textMessage='text_message')
    