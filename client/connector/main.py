import asyncio
import logging
import time
from typing import Callable
import aiohttp

from config import Config
from statistica import Statistica
from .errors import *

from utils.asycnrone import TimedQueue

# requests.adapters.DEFAULT_RETRIES = 1
logger = logging.getLogger(__name__)


class Connector:
    def __init__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(1),
        )
        self._async_request_tasks = TimedQueue()
        # self._session.headers = {
        #     'Bypass-Tunnel-Reminder': 'true'
        # }
        self._server = Config.server.__copy__()

    async def close_session(self) -> None:
        await self._session.close()

    async def load_image(
            self,
            url_value: str,
            callback: Callable,
            timestamp_checker: Callable,
    ) -> None:
        try:
            ts = time.time()
            async with self._session.get(
                url_value,
                timeout=Config.video.max_ping,
            ) as response:
                if not response:
                    raise UnvisibleConnectionException(f'Error {url_value} {response.status_code} ({response.reason})')
                if not getattr(asyncio.current_task(), 'active', True):
                    return
                if not timestamp_checker(ts):
                    return
                self._async_request_tasks.clear_previous()
                data = await response.read()
                ts2 = time.time()
                Statistica.requests.emplace(url=response.url, ping=(ts2 - ts), size=len(data))
                callback(data, timestamp=ts)
        # except ConnectTimeout:
        #     raise VisibleConnectionException('NO CONNECTION')
        except ServerUnavailable:
            if response.status_code == 403:
                if Config.TOKEN is not None:
                    raise VisibleConnectionException('INVALID TOKEN')
                else:
                    raise VisibleConnectionException('TOKEN REQUIRED')
            else:
                raise VisibleConnectionException('SERVER UNAVAILABLE')
        # except (ReadTimeout, requests.ConnectionError):
        #     return
        except Exception as e:
            raise UnvisibleConnectionException(f'Error {e.__class__.__name__}: {e}')

    @property
    def https(self) -> bool:
        return self._server.https

    @https.setter
    def https(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError('https property must be boolean')
        self._server.https = value

    @property
    def host(self) -> str:
        return self._server.host

    @host.setter
    def host(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError('host property must be boolean')
        self._server.host = value

    @property
    def port(self) -> int:
        return self._server._port

    @port.setter
    def port(self, value: int):
        if not isinstance(value, int):
            raise TypeError('port property must be boolean')
        if value < 0 or value > 65535:
            return ValueError('port property must be between 0 and 65535')
        self.port = value

    @property
    def url(self) -> str:
        protocol = 'https://' if self._server.https else 'http://'
        return f'{protocol}{self.host}:{self.port}'
