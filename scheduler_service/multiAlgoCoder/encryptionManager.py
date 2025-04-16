import os
from utilities.utils import Utils as utils
import threading
from typing import Dict
from pydantic import BaseModel, Field
from .decoder import decoder


class _SingletonBase:
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__new__(cls, *args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
# end class SingletonBase

class EncryptionManager(BaseModel, _SingletonBase):
    """
    Manage Pwd encryption
    """
    data_folder: str = Field(default=os.path.join("bin", "data"))
    iv_folder: str = Field(default=os.path.join("bin", "iv"))
    master_key_file:str = Field(default=os.path.join("bin", "key","master_key_ase.bin"))
    master_key:bytes = Field(default_factory=bytes)
    iv_master_key_file:str = Field(default=os.path.join("bin", "iv","master_key_iv_ase.bin"))
    iv_master_key:bytes = Field(default_factory=bytes)
    key_file:str = Field(default=os.path.join("bin", "key","key_ase.bin"))
    key:bytes = Field(default_factory=bytes)
    encryption_dict: Dict[str, bytes] = Field(default_factory=dict)
    iv_dict: Dict[str, bytes] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)
        self.__load_and_update_data_and_iv()
        self.__get_master_key()
        self.__get_iv_master_key()
        self.__get_key()

    def __get_master_key(self):
        self.master_key = utils.readFile(self.master_key_file, 'rb')

    def __get_iv_master_key(self):
        self.iv_master_key = utils.readFile(self.iv_master_key_file, 'rb')

    def __get_key(self):
        self.key = utils.readFile(self.key_file,'rb')


    @property
    def encode_data_folder(self):
        return self.data_folder
    
    @property
    def encode_iv_folder(self):
        return self.iv_folder

    def _load_files_from_folder(self, folder: str, dict_to_update: Dict[str, bytes]) -> None:
        """Tải dữ liệu từ thư mục vào dict."""
        for file_name in os.listdir(folder):
            if file_name.endswith('.bin'):
                key_prefix = file_name.rsplit('_', 2)[0]
                file_path = os.path.join(folder, file_name)
                if key_prefix not in dict_to_update:
                    dict_to_update[key_prefix] = utils.readFile(file_path, 'rb')

    def __load_and_update_data_and_iv(self):
        """Tải dữ liệu mã hóa và IV từ thư mục hoặc cập nhật nếu có file mới."""
        self._load_files_from_folder(self.data_folder, self.encryption_dict)
        self._load_files_from_folder(self.iv_folder, self.iv_dict)

    def update_data_and_iv(self):
        """Cập nhật dữ liệu và IV nếu có file mới."""
        # Cập nhật dữ liệu mã hóa
        self._load_files_from_folder(self.data_folder, self.encryption_dict)
        
        # Cập nhật IV
        self._load_files_from_folder(self.iv_folder, self.iv_dict)

    def update_encrypted_data(self,key_prefix: str):
        path = os.path.join("bin", "data", f"{key_prefix}_encryption_data.bin")
        self.encryption_dict[key_prefix] = utils.readFile(path, 'rb')

    def get_encrypted_data(self, key_prefix: str) -> bytes:
        if key_prefix not in self.encryption_dict:
            self.__update_encrypted_data(key_prefix)
        return self.encryption_dict.get(key_prefix)

    def update_iv(self,key_prefix: str):
        path = os.path.join("bin", "iv", f"{key_prefix}_iv_key_ase.bin")
        self.iv_dict[key_prefix] = utils.readFile(path, 'rb')

    def get_iv(self, key_prefix: str) -> bytes:
        if key_prefix not in self.iv_dict:
            self.__update_iv(key_prefix)
        return self.iv_dict.get(key_prefix)
    
    
    def decrypt(self, key_prefix: str) -> bytes:
        data = self.get_encrypted_data(key_prefix)
        iv = self.get_iv(key_prefix)
        decode_data = None
        if data is None or iv is None:
            raise ValueError("Key or IV not found for the given prefix")
        with decoder(self.master_key, None, self.iv_master_key) as de:
            de.AESEncryptKey = self.key
            decode_data = de.AESDecryptData(data,iv)
        return decode_data
# end class EncryptionManager