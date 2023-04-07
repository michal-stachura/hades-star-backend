from django.contrib import admin

# Register your models here.
from hades_star_backend.corporations.models import Corporation, Filter


@admin.register(Corporation)
class CorporationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "level",
        "flag_ship",
        "required_influence",
        "created_at",
        "updated_at",
    ]

    list_filter = ["level"]

    search_fields = ["id", "name", "server_id"]


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ["name", "corporation", "created_by", "created_at"]

    search_fields = ["id", "name", "corporation"]
