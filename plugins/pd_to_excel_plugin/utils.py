import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel
from typing import Any, Type
import yaml
import glob
import os
from datetime import datetime
from typing import Tuple

def read_dataframe_from_sql(query, conn_string):
    engine = create_engine(conn_string)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def create_sample_dataframe():
    data = {'Column A': [1, 2, 3], 'Column B': ['A', 'B', 'C']}
    return pd.DataFrame(data)

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
    

def remove_suffix(input_string: str, suffix: str) -> str:
    """Remove suffix from a string if present."""
    if input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def date_syntax(syntax: str = "[YYYYMMDD]") -> str:
    """Return the current date in the specified syntax format."""
    if syntax == "[YYYYMMDD]":
        return datetime.now().strftime("%Y%m%d")
    elif syntax == "[YYYYMMDDHHMMSS]":
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        return datetime.now().strftime(syntax)


def record_id(file_id: str, file_id_len: int, index: int, id_len: int = 20) -> int:
    """Generate a record ID with leading zeros."""
    rec_id = f'{file_id}{str(index + 1).zfill(id_len - file_id_len)}'
    return int(rec_id)


def get_syntax(file_name:str,split_character: str = "_") ->str:
    return file_name.split(split_character)[-1]


def process_syntax(file_name: str , split_character: str = "_",syntax: str = None) -> str:
    """Process the file name based on syntax and return the updated file name."""
    file_type = file_name.split('.')[-1] if '.' in file_name else ""
    syntax_part = get_syntax(file_name,split_character)
    if not syntax:
        syntax = syntax_part
    if syntax not in ["[YYYYMMDD]","[YYYYMMDDHHMMSS]"] or not syntax_part:
        return file_name
    if syntax in file_name:
        file_name = remove_suffix(file_name, split_character + syntax) + split_character + date_syntax(syntax_part)
    if file_type:
        file_name += "." + file_type
    return file_name


def full_file_name(file_name: str, file_type: str) -> str:
    """Return the full file name including type if not present."""
    return file_name if "." in file_name else f"{file_name}.{file_type}"


def get_script_and_name_arr(script: str, name: str) -> Tuple[list, list]:
    """
    Helper method to parse the script and name arrays.
    
    Args:
        script (str): Script string.
        name (str): Name string.
    
    Returns:
        Tuple[list, list]: Parsed script array and name array.
    """
    # Assuming the logic splits the input script and name into arrays
    script_arr = script.split(';') if script else []
    name_arr = name.split(',') if name else []
    return script_arr, name_arr

def create_directory(directory_path):
    """Tạo một thư mục."""
    os.makedirs(directory_path, exist_ok=True)


def report_folder_name(base_path):
    now = datetime.now()
    rpt_folder_name = now.strftime('%Y%m%d')
    return os.path.join(base_path, rpt_folder_name)
    

def create_file_name(base_path:str,file_pattern:str,syntax: str = "[YYYYMMDD]")->str:
    path = report_folder_name(base_path)
    create_directory(path)
    file_name = file_pattern
    if syntax:
        file_name = f"{file_name}_{date_syntax(syntax)}"
    return os.path.join(path, file_name)

def find_latest_file(search_pattern:str):
    # Lấy danh sách file khớp với pattern
    files = glob.glob(search_pattern)
    
    if not files:
        return None  # Nếu không tìm thấy file nào
    
    # Lấy file mới nhất dựa trên timestamp trong tên file
    latest_file = max(files, key=os.path.getctime)
    
    return latest_file

def find_latest_export_report_file(base_path:str,file_pattern:str,file_type:str):
    path = report_folder_name(base_path)
    # file_name = f"{file_pattern}_{TaskUtils.date_syntax('[YYYYMMDD]')}"
    # Tạo pattern để tìm file theo định dạng
    search_pattern = f"{os.path.join(path,file_pattern)}_*.{file_type}"
    return find_latest_file(search_pattern)

