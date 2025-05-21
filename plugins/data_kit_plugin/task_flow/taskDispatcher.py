import threading
import concurrent.futures
import time
from typing import List
from .taskProcessor import TaskProcessor
from .model import Task
from .model import TaskCompleted
from .task_queue import TaskQueue
from .task_queue import CompletedTaskQueue
from utilities import Logger

class TaskDispatcher:
    def __init__(self,max_workers:int = 3):
        # for Queue
        self.task_queue_1 = TaskQueue()
        self.task_queue_2 = TaskQueue()
        self.task_queue_3 = TaskQueue()
        # for Threading
        self.completed_tasks_queue = CompletedTaskQueue()
        self.completed_tasks_queue_lock = threading.Lock()
        self.completed_tasks_event = threading.Event()

        self.task_completion_event_1 = threading.Event()
        self.task_completion_event_2 = threading.Event()
        self.task_completion_event_3 = threading.Event()

        # for log
        self._result_task = []

        self.logger = Logger().logger
        # Max workers for ThreadPoolExecutor
        self.max_workers = max_workers + 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug('Exiting job handler')
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            'run_time', 'task_id', 'logger',
            '_result_task', 'task_queue_1', 'task_queue_2', 'task_queue_3',
            'task_completion_event_1', 'task_completion_event_2', 'task_completion_event_3',
            'completed_tasks_queue', 'completed_tasks_queue_lock','max_workers'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    @property
    def result_task(self) -> List[TaskCompleted]:
        return self._result_task



    def enqueue(self,task:Task):
        if task.process_num == 1:
            self.task_queue_1.enqueue(task)
        elif task.process_num == 2:
            self.task_queue_2.enqueue(task)
        else:
            self.task_queue_3.enqueue(task)
    # end enqueue


    def run_tasks(self):
        """Run the task handler, processing tasks in multiple threads."""
        try:
            processor1 = TaskProcessor(self.task_queue_1, self.completed_tasks_queue, self.completed_tasks_queue_lock, self.task_completion_event_1)
            processor2 = TaskProcessor(self.task_queue_2, self.completed_tasks_queue, self.completed_tasks_queue_lock, self.task_completion_event_2)
            processor3 = TaskProcessor(self.task_queue_3, self.completed_tasks_queue, self.completed_tasks_queue_lock, self.task_completion_event_3)

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                
                future_processor1 = executor.submit(processor1.run)
                future_processor2 = executor.submit(processor2.run)
                future_processor3 = executor.submit(processor3.run)

                future_completed_tasks = executor.submit(self._process_completed_tasks)

                # Chờ các task processors hoàn thành
                concurrent.futures.wait([future_processor1, future_processor2, future_processor3])

                # Chờ xử lý các tasks đã hoàn thành
                future_completed_tasks.result()
            
            # end thread 
            self._log_active_threads()
            

        except Exception as e:
            self.logger.exception(f"Error during run_handler: {e}")
    # end run_tasks
    
    def _log_active_threads(self):
        """Log detailed information about active threads."""
        self.logger.info(f"Number of active threads: {threading.active_count()}")
        
        for thread in threading.enumerate():
            self.logger.info(f"Thread name: {thread.name}, "
                            f"Is daemon: {thread.daemon}, "
                            f"Is alive: {thread.is_alive()}")
    # end _log_active_threads

    def _process_completed_tasks(self):
        """Process completed tasks in a separate thread."""
        while True:
            try:
                if not self.completed_tasks_queue.is_empty():
                    with self.completed_tasks_queue_lock:
                        task_result = self.completed_tasks_queue.dequeue()
                        self._result_task.append(task_result)

                    self.completed_tasks_queue.task_done()
                else:
                    time.sleep(0.5)
                    if self._all_tasks_completed():
                        self.completed_tasks_event.set()
                        break
            except Exception as e:
                self.logger.exception(f"Error while processing completed tasks: {e}")
                self.completed_tasks_event.set()
                break

    

    def _all_tasks_completed(self):
        """Check if all tasks have been completed."""
        return all(event.is_set() for event in [self.task_completion_event_1, self.task_completion_event_2, self.task_completion_event_3])
