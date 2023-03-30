import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.utils.common_model import CommonModel
from hades_star_backend.utils.ship_attributes import ShipAttribute


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

    def __create_base_attributes(self):
        new_items = []
        # Weapon
        attributes = ShipAttribute("weapon")
        for attribute in attributes.get_attributes():
            new_items.append(
                Weapon(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribure_index(attribute[0]),
                )
            )
        Weapon.objects.bulk_create(new_items)

        new_items = []
        # Shield
        attributes = ShipAttribute("shield")
        for attribute in attributes.get_attributes():
            new_items.append(
                Shield(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribure_index(attribute[0]),
                )
            )
        Shield.objects.bulk_create(new_items)

        new_items = []
        # Support
        attributes = ShipAttribute("support")
        for attribute in attributes.get_attributes():
            new_items.append(
                Support(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribure_index(attribute[0]),
                )
            )
        Support.objects.bulk_create(new_items)

        new_items = []
        # Mining
        attributes = ShipAttribute("mining")
        for attribute in attributes.get_attributes():
            new_items.append(
                Mining(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribure_index(attribute[0]),
                )
            )
        Mining.objects.bulk_create(new_items)

        new_items = []
        # Trade
        attributes = ShipAttribute("trade")
        for attribute in attributes.get_attributes():
            new_items.append(
                Trade(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribure_index(attribute[0]),
                )
            )
        Trade.objects.bulk_create(new_items)

    def remove_corporation(self, corporation_id: str) -> bool:
        corporation = self.corporation.all().filter(id=corporation_id).first()
        if corporation:
            self.corporation.remove(corporation)
            return True
        return False

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        if not Weapon.objects.filter(member=self).exists():
            self.__create_base_attributes()


class AtributeCommonModel(models.Model):

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="members_%(class)s"
    )
    set = models.PositiveSmallIntegerField(default=0)
    max = models.PositiveSmallIntegerField(default=12, editable=True)
    position = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(set__lte=12),
                name="%(app_label)s_%(class)s_max_set__lte_12",
                violation_error_message="Maximum value you can set must be lower than 12",
            ),
            models.UniqueConstraint(
                fields=["member", "name"],
                name="%(app_label)s_%(class)s_unique_member_attribute",
            ),
        ]
        abstract = True

    def __str__(self) -> str:
        return f"{self.name}"


class Weapon(AtributeCommonModel):
    attributes = ShipAttribute("weapon")

    name = models.CharField(
        max_length=30,
        choices=attributes.get_attributes(),
        default=attributes.get_default_attribute(),
    )


class Shield(AtributeCommonModel):
    attributes = ShipAttribute("shield")

    name = models.CharField(
        max_length=30,
        choices=attributes.get_attributes(),
        default=attributes.get_default_attribute(),
    )


class Support(AtributeCommonModel):
    attributes = ShipAttribute("support")

    name = models.CharField(
        max_length=30,
        choices=attributes.get_attributes(),
        default=attributes.get_default_attribute(),
    )

    class Meta(AtributeCommonModel.Meta):
        constraints = AtributeCommonModel.Meta.constraints + [
            models.CheckConstraint(
                check=(
                    models.Q(name="SANCTUARY", set__lte=1)
                    | models.Q(
                        name__in=[
                            "EMP",
                            "TELEPORT",
                            "RED_STAR_LIFE_EXTENDER",
                            "REMOTE_REPAIR",
                            "TIME_WRAP",
                            "UNITY",
                            "STEALTH",
                            "FORTIFY",
                            "IMPULSE",
                            "ALPHA_ROCKET",
                            "SALVAGE",
                            "SUPRESS",
                            "DESTINY",
                            "BARRIER",
                            "VENEGANCE",
                            "DELTA_ROCKET",
                            "LEAP",
                            "BOND",
                            "LASER_TURRET",
                            "ALPHA_DRONE",
                            "SUSPEND",
                            "OMEGA_ROCKET",
                            "REMOTE_BOMB",
                        ],
                        set__lte=12,
                    )
                ),
                name="%(app_label)s_%(class)s_max_set__gt_1_or_lt_12",
                violation_error_message="For Sanctuary maximum value you can set must be lower than 1, rest attributes must be lower than 12",  # noqa E501
            )
        ]


class Mining(AtributeCommonModel):
    attributes = ShipAttribute("mining")

    name = models.CharField(
        max_length=30,
        choices=attributes.get_attributes(),
        default=attributes.get_default_attribute(),
    )


class Trade(AtributeCommonModel):
    attributes = ShipAttribute("trade")

    name = models.CharField(
        max_length=30,
        choices=attributes.get_attributes(),
        default=attributes.get_default_attribute(),
    )
