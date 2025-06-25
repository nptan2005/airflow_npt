from airflow.models import BaseOperator

# from airflow.utils.decorators import apply_defaults
from pd_to_excel_plugin.pd_to_file import PdToFile
from pd_to_excel_plugin.utils import create_file_name
from pd_to_excel_plugin.export_constant import ExportConstant
import logging


class ExportOperator(BaseOperator):
    # @apply_defaults
    def __init__(
        self,
        dataframe_array,
        name_arr,
        output_path,
        file_name_prefix,
        file_extension,
        template,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.dataframe_array = dataframe_array  # DataFrame để xuất ra Excel
        self.name_arr = name_arr
        self.output_path = output_path  # Đường dẫn thư mục để lưu file
        self.file_name_prefix = file_name_prefix  # Tên file Excel (prefix)
        self.file_extension = file_extension
        self.template = template
        self._file_name = create_file_name(
            base_path=self.output_path,
            file_pattern=f"{self.file_name_prefix}",
            syntax="[YYYYMMDDHHMMSS]",
        )
        self._logger = logging

    def execute(self, context):
        try:
            # Thiết lập logging
            self._logger.info(
                f"Export: {self.file_name_prefix} | Path: {self.output_path}"
            )
            is_completed = False
            note = ""
            with PdToFile(
                export_data=self.dataframe_array,
                export_name=self.name_arr,
                file_name=self._file_name,
                template=self.template if self.template else ExportConstant.DEFAULT,
                file_extension=self.file_extension,
            ) as writer:
                writer.to_file()
                is_completed = writer.is_successful
                note += writer.note
            self._logger.info("✅ Process successfull: %s", note)

            # Trả về đường dẫn file xuất
            return is_completed
        except (IOError, ValueError) as e:
            self._logger.exception("Export process encountered an error, %s", e)
            return is_completed
