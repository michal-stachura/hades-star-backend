from django.db import models

from hades_star_backend.utils.common_model import CommonModel


class Corporation(CommonModel):

    name = models.CharField(max_length=50, null=False)
    level = models.PositiveSmallIntegerField(null=False, default=1)
    flag_ship = models.PositiveSmallIntegerField(null=False, default=1)
    required_influence = models.PositiveIntegerField(null=True, blank=True)
    discord = models.URLField(null=True, blank=True)
    ws_wins = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name}"
