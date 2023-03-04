from io import TextIOBase
from typing import Callable

from .auto_save_file import AutoSaveFile


preambula_type = str | Callable[[...], str] | None


class AutoSaveFileRepeater(AutoSaveFile):
    def __init__(self,
                 stream:
                 TextIOBase,
                 filename: str,
                 *args, **kwargs):
        self._stream = stream
        super().__init__(filename, *args, **kwargs)

    def _save_next(self, s: str) -> None:
        if self._stream is not None:
            self._stream.write(s)
        super()._save_next(s)


class AutoSaveFileRepeaterA(AutoSaveFileRepeater):
    def __init__(self,
                 stream:
                 TextIOBase,
                 filename: str,
                 preambula: preambula_type,
                 *args, **kwargs):
        self._preambula = preambula
        super().__init__(stream, filename, *args, **kwargs)

    @property
    def mode(self) -> str:
        return 'a'

    def _save_next(self, s: str) -> None:
        if self._first and self._preambula:
            with open(self._filename, self.mode, encoding=self._encoding) as f:
                if isinstance(self._preambula, str):
                    f.write(self._preambula)
                elif isinstance(self._preambula, Callable):
                    f.write(self._preambula())
        self._first = False
        super()._save_next(s)
