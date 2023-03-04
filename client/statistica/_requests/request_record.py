from dataclasses import dataclass

from statistica.record_timed import RecordTimed


@dataclass
class RequestRecord(RecordTimed):
    url: str | None = None
    ping: float | None = None
    size: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_size(self, value: int) -> None:
        self.size = value
