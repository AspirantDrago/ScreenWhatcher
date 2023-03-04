from ..config_loader import ConfigLoader


class Keyboard(ConfigLoader):
    screenshot: str = 'Ctrl+S'
    reconnect: str = 'F5'
    fullscreen: str = 'FullScreen'
    change_theme: str = 'F12'
    close: str = 'ESC'
    zoom_up: str = '+'
    zoom_down: str = '-'

    def __copy__(self):
        result = Keyboard()
        result.screenshot = self.screenshot
        return result
