import os
from data_kit import  FileArchiver,FileImport,DataConstant,ExecuteCls
from db_conn import OracleConn
from core_config import configuration,app_service_config
from utilities import Logger
from ..model import Task
from ..task_utils import TaskUtils


class TaskImporter:
    def __init__(self,task:Task):
        """Initialize the TaskImporter with destination archive path."""
        self._destination_archive = os.path.join(
            configuration.file_path[app_service_config.default_archive_imp].root,
            configuration.file_path[app_service_config.default_archive_imp].path
        )
        self.task = task

        self._config_path = configuration.file_path[app_service_config.default_imp_key]

        self._file_name = self.get_file_name(os.path.join(self._config_path.root, 
                                                         self._config_path.path,
                                                         self.task.src_folder_name),
                                                         f'{self.task.frequency}_{self.task.src_file_name}',
                                                         self.task.src_file_type)
        
        self.logger = Logger().logger
        


    def __enter__(self):
        return self
    def __del__(self):
        self._clear_attributes()	

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources."""
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_destination_archive', 'task', '_file_name',
              '_config_path',
              'logger'
              ]
        for attr in attributes:
            setattr(self, attr, None)

    @property 
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self,value):
        self._file_name = value

    def get_file_name(self, file_path:str, config_file_name:str, config_file_type:str):
        config_syntax = TaskUtils.get_syntax(config_file_name)
        if config_syntax == "[YYYYMMDDHHMMSS]":
            config_file_name = config_file_name.replace("[YYYYMMDDHHMMSS]","[YYYYMMDD]")
            convert_file_name = TaskUtils.process_syntax(config_file_name)
            search_pattern = os.path.join(os.path.join(file_path,f'{convert_file_name}_*.{config_file_type}'))
            return  TaskUtils.find_latest_file(search_pattern)
        else:
            file_name = TaskUtils.full_file_name(
                TaskUtils.process_syntax(config_file_name), config_file_type
            )
            return os.path.join(os.path.join(file_path,file_name))
    # end get_file_name


    def import_file(self) -> tuple[bool, str, Exception]:
        """
        Read file and process DataFrame.

        Args:
            task (Task): The task containing file and configuration details.

        Returns:
            tuple[bool, str, Exception]: Status, note, and error if any.
        """
        note = ''
        is_completed = False
        error = None

        try:
            
            with FileImport(fileName=self._file_name, 
                            templateName=self.task.config_key_name) as file_import:
                # step 1: read file to pd
                df_imp = file_import.read_file_to_df()
                if df_imp is None or len(df_imp) == 0:
                    self.logger.info(f"Read file '{self.task.src_file_name}' is Error or Empty")
                    return is_completed, note, error
                # step 2: check transform data from config external class
                if file_import.template.external_process:
                    is_completed, note_ext, error, df_outcome = self.exe_transform(file_import.template.external_process, df_imp)
                    if note_ext:
                        self.logger.info(note_ext)
                    df_imp = df_outcome or df_imp
                # step 3: check data destination
                with OracleConn(self.task.connection_string,self.task.task_time_out) as db:
                    # step 3.1: check exsit table
                    if not db.check_table_exist(file_import.template.table_name):
                        self.logger.info(f"Destination table '{file_import.template.table_name}' does not exist")
                        if db.err_msg:
                            self.logger.info(f'{db.err_msg}')
                        return is_completed, note, error
                    # step 3.2: check config truncate table
                    if file_import.template.is_truncate_tmp_table:
                        db.truncate_table(file_import.template.table_name)

                    file_id = None
                    # step 3.3: insert log and get file id from db,app_service_config
                    file_id = db.import_log(app_service_config.import_log_prc, [self.task.config_key_name, file_import.fileName])
                    if db.err_msg:
                        self.logger.info(f'{db.err_msg}')
                    # step 3.4: check and assign file_id to dfIm
                    if db.check_column_exist(file_import.template.table_name, 'FILE_ID'):
                        df_imp["FILE_ID"] = file_id

                    if db.check_column_exist(file_import.template.table_name, 'IMP_REC_ID'):
                        df_imp["IMP_REC_ID"] = range(1, len(df_imp) + 1)


                    # step 3.5: get dataType
                    df_schema = db.get_data_type_table(file_import.template.table_name)
                    # step 3.6: transform df to oracle data type
                    if df_schema is not None:
                        df_imp = file_import.prepare_oracle_df(df_schema, df_imp)

                        if file_import.note:
                            self.logger.info(file_import.note)

                    
                # end process database - end step 3
                
                

                # step 4: convert to script
                sql = file_import.convert_sql(df_imp)
                # step 5: check and process database
                with OracleConn(self.task.connection_string,self.task.task_time_out) as db:
                    # step 5.1: import
                    db.execute_import_data(sql, df_imp)
                    if db.err_msg:
                       self.logger.info( f'{db.err_msg}')
                    # step 5.2: check and process database
                    if file_import.template.procedure_name:
                        db.execute_procedure(file_import.template.procedure_name)
                        if db.err_msg:
                            self.logger.info(f'{db.err_msg}')
                # step 6: update log 
                with OracleConn(self.task.connection_string,self.task.task_time_out) as db:
                    db.execute_procedure(app_service_config.import_status_prc, [1, file_id])
                    if db.err_msg:
                        self.logger.info(f'{db.err_msg}')

                is_completed = 1
                if is_completed:
                    note_archive = self.archive_file(file_import.fileName)
                    if note_archive:
                        self.logger.info(note_archive)

        except Exception as e:
            note += f'doImport is Error'
            self.logger.exception(f'import error {e}')

        return is_completed, note, error
    
    def archive_file(self,file_name:str) -> str:
        note_archive = None
        archive_folder = os.path.join(self._destination_archive, self.task.src_folder_name) if self.task.src_folder_name else self._destination_archive
        with FileArchiver(file_name, archive_folder) as archiver:
            note_archive = archiver.archive_file
        return note_archive
        


    def exe_transform(self, config_method, df) -> tuple[bool, str, Exception, any]:
        """
        Execute external process.

        Args:
            config_method (str): The external method configuration.
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            tuple[int, str, Exception, any]: Status, note, error, and return object.
        """
        note = ''
        is_completed = False
        error = None
        return_object = None

        try:
            module_name, method_name = config_method.split('.')
            if not module_name or not method_name:
                self.logger.info(' ===> config process is not correct')
                return is_completed, note, error, return_object

            class_execute_name = f"{DataConstant.EXTERNAL_MODULE_NAME}.{module_name}"
            with ExecuteCls(classExecuteName=class_execute_name, doTask=method_name) as executor:
                return_object = executor.do_cls_method(df)
                if executor.log_note:
                    self.logger.info(executor.log_note)
            is_completed = True

        except Exception as e:
            note += 'exeImportLogic is Error'
            self.logger.exception(f'exeImportLogic is Error, {e}')

        return is_completed, note, error, return_object

    
