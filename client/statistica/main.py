from ._requests import RequestsStats
from ._frames import FramesStats


class Statistica:
    def __init__(self):
        self.requests = RequestsStats()
        self.frames = FramesStats()

    def reset(self) -> None:
        self.requests.reset()
        self.frames.reset()


Statistica = Statistica()
