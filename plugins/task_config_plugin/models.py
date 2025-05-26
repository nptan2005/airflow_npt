from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship


class TaskDefinition(Base):
    __tablename__ = "custom_task_definitions"
    __table_args__ = ({"extend_existing": True, "schema": "task_flow"},)

    # Core Identifiers
    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Corresponds to task_id in Pydantic model
    task_name = Column(
        String(255), nullable=False, unique=True
    )  # Ensuring task names are unique for easier reference

    # Hierarchy and Ordering
    parent_task_id = Column(
        Integer, ForeignKey(f"{__tablename__}.id"), nullable=True
    )  # Self-referential for parent task
    task_order = Column(Integer, default=0)

    # Task Type and Execution Details
    task_type = Column(String(50), nullable=False)  # e.g., BASH, PYTHON, SQL
    connection_string = Column(String(255), nullable=True)  # Airflow connection ID
    script = Column(
        Text, nullable=True
    )  # For SQL queries, bash commands, Python script content/path
    config_key_name = Column(
        String(500), nullable=True
    )  # Reference to other configs if needed

    # Scheduling and Timing (simplified for now, can be expanded)
    run_time = Column(
        Integer, nullable=True
    )  # Interpretation depends on usage (e.g., specific time like 0800, or duration)
    frequency = Column(
        String(50), nullable=True
    )  # e.g., DAILY, HOURLY, CRON_EXPRESSION
    day_of_week = Column(Integer, nullable=True)  # 0-6 or 1-7
    day_of_month = Column(Integer, nullable=True)  # 1-31
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    task_time_out = Column(Integer, default=0)  # In seconds
    retry_number = Column(Integer, default=0)
    sub_task_max_retry = Column(
        Integer, default=3
    )  # Max retries for sub-tasks if this is a group

    # File/Data Handling Parameters
    output_name = Column(Text, nullable=True)  # Could be comma-separated or JSON
    src_folder_name = Column(String(250), nullable=True)
    src_file_name = Column(String(500), nullable=True)
    src_file_type = Column(
        String(50), nullable=True
    )  # Changed from 15 to 50 for flexibility
    dst_folder_name = Column(String(250), nullable=True)
    dst_file_name = Column(String(500), nullable=True)
    dst_file_type = Column(String(50), nullable=True)  # Changed from 15 to 50

    # Flags
    is_header = Column(Boolean, default=False)  # If this task is a grouping header
    is_notification = Column(Boolean, default=False)
    is_attachment = Column(Boolean, default=False)
    active = Column(
        Boolean, default=True
    )  # Is the task definition active for DAG generation

    # Notification Details
    email = Column(Text, nullable=True)  # Comma-separated or JSON list of emails

    # Process Control
    process_num = Column(Integer, nullable=True)  # e.g., for parallel execution limits

    # Audit and Request Tracking (from your SQL table)
    request_department = Column(String(255), nullable=True)
    request_user = Column(String(255), nullable=True)
    request_date = Column(DateTime, nullable=True)
    process_user = Column(String(255), nullable=True)
    process_date = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    # Relationships (for parent-child tasks)
    # children = relationship("TaskDefinition", backref=backref('parent', remote_side=[id]))

    # __table_args__ = (
    #     {"schema": "task_flow"},
    # )  # Ensures table is created in airflow schema

    def __repr__(self):
        return f"<TaskDefinition id={self.id} name='{self.task_name}' type='{self.task_type}'>"

    # You can add properties or methods here, e.g., to parse 'email' or 'output_name'
    # if they are stored as JSON strings or comma-separated values.
