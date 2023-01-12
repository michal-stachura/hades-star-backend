from random import randrange

from rest_framework import serializers

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.members.serializers import MemberDetailSerializer


class CorporationSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Corporation
        fields = ["id", "name", "members_count"]

    def get_members_count(self, _) -> int:
        return randrange(30)


class CorporationDetailSerializer(CorporationSerializer):
    members = serializers.SerializerMethodField()

    class Meta(CorporationSerializer.Meta):
        fields = CorporationSerializer.Meta.fields + [
            "level",
            "flag_ship",
            "required_influence",
            "members",
            "discord",
            "ws_wins",
        ]

    def get_members(self, obj) -> list:
        serializer = MemberDetailSerializer(obj.corporation_members.all(), many=True)
        return serializer.data
