import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.utils.common_model import CommonModel


class Member(CommonModel):
    WS_SHIP_ROLE_ALL = "A"
    WS_SHIP_ROLE_HUNTER = "H"
    WS_SHIP_ROLE_UTILITY = "U"
    WS_SHIP_ROLE_DEFENSIVE = "D"
    WS_SHIP_ROLE_VANGUARD = "V"
    WS_SHIP_ROLE_PHALANX = "P"

    WS_READY = "R"
    WS_OPTIONAL = "O"
    WS_EXCLUDED = "X"
    WS_PENDING = "-"

    TIMEZONES = tuple(zip(pytz.common_timezones, pytz.common_timezones))
    NEXT_WS_PREFERENCES = [
        (WS_READY, "Ready"),
        (WS_OPTIONAL, "Optional"),
        (WS_EXCLUDED, "Excluded"),
        (WS_PENDING, "Pending"),
    ]
    WS_SHIP_ROLES = [
        (WS_SHIP_ROLE_ALL, "All roles"),
        (WS_SHIP_ROLE_HUNTER, "Hunter"),
        (WS_SHIP_ROLE_UTILITY, "Utility"),
        (WS_SHIP_ROLE_DEFENSIVE, "Defensive"),
        (WS_SHIP_ROLE_VANGUARD, "Offensive Vanguard"),
        (WS_SHIP_ROLE_PHALANX, "Offensive Phalanx"),
    ]

    name = models.CharField(max_length=50, null=False)
    corporation = models.ManyToManyField(
        Corporation, blank=True, related_name="corporation_members"
    )
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    rs_level = models.PositiveSmallIntegerField(default=0)
    ws_ship_roles = ArrayField(
        models.CharField(max_length=1, blank=True, choices=WS_SHIP_ROLES),
        size=6,
        blank=True,
        null=True,
    )
    next_ws = models.CharField(max_length=1, blank=True, choices=NEXT_WS_PREFERENCES)
    max_mods = models.PositiveSmallIntegerField(default=1)
    bs_level = models.PositiveSmallIntegerField(default=1)
    as_leader = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
