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
            # TODO: Clea up this code
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
        detail=True, methods=["get"], url_path="sync-members", url_name="sync-members"
    )
    def sync_members(self, request, *args, **kwargs):
        corporation = self.get_object()
        if corporation.role_id:
            res = requests.get(
                f"{settings.HSC_BOT_API}/techByRole?asArray=1&token={settings.HSC_TOKEN}&roleid={corporation.role_id}&rolename=bloodtide"  # noqa E501
            )
            if res.status_code == 200:
                data = res.json()
                return Response(res.json(), status=res.status_code)

            else:
                return Response(res.json(), status=res.status_code)
        return Response(status=status.HTTP_400_BAD_REQUEST)
