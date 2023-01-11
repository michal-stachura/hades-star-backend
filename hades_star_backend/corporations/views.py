from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.corporations.serializers import (
    CorporationDetailSerializer,
    CorporationSerializer,
)


class CorporationViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Corporation.objects.all().order_by("name")
    lookup_field = "id"
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CorporationDetailSerializer
        return CorporationSerializer
