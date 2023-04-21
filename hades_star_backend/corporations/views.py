import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.corporations.models import Corporation, Filter
from hades_star_backend.corporations.serializers import (
    CorporationDetailSerializer,
    CorporationSerializer,
    FilterSerializer,
)
from hades_star_backend.members.models import Member
from hades_star_backend.utils.permissions import CorporationObjectSecretCheck


class CorporationViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
):
    queryset = (
        Corporation.objects.prefetch_related(
            "corporation_members", "corporation_filter"
        )
        .all()
        .order_by("name")
    )
    lookup_field = "id"
    permission_classes = [
        CorporationObjectSecretCheck,
    ]

    def get_serializer_class(self):
        if self.action in ["retrieve", "partial_update"]:
            return CorporationDetailSerializer
        return CorporationSerializer

    def create(self, request, *args, **kwargs):
        new_corporation = Corporation.objects.create(
            name=request.data.get("name"),
            secret=request.data.get("secret"),
        )

        if new_corporation:
            serializer = self.get_serializer(new_corporation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Error adding corporation"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True, methods=["get"], url_path="check-secret", url_name="check-secret"
    )
    def check_secret(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]
        secret = request.GET.get("secret", None)

        if self.get_object().allow_edit(secret):
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"status_text": "This secret is not correct"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(
        detail=True, methods=["patch"], url_path="set-secret", url_name="set-secret"
    )
    def set_secret(self, request, *args, **kwargs):
        new_secret = request.data.get("new_secret", None)
        if new_secret is not None and new_secret != "":
            self.get_object().set_secret(new_secret)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"status_text": "Please provide a new secret"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=["post"], url_path="add-filter", url_name="add-filter")
    def add_filter(self, request, *args, **kwargs):
        filter = Filter.objects.create(
            name=request.data.get("name", ""),
            corporation=self.get_object(),
            conditions=request.data.get("conditions", {}),
        )
        serializer = FilterSerializer(filter)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True, methods=["patch"], url_path="edit-filter", url_name="edit-filter"
    )
    def edit_filter(self, request, *args, **kwargs):
        corporation = self.get_object()
        filter_id_to_edit = request.data.get("filter_id", None)

        try:
            # TODO: Clean up this code
            corp_filter = corporation.corporation_filter.get(id=filter_id_to_edit)
            corp_filter.name = request.data.get("name", "")
            corp_filter.conditions = request.data.get("conditions", {})
            corp_filter.save()
            serializer = FilterSerializer(corp_filter)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Filter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=["delete"],
        url_path="delete-filter",
        url_name="delete-filter",
    )
    def delete_filter(self, request, *args, **kwargs):
        corporation = self.get_object()
        filter_id_to_delete = request.data.get("filter_id", None)

        try:
            corp_filter = corporation.corporation_filter.get(id=filter_id_to_delete)
            corp_filter.delete()
            resp_status = status.HTTP_204_NO_CONTENT
        except Filter.DoesNotExist:
            resp_status = status.HTTP_404_NOT_FOUND

        return Response(status=resp_status)

    @action(
        detail=True,
        methods=["get"],
        url_path="sync-tech",
        url_name="sync-tech",
    )
    def sync_tech(self, request, *args, **kwargs):
        corporation = self.get_object()
        if corporation.role_id:
            current_members_hsc_ids = corporation.get_current_members_hsc_ids()

            if current_members_hsc_ids != []:
                members_with_hsc_id = corporation.corporation_members.filter(
                    hsc_id__in=current_members_hsc_ids
                )
                res = requests.get(
                    f"{settings.HSC_BOT_API}/techByRole?asArray=1&token={settings.HSC_TOKEN}&roleid={corporation.role_id}&rolename=bloodtide"  # noqa E501
                )
                hsc_members = res.json() if res.status_code == 200 else []
                for member in members_with_hsc_id:
                    try:
                        hsc_tech = list(
                            filter(
                                lambda item: item["id"] == member.hsc_id,
                                hsc_members["data"],
                            )
                        )[0]
                        member.update_attributes(hsc_tech)
                    except IndexError:
                        continue

            serializer = CorporationDetailSerializer(corporation)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="sync-members",
        url_name="sync-members",
    )
    def sync_members(self, request, *args, **kwargs):
        corporation = self.get_object()

        if request.method == "GET":
            if corporation.role_id:
                res = requests.get(
                    f"{settings.HSC_BOT_API}/techByRole?asArray=1&token={settings.HSC_TOKEN}&roleid={corporation.role_id}&rolename=bloodtide"  # noqa E501
                )
                return Response(res.json(), status=res.status_code)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "POST":

            current_members_hsc_ids = corporation.get_current_members_hsc_ids()
            selected_members = request.data.get("selected_members", [])
            members_to_add = []
            for member in selected_members:
                tz_offset = member["tz_offset"] if "tz_offset" in member else None
                if member["id"] not in current_members_hsc_ids:
                    members_to_add.append(
                        Member(
                            name=member["name"],
                            hsc_id=member["id"],
                            time_zone=Member.find_timezone_name(tz_offset),
                            corporation=corporation,
                            rs_level=member["tech"]["rs"] if "tech" in member else 0,
                            bs_level=member["tech"]["bs"] if "tech" in member else 1,
                            miner_level=member["tech"]["miner"]
                            if "tech" in member
                            else 1,
                            transport_level=member["tech"]["transp"]
                            if "tech" in member
                            else 1,
                        )
                    )

            if members_to_add != []:
                Member.objects.bulk_create(members_to_add)

                for member in members_to_add:
                    try:
                        hsc_tech = list(
                            filter(
                                lambda item: item["id"] == member.hsc_id,
                                selected_members,
                            )
                        )[0]
                        member.create_base_attributes(hsc_tech)
                    except IndexError:
                        continue

            serializer = CorporationDetailSerializer(corporation)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
