from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.members.models import Member
from hades_star_backend.members.serializers import MemberDetailSerializer
from hades_star_backend.utils.ship_attributes import ShipAttribute


class MemberViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = (
        Member.objects.all()
        .prefetch_related(
            "members_weapon",
            "members_shield",
            "members_support",
            "members_mining",
            "members_trade",
        )
        .order_by("name")
    )
    serializer_class = MemberDetailSerializer
    lookup_field = "id"
    permission_classes = [
        AllowAny,
    ]

    @action(detail=True, methods=["patch"], url_path="next-ws", url_name="next-ws")
    def next_ws(self, request, *args, **kwargs):
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=["patch"], url_path="attribute", url_name="attribute")
    def attribute(self, request, *args, **kwargs):
        attribute_name = request.data.get("attribute_name", None)
        attribute_id = request.data.get("attribute_id", None)
        attrribute_value = request.data.get("value", None)
        if attribute_name and attribute_id and attrribute_value:
            attribute = self.__update_attribute(
                attribute_name, attribute_id, attrribute_value
            )
            return Response({"current_value": attribute.value})
        return Response(status=status.HTTP_404_NOT_FOUND)

    def __update_attribute(self, attribute_name, attribute_id, attribute_value):
        group_name = ShipAttribute().find_group_name_by_attribute_name(attribute_name)
        if group_name == "weapon":
            attribute = self.get_object().members_weapon.all().get(id=attribute_id)
        elif group_name == "shield":
            attribute = self.get_object().members_shield.all().get(id=attribute_id)
        elif group_name == "support":
            attribute = self.get_object().members_support.all().get(id=attribute_id)
        elif group_name == "mining":
            attribute = self.get_object().members_mining.all().get(id=attribute_id)
        elif group_name == "trade":
            attribute = self.get_object().members_trade.all().get(id=attribute_id)
        else:
            attribute = None

        if attribute:
            attribute.value = attribute_value
            attribute.save()
        return attribute
