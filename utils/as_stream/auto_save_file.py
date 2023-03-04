import aiofiles

from .auto_save_stream import AutoSaveStream


class AutoSaveFile(AutoSaveStream):
    def __init__(self, filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._filename = filename
        self._first = True

    def _save_next(self, s: str) -> None:
        if self._first:
            with open(self._filename, self.mode, encoding=self._encoding) as f:
                pass
        with open(self._filename, 'a', encoding=self._encoding) as f:
            f.write(s)
        self._first = False

    @property
    def mode(self) -> str:
        return 'w'
