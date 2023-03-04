from contextlib import redirect_stdout, redirect_stderr

from .auto_save_out import AutoSaveOutA, AutoSaveOut
from .auto_save_err import AutoSaveErrA, AutoSaveErr


def stdout(filename: str, mode: str = 'w'):
    if mode == 'w':
        redirect_stdout(AutoSaveOut(filename)).__enter__()
    elif mode == 'a':
        redirect_stdout(AutoSaveOutA(filename)).__enter__()
    else:
        raise ValueError('Wrong mode')


def stderr(filename: str, mode: str = 'a'):
    if mode == 'w':
        redirect_stderr(AutoSaveErr(filename)).__enter__()
    elif mode == 'a':
        redirect_stderr(AutoSaveErrA(filename)).__enter__()
    else:
        raise ValueError('Wrong mode')
