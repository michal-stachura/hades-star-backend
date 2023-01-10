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
    class Meta(CorporationSerializer.Meta):
        fields = CorporationSerializer.Meta.fields + [
            "level",
            "flag_ship",
            "required_influence",
        ]
