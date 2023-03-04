from ..config_loader import ConfigLoader


class Other(ConfigLoader):
    THEMES = ('dark', 'light', 'auto')

    statistica_lag_size: int = 100
    theme: str = 'auto'
    scale_factor: float = 1.1

    @classmethod
    def next_theme(cls) -> None:
        try:
            ind = cls.THEMES.index(cls.theme)
            ind = (ind + 1) % len(cls.THEMES)
            cls.theme = cls.THEMES[ind]
        except ValueError:
            cls.theme = 'auto'
