import os
from typing import Tuple,Optional,Dict,List
from data_kit import  FileArchiver
from conn_kit import SftpConn
from utilities import Logger
from core_config import configuration,app_service_config
from ..model import Task
from ..task_utils import TaskUtils


class TaskSFTP:
    def __init__(self, task:Task,src_path:str = None,dst_path:str = None):
        self.task = task
        self.src_path = src_path
        self.dst_path = dst_path
        self._destination_path = None
        self._source_path = None
        self._is_remove_src = False
        self._destination_archive = os.path.join(
            configuration.file_path[app_service_config.default_archive_sftp].root,
            configuration.file_path[app_service_config.default_archive_sftp].path
        )
        self._connection_str = task.connection_string
        self.logger = Logger().logger
       
    def __enter__(self):
        return self

    def __del__(self):
        self._clear_attributes()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            'task', 'src_path','dst_path','_source_path',
            '_destination_path','_is_remove_src',
            '_connection_str',
            '_sftp_root_path',
            'logger'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    @property
    def sftp_root_path(self):
        return self._sftp_root_path
    
    @sftp_root_path.setter
    def sftp_root_path(self,value):
        self._sftp_root_path = value

    @property
    def connection_str(self):
        return self._connection_str
    
    @connection_str.setter
    def connection_str(self,value):
        self._connection_str = value

    @property 
    def destination_path(self):
        return self._destination_path

    
    @property
    def source_path(self):
        return self._source_path
    
    @property
    def is_remove_src(self):
        return self._is_remove_src
    @is_remove_src.setter
    def is_remove_src(self,value):
        self._is_remove_src = value

    def download(self) -> Tuple[bool,str,Optional[Exception]]:
        note = ''
        is_completed = False
        error = None
        try:
            if not self.dst_path:
                imp_path_config = configuration.file_path[app_service_config.default_imp_key]
                imp_base_path = os.path.join(imp_path_config.root, imp_path_config.path,self.task.dst_folder_name)
                dowload_file_name = TaskUtils.full_file_name(
                    TaskUtils.process_syntax(f'{self.task.frequency}_{self.task.dst_file_name}'), self.task.dst_file_type
                )
                self._destination_path = os.path.join(imp_base_path, dowload_file_name)
            else:
                self._destination_path = self.dst_path

            
            if not self.src_path:
                src_file_name = TaskUtils.full_file_name(
                    TaskUtils.process_syntax(self.task.src_file_name), self.task.src_file_type
                )
                self._source_path = os.path.join(self.task.src_folder_name,src_file_name)
            else:
                self._source_path = self.src_path
            
            with SftpConn(self._connection_str, self._source_path, self._destination_path) as sftp:
                sftp.download_file()
                is_completed = sftp.is_successful
                
                if is_completed and self._is_remove_src:
                    sftp.delete_file()
        except Exception as e:
            note += f'sFTP:download process encountered an error'
            self.logger.exception(f'sFTP:download process encountered an error: {e}')

        return is_completed, note, error
    # end download

    def convert_file_suffix(self,config_file_name:str):
        config_syntax = TaskUtils.get_syntax(config_file_name)
        if config_syntax == "[YYYYMMDDHHMMSS]":
            return config_file_name.replace("[YYYYMMDDHHMMSS]","[YYYYMMDD]")
        return config_file_name

    def upload(self) -> tuple[bool,str,Optional[Exception]]:
        note = ''
        is_completed = False
        error = None
        try:
            if not self.src_path:
                export_path_config = configuration.file_path[app_service_config.default_exp_key]
                export_base_path = os.path.join(export_path_config.root, export_path_config.path,self.task.src_folder_name)
                _src_file_name = self.convert_file_suffix(self.task.src_file_name)
                export_file_name = TaskUtils.process_syntax(file_name=f'{self.task.frequency}_{_src_file_name}')
                self._source_path = TaskUtils.find_latest_export_report_file(base_path=export_base_path,file_pattern=export_file_name,file_type=self.task.src_file_type)
            else:
                self._source_path = self.src_path
  
            if not self.dst_path:
                upload_file_name = TaskUtils.full_file_name(
                    TaskUtils.process_syntax(f'{self.task.frequency}_{self.task.dst_file_name}'), self.task.dst_file_type
                )
                self._destination_path = os.path.join(self.task.dst_folder_name, upload_file_name)
            else:
                self._destination_path = self.dst_path
            
            with SftpConn(self._connection_str, self._source_path, self._destination_path) as sftp:
                
                sftp.upload_file()
                is_completed = sftp.is_successful
                if is_completed and self._is_remove_src:
                    note_archive = self.archive_file(self._source_path)
                    if note_archive:
                        note += note_archive
               
        except Exception as e:
            note += f'sFTP:upload process encountered an error'
            self.logger.exception(f'sFTP:upload process encountered an error: {e}')
        return is_completed, note, error
    # end upload

    def archive_file(self,file_name:str) -> str:
        note_archive = None
        with FileArchiver(file_name, self._destination_archive) as archiver:
            note_archive = archiver.archive_file
        return note_archive
    # end archive_file
    