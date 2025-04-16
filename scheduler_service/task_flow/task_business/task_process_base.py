from typing import Tuple,Optional
from ..model import Task

class TaskProcessBase:
    
    @staticmethod
    def execute_procedure(task:Task) -> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskDBExecutor
        with TaskDBExecutor(task) as db:
            is_completed, note, error = db.execute_procedure()
            if is_completed and task.is_notification and task.email:
                from ..task_engine import TaskEmailSender
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, process: {task.script} completed!' )
                    if note_email:
                        note += f' >>>>>>> SubTask:{note_email}'
        return is_completed,note, error
    # end _execute_procedure
    @staticmethod
    def execute_export(task:Task) -> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        # --
        report_full_path = None
        # export file
        from ..task_engine import TaskExporter
        with TaskExporter(task) as exporter:
            is_completed, note, error = exporter.export()
            report_full_path = exporter.attach_file
        # check and send email
        if is_completed and task.email:
            from ..task_engine import TaskEmailSender
            note_email = None
            if task.is_attachment and report_full_path:
                with TaskEmailSender(task,report_full_path, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Report as attachment file: {task.dst_file_name}' )
            elif  task.is_notification:
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, export: {task.dst_file_name} completed!' )
            if note_email:
                note += f' >>>>>>> SubTask:{note_email}'

        return is_completed,note, error
    # end _execute_export
    @staticmethod
    def execute_email_report(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskEmailSender
        with TaskEmailSender(task) as sender:
            is_completed, note, error = sender.pd_to_email()
        return is_completed,note, error
    # end _execute_email_report
    @staticmethod
    def execute_email_send_attach(self,task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskEmailSender
        with TaskEmailSender(task) as sender:
            is_completed, note, error = sender.send_attachment_report()
        return is_completed,note, error
    # end _execute_email_send_attach
    @staticmethod
    def execute_sftp_upload(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.sftp_root_path = task.dst_folder_name
            sftp.is_remove_src = False
            is_completed, note, error = sftp.upload()
        return is_completed,note, error
    # end _execute_sftp_upload
    @staticmethod
    def execute_sftp_move_to_server(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.sftp_root_path = task.dst_folder_name
            sftp.is_remove_src = True
            is_completed, note, error = sftp.upload()
        return is_completed,note, error
    # end _execute_sftp_move_to_server
    @staticmethod
    def execute_sftp_download(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.is_remove_src = False
            is_completed, note, error = sftp.download()
        return is_completed,note, error
    # end _execute_sftp_download
    @staticmethod
    def execute_sftp_move_to_local(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.is_remove_src = True
            is_completed, note, error = sftp.download()
        return is_completed,note, error
    # end _execute_sftp_move_to_local
    @staticmethod
    def execute_import(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskImporter
        with TaskImporter(task) as importer:
            is_completed, note, error = importer.import_file()
            if is_completed and task.is_notification and task.email:
                from ..task_engine import TaskEmailSender
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, process: {task.src_file_name} completed!' )
                    if note_email:
                        note += f' >>>>>>> SubTask:{note_email}'
        return is_completed,note, error
    # end _execute_import
    @staticmethod
    def execute_python(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        from ..task_engine import TaskPyExecutor
        with TaskPyExecutor(task) as py_exec:
            is_completed, note, error = py_exec.execute()
            if is_completed and task.is_notification and task.email:
                from ..task_engine import TaskEmailSender
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, process: {task.script} completed!' )
                    if note_email:
                        note += f' >>>>>>> SubTask:{note_email}'
        return is_completed,note, error
    # end _execute_python

    @staticmethod
    def execute_sftp_import(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        if not task.config_key_name:
            return False, 'Config Key is not found', None
        from core_config import import_configuration
        config = import_configuration.import_template[task.config_key_name]
        sftp_conn = config.sftp_conn
        if not sftp_conn:
            return False, 'sftp conn is not found', None
        src_import_path = None
        from ..task_engine.taskSFTP import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.connection_str = sftp_conn
            sftp.is_remove_src = True
            is_completed, note, error = sftp.download()
            src_import_path = sftp.destination_path

        if is_completed == False:
            return False, f'download file is not success, {note}', None
        
        if not src_import_path:
            return False, f'file is not found, {note}', None

        from ..task_engine import TaskImporter
        with TaskImporter(task) as importer:
            importer.file_name = src_import_path
            is_completed, note, error = importer.import_file()
            if is_completed and task.is_notification and task.email:
                from ..task_engine.taskEmailSender import TaskEmailSender
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, process: {task.src_file_name} completed!' )
                    if note_email:
                        note += f' >>>>>>> SubTask:{note_email}'
        return is_completed,note, error
    

    @staticmethod
    def execute_sftp_export(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        if not task.config_key_name:
            return False, 'Config Key is not found', None
        from core_config import export_configuration
        config = export_configuration.export_template[task.config_key_name]
        sftp_conn = config.sftp_conn
        if not sftp_conn:
            return False, 'sftp conn is not found', None
        
        report_full_path = None
        # export file
        from ..task_engine import TaskExporter
        with TaskExporter(task,is_export_to_server=True) as exporter:
            is_completed, note, error = exporter.export()
            report_full_path = exporter.attach_file
        # check and send email
        if is_completed and task.email:
            from ..task_engine import TaskEmailSender
            note_email = None
            if task.is_attachment and report_full_path:
                with TaskEmailSender(task,report_full_path, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Report as attachment file: {task.dst_file_name}' )
            elif task.is_notification:
                with TaskEmailSender(task,None, is_archive= False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(f'Task {task.task_name}, export: {task.dst_file_name} completed!' )
            if note_email:
                note += f' >>>>>>> SubTask:{note_email}'

        from ..task_engine import TaskSFTP
        with TaskSFTP(task) as sftp:
            sftp.connection_str = sftp_conn
            sftp.sftp_root_path = task.dst_folder_name
            sftp.is_remove_src = True
            is_completed, note, error = sftp.upload()

        if is_completed == False:
            return False, f'upload file is not success, {note}', None
        
        
        return is_completed,note, error
    # end execute_sftp_export

    @staticmethod
    def execute_prc_out_rscode(task:Task) -> Tuple[bool, str, Optional[Exception]]:
        from core_config import prc_configuration
        from ..task_engine import TaskDBExecutor, TaskEmailSender
        is_completed,note, error = False,'', None
        procedure_config = prc_configuration.procedures_template[task.config_key_name]
        # Prepare parameters for callproc
        procedure_config = prc_configuration.procedures_template[task.config_key_name]
        in_params = {param.name: param.value for param in procedure_config.in_params}
        out_params_type = {param.name: param.type.upper() for param in procedure_config.out_params}
        is_retry = procedure_config.is_retry
        success_value = procedure_config.conditions["success_value"]
        email_notify = procedure_config.conditions["email_notify"]

        

        with TaskDBExecutor(task) as db:
            is_completed, note, error, out_results = db.execute_procedure_out_param(
                list(in_params.values()), out_params_type
            )

            rs_code = out_results.get("o_rscode")
            rs_desc = out_results.get("o_rsdesc")
            # rs_code = '01' #test
            # retry
            num_of_retry = 0
            if rs_code != success_value and is_retry:
                max_retries = 0 if not is_retry else task.retry_number
                for _ in range(max_retries):
                    num_of_retry += 1
                    is_completed, note, error, out_results = db.execute_procedure_out_param(
                        list(in_params.values()), out_params_type
                    )
                    rs_code = out_results.get("o_rscode")
                    rs_desc = out_results.get("o_rsdesc")
                    if rs_code == success_value:
                        break

            # Gửi email thông báo nếu cần
            if email_notify and task.is_notification and task.email:
                with TaskEmailSender(task, None, is_archive=False) as sender:
                    is_completed, note_email, error = sender.send_notify_email(
                        f"Task {task.task_name}, process: {task.script} completed!"
                        f"\n'o_rscode' = '{rs_code}'"
                        f"\n'rs_desc' = '{rs_desc}'"
                        f"\n'process status' = '{is_completed}'"
                        f"\n'Retry' = '{is_retry}', num of Retry = {num_of_retry}"
                        f"\n'Note' = '{note}'"
                    )
                    if note_email:
                        note += f'SubTask: {note_email}'

        return is_completed, note, error
    # end _execute_procedure

    @staticmethod
    def execute_testing(task:Task)-> Tuple[bool, str, Optional[Exception]]:
        is_completed,note, error = False,'', None
        # import os
        # import time
        # from datetime import datetime
        # from multiprocessing import Process, current_process
        # from threading import Thread, current_thread
        # is_completed = 1
        
        # def io_bound(sec):
        #     log = ''
        #     pid = os.getpid()
        #     threadName = current_thread().name
        #     processName = current_process().name

        #     log+= f"{pid} * {processName} * {threadName} \
        #         ---> Start sleeping..."
        #     time.sleep(sec)
        #     log += f"\n{pid} * {processName} * {threadName} \
        #         ---> Finished sleeping..."
        #     return log
        # # end io_bound

        # def cpu_bound(n):
        #     log = ''
        #     pid = os.getpid()
        #     threadName = current_thread().name
        #     processName = current_process().name

        #     log += f"{pid} * {processName} * {threadName} \
        #         ---> Start counting..."

        #     while n>0:
        #         n -= 1

        #     log += f"{pid} * {processName} * {threadName} \
        #         ---> Finished counting..."
        #     return log
        # # end cpu_bound
        # start = time.time()
        # COUNT = 200000000
        # SLEEP = 1
        
        # note+=io_bound(SLEEP)
        # note+=cpu_bound(1000)
        
        # end = time.time()
        # note+= f'\nTime taken in seconds: {end - start}'
        # time.sleep(1.5)
        is_completed = True
        note = ' ===> TEST'
        return is_completed,note, error
    # end _execute_testing
    
