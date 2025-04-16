import time
from datetime import datetime
from typing import List,Union

import pandas as pd
# import functools
import schedule
from utilities import Logger
from .model import Task
from .model import TaskCompleted
from .taskConstant import TaskConstant
from .taskDispatcher import TaskDispatcher
from conn_kit import EmailSender,ConnKitConstant
from core_config import configuration,app_service_config
from .task_data.task_data_load import TaskDataLoading
# from .taskFactory import TaskFactory

# log = logger()
# # #######################################################################################
# # schedule handle
# def catch_exceptions(cancel_on_failure=False):
#     def catch_exceptions_decorator(job_func):
#         @functools.wraps(job_func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return job_func(*args, **kwargs)
#             except:
#                 import traceback
#                 log.debug(traceback.format_exc())
#                 if cancel_on_failure:
#                     return schedule.CancelJob
#         return wrapper
#     return catch_exceptions_decorator
# # end catch_exceptions

# def print_elapsed_time(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         start_timestamp = time.time()
        
#         log.debug('Schedule join "%s"' % func.__name__)
#         result = func(*args, **kwargs)
#         elapsed_time = time.time() - start_timestamp
#         log.debug(f'LOG: Job "{func.__name__}" completed in {elapsed_time:.2f} seconds')
#         return result

#     return wrapper
# # end print_elapsed_time



