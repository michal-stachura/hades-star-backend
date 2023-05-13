from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WslogsConfig(AppConfig):
    name = "hades_star_backend.wslogs"
    verbose_name = _("WS Logs")

    def ready(self):
        try:
            import hades_star_backend.wslogs.signals  # noqa F401
        except ImportError:
            pass
