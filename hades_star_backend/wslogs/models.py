from django.db import models

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.utils.common_model import CommonModel


class WsLog(CommonModel):

    WS_SMALL = "5vs5"
    WS_MEDIUM = "10vs10"
    WS_LARGE = "15vs15"

    WS_MATCH_TYPES = (
        (WS_SMALL, "5 vs. 5"),
        (WS_MEDIUM, "10 vs. 10"),
        (WS_LARGE, "15 vs. 15"),
    )

    corporation = models.ForeignKey(
        Corporation, on_delete=models.CASCADE, related_name="corporation_wslogs"
    )
    opponent_corporation_name = models.CharField(max_length=90, blank=True)
    match_type = models.CharField(
        max_length=6, choices=WS_MATCH_TYPES, blank=True, null=True
    )
    match_start = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        corp_name = (
            self.opponent_corporation_name
            if self.opponent_corporation_name
            else "Not set yet"
        )
        return f"{self.match_type} - {self.corporation.name} vs {corp_name}"
