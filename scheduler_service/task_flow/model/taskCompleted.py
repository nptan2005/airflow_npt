from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCompleted(BaseModel):
    start_date: datetime = Field(default=None) 
    task_id: int = Field(default=None) 
    task_name: str = Field(default=None) 
    task_type: str = Field(default=None) 
    is_finished: bool = Field(default=False) 
    is_error: bool = Field(default=False) 
    duration: int = -1
    note: str = Field(default=None) 
    is_frequency_task: Optional[bool] =Field(default=False)
    is_notify_fail: Optional[bool] =Field(default=False)
    is_notify_sucess: Optional[bool] =Field(default=False)


    class Config:
        arbitrary_types_allowed = True  # Cho phép các kiểu tùy ý như Exception

    def __str__(self):
        return (
            f'TaskCompleted(start_date={self.start_date}, '
            f'task_id={self.task_id}, '
            f'task_name={self.task_name}, '
            f'task_type={self.task_type}, '
            f'is_finished={self.is_finished},'
            f'is_error={self.is_error},'
            f'duration={self.duration}, '
            f'note={self.note}'
        )
