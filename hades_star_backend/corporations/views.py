from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.corporations.models import Corporation
from hades_star_backend.corporations.serializers import CorporationSerializer


class CorporationViewSet(GenericViewSet, ListModelMixin):
    serializer_class = CorporationSerializer
    queryset = Corporation.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
