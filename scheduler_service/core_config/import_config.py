from typing import Dict, List, Optional

from pydantic import BaseModel, Field,field_validator

from .config_utils import ConfigUtils


class _ImportTemplate(BaseModel):
    header: Optional[List[str]] = Field(default=None)
    file_extension: str = Field(default='xlsx')
    separate:Optional[str] = Field(default='|')
    sftp_conn:Optional[str] = Field(default=None)
    sftp_move:bool = Field(default=False)
    start_row: int = Field(default=2)
    end_row: Optional[int] = Field(default=0)
    start_col: int = Field(default=1)
    end_col: Optional[int] = Field(default=0)
    is_read_to_empty_row: bool = Field(default=False)
    table_name: str
    is_truncate_tmp_table: bool = Field(default=False)
    procedure_name: str = Field(default=None)
    external_process: Optional[str] = Field(default=None)
    column_mapping: Optional[Dict[str, str]] = Field(default=None)
    @field_validator('sftp_move','is_read_to_empty_row','is_truncate_tmp_table',  mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)



class _ImportConfig(BaseModel):
    import_template: Dict[str, _ImportTemplate]

    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
# end class _ModuleConfig

# @staticmethod
# # @cached(cache)
# # @functools.lru_cache(maxsize=1)
# def _load_config(file_path: str) -> _ModuleConfig:
#     try:
#         with open(file_path, 'r') as file:
#             config_dict = yaml.safe_load(file)
#         # Đảm bảo dữ liệu chứa khóa 'import_template'
#         return _ModuleConfig(**config_dict)
#     except FileNotFoundError:
#         print(f"File is not exist: {file_path}")
#         raise
#     except IOError as e:
#         print(f"Open file is Error: {e}")
#         raise

import os

import_config_path = os.path.join("configurable", "import_config.yaml")

import_configuration = ConfigUtils.load_config(import_config_path,_ImportConfig)

