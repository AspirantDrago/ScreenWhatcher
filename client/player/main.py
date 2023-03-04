import aiofiles
import logging
import time
from typing import Any, Optional
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel
from pathlib import Path
import os.path
from PIL import Image, ImageQt
from io import BytesIO

from statistica import Statistica
from config import Config

logger = logging.getLogger(__name__)


class Player:
    PADDING_WIDTH = 1

    def __init__(self, canvas: QLabel):
        self._canvas = canvas
        self.reset()

    def reset(self):
        self._last_image: Image.Image | None = None
        self._timestamp = time.time()
        self._scale: float | None = None

    def _find_scale(self) -> None:
        player_w = self._canvas.width() - 2 * self.PADDING_WIDTH
        player_h = self._canvas.width() - 2 * self.PADDING_WIDTH
        image_w, image_h = self._last_image.size
        self._scale = min(player_w / image_w, player_h / image_h)

    def zoom_up(self):
        if self._scale is not None:
            self._scale *= Config.other.scale_factor
            self.show_image()

    def zoom_down(self):
        if self._scale is not None:
            self._scale /= Config.other.scale_factor
            self.show_image()

    def show_image(
            self,
            data: Optional[bytes] = None,
            timestamp: Optional[float] = None
    ) -> None:
        if timestamp is None:
            timestamp = time.time()
        if timestamp <= self._timestamp:
            logger.debug('Received an old frame')
            return
        if data is None:
            if self._last_image is None:
                return
        else:
            self._last_image = Image.open(BytesIO(data), formats=['jpeg'])
            Statistica.frames.emplace()
        im = ImageQt.ImageQt(self._last_image)
        pixmap = QtGui.QPixmap().fromImage(im)
        if pixmap.size().isEmpty():
            logger.debug('Received an empty frame')
            return
        if self._scale is None:
            self._find_scale()
        pixmap = pixmap.scaled(
            int(pixmap.width() * self._scale),
            int(pixmap.height() * self._scale),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self._timestamp = timestamp
        self._canvas.setPixmap(pixmap)

    def timestamp_checker(self, timestamp: float) -> bool:
        return timestamp > self._timestamp

    @property
    def scale(self) -> float:
        if self._scale is None:
            return 1.0
        return self._scale

    def show_message(self, message: Any) -> None:
        self._canvas.setText(str(message))

    async def _save_image(self, path: str, image: memoryview) -> None:
        async with aiofiles.open(path, "wb") as file:
            await file.write(image)
            self.show_message('saved')

    async def save_screenshot(self) -> None:
        if self._last_image is not None:
            Path('screenshots').mkdir(parents=True, exist_ok=True)
            filename = f'screen_{time.strftime("%Y%m%d-%H%M%S")}.png'
            filename = os.path.join('screenshots', filename)
            buffer = BytesIO()
            self._last_image.save(buffer, 'PNG', quality=1)
            await self._save_image(filename, buffer.getbuffer())
