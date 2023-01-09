from random import randrange

from rest_framework import serializers

from hades_star_backend.corporations.models import Corporation


class CorporationSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Corporation
        fields = ["id", "name", "members_count"]

    def get_members_count(self, _) -> int:
        return randrange(30)


class CorporationDetailSerializer(CorporationSerializer):
    members = serializers.SerializerMethodField()
    discord = serializers.SerializerMethodField()
    ws_wins = serializers.SerializerMethodField()

    class Meta(CorporationSerializer.Meta):
        fields = CorporationSerializer.Meta.fields + [
            "level",
            "flag_ship",
            "required_influence",
            "members",
            "discord",
            "ws_wins",
        ]

    def get_discord(self, _) -> str:
        return "wwww.discord.com"

    def get_ws_wins(self, _) -> int:
        return 123

    def get_members(self, _) -> list:
        return [
            {
                "id": "uuid-1",
                "username": "Stamina",
                "next_ws": "R",
                "timeZone": "UTC+2",
                "rs_level": 10,
                "bs_level": 6,
                "max_mods": 6,
                "as_eader": False,
                "preferences": ["A"],
            },
            {"id": "uuid-2", "username": "Other username", "next_ws": "R"},
            {"id": "uuid-3", "username": "Boss", "next_ws": "-"},
            {"id": "uuid-4", "username": "Not a boss", "next_ws": "X"},
            {"id": "uuid-5", "username": "AAAA", "next_ws": "-"},
        ]
