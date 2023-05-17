from rest_framework import serializers

from hades_star_backend.wslogs.models import WsLog


class WsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WsLog
        fields = [
            "id",
            "corporation",
            "opponent_corporation_name",
            "match_type",
            "match_start",
        ]
