from typing import Any

from statistica.deque import Deque
from .frame_record import FrameRecord


class FramesStats(Deque):
    def emplace(self, **kwargs) -> FrameRecord:
        return self._push(FrameRecord(**kwargs))

    def stats(self) -> dict[str, Any]:
        self._update()
        return {
            'count': self._len,
            'fps': self._normed('_len'),
        }
