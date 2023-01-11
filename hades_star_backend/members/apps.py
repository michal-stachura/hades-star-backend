from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembersConfig(AppConfig):
    name = "hades_star_backend.members"
    verbose_name = _("Members")

    def ready(self):
        try:
            import hades_star_backend.members.signals  # noqa F401
        except ImportError:
            pass
