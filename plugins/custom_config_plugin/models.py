from sqlalchemy import Column, Integer, String, Text
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.sql import func


class AppSetting(Base):
    __tablename__ = "custom_app_settings"
    __table_args__ = ({"extend_existing": True, "schema": "task_flow"},)

    id = Column(Integer, primary_key=True, autoincrement=True)
    environment = Column(
        String(50), nullable=False, default="default"
    )  # e.g., UAT, PROD, common
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AppSetting environment='{self.environment}' key='{self.key}' value='{self.value[:50]}'>"

    @property
    def pretty_value(self):
        # Could be used to format JSON or long text in the UI
        return self.value

    # You can add methods here to parse/validate values if they are complex (e.g., JSON)
