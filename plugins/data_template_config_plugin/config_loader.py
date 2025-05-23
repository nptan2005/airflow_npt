from typing import Dict, Optional
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)  # Re-using Pydantic models for structure
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session
from data_template_config_plugin.models import (
    DBImportTemplate,
    DBExportTemplate,
    DBExportSheetConfig,
)

# --- Pydantic models mirroring your original core_config structures ---
# These will be populated from the database models.


class CoreImportHeaderItem(BaseModel):  # Assuming header items are just strings
    item: str


class CoreImportTemplate(BaseModel):
    header: Optional[list[str]] = Field(default_factory=list)
    file_extension: str = Field(default="xlsx")
    separate: Optional[str] = Field(default="|")
    sftp_conn: Optional[str] = None
    sftp_move: bool = Field(default=False)
    start_row: int = Field(default=2)
    end_row: Optional[int] = Field(default=0)
    start_col: int = Field(default=1)
    end_col: Optional[int] = Field(default=0)
    is_read_to_empty_row: bool = Field(default=False)
    table_name: str
    is_truncate_tmp_table: bool = Field(default=False)
    procedure_name: Optional[str] = None
    external_process: Optional[str] = None
    column_mapping: Optional[Dict[str, str]] = Field(default_factory=dict)

    @field_validator(
        "sftp_move", "is_read_to_empty_row", "is_truncate_tmp_table", mode="before"
    )
    def parse_bool_str(
        cls, v
    ):  # Handles potential string 'true'/'false' from various sources
        if isinstance(v, str):
            return v.lower() in ["true", "1", "yes", "t"]
        return bool(v)


class CoreSheetConfig(BaseModel):
    is_header: bool = Field(default=True)
    sheet_title_name: Optional[str] = ""
    sheet_name: str  # This is sheet_display_name from DB model
    is_format: bool = Field(default=False)
    column_mapping: Optional[Dict[str, str]] = Field(default_factory=dict)

    @field_validator("is_header", "is_format", mode="before")
    def parse_bool_str_sheet(cls, v):
        if isinstance(v, str):
            return v.lower() in ["true", "1", "yes", "t"]
        return bool(v)


class CoreExportTemplate(BaseModel):
    file_extension: str = "xlsx"
    separate: str = "|"
    sftp_conn: Optional[str] = None
    sftp_move: bool = Field(default=True)
    sheets: Dict[str, CoreSheetConfig] = Field(default_factory=dict)

    @field_validator("sftp_move", mode="before")
    def parse_bool_str_export(cls, v):
        if isinstance(v, str):
            return v.lower() in ["true", "1", "yes", "t"]
        return bool(v)


