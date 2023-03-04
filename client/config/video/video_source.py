from ..config_loader import ConfigLoader


class VideoSource(ConfigLoader):
    name: str = 'screen'
    number: int | None = None

    @property
    def url_suffix(self) -> str:
        result = f'/{self.name}'
        if self.number is not None:
            result += f'/{self.number}'
        return result
