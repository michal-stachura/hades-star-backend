from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CorporationsConfig(AppConfig):
    name = "hades_star_backend.corporations"
    verbose_name = _("Corporations")

    def ready(self):
        try:
            import hades_star_backend.corporations.signals  # noqa F401
        except ImportError:
            pass
