from django.db import models

from hades_star_backend.utils.common_model import CommonModel


class Corporation(CommonModel):

    name = models.CharField(max_length=50, null=False)
    level = models.PositiveSmallIntegerField(null=False, default=1)
    flag_ship = models.PositiveSmallIntegerField(null=False, default=1)
    required_influence = models.PositiveIntegerField(null=True, blank=True)
    discord = models.URLField(null=True, blank=True)
    ws_wins = models.PositiveSmallIntegerField(default=0)
    secret = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return f"{self.name}"

    def allow_edit(self, secret_string: str) -> bool:
        return secret_string == self.secret

    def set_secret(self, new_secret: str) -> None:
        self.secret = new_secret
        self.save()


class Filter(CommonModel):

    name = models.CharField(max_length=50, null=False)
    corporation = models.ForeignKey(
        Corporation, on_delete=models.CASCADE, related_name="corporation_filter"
    )
    created_by = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        related_name="member_filter",
        blank=True,
        null=True,
    )
    conditions = models.JSONField(null=False, blank=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"
