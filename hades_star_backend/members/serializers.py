from rest_framework import serializers

from hades_star_backend.members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name"]


class MemberDetailSerializer(MemberSerializer):
    class Meta(MemberSerializer.Meta):
        fields = MemberSerializer.Meta.fields + [
            "corporation",
            "time_zone",
            "rs_level",
            "ws_ship_roles",
            "next_ws",
            "max_mods",
            "bs_level",
            "as_leader",
        ]
