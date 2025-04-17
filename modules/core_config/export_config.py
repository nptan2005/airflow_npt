from typing import Dict, List, Optional

from pydantic import BaseModel, Field,field_validator

from .config_utils import ConfigUtils

class _SheetConfig(BaseModel):
    is_header: bool = Field(default=True, description="Flag to indicate if header is present")
    sheet_title_name: Optional[str] = Field("", description="Title of the sheet")
    sheet_name: str = Field(default=None, description="Name of the sheet in Excel")
    is_format: bool = Field(default=False, description="Flag to format")
    column_mapping: Dict[str, str] = Field(default=None, description="Mapping between DataFrame columns and Excel columns")

    @field_validator('is_header', 'is_format', mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

class _ExportTemplate(BaseModel):
    file_extension: str = "xlsx"
    separate: str = "|"
    sftp_conn: Optional[str] = Field(default=None)
    sftp_move: bool = Field(default=True, description="Flag to move file after SFTP upload")
    sheets: Dict[str, _SheetConfig] = Field(..., description="Dictionary of sheet configurations")

    @field_validator('sftp_move',  mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

class _ExportConfig(BaseModel):
    export_template: Dict[str,_ExportTemplate]

    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)

import os

export_config_path = os.path.join("configurable", "export_config.yaml")


export_configuration = ConfigUtils.load_config(export_config_path,_ExportConfig)