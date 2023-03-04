from ..config_loader import ConfigLoader


class Server(ConfigLoader):
    host: str = '127.0.0.1'
    https: bool = False
    port: int | None = None
    token: str | None = None

    @property
    def _port(self) -> int:
        if self.port is not None:
            return self.port
        if self.https:
            return 443
        return 80

    def __copy__(self):
        result = Server()
        result.host = self.host
        result.https = self.https
        result.port = self.port
        result.token = self.token
        return result
