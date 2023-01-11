import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models

from hades_star_backend.utils.common_model import CommonModel


class Member(CommonModel):
    WS_READY = "R"
    WS_OPTIONAL = "O"
    WS_EXCLUDED = "X"
    WS_PENDING = "-"

    TIMEZONES = tuple(zip(pytz.common_timezones, pytz.common_timezones))
    PREFERENCES = [
        (WS_READY, "Ready"),
        (WS_OPTIONAL, "Optional"),
        (WS_EXCLUDED, "Excluded"),
        (WS_PENDING, "Pending"),
    ]

    name = models.CharField(max_length=50, null=False)
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    rs_level = models.PositiveSmallIntegerField(default=0)
    preferences = ArrayField(
        models.CharField(max_length=1, blank=True, choices=PREFERENCES), size=5
    )
    next_ws = models.CharField(max_length=1, blank=True, choices=PREFERENCES)
    max_mods = models.PositiveSmallIntegerField(default=1)
    bs_level = models.PositiveSmallIntegerField(default=1)
    as_leader = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
