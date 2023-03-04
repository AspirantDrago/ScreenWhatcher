from io import TextIOBase, UnsupportedOperation
from collections import deque
from typing import Iterable, BinaryIO
from abc import ABC, abstractmethod


class AutoSaveStream(TextIOBase, ABC):
    def __init__(self, *args, endline='\n', **kwargs):
        super().__init__()
        self._closed = False
        self._endline = endline
        self._clear()
        self._encoding = 'utf-8'
        self.buffer = None

    @staticmethod
    def only_opened(method):
        def wrapper(self, *args, **kwargs):
            if self._closed:
                raise ValueError('AutoSaveStream closed')
            return method(self, *args, **kwargs)

        return wrapper

    @property
    @only_opened
    def newlines(self) -> tuple[str, ...]:
        return tuple(self._buffer)

    def _clear(self) -> None:
        self._buffer = deque([''])

    def _append(self, s: str) -> None:
        self._buffer.append(s)

    @abstractmethod
    def _save_next(self, s: str) -> None:
        pass

    def _add_new_line(self):
        self._append('')
        self._save_next(self._endline)

    @only_opened
    def write(self, __s: str) -> int:
        self._buffer[-1] += __s
        self._save_next(__s)
        return len(__s)

    @only_opened
    def writelines(self, __lines: Iterable[str]) -> None:
        for line in __lines:
            self.write(line)
            self._add_new_line()

    def close(self) -> None:
        self._clear()
        self._closed = True

    def closed(self) -> bool:
        return self._closed

    def fileno(self) -> int:
        raise OSError(f'{self.__class__.__name__} don\'t have file descriptor')

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    def readable(self) -> bool:
        return False

    def read(self, __size: int | None = ...) -> str:
        raise OSError(f'{self.__class__.__name__} is write-only')

    def readline(self, __size: int = ...) -> str:
        raise OSError(f'{self.__class__.__name__} is write-only')

    def readlines(self, __hint: int = ...) -> list[str]:
        raise OSError(f'{self.__class__.__name__} is write-only')

    def seek(self, __offset: int, __whence: int = ...) -> int:
        raise OSError(f'{self.__class__.__name__} is not seekable')

    def seekable(self) -> bool:
        return False

    def tell(self) -> int:
        raise OSError(f'{self.__class__.__name__} is not seekable')

    def truncate(self, __size: int | None = ...) -> int:
        raise OSError(f'{self.__class__.__name__} is not seekable')

    def writable(self) -> bool:
        return True

    def detach(self) -> BinaryIO:
        raise UnsupportedOperation

