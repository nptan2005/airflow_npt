import os
from datetime import datetime
from typing import Optional, Tuple
import inspect
from core_config import configuration,app_service_config
from conn_kit import EmailSender
from data_kit import DataExport,FileArchiver
from db_conn import OracleConn
from ..model import Task
from ..task_utils import TaskUtils
from utilities import Logger


class TaskEmailSender:
    def __init__(self, task: Task, attachment_file:str = None, is_archive:bool = True):
        self._destination_archive = os.path.join(
            configuration.file_path[app_service_config.default_archive_path].root,
            configuration.file_path[app_service_config.default_archive_path].path
        )
        self.task = task
        self.attachment_file = attachment_file
        self.is_archive = is_archive
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
            'task', '_destination_archive', 
            'attachment_file', 'is_archive','logger'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    def _data_array(self) ->tuple[list,str]:
        data_arr = []
        note = ''
        if self.task.script:
            try:
                with OracleConn(self.task.connection_string,self.task.task_time_out) as db:
                    data_arr = db.execute_script_list(self.task.script)
            except Exception as e:
                note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] execute script array {self.task.script} is Error'
                self.logger.exception(f"execute '{self.task.script}' Error, {e}")
                return False, note, data_arr


        return True, note, data_arr
    # end _data_array

    def _check_valid(self) -> Tuple[bool,str,list]:
        if not self.task.is_notification:
            return False, '|Configuration error: Not an email notification task'
        if not self.task.email:
            return False, '|Email configuration missing'
        return True, ''
    
    # Send notification email
    def send_notify_email(self, text_message) -> Tuple[int, str, Optional[Exception]]:

        return self.send_email(
            text_message=text_message
            )
    # end send_notify_email

    # Email report
    def pd_to_email(self) -> Tuple[bool, str, Optional[Exception]]:
        """
        Sends a report via email.

        Args:
            task (Task): Task containing email and report information.

        Returns:
            Tuple[int, str, Optional[Exception]]: Status, note, and exception (if any).
        """
        is_completed, note, error = False,'', None
        is_valid_data, note, data = self._data_array()
        if is_valid_data:
            try:
                
                is_completed, note_part, error = self.send_email(
                    text_message=None,
                    data=data
                )
                if note_part:
                    note += note_part

            except Exception as e:
                note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Email report encountered an error'
                self.logger.exception(f"Email report encountered an error, {e}")

 
        # end check input not valid


        return is_completed, note, error
    # end pd_to_email

    # send attach file
    def send_attachment_report(self) -> Tuple[bool, str, Optional[Exception]]:
        is_completed, note, error = False,'', None
        if self.task.is_attachment:
            is_valid_data, _note, data = self._data_array()
            if _note:
                note += _note
            if is_valid_data:
                try:
                    config = configuration.file_path[app_service_config.default_attchment_path]
                    base_path = os.path.join(config.root, config.path,self.task.dst_folder_name)
                    file_name = TaskUtils.create_file_name(base_path=base_path,file_pattern=f'{self.task.frequency}_{self.task.dst_file_name}', syntax ="[YYYYMMDDHHMMSS]")
                    _note = ''
                    with DataExport(export_date=data,export_name=self.task.output_name, file_name=file_name,file_type= self.task.dst_file_type,is_header= self.task.is_header) as writer:
                        writer.to_file()
                        is_completed = writer.is_successful
                        _note += writer.note
                        self.attachment_file = f'{file_name}.{writer.file_type}'
                        self.is_archive = True

                    if is_completed == 1:
                        is_completed, note, error = self.send_email(f"Send Report '{self.task.task_name}'",None)
                    else:
                        note += _note
                except Exception as e:
                    note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Email report encountered an error'
                    self.logger.exception(f'Email report encountered an error {e}')
        else:
            note += f'|Config is_attachment = {self.task.is_attachment}'

        return is_completed, note, error

    # Send email
    def send_email(
        self,text_message: Optional[str] = None, data: Optional[list] = None
    ) -> Tuple[bool, str, Optional[Exception]]:
        """
        Sends an email.
        
        Args:
            is_notification (bool): Whether to send a notification.
            subject (str): Email subject.
            to_email (Optional[list]): List of recipient email addresses.
            text_message (Optional[str]): Email body.
            data (Optional[list]): Additional data for the email.

        Returns:
            Tuple[int, str, Optional[Exception]]: Status, note, and exception (if any).
        """
        is_completed, note, error = False,'', None
        is_valid, note = self._check_valid()
        if is_valid:
            try:
                if not self.task.email:
                    to_email = ['tannp@bvbank.net.vn']
                else:
                    to_email = self.task.email

                with EmailSender(
                    connection_name=app_service_config.default_email_conn,
                    email_template=app_service_config.email_template
                ) as sender:
                    if data is not None:
                        sender.data_report = data


                    sender.attachment = self.attachment_file
                    # sender.chart_img = chart_img

                    sender.header = self.task.task_name
                    sender.send(
                        subject=f'[{datetime.now().strftime("%d-%m-%Y")}]{self.task.task_name}', 
                        receivers=to_email, textMessage=text_message
                    )

                    if sender.note:
                        note += ' >>>>>> Send email: ' + sender.note

                    is_completed = True

                    if is_completed and self.is_archive:
                        if sender.attachment:
                            with FileArchiver(sender.attachment, self._destination_archive) as ar:
                                archive_note = ar.archive_file
                            if archive_note:
                                note += archive_note

                        if sender.chart_img:
                            with FileArchiver(sender.chart_img, self._destination_archive) as ar:
                                archive_note = ar.archive_file
                            if archive_note:
                                note += archive_note

            except Exception as e:
                note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Process encountered an error'
                error = e

        return is_completed, note, error

    

    
