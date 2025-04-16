import os
import sys
from datetime import datetime
from iso8583_kit import JCBParser
from .iso8503_utils import ISO8583Field,LoggerStream,ISO8583Print
from utilities import Utils as utils
from core_config import configuration,app_service_config
from utilities import Logger

class JCBBatchDump:
    def __init__(self, file_name: str,is_dump_to_file: bool = True,is_logger:bool=False):
        self.logger = Logger().logger
        self._file_name = file_name
        self._is_dump_to_file = is_dump_to_file
        self._is_logger = is_logger
        try:
            self._config_path_imp = configuration.file_path[app_service_config.default_imp_key]
            self._path = 'ISO_BATCH'
            self._reportPath = os.path.join(self._config_path_imp.root,self._config_path_imp.path,self._path)
            self._fileReadPath = os.path.join (self._reportPath, self._file_name)
            self.logger.info(f'Process batch file: {self._fileReadPath}')
            self._file_content = utils.readFile(self._fileReadPath,'rb')
            self._msg_len = len(self._file_content)
            self.logger.info(f'Length of file content: {self._msg_len}')
            self._parsor = JCBParser()
            self._iso_dict = self._parsor.iso_decode(self._file_content)
            
            self._config_path_exp = configuration.file_path[app_service_config.default_exp_key]
            self._export_father_path = os.path.join (self._config_path_exp.root, self._config_path_exp.path)
        except Exception  as e:
            self.logger.exception(f'Init error {e}')
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()

    def __del__(self):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_file_name', '_config',  '_reportPath', '_path',
            '_fileReadPath','_file_content','_msg_len',
            "_parsor",'_iso_dict','_config_path_imp','_config_path_exp'
            'logger','_export_father_path','_is_logger','_is_dump_to_file'
        ]
        for attr in attributes:
            setattr(self, attr, None)
            
    @property
    def file_name(self):
        return self._file_name
    
    @property
    def file_content(self):
        return self._file_content
    
    @property
    def msg_len(self):
        return self._msg_len
    
    @property
    def parsor(self):
        return self._parsor
    
    @property
    def iso_dict(self):
        return self._iso_dict
    
    def fullPath(self):
        now = datetime.now()
        try:
            _file_name_base, _file_extension = os.path.splitext(os.path.basename(self._file_name))
            _fileName = _file_name_base + '_' + now.strftime("%Y%m%d_%H%M%S") + _file_extension
            _folderName = now.strftime("%Y%m%d")
            _path = os.path.join (self._export_father_path, _folderName) 
            utils.create_directory(_path)
            return os.path.join (_path, _fileName)
        except Exception  as e:
            self.logger.exception(f'Create export path is Error {e}')
            return os.path.join(self._export_father_path, _fileName)

    def raw_iso_field_dump(self,iso_dict:dict[int,dict[str,ISO8583Field]]):
        if self._is_logger or self._is_dump_to_file:
            stream = LoggerStream(self._is_dump_to_file,self._is_logger)
        else:
            stream = sys.stdout

        indent = 120
        sub_indent = 20
        title = 'Parse and dump ISO batch file into detailed fields'
        ISO8583Print.msg_to_stream(f"{'=' * indent}",stream)
        ISO8583Print.msg_to_stream(f"{'>' * 10}{title:50s}{'<' * 10}",stream)
        ISO8583Print.msg_to_stream(f"{'*' * indent}",stream)
        for num, parsed_data in iso_dict.items():
            
            ISO8583Print.msg_to_stream(f'Message Number: {num}',stream)
            print(f"{'*' * sub_indent}",stream)
            for key, isoData in parsed_data.items():
                ISO8583Print.print_raw_iso_field(isoData,stream, 120)

            ISO8583Print.msg_to_stream(f"{'-' * indent}",stream)
            
        
        if self._is_dump_to_file:
            stream.writeToFile(self.fullPath())
        
        if self._is_logger:
            # Đảm bảo flush buffer sau khi hoàn thành
            stream.writeToLog()
        stream.flush()
    # raw_iso_field_dump

    def iso_to_stream(self,iso_dict:dict[int,dict[str,ISO8583Field]]):
        if self._is_logger or self._is_dump_to_file:
            stream = LoggerStream(self._is_dump_to_file,self._is_logger)
        else:
            stream = sys.stdout

        indent = 120
        title = 'Parse and dump ISO batch file into detailed fields'
        ISO8583Print.msg_to_stream(f"{'*' * indent}",stream)
        ISO8583Print.msg_to_stream(f"{'>' * int((indent - len(title))/2)}{title:50s}{'<' * int((indent - len(title))/2)}",stream)
        ISO8583Print.msg_to_stream(f"|{'*' * (indent-2)}|",stream)
        ISO8583Print.msg_to_stream(f">File Name: {self._file_name:168s}",stream)
        ISO8583Print.msg_to_stream(f">Read Path: {self._reportPath:168s}",stream)
        ISO8583Print.msg_to_stream(f">Total message length: {str(self._msg_len):158s}",stream)
        ISO8583Print.msg_to_stream(f"|{'-' * (indent-2)}|",stream)
        for num, parsed_data in iso_dict.items():
            
            ISO8583Print.msg_to_stream(f"| {' ' * 48}Message Number: {str(num):4s} {' ' * 48}|",stream)
            ISO8583Print.msg_to_stream(f"|{'-' * (indent-2)}|",stream)
            ISO8583Print.msg_to_stream(f"|{'Field':7s}{' | Description':<51} | {'Value':56} |",stream)
            ISO8583Print.msg_to_stream(f"|{'-' * (indent-2)}|",stream)
            for key, isoData in parsed_data.items():
                ISO8583Print.print_iso_field(isoData,stream, 120)

            ISO8583Print.msg_to_stream(f"|{'-' * (indent-2)}|",stream)
        
        
        if self._is_dump_to_file:
            stream.writeToFile(self.fullPath())
        
        if self._is_logger:
            # Đảm bảo flush buffer sau khi hoàn thành
            stream.writeToLog()
        stream.flush()
        
    # iso_to_stream
    
    def iso_dump(self):
        self.iso_to_stream(self._iso_dict)
        self.logger.info(f"Dump jcb batch file is successfully {self._file_name}")