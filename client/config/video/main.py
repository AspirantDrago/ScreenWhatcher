from ..config_loader import ConfigLoader
from .video_source import VideoSource


class Video(ConfigLoader):
    fps: int = 30
    quality: float = 1.0
    max_ping: float = 1.0
    source: VideoSource = VideoSource()

    @property
    def delay_s(self) -> float:
        return 1 / self.fps

    @property
    def delay_ms(self) -> int:
        return 1000 // self.fps