class DataTemplateConfigLoader:
    @staticmethod
    @provide_session
    def get_import_template(
        template_name: str, session: Session = None
    ) -> Optional[CoreImportTemplate]:
        db_template = (
            session.query(DBImportTemplate)
            .filter_by(template_name=template_name)
            .first()
        )
        if not db_template:
            return None

        # Convert DB model to Pydantic model
        # JSONB fields are already Python dicts/lists when loaded by SQLAlchemy
        return CoreImportTemplate(
            header=db_template.header_json or [],
            file_extension=db_template.file_extension,
            separate=db_template.separate,
            sftp_conn=db_template.sftp_conn,
            sftp_move=db_template.sftp_move,
            start_row=db_template.start_row,
            end_row=db_template.end_row,
            start_col=db_template.start_col,
            end_col=db_template.end_col,
            is_read_to_empty_row=db_template.is_read_to_empty_row,
            table_name=db_template.table_name,
            is_truncate_tmp_table=db_template.is_truncate_tmp_table,
            procedure_name=db_template.procedure_name,
            external_process=db_template.external_process,
            column_mapping=db_template.column_mapping_json or {},
        )

    @staticmethod
    @provide_session
    def get_all_import_templates(
        session: Session = None,
    ) -> Dict[str, CoreImportTemplate]:
        all_db_templates = session.query(DBImportTemplate).all()
        import_configs: Dict[str, CoreImportTemplate] = {}
        for db_template in all_db_templates:
            core_template = CoreImportTemplate(
                header=db_template.header_json or [],
                file_extension=db_template.file_extension,
                separate=db_template.separate,
                sftp_conn=db_template.sftp_conn,
                sftp_move=db_template.sftp_move,
                start_row=db_template.start_row,
                end_row=db_template.end_row,
                start_col=db_template.start_col,
                end_col=db_template.end_col,
                is_read_to_empty_row=db_template.is_read_to_empty_row,
                table_name=db_template.table_name,
                is_truncate_tmp_table=db_template.is_truncate_tmp_table,
                procedure_name=db_template.procedure_name,
                external_process=db_template.external_process,
                column_mapping=db_template.column_mapping_json or {},
            )
            import_configs[db_template.template_name] = core_template
        return import_configs

    @staticmethod
    @provide_session
    def get_export_template(
        template_name: str, session: Session = None
    ) -> Optional[CoreExportTemplate]:
        db_template = (
            session.query(DBExportTemplate)
            .filter_by(template_name=template_name)
            .first()
        )
        if not db_template:
            return None

        sheets_config: Dict[str, CoreSheetConfig] = {}
        for db_sheet in db_template.sheets:  # Uses the SQLAlchemy relationship
            sheets_config[db_sheet.sheet_name_key] = CoreSheetConfig(
                is_header=db_sheet.is_header,
                sheet_title_name=db_sheet.sheet_title_name,
                sheet_name=db_sheet.sheet_display_name,  # Map display_name to Pydantic's sheet_name
                is_format=db_sheet.is_format,
                column_mapping=db_sheet.column_mapping_json or {},
            )

        return CoreExportTemplate(
            file_extension=db_template.file_extension,
            separate=db_template.separate,
            sftp_conn=db_template.sftp_conn,
            sftp_move=db_template.sftp_move,
            sheets=sheets_config,
        )

    @staticmethod
    @provide_session
    def get_all_export_templates(
        session: Session = None,
    ) -> Dict[str, CoreExportTemplate]:
        all_db_templates = session.query(DBExportTemplate).all()
        export_configs: Dict[str, CoreExportTemplate] = {}
        for db_template in all_db_templates:
            sheets_config: Dict[str, CoreSheetConfig] = {}
            for db_sheet in db_template.sheets:
                sheets_config[db_sheet.sheet_name_key] = CoreSheetConfig(
                    is_header=db_sheet.is_header,
                    sheet_title_name=db_sheet.sheet_title_name,
                    sheet_name=db_sheet.sheet_display_name,
                    is_format=db_sheet.is_format,
                    column_mapping=db_sheet.column_mapping_json or {},
                )
            core_template = CoreExportTemplate(
                file_extension=db_template.file_extension,
                separate=db_template.separate,
                sftp_conn=db_template.sftp_conn,
                sftp_move=db_template.sftp_move,
                sheets=sheets_config,
            )
            export_configs[db_template.template_name] = core_template
        return export_configs


# Example usage (outside of Airflow tasks, you'd need to manage the session):
# if __name__ == '__main__':
#     # This part is for standalone testing and requires a way to get an SQLAlchemy session
#     # In Airflow tasks, @provide_session handles it.
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import sessionmaker
#     # Replace with your Airflow DB connection string
#     DATABASE_URL = "postgresql://airflow:airflow@localhost:5432/airflow"
#     engine = create_engine(DATABASE_URL)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#     local_session = SessionLocal()
#     try:
#         # Test fetching import config
#         # atom_config = DataTemplateConfigLoader.get_import_template("ATOM_POS_SET_TXN", session=local_session)
#         # if atom_config:
#         #     print("ATOM_POS_SET_TXN Import Config:")
#         #     print(atom_config.model_dump_json(indent=2))
#         # else:
#         #     print("ATOM_POS_SET_TXN not found.")
#
#         # Test fetching export config
#         # report_config = DataTemplateConfigLoader.get_export_template("ACQ_POS_ACCOUNTING_REPORT", session=local_session)
#         # if report_config:
#         #     print("\nACQ_POS_ACCOUNTING_REPORT Export Config:")
#         #     print(report_config.model_dump_json(indent=2))
#         # else:
#         #     print("ACQ_POS_ACCOUNTING_REPORT not found.")
#
#         all_imports = DataTemplateConfigLoader.get_all_import_templates(session=local_session)
#         print(f"\nFound {len(all_imports)} import templates.")
#         # for name, conf in all_imports.items():
#         #     print(f"Import Template: {name}")
#
#         all_exports = DataTemplateConfigLoader.get_all_export_templates(session=local_session)
#         print(f"Found {len(all_exports)} export templates.")
#
#     finally:
#         local_session.close()
