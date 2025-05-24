from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # For PostgreSQL
# from sqlalchemy.types import JSON # Generic JSON type, might work for SQLite if JSONB isn't available
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.sql import func

class DBImportTemplate(Base):
    __tablename__ = "custom_import_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(String(255), nullable=False, unique=True, comment="e.g., ATOM_POS_SET_TXN")

    # Fields from _ImportTemplate Pydantic model
    header_json = Column(JSONB, nullable=True, comment="JSON array of header strings") # Or Text
    file_extension = Column(String(50), default="xlsx")
    separate = Column(String(10), nullable=True, default="|")
    sftp_conn = Column(String(255), nullable=True)
    sftp_move = Column(Boolean, default=False)
    start_row = Column(Integer, default=2)
    end_row = Column(Integer, nullable=True, default=0)
    start_col = Column(Integer, default=1)
    end_col = Column(Integer, nullable=True, default=0)
    is_read_to_empty_row = Column(Boolean, default=False)
    table_name = Column(String(255), nullable=False)
    is_truncate_tmp_table = Column(Boolean, default=False)
    procedure_name = Column(String(255), nullable=True)
    external_process = Column(String(255), nullable=True)
    column_mapping_json = Column(JSONB, nullable=True, comment="JSON object for column mappings") # Or Text
    
    description = Column(Text, nullable=True, comment="Optional description for this template")
    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    __table_args__ = ({"schema": "airflow"},)

    def __repr__(self):
        return f"<DBImportTemplate name='{self.template_name}'>"

class DBExportTemplate(Base):
    __tablename__ = "custom_export_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(String(255), nullable=False, unique=True, comment="e.g., ACQ_POS_ACCOUNTING_REPORT")

    # Fields from _ExportTemplate Pydantic model
    file_extension = Column(String(50), default="xlsx")
    separate = Column(String(10), default="|")
    sftp_conn = Column(String(255), nullable=True)
    sftp_move = Column(Boolean, default=True)
    
    description = Column(Text, nullable=True, comment="Optional description for this template")
    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    # Relationship to sheets
    sheets = relationship("DBExportSheetConfig", back_populates="export_template", cascade="all, delete-orphan")

    __table_args__ = ({"schema": "airflow"},)

    def __repr__(self):
        return f"<DBExportTemplate name='{self.template_name}'>"

class DBExportSheetConfig(Base):
    __tablename__ = "custom_export_sheet_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    export_template_id = Column(Integer, ForeignKey(f'{DBExportTemplate.__table_args__[0]["schema"]}.{DBExportTemplate.__tablename__}.id'), nullable=False)
    
    # This 'sheet_name_key' corresponds to the key in the 'sheets' dictionary of your YAML/Pydantic model
    sheet_name_key = Column(String(255), nullable=False, comment="Key for this sheet, e.g., ACQ_BANK, MERCHANT")

    # Fields from _SheetConfig Pydantic model
    is_header = Column(Boolean, default=True)
    sheet_title_name = Column(String(500), nullable=True) # Increased length
    # sheet_name is the display name, sheet_name_key is the programmatic key
    sheet_display_name = Column(String(255), nullable=False, comment="Actual name of the sheet in Excel") 
    is_format = Column(Boolean, default=False)
    column_mapping_json = Column(JSONB, nullable=True, comment="JSON object for column mappings") # Or Text

    created_at = Column(UtcDateTime, default=func.now())
    updated_at = Column(UtcDateTime, default=func.now(), onupdate=func.now())

    export_template = relationship("DBExportTemplate", back_populates="sheets")

    __table_args__ = (
        UniqueConstraint('export_template_id', 'sheet_name_key', name='uq_export_template_sheet_name_key'),
        {"schema": "airflow"},
    )

    def __repr__(self):
        return f"<DBExportSheetConfig template_id={self.export_template_id} sheet_key='{self.sheet_name_key}'>"