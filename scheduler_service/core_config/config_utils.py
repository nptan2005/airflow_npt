from typing import Any, Dict, Type
import inspect
import threading
from typing import Any, Dict, Type
import yaml
from pydantic import BaseModel
import yaml
class ConfigUtils:

    @staticmethod
    def read_file(filePath, mode='r'):
        try:
            with open(filePath, mode) as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'File not found: {filePath}')
        except IOError as e:
            raise IOError(f'Error reading file {filePath}: {e}')
        
    @staticmethod
    def check_import():
        """Check and don't allow import"""
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)
        
        if caller_module is None:
            return
        
        # Kiểm tra xem module gọi có phải là module nội bộ không
        caller_name = caller_module.__name__
        if not caller_name.startswith("core_config"):
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