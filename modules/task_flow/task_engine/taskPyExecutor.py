import inspect
from ..model import Task
from data_kit import ExecuteCls
from core_config import app_service_config

class TaskPyExecutor:
    def __init__(self, task: Task):
        self.task = task

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.task = None

    def execute(self) -> tuple[int, str, Exception]:
        """
        Execute an external process based on the task's script.
        
        Args:
            task (Task): The task containing script details.
        
        Returns:
            tuple[int, str, Exception]: Status, note, and error if any.
        """
        note = ''
        is_completed = 0
        error = None
        
        if not self.task.script:
            note = f'| Config is not correct, script {self.task.script}'
            return is_completed, note, error

        py_arr = self.task.script.split('.')
        if len(py_arr) != 2:
            note = '| Config process is not correct'
            return is_completed, note, error

        class_execute_name = f'{app_service_config.default_ext_module}.{py_arr[0]}'
        do_task = py_arr[1]

        try:
            with ExecuteCls(classExecuteName=class_execute_name, doTask=do_task) as t:
                t.do_cls_inst_no_param
                note = t.log_note or note
                is_completed = 1
        except Exception as e:
            note = f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]doExternalProcess is Error'
            error = e

        return is_completed, note, error
