from typing import List
from pydantic import ValidationError
import functools
import schedule
from datetime import datetime
import time
# for testing
from utilities import Logger
from task_flow import Task,TaskDispatcher
from task_flow.taskConstant import TaskConstant





log = Logger().logger
# #######################################################################################
# schedule handle
def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                log.debug(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator
# end catch_exceptions

def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        
        log.debug(f'Schedule join "{func.__name__}"')
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_timestamp
        log.debug(f'LOG: Job "{func.__name__}" completed in {elapsed_time:.2f} seconds')
        return result

    return wrapper
# end print_elapsed_time



# end schedule handle
# #######################################################################################

# #######################################################################################
def _test_dispatcher_task() -> List[Task]:
    """Simulate task dispatching for testing purposes."""
    tasks = []
    task_counter = 0
    
    for i in range(1, 100):
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
            print(f"Validation error for task {i}: {e}")
    
    return tasks
# end _test_dispatcher_task

@print_elapsed_time
@catch_exceptions(cancel_on_failure=False)
def run_job(cycle_time): 
    run_time = run_time_calculate(cycle_time)
    log.info('----------------------------------------------------')
    log.info(f'Job Start with RunTime: [{run_time}]')
    tasks = _test_dispatcher_task()
    with TaskDispatcher(run_time=run_time) as p:
        for task in tasks:
            task.run_time = run_time
            p.enqueue(task)
        p.run_tasks()

# end

_run_time_list = []
def get_time() -> tuple[int,int,int]:
    now = datetime.now()
    hour = int(now.strftime("%H"))
    min = int(now.strftime("%M"))
    sec = int(now.strftime("%S"))
    return sec, min, hour
def run_time_calculate(cycle_time) -> int:
    run_time = 0
    sec, min, hour = get_time()
    div = min % cycle_time
    if div > 0:
        min = min - div + cycle_time
    run_time = (hour * 100) + min

    return run_time 
# end run_time_calculate
# _time = run_time_calculate(5)
_time = -5
# for i in range(1,60):
while _time < 2355:
    _time += 5
    time_str = str(_time)
    min = ''
    hour = ''
    if len(time_str) == 4:
        hour=time_str[:2]
        min=time_str[-2:]
    elif len(time_str) == 3:
        hour= '0' + time_str[:1]
        min=time_str[-2:]
    elif len(time_str) == 2:
        hour = '0'
        min=time_str[-2:]
    elif len(time_str) == 1:
        hour = '0'
        min=time_str
    
    _hour = int(hour)
    _min = int(min)
    if _min > 55:
        _min = 0
        _hour += 1
    _time = (_hour * 100) + _min
    _run_time_list.append(_time)
print(_run_time_list)