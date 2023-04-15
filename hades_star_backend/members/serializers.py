from rest_framework import serializers

from hades_star_backend.members.models import (
    Member,
    Mining,
    Shield,
    Support,
    Trade,
    Weapon,
)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name"]


class ModuleAttributeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Meta.model = self.context.get("model", Weapon)

    class Meta:
        fields = ["id", "name", "set", "max"]


class MemberDetailSerializer(MemberSerializer):
    attributes = serializers.SerializerMethodField()
    is_visible = serializers.SerializerMethodField()
    next_ws = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_fields = MemberSerializer.Meta.fields + [
            "corporation",
            "time_zone",
            "rs_level",
            "ws_ship_roles",
            "next_ws",
            "max_mods",
            "bs_level",
            "as_leader",
            "attributes",
            "hsc_id",
            "is_visible",
        ]

        excluded_fields = self.context.get("excluded_fields", [])
        self.Meta.fields = list(set(base_fields) - set(excluded_fields))

    def get_next_ws(self, obj):
        return obj.next_ws or "-"

    def get_is_visible(self, obj):
        return True

    def get_attributes(self, obj):
        attributes = {}
        serializer = ModuleAttributeSerializer(
            obj.members_weapon.all(), many=True, context={"model": Weapon}
        )
        attributes["weapon"] = serializer.data

        serializer = ModuleAttributeSerializer(
            obj.members_shield.all(), many=True, context={"model": Shield}
        )
        attributes["shield"] = serializer.data

        serializer = ModuleAttributeSerializer(
            obj.members_support.all(), many=True, context={"model": Support}
        )
        attributes["support"] = serializer.data

        serializer = ModuleAttributeSerializer(
            obj.members_mining.all(), many=True, context={"model": Mining}
        )
        attributes["mining"] = serializer.data

        serializer = ModuleAttributeSerializer(
            obj.members_trade.all(), many=True, context={"model": Trade}
        )
        attributes["trade"] = serializer.data
        return attributes
