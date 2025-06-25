from airflow.models import BaseOperator

# from airflow.utils.decorators import apply_defaults
import pandas as pd
import logging


class ExcelExportOperator(BaseOperator):
    # @apply_defaults
    def __init__(self, dataframe, output_path, file_name_prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataframe = dataframe  # DataFrame để xuất ra Excel
        self.output_path = output_path  # Đường dẫn thư mục để lưu file
        self.file_name_prefix = file_name_prefix  # Tên file Excel (prefix)

    def execute(self, context):
        try:
            # Thiết lập logging
            logging.info("Bắt đầu xử lý xuất file Excel...")

            # Đặt subfix ngày giờ vào tên file
            current_time = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{self.file_name_prefix}_{current_time}.xlsx"
            full_path = f"{self.output_path}/{file_name}"

            # Xuất DataFrame ra file Excel
            self.dataframe.to_excel(full_path, index=False, engine="openpyxl")
            logging.info(f"✅ File Excel đã được xuất ra tại: {full_path}")

            # Trả về đường dẫn file xuất
            return full_path
        except Exception as e:
            logging.error(f"Lỗi xảy ra khi xuất file Excel: {e}")
            raise
