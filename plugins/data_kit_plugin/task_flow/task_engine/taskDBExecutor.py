from typing import Tuple,Optional,Dict
import inspect
from ..model import Task
from db_conn import  OracleConn
from utilities import Logger

class TaskDBExecutor:
    def __init__(self, task:Task):
        self.task = task
        self.logger = Logger().logger
    def __enter__(self):
        return self

    def __del__(self):
        del self.task
        del self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.task = None
        self.logger = None

    def execute_procedure(self) -> Tuple[bool, str, Optional[Exception]]:
        # Check if the script exists
        if self.task.script:
            try:
                with OracleConn(self.task.connection_string, self.task.task_time_out) as db:
                    for script in self.task.script:
                        db.execute_procedure(script)
                return True, '', None
            except Exception as e:
                note  = f'[{self.__class__.__name__}]'
                note += f"[{inspect.currentframe().f_code.co_name}] excute '{self.task.script}' Error"
                self.logger.exception(f"execute '{self.task.script}' Error, {e}")
                return False,note,None
        else:
            False, f"Configuration error, no valid script '{self.task.script}' provided", None
    # end execute_procedure

    def execute_procedure_out_param(self,params:list,out_params_type:dict)-> Tuple[bool,str,Optional[Exception],Optional[Dict]]:
        # Check if the script exists
        if not out_params_type:
            return False, 'Param not exist', None, None
        if not self.task.script:
            False, f"Configuration error, no valid script '{self.task.script}' provided", None, None
        if len(self.task.script) > 1 or len(self.task.script) == 0:
            False, f"Configuration error, alway one procedure provided", None, None
        out_results = None
        procedure = self.task.script[0]
        try:
            with OracleConn(self.task.connection_string, self.task.task_time_out) as db:
                out_results = db.execute_procedure_param(procedure,params,out_params_type)
            return True,'',None,out_results
        except Exception as e:
            note  = f'[{self.__class__.__name__}]'
            note += f"[{inspect.currentframe().f_code.co_name}] excute '{procedure}' Error"
            self.logger.exception(f"execute '{self.task.script}' Error, {e}")
            return False,note,e,out_results
    # end execute_cond_prc

    


