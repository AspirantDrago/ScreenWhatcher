import json
import logging

from .config_loader import ConfigLoader
from .video import Video
from .server import Server
from .other import Other
from .keyboard import Keyboard

logger = logging.getLogger(__name__)
CONFIG_FILENAME = 'config.json'


class Config(ConfigLoader):
    video: Video = Video()
    server: Server = Server()
    other: Other = Other()
    keyboard: Keyboard = Keyboard()

    def __init__(self):
        self.global_init()

    @classmethod
    def global_init(cls):
        try:
            with open(CONFIG_FILENAME) as f:
                cls.load(json.load(f))
        except Exception as e:
            logger.critical(f'Error reading settings file "{CONFIG_FILENAME}": {e}')


Config = Config()
