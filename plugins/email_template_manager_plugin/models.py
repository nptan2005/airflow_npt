from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.sql import func


class DBEmailTemplate(Base):
    __tablename__ = "custom_email_templates"
    __table_args__ = ({"extend_existing": True, "schema": "task_flow"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="Tên định danh duy nhất cho template",
    )
    subject = Column(String(500), nullable=False, comment="Chủ đề mặc định của email")
    body_html = Column(Text, nullable=False, comment="Nội dung HTML của email template")
    description = Column(Text, nullable=True, comment="Mô tả tùy chọn cho template này")

    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    # __table_args__ = (
    #     {"schema": "task_flow"},
    # )  # Đảm bảo bảng được tạo trong schema của task_flow

    def __repr__(self):
        return f"<DBEmailTemplate name='{self.template_name}'>"
