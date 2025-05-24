from sqlalchemy import Column, Integer, String, Text
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.sql import func

class EncryptedDataRef(Base):
    __tablename__ = "custom_encrypted_data_refs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tab_name = Column(String(255), nullable=False, unique=True, comment="Human-readable identifier or category for the encrypted data")
    # This will store the output of generateKey.encode_str(), which is the base64 encoded 'tab'
    # and acts as the reference to the actual encrypted data files.
    encoded_tab_reference = Column(Text, nullable=False, comment="Base64 encoded reference from multiAlgoCoder.encode_str")
    description = Column(Text, nullable=True, comment="Optional description for this encrypted entry")
    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    __table_args__ = ({"schema": "airflow"},)

    def __repr__(self):
        return f"<EncryptedDataRef id={self.id} tab_name='{self.tab_name}'>"