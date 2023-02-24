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

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.corporations.serializers import (
    CorporationDetailSerializer,
    CorporationSerializer,
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
