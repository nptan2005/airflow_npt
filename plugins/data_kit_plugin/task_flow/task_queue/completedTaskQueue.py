import queue
from ..model import TaskCompleted
from typing import Optional

class CompletedTaskQueue:
    def __init__(self):
        self._queue = queue.Queue()

    def enqueue(self, _taskCompleted: TaskCompleted) -> None:
        """Thêm task vào hàng đợi"""
        self._queue.put(_taskCompleted)

    def dequeue(self, timeout: Optional[int] = None) -> Optional[TaskCompleted]:
        """Lấy task ra khỏi hàng đợi. Nếu timeout, trả về None"""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def is_empty(self) -> bool:
        """Kiểm tra hàng đợi có trống không"""
        return self._queue.empty()

    def join(self) -> None:
        """Chờ tất cả task trong hàng đợi hoàn thành"""
        self._queue.join()

    def task_done(self) -> None:
        """Thông báo rằng một task đã hoàn thành"""
        self._queue.task_done()

    def __repr__(self) -> str:
        return f"<CompletedTaskQueue size={self._queue.qsize()}>"
