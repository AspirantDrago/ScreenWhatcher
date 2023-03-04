import asyncio
import time
from typing import Optional


class TimedTask(asyncio.Task):
    def __init__(self, *args, **kwargs):
        self.created_time = time.time()
        self.active = True
        super().__init__(*args, **kwargs)

    @staticmethod
    def current() -> Optional['TimedTask']:
        return asyncio.current_task()
