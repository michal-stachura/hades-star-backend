from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.members.models import Member
from hades_star_backend.members.serializers import MemberDetailSerializer
from hades_star_backend.utils.permissions import CorporationObjectSecretCheck
from hades_star_backend.utils.ship_attributes import ShipAttribute


class MemberViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
):
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
        CorporationObjectSecretCheck,
    ]

    def create(self, request, *args, **kwargs):
        corporation_id = request.data.get("corporation", None)
        if not corporation_id:
            return Response(
                {"detail": "Please provide member's corporation"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], url_path="next-ws", url_name="next-ws")
    def next_ws(self, request, *args, **kwargs):

        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            member.next_ws = request.data.get("next_ws", None)
            member.save()
            serializer = self.get_serializer(member)
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=["patch"], url_path="attribute", url_name="attribute")
    def attribute(self, request, *args, **kwargs):

        attribute_name = request.data.get("attribute_name", None)
        attribute_id = request.data.get("attribute_id", None)
        attrribute_set = request.data.get("set", None)

        if attribute_name and attribute_id and isinstance(attrribute_set, int):
            attribute = self.__update_attribute(
                attribute_name, attribute_id, attrribute_set
            )
            return Response({"set": attribute.set})
        return Response(status=status.HTTP_404_NOT_FOUND)

    def __update_attribute(self, attribute_name, attribute_id, attribute_set):
        group_name = ShipAttribute().find_group_name_by_attribute_name(attribute_name)
        if group_name == "Weapon":
            attribute = self.get_object().members_weapon.all().get(id=attribute_id)
        elif group_name == "Shield":
            attribute = self.get_object().members_shield.all().get(id=attribute_id)
        elif group_name == "Support":
            attribute = self.get_object().members_support.all().get(id=attribute_id)
        elif group_name == "Mining":
            attribute = self.get_object().members_mining.all().get(id=attribute_id)
        elif group_name == "Trade":
            attribute = self.get_object().members_trade.all().get(id=attribute_id)
        else:
            attribute = None

        if attribute:
            attribute.set = attribute_set
            attribute.save()
        return attribute