# # end schedule handle
# # #######################################################################################
class TaskScheduler:
    def __init__(self, cycle_time:int = 15,sleep_time:int = 5, run_time_list:list = None):
        """
        cycle_time: block time, default 15 min
        sleep_time: sleepTime for while, default 5s
        timeOffset: bias constant, default: 0s
        """
        self._scheduler = schedule.Scheduler()
        self._sleep_time = sleep_time
        self._cycle_time = cycle_time # block time: 15ph
        self._run_time_list = run_time_list
        self._is_running = app_service_config.service_running
        # for log
        self._logger = Logger().logger
        self.num_of_task = 0
        self.email_config = configuration.email[ConnKitConstant.EMAIL_ACCT_DEFAULT]
        self.email_list = self.email_config.mail_list


    def __enter__(self):
        self._schedule_waiting()
        return self
    
    def __del__(self):
        self._clear_attributes()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop
        self.cleanup
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_scheduler', '_sleep_time', '_cycle_time', '_run_time_list', '_is_running',
            'num_of_task',
            '_logger',
            'email_config',
            'email_list']
        for attr in attributes:
            setattr(self, attr, None)

    # Properties
    @property
    def scheduler(self):
        return self._scheduler
    
    @property
    def sleep_time(self) -> int:
        return self._sleep_time
    
    @sleep_time.setter
    def sleep_time(self,value):
        self._sleep_time = value
        
    @property
    def run_time_list(self) -> list:
        return self._run_time_list
    @run_time_list.setter
    def run_time_list(self, value:list):
        self._run_time_list = value
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @is_running.setter
    def is_running(self,value):
        self._is_running = value

    @property
    def logger(self):
        return self._logger
    
    @property
    def cycle_time(self):
        return self._cycle_time
    
    
    def _schedule_waiting(self):
        sec, min, hour = self._get_time
        self._roud_cycle_time(self._cycle_time)
        time_off_set = min%self._cycle_time
        tmp_sleep = (self._cycle_time - time_off_set)*60 - sec 
        if tmp_sleep > 0:
            self.logger.info(f'Scheduler start at {hour}:{min}:{sec} | Sleeping in ~{tmp_sleep} seconds, waiting for cycle Time {self._cycle_time} min')
            time.sleep(tmp_sleep)

        sec, min, hour = self._get_time
        self.logger.info(f'Scheduler set Job at {hour}:{min}:{sec}')
    # end __scheduleWaiting

    def _roud_cycle_time(self, value:int):
        """must be a multiple of 5 (minutes)"""
        
        if value < 5:
            value = 5
        else:
            div = value % 5
            if div > 0:
                value = value - div
            
        self._cycle_time = value
    # end _roud_cycle_time

    
    
    # end properties
    # #######################################################################################
    # schedule handle
    def _handle_sigterm(self, sig, frame):
        self.logger.warning('SIGTERM received...')
        self._is_running = False
        self.stop

    @property
    def stop(self):
        self._is_running = False
        sec,min,hour = self._get_time
        self.logger.info(f'Schedule is stopping at {hour}:{min}:{sec}')
        return self.scheduler.cancel_job
    
    @property
    def cleanup(self):
        self.scheduler.clear()
    # end cleanup

    # #######################################################################################
    @property
    def _get_time(self) -> tuple[int,int,int]:
        now = datetime.now()
        hour = int(now.strftime("%H"))
        min = int(now.strftime("%M"))
        sec = int(now.strftime("%S"))
   
        return sec,min,hour 
    # end getHour

    def run_time_calculate(self,min:int,hour:int) -> int:
        run_time = 0
        div = min % self.cycle_time
        if div > 0:
            min = min - div + self.cycle_time
            if min > 55:
                min = 0
                hour += 1
                if hour > 23:
                    hour = 0
        run_time = (hour * 100) + min

        return run_time 
    # end run_time_calculate

    

    def _get_tasks(self, run_time:int, task_id:str = TaskConstant.ALL_JOB) -> List[Task]:
        tasks = []
        with TaskDataLoading() as db:
            tasks = db.get_tasks_from_db(run_time=run_time,task_id=task_id)
        return tasks
    # end get_tasks

    def _log_task_history(self,task_result: Union[List[TaskCompleted], None],run_time:int):
        with TaskDataLoading() as db:
            db.log_task_history(task_result=task_result,run_time=run_time)
        
        # end log_task_history

    
    def _report_data(self,result_task:Union[List[TaskCompleted], None],total_duration:pd.Timedelta) -> List[pd.DataFrame]:
        seq = 0
        report_data = []
        email_data = []
        if not isinstance(result_task, list):
            self.logger.error(f"Expected list, got {type(result_task)}")
            return []
        task_counter = len(result_task)
        if result_task and task_counter > 0:
            for item in result_task:
                if item.is_frequency_task:
                    if item.is_notify_fail == False and item.is_finished == False:
                        continue
                    if item.is_notify_sucess == False and item.is_notify_sucess == True:
                        continue
                seq += 1
                note = ''
                if item.is_error:
                    note += 'Process Task is Error'
                report_data.append([seq,
                                    item.task_id, 
                                    item.task_name,
                                    item.task_type,
                                    item.is_finished,
                                    item.duration,
                                    note])
        if seq > 0:
            _columns = ['No.','TaskID', 'TaskName',
                                         'TaskType', 'IsCompleted','Duration', 'Note']
            df = pd.DataFrame(report_data, columns = _columns)

            total_tasks = len(df)
            total_completed_tasks = df[df['IsCompleted'] == True].shape[0]
            # total_duration = df['Duration'].sum()
            summary_row = pd.DataFrame({
                'No.': [''],
                'TaskID': [f'Total tasks: '],
                'TaskName': [f'{total_tasks}'],
                'TaskType': [f'Completed:'],
                'IsCompleted': [f'{total_completed_tasks}'],
                'Duration': [total_duration],
                'Note': ['']
            })
            df_with_summary = pd.concat([df, summary_row], ignore_index=True)

            email_data = [df_with_summary]
        return email_data
    # end _report_data

    def _email_report(self,header:str,subject:str,duration:pd.Timedelta,task_result:List[TaskCompleted]):
        if app_service_config.is_email_summary:
            _email_data = self._report_data(task_result,duration)
            if _email_data and len(_email_data) > 0:
                with EmailSender(
                                connection_name=app_service_config.default_email_conn,
                                email_template=app_service_config.email_template
                            ) as sender:
                        sender.data_report = _email_data
                        sender.header = header
                        sender.send(
                            subject=f'[{datetime.now().strftime("%d-%m-%Y")}] Schedule: {subject}', 
                            receivers=self.email_list, textMessage=None
                        )
                        if sender.note:
                            self.logger.info(sender.note)
        # end is_email_summary
    # end _email_report


    
    def run(self, run_time:int, task_id:str = TaskConstant.ALL_JOB): 
        self.logger.info('----------------------------------------------------')
        sec,min,hour = self._get_time
        if not run_time:
            run_time = self.run_time_calculate(min,hour)
        task_note = f'Start Schedule with Run Time = [{run_time}] at: [{hour}:{min}:{sec}]'
        self.logger.info(task_note)
        if not app_service_config.service_temporary_stop:
            tasks = self._get_tasks(run_time=run_time,task_id=task_id)
            # tasks = self._test_dispatcher_task()
            self.num_of_task = len(tasks)
            if tasks and self.num_of_task > 0:
                start_task_time = datetime.now()
                result_task = List[TaskCompleted]
                try:
                    with TaskDispatcher() as dispatcher:
                        for task in tasks:
                            dispatcher.enqueue(task)
                        dispatcher.run_tasks()
                        result_task = dispatcher.result_task
                finally:
                    duration = datetime.now() - start_task_time
                    # send email
                    self._email_report(header=task_note,
                                    subject=f'{hour}:{min}:{sec}',
                                    duration=duration,
                                    task_result=result_task)
                    # write log
                    sec,min,hour = self._get_time
                    self.logger.info(f'Finished Tasks with Run Time: [{run_time}] at {hour}:{min}:{sec} | Duration: {duration} | '
                        f'Total Tasks: {len(result_task)}/{self.num_of_task}'
                        )
                    
                    # db log
                    self._log_task_history(task_result=result_task,run_time=run_time)
        # end service_start
        else:
            self.logger.info('Task is temporary stop by config')

    # end run

    def _generate_time_serial(self):
        _run_time_list = []
        _time = self._cycle_time * -1
        # for i in range(1,60):
        while _time < 2355:
            _time += self._cycle_time
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
        return _run_time_list
    # end generate_time_serial

    def set_daily_schedule(self):
        time_serial = self._generate_time_serial()
        if self.run_time_list is not None:
            time_serial = list(set(time_serial + self.run_time_list))
        time_serial.sort()
        # self.logger.info(time_serial)
        # 
        for run_time in time_serial:
            time_str = str(run_time)
            if len(time_str) > 0 or len(time_str) <= 4:
                time_format_str = self._time_format(time_str)
                self.scheduler.every().day.at(time_format_str).do(self.run,run_time = run_time)
                self.logger.info(f'Set daily schedule at {time_format_str}, time args = [{run_time}]')
    # end setDailySchedule

    def _time_format(self,time_str:str) -> str:
        min = ''
        hour = ''
        if len(time_str) == 4:
            hour=time_str[:2]
            min=time_str[-2:]
        elif len(time_str) == 3:
            hour= '0' + time_str[:1]
            min=time_str[-2:]
        elif len(time_str) == 2:
            hour= '00' 
            min=time_str
        elif len(time_str) == 1:
            hour= '00' 
            min= '0' + time_str
        else:
            hour= '00'
            min= '00'
        return f'{hour}:{min}'
    
    # end getStrTime