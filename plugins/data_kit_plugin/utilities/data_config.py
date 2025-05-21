import base64
import os
import threading
from typing import Dict, Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, EmailStr
from data_kit_plugin.utilities.utils import  Utils as utils

load_dotenv()

from data_kit_plugin.multiAlgoCoder.encryptionManager import EncryptionManager
_manager = EncryptionManager()

class _OrlDatabaseConfig(BaseModel):
    host:str
    port:int
    service_name:str
    username:str
    password:str
    tns:str
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)

    @field_validator('password', mode='before')
    def decode_password(cls,value):
        tab_bytes = base64.b64decode(value)
        tab_str = tab_bytes.decode()

        return _manager.decrypt(tab_str)
# end class OrlDatabaseConfig


class _EmailConfig(BaseModel):
    host:str
    port:int
    email:str
    password:str
    mail_list:Optional[List[EmailStr]]
    is_ssl:Optional[bool] = Field(default=True)
    password_authen:Optional[bool] = Field(default=True)
    is_debug:Optional[bool] = Field(default=True)
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)

    @field_validator('is_ssl', 'password_authen','is_debug', mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

    @field_validator('password', mode='before')
    def decode_password(cls,value):
        tab_bytes = base64.b64decode(value)
        tab_str = tab_bytes.decode()

        return _manager.decrypt(tab_str)
# end class EmailConfig

class _sftpConfig(BaseModel):
    host:str
    port:int
    username:str
    password:str
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)

    @field_validator('password', mode='before')
    def decode_password(cls,value):
        tab_bytes = base64.b64decode(value)
        tab_str = tab_bytes.decode()

        return _manager.decrypt(tab_str)
# end class EmailConfig


class _FilePath(BaseModel):
    root:str
    path:str
    file:Optional[str] = None  # file có thể là None
    full_path:str = Field(default=None)
    _file_content:Optional[str] = None 
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
        self._post_init()

    def _post_init(self):
        self.root = os.getenv("CONFIG_PATH", "./config")
        # Tạo full_path và file_content sau khi khởi tạo model
        if self.file is None:
            self.full_path = os.path.join(self.root, self.path)
        else:
            self.full_path = os.path.join(self.root, self.path, self.file)
        self._file_content = self._read_file_content()

    @property
    def file_content(self):
        if self._file_content is None:
            self._file_content = self._read_file_content()
        return self._file_content
    
    def _read_file_content(self):
        # Đọc nội dung file
        if self.file is not None:
            try:
                return utils.read_file(self.full_path, 'r')
            except FileNotFoundError:
                raise FileNotFoundError(f"File template không tồn tại: {self.full_path}")
            except IOError as e:
                raise IOError(f"Lỗi xảy ra khi đọc file template: {e}")
        return None
# end FilePath

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
# end _SheetConfig

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
# end _ExportTemplate

class _ExportConfig(BaseModel):
    export_template: Dict[str,_ExportTemplate]

    def __init__(self, **data):
        super().__init__(**data)
# end _ExportConfig


class _AppConfig(BaseModel):
    oracle_database: Dict[str, _OrlDatabaseConfig]
    # encrytion_manager: EncryptionManager = manager
    email: Dict[str,_EmailConfig]
    file_path: Dict[str,_FilePath] 
    sftp: Dict[str,_sftpConfig]
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
# end class AppConfig
import yaml


class _AppConfigSingleton:
    _instance = None
    _lock: threading.Lock = threading.Lock()
    def __init__(self, **data):
        utils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
    def __new__(cls, config_path: str):
        with cls._lock:
            if cls._instance is None:
                config_data = cls._load_config(config_path)
                cls._instance = _AppConfig(**config_data)
        return cls._instance

    @staticmethod
    def _load_config(file_path: str) -> dict:
        try:
            with open(file_path, 'r') as file:
                config_dict = yaml.safe_load(file)
            return config_dict
        except FileNotFoundError:
            print(f"File is not exist: {file_path}")
            raise
        except IOError as e:
            print(f"Open file is Error: {e}")
            raise

# end class AppConfigSingleton
app_config_path = os.path.join(os.getenv("CONFIG_PATH", "./config"), "config.yaml")
configuration = _AppConfigSingleton(app_config_path)
export_config_path = os.path.join(os.getenv("CONFIG_PATH", "./config"), "export_config.yaml")
export_configuration = utils.load_config(export_config_path,_ExportConfig)