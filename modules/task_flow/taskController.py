
from .taskConstant import TaskConstant
from typing import Optional
from .model import Task
from .task_business import TaskProcessBase
from .task_business import acqAutoAccounting
class TaskController:
    @staticmethod
    def get_tasks():
        task_executor_map = {
                TaskConstant.TASK_EXECUTE_PROCEDURE: TaskProcessBase.execute_procedure,
                TaskConstant.TASK_EXPORT: TaskProcessBase.execute_export,
                TaskConstant.TASK_EMAIL_REPORT: TaskProcessBase.execute_email_report,
                TaskConstant.TASK_EMAIL_SEND_ATTACH: TaskProcessBase.execute_email_send_attach,
                TaskConstant.TASK_SFTP_UPLOAD: TaskProcessBase.execute_sftp_upload,
                TaskConstant.TASK_SFTP_MOVE_TO_SERVER: TaskProcessBase.execute_sftp_move_to_server,
                TaskConstant.TASK_SFTP_DOWNLOAD: TaskProcessBase.execute_sftp_download,
                TaskConstant.TASK_SFTP_MOVE_TO_LOCAL: TaskProcessBase.execute_sftp_move_to_local,
                TaskConstant.TASK_IMPORT: TaskProcessBase.execute_import,
                TaskConstant.TASK_SFTP_IMPORT:TaskProcessBase.execute_sftp_import,
                TaskConstant.TASK_SFTP_EXPORT:TaskProcessBase.execute_sftp_export,
                TaskConstant.TASK_EXECUTE_PYTHON: TaskProcessBase.execute_python,
                TaskConstant.TASK_TESTING: TaskProcessBase.execute_testing,
                TaskConstant.TASK_EXT_PRC_OUT_RSCODE: TaskProcessBase.execute_prc_out_rscode,
                "ACQ_AUTO_ACCOUNTING": acqAutoAccounting.execute_auto_accounting
            }
        return task_executor_map
    
    # end get Task
    @staticmethod
    def execute_task(task: Task) -> tuple[bool,str,Optional[Exception]]:

        task_executor_map = TaskController.get_tasks()

        if task.task_type in task_executor_map:
            return task_executor_map[task.task_type](task)
        else:
            return True,' | Invalid config, task not matching', None
    # end execute_task