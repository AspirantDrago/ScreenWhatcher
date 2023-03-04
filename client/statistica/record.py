import logging

logger = logging.getLogger(__name__)


class Record:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.info(f'Set parameter <{key}> with value <{value}> for object of class <{self.cls_name}>')
            else:
                logger.warning(f'Unknown parameter <{key}> with value <{value}> for object of class <{self.cls_name}>')

    @property
    def cls_name(self):
        return self.__class__.__name__
