import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time
from datetime import datetime
from  utilities import Logger
from .model import Task
from .model import TaskCompleted
from .task_queue import CompletedTaskQueue
from .task_queue import TaskQueue



class TaskProcessor:
    def __init__(self, task_queue: TaskQueue, completed_queue: CompletedTaskQueue, 
                 queue_lock: threading.Lock, completion_event: threading.Event):
        self.task_queue = task_queue
        self.completed_queue = completed_queue
        self.queue_lock = queue_lock
        self.completion_event = completion_event

        self.parent_task_dict = {}

        self._logger = Logger().logger


    def __del__(self):
        self._clear_attributes()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            'task_queue', 
            'completed_queue', 
            'queue_lock', 
            'completion_event',
            'parent_task_dict'
        ]
        for attr in attributes:
            setattr(self, attr, None)
    # end _clear_attributes
    def get_duration(self, start_time: datetime):
        return datetime.now() - start_time
    # end get_duration

 
    def _save_task_status(self, parent_id: int, is_success: bool):
        with self.queue_lock:
            self.parent_task_dict[parent_id] = is_success
    # end _save_task_status

    def run(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            while True:
                if self.task_queue.is_empty():
                    time.sleep(0.5)
                    self.completion_event.set()  # Mark task as completed
                    if self.completion_event.is_set():
                        time.sleep(0.5)
                        break
                    continue
                # end check task_queue empty

                # procees task:
                task = self.task_queue.dequeue()

                # Handle sub-task logic
                if task.is_sub_task and not self._handle_sub_task_logic(task):
                    continue

                # process task
                start_date = datetime.today()
                start_time = datetime.now()
                future = executor.submit(self.process_task, task, start_date, start_time)
                try:
                    task_completed = future.result(timeout=task.task_time_out)  # Đặt timeout
                    self.task_queue.task_done()
                    self._handle_task_completion(task_completed)
                except TimeoutError as e:
                    self._handle_timeout(task, start_time, e)
                except Exception as e:
                    self._handle_exception(task, start_time, e)
                # end try
            # end while
        # end thread
    # end run
    def _is_parent_task_processed(self,parent_id:int) -> bool:
        with self.queue_lock:
            if parent_id in self.parent_task_dict:
                return True
            return False
        # end _is_parent_task_processed

    def _is_parent_task_status(self, parent_id: int) -> bool:
        """Check if parent task is completed.
        """
        with self.queue_lock:
            return self.parent_task_dict.get(parent_id, False)
    # end _is_parent_task_completed
    def _handle_sub_task_logic(self, task: Task) -> bool:
        """Handle the logic for sub-tasks.
        False: skip
        """
        if not self._is_parent_task_processed(task.parent_task_id) and task.sub_task_retry_counter < task.sub_task_max_retry:
            task.sub_task_retry_counter += 1
            self._logger.info(f'[{task.process_num}][{task.task_id}] '
                              f'Parent task {task.parent_task_id} is not processed, '
                              f'sub-task, retry {task.sub_task_retry_counter}')
            with self.queue_lock:
                self.task_queue.enqueue(task)
            time.sleep(0.5)
            return False  # Skip processing this sub-task
        parent_status = self._is_parent_task_status(task.parent_task_id)
        if not parent_status:
            self._logger.info(f'[{task.process_num}][{task.task_id}] Sub-task skipped.'
                               f'Parent task status = {parent_status} , after {task.sub_task_retry_counter} retries.')
            self.task_queue.task_done()
            return False

        return True  # Proceed with sub-task processing
    # end _handle_sub_task_logic
    

    def _handle_task_completion(self,task_completed: TaskCompleted):
        """Handle task completion logic."""
        self._save_task_status(task_completed.task_id, task_completed.is_finished)
        self.enqueue_completed_task(task_completed)
    # end _handle_task_completion

    def _handle_timeout(self, task: Task, 
                         start_time: datetime, 
                         error: TimeoutError):
        duration = self.get_duration(start_time)
        self._logger.exception( f'[{task.process_num}][{task.task_id}]'
                                f'[{task.task_name}][Duration: {duration}]'
                                f'Timeout = {task.task_time_out}. Error: {error}')
        task_completed = TaskCompleted(
            task_id=task.task_id,
            task_name=task.task_name,
            note=f'Task Time out = {task.task_time_out}',
            is_finished=False,
            is_error=False,
            is_frequency_task = task.is_frequency_task,
            is_notify_fail = task.is_notify_fail,
            is_notify_sucess = task.is_notify_sucess,
            duration=duration
        )
        self._handle_task_completion(task, task_completed)

    # end _handle_exception

    def _handle_exception(self, task: Task, 
                          start_time: datetime, 
                          error: Exception):
        duration = self.get_duration(start_time)
        self._logger.exception( f'[{task.process_num}][{task.task_id}]'
                                f'[{task.task_name}][Duration: {duration}]'
                                f'Run process is Error = {error}.')

        
        task_completed = TaskCompleted(
            task_id=task.task_id,
            task_name=task.task_name,
            is_frequency_task = task.is_frequency_task,
            is_notify_fail = task.is_notify_fail,
            is_notify_sucess = task.is_notify_sucess,
            note='Process Error',
            is_finished=False,
            is_error=True,
            duration=duration
        )
        self._handle_task_completion(task, task_completed)
    # end _handle_exception

    def enqueue_completed_task(self, completed_task: TaskCompleted):
        """Enqueue the completed task."""
        with self.queue_lock:
            self.completed_queue.enqueue(completed_task)

    def process_task(self, task: Task, start_date: datetime, start_time: datetime) -> TaskCompleted:
        """Process an individual task."""
        completed = TaskCompleted(
            start_date=start_date,
            task_id=task.task_id,
            task_name=task.task_name,
            task_type=task.task_type,
            is_frequency_task = task.is_frequency_task,
            is_notify_fail = task.is_notify_fail,
            is_notify_sucess = task.is_notify_sucess
        )
        self._logger.info(f'[{task.process_num}][{task.task_id}]'
                          f'[{task.task_name}][{task.task_type}]'
                          f'[{task.config_key_name}]'
                          f'[{task.connection_string}]START PROCESS')
        is_completed = False
        error = None
        note = ''
        try:
            from .taskController import TaskController
            is_completed,_note, error = TaskController.execute_task(task)
            completed.is_finished = is_completed
            completed.note = _note or ''
            if error:
                completed.is_error = True
                self._logger.exception(error)
        except Exception as e:
            completed.is_error = True
            self._logger.exception(e)
        finally:
            completed.duration = self.get_duration(start_time)
            completed.note += f'[Duration: {completed.duration}]'
            self._logger.info(f'[{task.process_num}][{task.task_id}]'
                        f'[{task.task_name}]'
                        f'{completed.note}'
                        f'>>>>>> PROCESSING END')
            
        return completed

    
    # end _execute

    
