from datetime import datetime
from sys import stderr

from .auto_save_file_repeater import AutoSaveFileRepeater, AutoSaveFileRepeaterA, preambula_type


class AutoSaveErr(AutoSaveFileRepeater):
    def __init__(self,
                 filename: str,
                 *args, **kwargs):
        super().__init__(stderr, filename, *args, **kwargs)


class AutoSaveErrA(AutoSaveFileRepeaterA):
    def __init__(self,
                 filename: str,
                 preambula: preambula_type = lambda : f"{'#' * 10}\n### {datetime.now()}\n",
                 *args, **kwargs):
        super().__init__(stderr, filename, preambula, *args, **kwargs)
    
    def _save_next(self, s: str) -> None:
        self._first = True
        super()._save_next(s)
