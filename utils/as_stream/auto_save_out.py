from sys import stdout

from .auto_save_file_repeater import AutoSaveFileRepeater, AutoSaveFileRepeaterA, preambula_type


class AutoSaveOut(AutoSaveFileRepeater):
    def __init__(self,
                 filename: str,
                 *args, **kwargs):
        super().__init__(stdout, filename, *args, **kwargs)


class AutoSaveOutA(AutoSaveFileRepeaterA):
    def __init__(self,
                 filename: str,
                 preambula: preambula_type = '-' * 10 + '\n',
                 *args, **kwargs):
        super().__init__(stdout, filename, preambula, *args, **kwargs)
