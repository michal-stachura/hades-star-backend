from rest_framework import serializers

from hades_star_backend.corporations.models import Corporation, Filter
from hades_star_backend.members.serializers import MemberDetailSerializer


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ["id", "name", "corporation", "created_by", "conditions"]


class CorporationSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Corporation
        fields = ["id", "name", "members_count"]

    def get_members_count(self, obj) -> int:
        return obj.corporation_members.all().count()


class CorporationDetailSerializer(CorporationSerializer):
    members = serializers.SerializerMethodField()
    filters = serializers.SerializerMethodField()

    class Meta(CorporationSerializer.Meta):
        fields = CorporationSerializer.Meta.fields + [
            "level",
            "flag_ship",
            "required_influence",
            "members",
            "discord",
            "ws_wins",
            "role_id",
            "filters",
        ]

    def get_members(self, obj) -> list:
        serializer = MemberDetailSerializer(
            obj.corporation_members.prefetch_related(
                "members_weapon",
                "members_shield",
                "members_support",
                "members_mining",
                "members_trade",
            )
            .all()
            .order_by("name"),
            many=True,
            context={"excluded_fields": ["corporation"]},
        )
        return serializer.data

    def get_filters(self, obj) -> list:
        serializer = FilterSerializer(
            obj.corporation_filter.all(),
            many=True,
        )
        return serializer.data
