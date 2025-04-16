import base64
import os
import threading
from typing import Dict, Optional, List

from pydantic import BaseModel, Field, field_validator,EmailStr

# from cachetools import cached, TTLCache
# cache = TTLCache(maxsize=1, ttl=3600)
# import functools

from .config_utils import ConfigUtils

# @staticmethod
# def bytes_2_base64(value:bytes) -> str:
#     return base64.b64encode(value).decode()
# end convertBytesToBase64
from multiAlgoCoder import EncryptionManager
_manager = EncryptionManager()

class _OrlDatabaseConfig(BaseModel):
    host:str
    port:int
    service_name:str
    username:str
    password:str
    tns:str
    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
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
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
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
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
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
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
        self._post_init()

    def _post_init(self):
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
                return ConfigUtils.read_file(self.full_path, 'r')
            except FileNotFoundError:
                raise FileNotFoundError(f"File template không tồn tại: {self.full_path}")
            except IOError as e:
                raise IOError(f"Lỗi xảy ra khi đọc file template: {e}")
        return None

   
    
# end FilePath


class _AppConfig(BaseModel):
    oracle_database: Dict[str, _OrlDatabaseConfig]
    # encrytion_manager: EncryptionManager = manager
    email: Dict[str,_EmailConfig]
    file_path: Dict[str,_FilePath] 
    sftp: Dict[str,_sftpConfig]
    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
        super().__init__(**data)
# end class AppConfig
import yaml


class _AppConfigSingleton:
    _instance = None
    _lock: threading.Lock = threading.Lock()
    def __init__(self, **data):
        ConfigUtils.check_import()  # Kiểm tra khi khởi tạo
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

app_config_path = os.path.join("configurable", "config.yaml")
configuration = _AppConfigSingleton(app_config_path)


class EnvConfig(BaseModel):
    config_cycle_time: int
    config_sleep_time: int
    service_temporary_stop:bool
    service_running:bool
    is_email_summary:bool
    task_prc: str
    his_prc: str
    import_log_prc:str
    import_status_prc:str
    orl_sys_tbl_col:str
    orl_sys_tbl_tbl:str
    default_orl_db_conn:str
    default_sftp_conn:str
    default_email_conn:str
    email_template:str
    default_imp_key:str
    default_exp_key:str
    default_attchment_path:str
    default_archive_path:str
    default_archive_sftp:str
    default_archive_imp:str
    default_ext_module:str

    @field_validator('is_email_summary','service_running','service_temporary_stop', mode='before')
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ['true', '1', 'yes']
        return bool(v)

class AppEnvConfig(BaseModel):
    env: str
    UAT: Optional[EnvConfig] = None
    PROD: Optional[EnvConfig] = None

    def get_env_config(self):
        """Lấy cấu hình dựa trên môi trường từ khóa 'env'."""
        env_config = getattr(self, self.env, None)
        if not env_config:
            raise ValueError(f"Cấu hình cho môi trường '{self.env}' không tồn tại.")
        return env_config
    
def load_config(config_file: str, config_class: BaseModel):
    import yaml
    with open(config_file, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_class(**config_data)

srv_config_file = os.path.join("configurable", "appconfig.yaml")
app_service_config = load_config(srv_config_file, AppEnvConfig).get_env_config()
