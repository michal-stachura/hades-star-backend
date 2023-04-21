import random
from datetime import datetime

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
    corporation = models.ForeignKey(
        Corporation,
        null=True,
        on_delete=models.CASCADE,
        related_name="corporation_members",
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
    bs_level = models.PositiveSmallIntegerField(default=1)
    miner_level = models.PositiveSmallIntegerField(default=1)
    transport_level = models.PositiveBigIntegerField(default=1)
    as_leader = models.BooleanField(default=False)
    hsc_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(hsc_id__gte=0),
                name="member_hsc_id__gte_0",
                violation_error_message="HSC ID must be positive integer number",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"

    def update_attributes(self, hsc_tech: object) -> None:
        # Weapon
        attributes = ShipAttribute("weapon")
        members_weapons = self.members_weapon.all()
        weapons_to_update = []
        for weapon in members_weapons:
            attribute_hsc_id = attributes.get_attribute(weapon.name)[2]
            weapon.set = hsc_tech["tech"][attribute_hsc_id]
            weapons_to_update.append(weapon)
        Weapon.objects.bulk_update(weapons_to_update, ["set"])

        # Shield
        attributes = ShipAttribute("shield")
        members_shields = self.members_shield.all()
        shields_to_update = []
        for shield in members_shields:
            attribute_hsc_id = attributes.get_attribute(shield.name)[2]
            shield.set = hsc_tech["tech"][attribute_hsc_id]
            shields_to_update.append(shield)
        Shield.objects.bulk_update(shields_to_update, ["set"])

        # Support
        attributes = ShipAttribute("support")
        members_supports = self.members_support.all()
        supports_to_update = []
        for support in members_supports:
            attribute_hsc_id = attributes.get_attribute(support.name)[2]
            support.set = hsc_tech["tech"][attribute_hsc_id]
            supports_to_update.append(support)
        Support.objects.bulk_update(supports_to_update, ["set"])

        # Mining
        attributes = ShipAttribute("mining")
        members_minings = self.members_mining.all()
        minings_to_update = []
        for mining in members_minings:
            attribute_hsc_id = attributes.get_attribute(mining.name)[2]
            mining.set = hsc_tech["tech"][attribute_hsc_id]
            minings_to_update.append(mining)
        Mining.objects.bulk_update(minings_to_update, ["set"])

        # Trade
        attributes = ShipAttribute("trade")
        members_trades = self.members_trade.all()
        trades_to_update = []
        for trade in members_trades:
            attribute_hsc_id = attributes.get_attribute(trade.name)[2]
            trade.set = hsc_tech["tech"][attribute_hsc_id]
            trades_to_update.append(trade)
        Trade.objects.bulk_update(trades_to_update, ["set"])

    def create_base_attributes(self, hsc_tech: object | None = None) -> None:
        new_items = []
        # Weapon
        attributes = ShipAttribute("weapon")
        for attribute in attributes.get_attributes(with_hsc_id=True):
            tech_level = hsc_tech["tech"][attribute[2]] if hsc_tech else 0
            new_items.append(
                Weapon(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribute_index(attribute[0]),
                    set=tech_level,
                )
            )
        Weapon.objects.bulk_create(new_items)

        new_items = []
        # Shield
        attributes = ShipAttribute("shield")
        for attribute in attributes.get_attributes(with_hsc_id=True):
            tech_level = hsc_tech["tech"][attribute[2]] if hsc_tech else 0
            new_items.append(
                Shield(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribute_index(attribute[0]),
                    set=tech_level,
                )
            )
        Shield.objects.bulk_create(new_items)

        new_items = []
        # Support
        attributes = ShipAttribute("support")
        for attribute in attributes.get_attributes(with_hsc_id=True):
            tech_level = hsc_tech["tech"][attribute[2]] if hsc_tech else 0
            new_items.append(
                Support(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribute_index(attribute[0]),
                    set=tech_level,
                )
            )
        Support.objects.bulk_create(new_items)

        new_items = []
        # Mining
        attributes = ShipAttribute("mining")
        for attribute in attributes.get_attributes(with_hsc_id=True):
            tech_level = hsc_tech["tech"][attribute[2]] if hsc_tech else 0
            new_items.append(
                Mining(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribute_index(attribute[0]),
                    set=tech_level,
                )
            )
        Mining.objects.bulk_create(new_items)

        new_items = []
        # Trade
        attributes = ShipAttribute("trade")
        for attribute in attributes.get_attributes(with_hsc_id=True):
            tech_level = hsc_tech["tech"][attribute[2]] if hsc_tech else 0
            new_items.append(
                Trade(
                    member=self,
                    name=attribute[0],
                    max=attributes.get_maximum_value(attribute[0]),
                    position=attributes.get_attribute_index(attribute[0]),
                    set=tech_level,
                )
            )
        Trade.objects.bulk_create(new_items)

    def remove_corporation(self, corporation_id: str) -> bool:
        corporation = self.corporation.all().filter(id=corporation_id).first()
        if corporation:
            self.corporation.remove(corporation)
            return True
        return False

    def find_timezone_name(offset_minutes: int) -> str:
        if offset_minutes is None:
            return "UTC"
        offset_seconds = offset_minutes * 60
        possible_timezones = []

        for tz in pytz.common_timezones:
            timezone = pytz.timezone(tz)
            try:
                tz_offset = timezone.utcoffset(datetime.utcnow()).total_seconds()
            except AttributeError:
                continue
            if tz_offset == offset_seconds:
                possible_timezones.append(tz)
        if offset_minutes is not None and possible_timezones != []:
            return random.choice(possible_timezones)
        return "UTC"

    def save(self, *args, **kwargs):

        if self.is_being_created is True:
            self.create_base_attributes()
        super().save(*args, **kwargs)


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
