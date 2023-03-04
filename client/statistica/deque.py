from collections import deque
import time

from config import Config
from .record_timed import RecordTimed


class Deque:
    def __init__(self):
        self._arr: deque[RecordTimed] = deque()

    def _push(self, rec: RecordTimed) -> RecordTimed:
        self._arr.append(rec)
        self._update()
        return rec

    def _update(self) -> None:
        t = time.time()
        while self._arr:
            delta = t - self._arr[0].timestamp
            if delta > Config.other.statistica_lag_size:
                self._arr.popleft()
                continue
            break

    def reset(self) -> None:
        self._arr.clear()

    @property
    def _duration(self) -> float:
        if not self._arr:
            return 0.0
        t = time.time()
        delta = t - self._arr[0].timestamp
        return delta

    @property
    def duration(self) -> float:
        self._update()
        return self._duration

    @property
    def _len(self) -> int:
        return len(self._arr)

    def __len__(self) -> int:
        self._update()
        return self._len

    @property
    def _bool(self) -> bool:
        return bool(self._arr)

    def __bool__(self) -> bool:
        self._update()
        return self._bool

    def _normed(self, attr: str) -> float | None:
        if not self._duration:
            return
        return getattr(self, attr) / self._duration

    def normed(self, attr: str) -> float | None:
        self._update()
        return self._normed(attr)

    def _mean(self, attr: str) -> float | None:
        if not self._arr:
            return
        return getattr(self, attr) / self._len

    def mean(self, attr: str) -> float | None:
        self._update()
        return self._mean(attr)
