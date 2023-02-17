from django.contrib import admin

from hades_star_backend.members.models import (
    Member,
    Mining,
    Shield,
    Support,
    Trade,
    Weapon,
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "as_leader",
        "time_zone",
        "next_ws",
        "rs_level",
        "bs_level",
        "max_mods",
    ]

    list_filter = [
        "as_leader",
        "rs_level",
        "bs_level",
    ]

    search_fields = ["id", "name"]


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ["__str__", "member", "name", "value"]
    readonly_fields = ["position"]

    list_filter = ["name"]

    search_fields = ["member"]


@admin.register(Shield)
class ShieldAdmin(admin.ModelAdmin):
    list_display = ["__str__", "member", "name", "value"]
    readonly_fields = ["position"]

    list_filter = ["name"]

    search_fields = ["member"]


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ["__str__", "member", "name", "value"]
    readonly_fields = ["position"]

    list_filter = ["name"]

    search_fields = ["member"]


@admin.register(Mining)
class MiningAdmin(admin.ModelAdmin):
    list_display = ["__str__", "member", "name", "value"]
    readonly_fields = ["position"]
    list_filter = ["name"]

    search_fields = ["member"]


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "member", "name", "value"]
    readonly_fields = ["position"]

    list_filter = ["name"]

    search_fields = ["member"]
