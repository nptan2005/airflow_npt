
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from email_validator import EmailNotValidError, validate_email
from pydantic import EmailStr

from .model.task import Task


class TaskFactory:
    @staticmethod
    def create_from_sql_result(result: dict) -> Task:
        """
        Create a Task object from an SQL query result dictionary.
        :param result: Dictionary result from SQL query
        :return: Task object
        """
        return Task(
            task_id=result.get("task_id"),
            task_type=result.get("task_type"),
            task_name=result.get("task_name"),
            config_key_name=result.get("config_key_name"),
            process_num=result.get("process_num"),
            frequency=result.get("frequency"),
            day_of_week=result.get("day_of_week"),
            day_of_month=result.get("day_of_month"),
            is_export=result.get("is_export") == '1',
            is_import=result.get("is_import") == '1',
            is_header=result.get("is_header") == '1',
            is_notification=result.get("is_notification") == '1',
            is_attachment=result.get("is_attachment") == '1',
            script=result.get("script"),
            connection_string=result.get("connection_string"),
            output_name=result.get("output_name"),
            src_folder_name=result.get("src_folder_name"),
            src_file_name=result.get("src_file_name"),
            src_file_type=result.get("src_file_type"),
            dst_folder_name=result.get("dst_folder_name"),
            dst_file_name=result.get("dst_file_name"),
            dst_file_type=result.get("dst_file_type"),
            email=result.get("email"),
            run_time=int(result.get("run_time")) if result.get("run_time") else None,
            task_time_out=int(result.get("task_time_out")) if result.get("task_time_out") else None,
        )
    # end create_from_sql_result
    @staticmethod
    def normalize_task_data(task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chuẩn hóa dữ liệu đầu vào từ DataFrame để phù hợp với mô hình Task.
        
        Args:
            task_data: Dictionary chứa dữ liệu cho mỗi bản ghi từ DataFrame.
        
        Returns:
            task_data: Dictionary đã được chuẩn hóa.
        """
        # Đảm bảo các trường cần thiết có mặt và có giá trị hợp lệ
        required_fields = ["task_id", "task_type", "task_name","task_order","run_time"]
        
        for field in required_fields:
            if field not in task_data or pd.isna(task_data.get(field)):
                task_data[field] = None  # Gán None nếu thiếu hoặc không hợp lệ
        

        
        # Xử lý các trường hợp thiếu giá trị mặc định cho boolean
        boolean_fields = ["is_export", "is_import", "is_header", "is_notification", "is_attachment"]
        for field in boolean_fields:
            if field not in task_data or pd.isna(task_data.get(field)):
                task_data[field] = False
        
        # Xử lý các chuỗi rỗng hoặc null trong script, output_array, notification_email
        if 'script' in task_data and pd.isna(task_data['script']):
            task_data['script'] = None
        
        if 'output_name' in task_data and pd.isna(task_data['output_name']):
            task_data['output_name'] = None
        
        if 'email' in task_data and pd.isna(task_data['email']):
            task_data['email'] = None
        
        return task_data
    # end normalize_task_data
    @staticmethod
    def validate_email_list(email_list: List[str]) -> List[str]:
        """
        Kiểm tra tính hợp lệ của các email trong danh sách.
        
        Args:
            email_list (List[str]): Danh sách các email dưới dạng chuỗi.
        
        Returns:
            List[str]: Danh sách các email hợp lệ.
        
        Raises:
            ValueError: Nếu có email không hợp lệ.
        """
        valid_emails = []
        invalid_emails = []
        
        for email in email_list:
            try:
                # Xác thực và chuẩn hóa email
                validated = validate_email(email)
                valid_emails.append(validated.email)
            except EmailNotValidError as e:
                invalid_emails.append(email)
        
        if invalid_emails:
            raise ValueError(f"Các email không hợp lệ: {', '.join(invalid_emails)}")
        
        return valid_emails

