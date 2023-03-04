from dataclasses import dataclass

from statistica.record_timed import RecordTimed


@dataclass
class FrameRecord(RecordTimed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
