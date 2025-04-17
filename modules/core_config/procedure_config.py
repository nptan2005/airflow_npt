from typing import Dict, List, Optional

from pydantic import BaseModel, Field,field_validator

from .config_utils import ConfigUtils

# Define the parameter model
class Param(BaseModel):
    name: str
    type: str
    value: Optional[str] = Field(default=None)

# Define the procedure model
class ProcedureTemplate(BaseModel):
    in_params: List[Param] = Field(default_factory=list)
    out_params: List[Param] = Field(default_factory=list)
    is_retry: Optional[bool] = Field(default=False)
    conditions: Optional[dict] = Field(default=None)
    @field_validator('is_retry',  mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

# Define the complete configuration model
class _ProcedureConfig(BaseModel):
    procedures_template: dict[str, ProcedureTemplate]
    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)

import os

prc_config_path = os.path.join("configurable", "procedure_config.yaml")

# if _validate_yaml(module_config_path) == True:
prc_configuration = ConfigUtils.load_config(prc_config_path,_ProcedureConfig)