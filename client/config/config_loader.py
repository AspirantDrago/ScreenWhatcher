from typing import Any
import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class ConfigLoader:
    @classmethod
    def load(cls, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if hasattr(cls, key):
                if isinstance(value, dict):
                    try:
                        getattr(cls, key).load(value)
                    except BaseException as e:
                        logger.error(f'Error loading settings for {key} with value <{value}>: {e}')
                else:
                    setattr(cls, key, value)
                    logger.info(f'Set parameter <{key}> with value <{value}> for class <{cls.__name__}>')
            else:
                logger.warning(f'Unknown parameter <{key}> with value <{value}> for class <{cls.__name__}>')
