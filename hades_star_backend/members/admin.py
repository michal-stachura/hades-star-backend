from django.contrib import admin

from hades_star_backend.members.models import Member


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
