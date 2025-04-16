
from typing import Tuple,Optional
from ..model import Task
from core_config import prc_configuration
from ..task_engine import TaskDBExecutor, TaskEmailSender
class acqAutoAccounting:
    @staticmethod
    def execute_auto_accounting(task:Task) -> Tuple[bool, str, Optional[Exception]]:
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