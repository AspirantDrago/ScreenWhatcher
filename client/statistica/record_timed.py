import time

from .record import Record


class RecordTimed(Record):
    def __init__(self, *args, **kwargs):
        self._timestamp = time.time()
        super().__init__(*args, **kwargs)

    @property
    def timestamp(self) -> float:
        return self._timestamp

    def __lt__(self, other: 'RecordTimed') -> bool:
        return self.timestamp < other.timestamp

    def __le__(self, other: 'RecordTimed') -> bool:
        return self.timestamp <= other.timestamp

    def __gt__(self, other: 'RecordTimed') -> bool:
        return self.timestamp > other.timestamp

    def __ge__(self, other: 'RecordTimed') -> bool:
        return self.timestamp >= other.timestamp
