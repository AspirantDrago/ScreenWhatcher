import asyncio
import functools
import sys
import time
from typing import Optional
from PyQt6 import sip, QtCore, QtWidgets, QtGui  # Don't remove
from qasync import QApplication, asyncSlot, asyncClose
import qasync
import nest_asyncio
import qdarktheme
import signal

from config import Config
from connector import Connector
from streamer import Streamer
from player import Player
from statistica import Statistica
from keyboard import Keyboard
from ui import Ui_MainWindow

SCREEN_SIZE = [600, 450]

nest_asyncio.apply()
signal.signal(signal.SIGINT, signal.SIG_DFL)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class ClientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    timer = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._connector = Connector()
        self._player = Player(self.video)
        self._streamer = Streamer(
            connector=self._connector,
            video_source=Config.video.source,
            player=self._player
        )
        self._keyboard = Keyboard()
        self._cursor_point: QtCore.QPoint | None = None
        self.btn_reconnect.clicked.connect(self.reconnect)
        self.timer.connect(self.timer_event)
        self.timer.emit()
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.screenshot), self)\
            .activated.connect(self.save_screenshot)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.reconnect), self) \
            .activated.connect(self.reconnect)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.fullscreen), self) \
            .activated.connect(self.toggleFullScreen)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.close), self) \
            .activated.connect(self.close)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.change_theme), self) \
            .activated.connect(self.toggle_theme)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.zoom_up), self) \
            .activated.connect(self._player.zoom_up)
        QtGui.QShortcut(QtGui.QKeySequence(Config.keyboard.zoom_down), self) \
            .activated.connect(self._player.zoom_down)
        self.statusbar_label = QtWidgets.QLabel(self)
        self.statusbar.addWidget(self.statusbar_label)

        self._scrollArea_old_wheelEvent = self.scrollArea.wheelEvent

        def wheelEvent(event: QtGui.QWheelEvent):
            if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                dy = event.angleDelta().y()
                if dy > 0:
                    self._player.zoom_up()
                else:
                    self._player.zoom_down()
                return
            self._scrollArea_old_wheelEvent(event)

        setattr(self.scrollArea, 'wheelEvent', wheelEvent)
        self.scrollArea.viewport().installEventFilter(self.scrollArea)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.video.underMouse():
            self.video.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)
            self._cursor_point = event.pos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.video.underMouse():
            self.video.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
            self._cursor_point = None

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.video.underMouse():
            delta = event.pos() - self._cursor_point
            x = delta.x()
            y = delta.y()
            if x or y:
                self.scrollArea.horizontalScrollBar().setValue(
                    self.scrollArea.horizontalScrollBar().value() - x
                )
                self.scrollArea.verticalScrollBar().setValue(
                    self.scrollArea.verticalScrollBar().value() - y
                )
            self._cursor_point = event.pos()

    @asyncClose
    async def closeEvent(self, event):
        await self._connector.close_session()
        sys.exit(0)

    @asyncSlot()
    async def save_screenshot(self):
        if self.video.text():
            return
        await self._player.save_screenshot()

    @asyncSlot()
    async def timer_event(self):
        while True:
            t1 = time.time()
            task = self._connector._async_request_tasks.create_timed_task(
                self._streamer.getImage()
            )
            self.update_statusbar()
            t2 = time.time()
            await asyncio.sleep(
                max(0.0, Config.video.delay_s - (t2 - t1))
            )

    def toggle_theme(self) -> None:
        Config.other.next_theme()
        self._player.show_message(f'{Config.other.theme.upper()} theme selected')
        qdarktheme.setup_theme(Config.other.theme)

    def toggleFullScreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def reconnect(self) -> None:
        self.video.setText('Loading ...')
        Config.global_init()
        Statistica.reset()

    def update_statusbar(self) -> None:
        def placeholder(obj, tol: Optional[int] = None) -> str:
            if obj is None:
                return '...'
            if tol is not None:
                obj = round(obj, tol)
                if tol == 0:
                    obj = int(obj)
            return str(obj)

        requests_stats = Statistica.requests.stats()
        frames_stats = Statistica.frames.stats()
        text = ''
        text += 'FPS: {}'.format(
            placeholder(frames_stats["fps"], 0),
        )
        text += '\t\tping: {:>3} ms\t(mean {:>3} ms)'.format(
            placeholder(requests_stats["ping"], 0),
            placeholder(requests_stats["ping_mean"], 0),
        )
        text += '\t {}'. format(requests_stats["speed_humany"])
        text += '\t\tzoom: {:>3}%'.format(
            placeholder(self._player.scale * 100, 0),
        )
        self.statusbar_label.setText(text)


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    app = QApplication(sys.argv)
    app.exec_ = app.exec
    qdarktheme.setup_theme(Config.other.theme)
    loop = asyncio.get_event_loop()

    future = asyncio.Future()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    window = ClientWindow()
    window.show()

    await future
    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
