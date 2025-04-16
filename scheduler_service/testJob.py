# import glob
# import os

# from core.conn_kit import ConnKitConstant
# from core.data_kit import DataConstant
# from core.db_conn import ConnConstant
# from core.task_flow import (Task, TaskConstant, TaskDispatcher, TaskFactory,
#                        TaskScheduler)

# # Giả lập dữ liệu từ SQL query
# test_sql_export_email = {
#     "task_id": 1,
#     "task_type": TaskConstant.TASK_EXPORT,
#     "task_name": "Export Sales Report",
#     "config_key_name": "sales_report",
#     "process_num": 3,
#     "frequency": "DAILY",
#     "day_of_week": 2,
#     "day_of_month": 15,
#     "is_export": "1",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "0",
#     "is_header": "1",
#     "is_notification": "1",
#     "is_attachment": "1",
#     "script": "SELECT SYSDATE FROM dual",
#     "connection_string": "CARD_DW",
#     "output_name": "sales_report_output",
#     "src_folder_name": "src_folder",
#     "src_file_name": "sales_data",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "dst_folder",
#     "dst_file_name": "report",
#     "dst_file_type": "xlsx",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600",  # Giả sử đây là kiểu chuỗi
#     "task_time_out": 3600
# }

# test_sql_sftp_upload = {
#     "task_id": 2,
#     "task_type": TaskConstant.TASK_SFTP_UPLOAD,
#     "task_name": "upload file",
#     "config_key_name": "",
#     "process_num": 1,
#     "frequency": "DAILY",
#     "day_of_week": 0,
#     "day_of_month": 0,
#     "is_export": "0",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "0",
#     "is_header": "0",
#     "is_notification": "0",
#     "is_attachment": "0",
#     "script": "",
#     "connection_string": "SFTP_DEFAULT",
#     "output_name": "test_upload",
#     "src_folder_name": "test_sftp",
#     "src_file_name": "TestExport_excel_[YYYYMMDD]",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "/var/tmp/test",
#     "dst_file_name": "TestExport_excel_[YYYYMMDDHHMMSS]",
#     "dst_file_type": "xlsx",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600"  # Giả sử đây là kiểu chuỗi
# }


# test_sql_sftp_online_txn = {
#     "task_id": 2,
#     "task_type": TaskConstant.TASK_SFTP_MOVE_TO_LOCAL,
#     "task_name": "move file",
#     "config_key_name": "",
#     "process_num": 1,
#     "frequency": "DAILY",
#     "day_of_week": 0,
#     "day_of_month": 0,
#     "is_export": "0",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "0",
#     "is_header": "0",
#     "is_notification": "0",
#     "is_attachment": "0",
#     "script": "",
#     "connection_string": ConnKitConstant.SFTP_CONN_DEFAULT,
#     "output_name": "test_download",
#     "src_folder_name": "/var/tmp/test",
#     "src_file_name": "Atom_2_[YYYYMMDD]",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "ACQ_POS",
#     "dst_file_name": "atom_online_txn_[YYYYMMDDHHMMSS]",
#     "dst_file_type": "xlsx",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600"  # Giả sử đây là kiểu chuỗi
# }



# test_sql_sftp_bank_benefit = {
#     "task_id": 2,
#     "task_type": TaskConstant.TASK_SFTP_MOVE_TO_LOCAL,
#     "task_name": "move file",
#     "config_key_name": "",
#     "process_num": 1,
#     "frequency": "DAILY",
#     "day_of_week": 0,
#     "day_of_month": 0,
#     "is_export": "0",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "0",
#     "is_header": "0",
#     "is_notification": "0",
#     "is_attachment": "0",
#     "script": "",
#     "connection_string": ConnKitConstant.SFTP_CONN_ACQ_POS,
#     "output_name": "test_download",
#     "src_folder_name": "/ke_toan_the/in",
#     "src_file_name": "ACQ_BANK_BENEFIT_[YYYYMMDD]",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "ACQ_POS",
#     "dst_file_name": "acq_bank_benefit_[YYYYMMDDHHMMSS]",
#     "dst_file_type": "xlsx",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600"  # Giả sử đây là kiểu chuỗi
# }

# test_sql_import_online_txn = {
#     "task_id": 2,
#     "task_type": TaskConstant.TASK_IMPORT,
#     "task_name": "import file",
#     "config_key_name": DataConstant.IMP_ATOM_SET_TXN,
#     "process_num": 2,
#     "frequency": "DAILY",
#     "day_of_week": 0,
#     "day_of_month": 0,
#     "is_export": "0",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "1",
#     "is_header": "0",
#     "is_notification": "0",
#     "is_attachment": "0",
#     "script": "",
#     "connection_string": ConnConstant.DB_CONN_DEFAULT,
#     "output_name": "test_import",
#     "src_folder_name": "ACQ_POS",
#     "src_file_name": "atom_online_txn_[YYYYMMDDHHMMSS]",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "",
#     "dst_file_name": "",
#     "dst_file_type": "",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600"  # Giả sử đây là kiểu chuỗi
# }



# test_sql_import_bank_benefit_txn = {
#     "task_id": 2,
#     "task_type": TaskConstant.TASK_IMPORT,
#     "task_name": "import file",
#     "config_key_name": DataConstant.ACQ_BANK_BENEFIT,
#     "process_num": 2,
#     "frequency": "DAILY",
#     "day_of_week": 0,
#     "day_of_month": 0,
#     "is_export": "0",  # Giả sử đây là dữ liệu kiểu chuỗi (SQL trả về dạng này)
#     "is_import": "1",
#     "is_header": "0",
#     "is_notification": "0",
#     "is_attachment": "0",
#     "script": "",
#     "connection_string": ConnConstant.DB_CONN_DEFAULT,
#     "output_name": "test_import",
#     "src_folder_name": "ACQ_POS",
#     "src_file_name": "acq_bank_benefit_[YYYYMMDDHHMMSS]",
#     "src_file_type": "xlsx",
#     "dst_folder_name": "",
#     "dst_file_name": "",
#     "dst_file_type": "",
#     "email": "tannp@bvbank.net.vn",
#     "run_time": "1600"  # Giả sử đây là kiểu chuỗi
# }

# # Sử dụng TaskFactory để chuẩn hóa dữ liệu
# normalized_task_data = TaskFactory.normalize_task_data(test_sql_export_email)

# # # In ra dữ liệu đã chuẩn hóa
# # print("Normalized Task Data:")
# # print(normalized_task_data)

# # # Tạo đối tượng Task từ dữ liệu đã chuẩn hóa
# task_object = TaskFactory.create_from_sql_result(normalized_task_data)


# # with TaskDispatcher() as p:
# #     p.enqueue(task_object)
# #     p.run_tasks()

# # tasks = [2,3,4,5,6]
# # with TaskScheduler(5,5) as test:
# #     # for i in tasks:
# #     #     test.run(1615,i)
# #     test.run(1615)
# # def _generate_time_serial():
# #     _run_time_list = []
# #     for i in range(0, 2400,15):
# #         hour = f"{i//100:02}"
# #         minute = f"{i%100:02}"
# #         if int(minute) < 60:
# #             _run_time_list.append(f"{hour}{minute}")
# #     return _run_time_list
# # print(_generate_time_serial())

# from core.task_flow import tasks_list

# l = tasks_list.acq_tasks[0]
# print(l.task_id)

from utilities import Logger
l = Logger().logger
l.info('a')

import os

file_path = "abc.txt"
file_name, file_extension = os.path.splitext(os.path.basename(file_path))
print(file_name)  # Kết quả: abc
print(file_extension)  # Kết quả: .txt