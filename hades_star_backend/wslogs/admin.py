from django.contrib import admin

from hades_star_backend.wslogs.models import WsLog


@admin.register(WsLog)
class WsLogAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "match_type",
        "match_start",
        "created_at",
    )

    list_filter = ("match_type",)

    search_fields = ("id",)
