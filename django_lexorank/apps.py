from django.apps import AppConfig
from django.conf import settings


class DjangoLexorankConfig(AppConfig):
    name = "django_lexorank"

    SETTINGS_MAP: dict[str, str] = {
        "LEXORANK_DEFAULT_RANK_LENGTH": "default_rank_length",
        "LEXORANK_REBALANCING_LENGTH": "rebalancing_length",
        "LEXORANK_MAX_RANK_LENGTH": "max_rank_length",
    }

    def ready(self) -> None:
        from .lexorank import LexoRank

        for setting_name, attr_name in self.SETTINGS_MAP.items():
            value = getattr(settings, setting_name, None)
            if value is not None:
                setattr(LexoRank, attr_name, value)
