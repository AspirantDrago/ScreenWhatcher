import logging

from connector import Connector
from config import Config
from config.video.video_source import VideoSource
from player import Player

logger = logging.getLogger(__name__)


class Streamer:
    def __init__(self, connector: Connector, video_source: VideoSource, player: Player):
        self._connector = connector
        self._video_source = video_source
        self._player = player
        self._last_image = None

    @property
    def url(self) -> str:
        return self._connector.url + self._video_source.url_suffix

    async def getImage(self) -> None:
        try:
            await self._connector.load_image(self.url, self._player.show_image, self._player.timestamp_checker)
        except Exception as e:
            logger.error(f'Error {e.__class__.__name__}: {e}')
