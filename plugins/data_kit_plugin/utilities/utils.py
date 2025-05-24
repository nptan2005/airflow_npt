from pydantic import BaseModel
from typing import Any, Type
import yaml
from sqlalchemy import create_engine
import pandas as pd
import base64
import binascii
import datetime
import json
import os
import shutil
from pathlib import Path
import inspect
import threading

import hexdump
class Utils:
    
    @staticmethod
    def read_dataframe_from_sql(query, conn_string):
        engine = create_engine(conn_string)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df

    
    @staticmethod
    def get_current_timestamp() -> str:
        """Trả về timestamp hiện tại."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def getCurrentDateTime() -> datetime:
        return datetime.datetime.now()

    @staticmethod
    def parseDate(dateStr):
        try:
            format_string = "%d/%m/%y %H.%M.%S"
            return datetime.datetime.strptime(dateStr, format_string)
        except ValueError:
            raise ValueError("Error: Input Text: {dateStr} is invalid, can't covert to Date")
            return None
        
    @staticmethod
    def isNumber(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError as e:
            # self._logNote += f"Can not convert string to float {e}"
            return False
    @staticmethod
    def convertStrToNumber(s: str) -> float:
        if Utils.isNumber(s):
            return float(s)
        else:
            return 0

    @staticmethod
    def get_file_size(file_path):
        """Trả về kích thước của file."""
        if os.path.isfile(file_path):
            return os.path.getsize(file_path)
        else:
            return 0

    @staticmethod
    def create_directory(directory_path):
        """Tạo một thư mục."""
        os.makedirs(directory_path, exist_ok=True)

    @staticmethod
    def checkPathExists(path: str) -> bool:
        """
        Kiểm tra xem đường dẫn có tồn tại hay không.

        Args:
            path (str): Đường dẫn cần kiểm tra.

        Returns:
            bool: True nếu đường dẫn tồn tại, False nếu không.
        """
        return os.path.exists(path)
    
    @staticmethod
    def checkPathIsDir(path:str) -> bool:
        return os.path.isdir(path)
    
    @staticmethod
    def checkFileIsExist(path:str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def readFile(filePath, mode = 'r'):
        """Read File
        ##### Tham so mode:
        'r': Mở file để đọc dữ liệu văn bản (text data). Đây là chế độ mặc định.
        'w': Mở file để ghi dữ liệu văn bản. Nếu file đã tồn tại, nội dung của file sẽ bị ghi đè.
        'a': Mở file để ghi dữ liệu văn bản. Nội dung mới sẽ được thêm vào cuối file.
        'x': Mở file để tạo file mới. Nếu file đã tồn tại, sẽ xảy ra lỗi.
        'b': Mở file ở chế độ nhị phân. Chế độ này có thể kết hợp với các chế độ khác, chẳng hạn như 'rb' (đọc nhị phân), 'wb' (ghi nhị phân), v.v.
        '+': Mở file để đọc và ghi.
        """
        with open(filePath, mode) as f:
            return f.read()

    @staticmethod
    def writeFile(value, filePath, mode = 'w'):
        """Write File
        ##### Tham so mode:
        'r': Mở file để đọc dữ liệu văn bản (text data). Đây là chế độ mặc định.
        'w': Mở file để ghi dữ liệu văn bản. Nếu file đã tồn tại, nội dung của file sẽ bị ghi đè.
        'a': Mở file để ghi dữ liệu văn bản. Nội dung mới sẽ được thêm vào cuối file.
        'x': Mở file để tạo file mới. Nếu file đã tồn tại, sẽ xảy ra lỗi.
        'b': Mở file ở chế độ nhị phân. Chế độ này có thể kết hợp với các chế độ khác, chẳng hạn như 'rb' (đọc nhị phân), 'wb' (ghi nhị phân), v.v.
        '+': Mở file để đọc và ghi.
        """
        with open(filePath, mode) as f:
            f.write(value)

    @staticmethod
    def move_and_rename_file(source_path: str, destination_file_path: str):
        """
        Di chuyển và đổi tên file.

        Args:
            source_path (str): Đường dẫn đến file nguồn.
            destination_path (str): Đường dẫn đến thư mục đích.
        """

        # Kiểm tra xem file nguồn có tồn tại hay không
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File don't exist: {source_path}")

        # Di chuyển và đổi tên file
        try:
            shutil.move(source_path, destination_file_path)
            # print(f"File move is ok!!: {destination_file_path}")
        except Exception as e:
            # print(e)
            raise e
    # end move_and_rename_fil

    @staticmethod
    def move_folder_and_files(source_folder: str, destination_folder: str):
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"File don't exist: {source_folder}")
        
        try:
            # Di chuyển tất cả các tệp tin và thư mục con
            for item in os.listdir(source_folder):
                source_path = os.path.join(source_folder, item)
                destination_path = os.path.join(destination_folder, item)
                if os.path.isdir(source_path):
                    shutil.move(source_path, destination_path)
                

            # Xóa thư mục nguồn sau khi di chuyển
            os.rmdir(source_folder)

        except Exception as e:
            # print(e)
            raise e
    # end move_folder_and_files

    @staticmethod
    def checkTypeOfValue(value):
        """Check Type of Key"""
        if isinstance(value, bytes):
            return "bytes"
        elif isinstance(value, str):
            return "str"
        else:
            return "unknown"
        
    @staticmethod
    def convertBytesToBase64(value:bytes) -> str:
        return base64.b64encode(value).decode()
    
    @staticmethod
    def convertStrToBytes(value: str) -> bytes:
        """Convert Value, string Type to bytes."""
        try:
            return value.encode()  # Sử dụng encode() để chuyển đổi string sang bytes
        except UnicodeDecodeError:
            raise ValueError("Invalid value. Value Must ASCII Character.")
        
    @staticmethod   
    def convertHexToBytes(value: str) -> bytes:
        """Convert Value, Hex format to bytes."""
        try:
            return binascii.unhexlify(value)  # Sử dụng unhexlify() để chuyển đổi hex sang bytes
        except binascii.Error:
            raise ValueError("Invalid Value. Value Must HEX Character.")

    @staticmethod    
    def convertBase64ToBytes(value: str) -> bytes:
        """Convert value, Base64 format to bytes."""
        try:
            return base64.b64decode(value)  # Sử dụng b64decode() để chuyển đổi base64 sang bytes
        except binascii.Error:
            raise ValueError("Invalid value. Value Must Base64 Character.")
        
    @staticmethod
    def hexFormat(value:str) -> str:
        return hexdump.hexdump(value)
    
    @staticmethod 
    def convertBytesToAscii(value:bytes) -> str:
        if value is not None:
            return value.decode("ascii", errors="ignore")
        return None
    
    @staticmethod 
    def convertBytesToHex(value:bytes) -> str:
        if value is not None:
            return binascii.hexlify(value).decode('utf-8')
        return None
    
    @staticmethod 
    def convertHexToInt(value:str) -> int:
        if value is not None:
            return int(value, 16)
        return None
    
    
    @staticmethod 
    def convertBytesToUnicode(value:bytes) -> str:
        if value is not None:
            return value.decode("utf-8", errors="ignore")
        return None
    
    @staticmethod
    def strToBool(s:str) -> bool:
        return s.lower() in ['true', '1', 't', 'y', 'yes']
    
    @staticmethod
    def readJsonFromPath(filePath:str) -> dict:
        try:
            with open(filePath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            FileNotFoundError(f"File config is not Exist: {filePath}")
            raise
        except PermissionError:
            raise PermissionError(f"Don't not Permission: {filePath}")
        except Exception as e:
            Exception(f"Json Read file: Error on reading file: {e}")
            raise
    @staticmethod
    def check_filename_type(filename):
        """"
            print(check_filename_type("/home/user/documents/file.txt"))  # Output: Full path
            print(check_filename_type("documents/file.txt"))             # Output: Contains folder
            print(check_filename_type("file.txt"))                       # Output: Filename only
        """
        path = Path(filename)
        if path.is_absolute():
            return "Full path"
        elif path.parent != Path('.'):
            return "Contains folder"
        else:
            return "Filename only"
        
    @staticmethod
    def check_import():
        """Check and don't allow import"""
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)
        
        if caller_module is None:
            return
        
        # Kiểm tra xem module gọi có phải là module nội bộ không
        caller_name = caller_module.__name__
        if not caller_name.startswith("data_kit_plugin"):
            raise ImportError(f"Module {caller_name} is not allowed to import this module")
        
    @staticmethod
    def validate_yaml(file_path: str) -> bool:
        try:
            with open(file_path, 'r') as file:
                yaml.safe_load(file)
            # print("YAML file is valid.")
            return True
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print(f"YAML error at line {mark.line + 1}, column {mark.column + 1}:")
                print(exc)
            else:
                print("YAML error:", exc)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return False




    @staticmethod
    def load_config(file_path: str, config_class: Type[BaseModel]) -> Any:
        """
        Tải cấu hình từ file YAML và trả về đối tượng của lớp cấu hình.

        :param file_path: Đường dẫn đến file YAML.
        :param config_class: Lớp cấu hình để tạo đối tượng từ dữ liệu YAML.
        :return: Đối tượng của lớp cấu hình.
        """
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                config_dict = yaml.safe_load(file)
            if not isinstance(config_dict, dict):
                raise ValueError("Invalid YAML file format: expected a dictionary.")
            # Tạo đối tượng của lớp cấu hình từ dữ liệu
            return config_class(**config_dict)
        except FileNotFoundError:
            print(f"File is not exist: {file_path}")
            raise
        except IOError as e:
            print(f"Open file is Error: {e}")
            raise
        except yaml.YAMLError as e:
            print(f"YAML parsing error: {e}")
            raise
        except ValueError as e:
            print(f"Value error: {e}")
            raise
    
class _BaseModelCheck:
    """"Don't allow import"""
    @staticmethod
    def _check_import():
        import inspect
        import sys

        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)
        
        if caller_module.__name__ != "allowed_module_name":
            raise ImportError(f"Module {caller_module.__name__} is not allowed to import this module")
        
class _SingletonInstance:
    _instances = {}
    _lock: threading.Lock = threading.Lock()
    # def __init__(self, **data):
    #     _check_import()  # Kiểm tra khi khởi tạo
    #     super().__init__(**data)
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__new__(cls, *args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
# end class SingletonBase