import os
from typing import Tuple,Optional,Dict,List
import pandas as pd
from utilities import Logger
from core_config import configuration,export_configuration,app_service_config
from db_conn import OracleConn
from data_kit import DataConstant,DataExport
from ..model import Task
from ..task_utils import TaskUtils


class TaskExporter:
    def __init__(self, task:Task,is_export_to_server:bool = False):
        self.task = task
        self._config = configuration.file_path[app_service_config.default_exp_key]
        if is_export_to_server:
            self.export_folder_name = self.task.src_folder_name
            self.export_file_name = self.task.src_file_name
            self.export_file_type = self.task.src_file_type
        else:
            self.export_folder_name = self.task.dst_folder_name
            self.export_file_name = self.task.dst_file_name
            self.export_file_type = self.task.dst_file_type


        self._base_path = os.path.join(self._config.root, self._config.path,self.export_folder_name)
        self._file_name = TaskUtils.create_file_name(base_path=self._base_path,file_pattern=f'{self.task.frequency}_{self.export_file_name}', syntax ="[YYYYMMDDHHMMSS]")

        self._attach_file = None
        self._config_key_name = task.config_key_name
        self._config_template = None
        if self._config_key_name:
            self._config_template = export_configuration.export_template[self._config_key_name]

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
            'task', '_config', '_base_path', '_attach_file','_file_name',
            '_config_key_name',
            '_config_template',
            'logger',
            'export_folder_name',
            'export_file_name',
            'export_file_type'
        ]
        for attr in attributes:
            setattr(self, attr, None)


    @property
    def attach_file(self):
        return self._attach_file
    
    

    

    # end _transform_df_array
    def _data_array(self) -> Tuple[List[pd.DataFrame], str]:
        data_arr = []
        note = ''
        
        try:
            with OracleConn(self.task.connection_string, self.task.task_time_out) as db:
                data_arr = db.execute_script_list(self.task.script)
        except Exception as e:
            note += f'Execute script array {self.task.script} encountered an error'
            self.logger.exception(f'Execute script array {self.task.script} encountered an error: {e}')

        return data_arr, note

    # end _data_array

    def _check_valid(self) -> Tuple[bool,str,list]:
        """
        check input value
        return is valid, note, data_arr
        """
        note = ''
        data_arr = []
        
        if not self.export_file_name or not self.export_folder_name:
            self.logger.info(f'| Configuration is not correct! fileName or folderName is missing! fileName={self.export_file_name}, folderName={self.export_folder_name}')
            return False, note, data_arr
        
        if not self.task.script or not self.task.output_name:
            self.logger.info(f'| Configuration is not correct, script={self.task.script}, outputArray={self.task.output_name}')
            return False, note, data_arr
        
        if len(self.task.script) != len(self.task.output_name):
            self.logger.info(f'| Configuration is not correct! scriptArr length={len(self.task.script)}, nameArr length={len(self.task.output_name)}')
            return False, note, data_arr
        
        # Step 3: Execute script and retrieve data
        data_arr, note = self._data_array()

        if not data_arr:
            self.logger.info(f'| Script execution failed, script={self.task.script}')
            return False, note, data_arr
        
        return True, note, data_arr
    # end _check_valid


    # --- Export file ---
    def export(self) -> Tuple[bool, str, Optional[Exception]]:
        """
        Export file from a DataFrame.
        
        Args:
            task (Task): Task object containing the necessary configuration.
        
        Returns:
            Tuple[bool, str, Exception]: Status (0 or 1), processing notes, and exception (if any).
        """
        note = ''
        is_completed = 0
        error = None

        try:
            is_valid, note, data_arr = self._check_valid()
            if is_valid:
                # Step 4: Format file name and path
                
                self.logger.info(f'Export: {self.export_file_name} | Path: {self.export_folder_name}')

                # Step 5: Write data to file
                with DataExport(export_data=data_arr,
                                export_name=self.task.output_name, 
                                file_name=self._file_name,
                                template=self.task.config_key_name if self.task.config_key_name else DataConstant.DEFAULT,
                                file_extension=self.export_file_type) as writer:
                    writer.to_file()
                    is_completed = writer.is_successful
                    note += writer.note
                    if self.task.is_attachment:
                        self._attach_file = f'{self._file_name}.{writer.file_type}'
        except Exception as e:
            note += f'Export process encountered an error'
            self.logger.exception(f'Export process encountered an error, {e}')

        return is_completed, note, error

    
    
