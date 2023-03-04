import asyncio
import time
from asyncio import Task
from collections import deque

from .timed_task import TimedTask


class TimedQueue:
    def __init__(self):
        self._queue: deque[TimedTask] = deque()

    def append(self, task: TimedTask | Task) -> None:
        self._queue.append(task)

    def appendleft(self, task: TimedTask | Task) -> None:
        self._queue.appendleft(task)

    def pop(self) -> TimedTask | Task:
        return self._queue.pop()

    def popleft(self) -> TimedTask | Task:
        return self._queue.popleft()

    def create_timed_task(self, coro, *args, **kwargs) -> TimedTask:
        task = asyncio.get_event_loop().create_task(coro, *args, **kwargs)
        task.created_time = time.time()
        task.active = True
        self.append(task)
        return task

    def clear_previous(self) -> None:
        i = 0
        current_task = asyncio.current_task()
        current_time = getattr(current_task, 'created_time', time.time())
        while self._queue:
            i += 1
            if i > len(self):
                break
            latest_task = self._queue[0]
            if latest_task.done() or latest_task.cancelled():
                latest_task.active = False
                self.popleft()
                break
            if not hasattr(latest_task, 'created_time'):
                self.append(self.popleft())
                continue
            if latest_task == current_task or latest_task.created_time >= current_time:
                break
            r1 = latest_task.cancel() == True
            assert r1, f"Task {latest_task} don't make cancelled"
            r2 = latest_task.cancelled() == True
            latest_task.active = False
            # assert r2, f"Task {latest_task} don't cancelled"
            self.popleft()

    def __len__(self) -> int:
        return len(self._queue)