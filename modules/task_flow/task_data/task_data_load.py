import pandas as pd
from pydantic import ValidationError
from typing import List
import datetime
from ..model import Task,TaskCompleted
from ..taskConstant import TaskConstant
from db_conn import ConnConstant,OracleConn
from utilities import Logger
from core_config import app_service_config
class TaskDataLoading:
    def __init__(self):
        self.logger = Logger().logger

    def __enter__(self):
        # self._schedule_waiting()
        return self
    
    def __del__(self):
        self._clear_attributes()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            'logger']
        for attr in attributes:
            setattr(self, attr, None)

    
    def get_tasks_from_db(self, run_time:int, task_id:str = TaskConstant.ALL_JOB) -> List[Task]:
        tasks = []
        try:
            df = pd.DataFrame()
            with OracleConn(app_service_config.default_orl_db_conn) as conn:
                param = [run_time, task_id]
                df = conn.execute_prc_with_cursor(app_service_config.task_prc,param)
            if not df.empty:
                tasks_dict = df.to_dict(orient='records')
                for task_data in tasks_dict:
                    try:
                        # task_data = TaskFactory.normalize_task_data(task_data)
                        task = Task(**task_data)
                        task.connection_string = task.connection_string or ConnConstant.DB_CONN_DEFAULT
                        tasks.append(task)
                    except ValidationError as e:
                        self.logger.error(f"Validation error for task data {task_data}: {e}")
                # end for   
        
            else:
                self.logger.info(f"No tasks assigned for schedule at {run_time}")
        except Exception as e:
            self.logger.exception(f"Error during task assignment: {e}")
        return tasks
    # end get_tasks_from_db


    def _test_dispatcher_task(self) -> List[Task]:
        """Simulate task dispatching for testing purposes."""
        tasks = []
        task_counter = 0
        
        for i in range(1, 10):
            task_counter += 1
            try:
                task = Task(
                    task_id=i,
                    task_order=task_counter,
                    task_type=TaskConstant.TASK_TESTING,
                    task_name=f"Task {i}",
                    run_time=0,
                    config_key_name=f"Config {i}",
                    process_num=task_counter,
                    frequency="Daily",
                    day_of_week=1,
                    day_of_month=15,
                    is_export=True,
                    is_import=False,
                    is_header=True,
                    is_notification=True,
                    is_attachment=False,
                    script="SELECT * FROM acb; DELETE FROM xyz",  # Chuỗi script
                    connection_string="db_conn_string",
                    output_name="output1; output2",  # Chuỗi output array
                    src_folder_name="source_folder",
                    src_file_name="file1.txt",
                    src_file_type="txt",
                    dst_folder_name="dest_folder",
                    dst_file_name="file2.txt",
                    dst_file_type="txt",
                    email="sample@example.com; abc@acm.com",  # Chuỗi email
                    start_date=datetime.now(),
                    end_date=None,
                    task_time_out= 1 if task_counter == 2 else 10
                )
                tasks.append(task)
                if task_counter >= 3:
                    task_counter = 0
            
            except ValidationError as e:
                self.logger.exception(f"Validation error for task {i}: {e}")
        self.num_of_task = len(tasks)
        return tasks
    # end _test_dispatcher_task

    def log_task_history(self,task_result:List[TaskCompleted],run_time:int):
        if task_result and len(task_result) > 0:
            try:
                with OracleConn(app_service_config.default_orl_db_conn) as db:
                    for item in task_result:
                        db.execute_procedure(
                            app_service_config.his_prc,
                            params=[
                                item.task_id, 
                                item.task_name, 
                                item.start_date, 
                                item.note[0:999], 
                                1 if item.is_finished == True else 0
                            ]
                        )
            except Exception as e:
                self.logger.exception(f'Failed to log task history to database, {e}')
        # end log_task_history
