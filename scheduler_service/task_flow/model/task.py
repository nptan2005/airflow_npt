from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime

class Task(BaseModel):
    task_id: int
    parent_task_id: Optional[int] = Field(default=None)
    task_order: int = Field(default=0)
    task_type: str
    task_name: str
    run_time: Optional[int] = Field(default=0)
    config_key_name: Optional[str] = Field(default=None)
    process_num: int = Field(default=None) 
    frequency: str = Field(default=None) 
    day_of_week: int = Field(default=None) 
    day_of_month: int = Field(default=None) 
    is_header: bool = Field(default=False)
    is_notification: bool = Field(default=False)
    is_attachment: bool = Field(default=False)
    script: Optional[List[str]] = Field(default=False)  # Danh sách script
    connection_string: str = Field(default=False)
    output_name: Optional[List[str]] = Field(default=None)  # Danh sách output
    src_folder_name: Optional[str] = Field(default=None)
    src_file_name: Optional[str] = Field(default=None)
    src_file_type: Optional[str] = Field(default=None)
    dst_folder_name: Optional[str] = Field(default=None)
    dst_file_name: Optional[str] = Field(default=None)
    dst_file_type: Optional[str] = Field(default=None)
    email: Optional[List[EmailStr]] = None  # Danh sách email
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    task_time_out: Optional[int] = Field(default=0) 
    retry_number: Optional[int] = Field(default=0) 
    is_sub_task: Optional[bool] = Field(default=False)
    sub_task_max_retry: Optional[int] = Field(default=3)
    sub_task_retry_counter: Optional[int] = Field(default=0) 
    is_frequency_task: Optional[bool] =Field(default=False)
    is_notify_fail: Optional[bool] =Field(default=False)
    is_notify_sucess: Optional[bool] =Field(default=False)

    @field_validator('is_header', 'is_sub_task','is_notification','is_attachment','is_frequency_task','is_notify_fail','is_notify_sucess', mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

    # Validator để tách chuỗi email thành danh sách
    @field_validator('email', mode='before')
    def split_emails(cls, v):
        if isinstance(v, str):
            # Tách chuỗi email và kiểm tra tính hợp lệ
            return [email.strip() for email in v.split(';') if email.strip()]
        return v

    # Validator để tách script thành danh sách và xử lý dấu chấm phẩy
    @field_validator('script', mode='before')
    def split_scripts(cls, v):
        if isinstance(v, str):
            scripts = [s.strip() for s in v.split(';') if s.strip()]  # Tách bằng dấu ';'
            return [s if not s.lower().startswith("select") else s.rstrip(';') for s in scripts]  # Xóa dấu ';' với câu lệnh select
        return v

    # Validator để tách output_array thành danh sách
    @field_validator('output_name', mode='before')
    def split_output_name(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(';') if item.strip()]
        return v
    
    class Config:
        frozen = False

    def __str__(self):
        return (
            f"Task(task_id={self.task_id},task_order={self.task_order}, task_type={self.task_type}, task_name={self.task_name}, "
            f"config_key_name={self.config_key_name}, process_num={self.process_num}, "
            f"frequency={self.frequency}, day_of_week={self.day_of_week}, day_of_month={self.day_of_month}, "
            f"is_export={self.is_export}, is_import={self.is_import}, is_header={self.is_header},is_notification={self.is_notification},is_attachment={self.is_attachment} "
            f"script={self.script},output_name={self.output_name}, connection_string={self.connection_string}, "
            f"src_folder_name={self.src_folder_name}, src_file_name={self.src_file_name},src_file_type={self.src_file_type} "
            f"dst_folder_name={self.dst_folder_name}, dst_file_name={self.dst_file_name},dst_file_type={self.dst_file_type} "
            f"email={self.email}, run_time={self.run_time}, "
            f"start_date={self.start_date}, end_date={self.end_date},"
            f"task_time_out={self.task_time_out}, retry_number = {self.retry_number})"
        )

