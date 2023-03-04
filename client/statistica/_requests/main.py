from typing import Any

from statistica.deque import Deque
from .request_record import RequestRecord


class RequestsStats(Deque):
    SPEED_UNITS = ['bps', 'Kbps', 'Mbps', 'Gbps']

    def emplace(self, **kwargs) -> RequestRecord:
        return self._push(RequestRecord(**kwargs))

    def stats(self) -> dict[str, Any]:
        self._update()
        return {
            'count': self._len,
            'ping': self._ping,
            'ping_mean': self._mean('_sum_ping'),
            'speed': self._normed('_sum_size'),
            'speed_humany': self._speed_humany,
        }

    @property
    def _speed_humany(self) -> str:
        unit = 0
        value = self._normed('_sum_size')
        if value is None:
            value = 0
        while value >= 100:
            unit += 1
            value /= 1000
        if unit == 0:
            return f'{int(value)} {self.SPEED_UNITS[0]}'
        if value >= 10:
            return f'{value:.1f} {self.SPEED_UNITS[unit]}'
        return f'{value:.2f} {self.SPEED_UNITS[unit]}'


    @property
    def _sum_size(self) -> int:
        result = 0
        for rec in self._arr:
            result += rec.size
        return result * 8

    @property
    def _sum_ping(self) -> float:
        result = 0
        for rec in self._arr:
            result += rec.ping
        return result * 1000

    @property
    def _ping(self) -> int:
        if self._arr:
            return int(round(self._arr[-1].ping * 1000))

    @property
    def ping(self) -> int:
        self._update()
        return self._ping
