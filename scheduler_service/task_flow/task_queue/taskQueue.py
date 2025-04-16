import queue
from typing import Optional
from ..model import Task
class TaskQueue:
    def __init__(self):
        self._queue = queue.Queue()

    def enqueue(self, task: Task):
        """Add a task to the queue."""
        self._queue.put(task)

    def dequeue(self,timeout: Optional[int] = None) -> Optional[Task]:
        """Remove and return a task from the queue."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._queue.empty()

    def join(self):
        """Wait for all tasks in the queue to be processed."""
        self._queue.join()

    def task_done(self):
        """Indicate that a previously enqueued task is complete."""
        self._queue.task_done()

    def __repr__(self) -> str:
        return f"<TaskQueue size={self._queue.qsize()}>"
