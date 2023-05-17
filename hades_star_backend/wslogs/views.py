from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from hades_star_backend.wslogs.models import WsLog
from hades_star_backend.wslogs.serializers import WsLogSerializer


# Create your views here.
class WSLogsViewSet(GenericViewSet, ListModelMixin):
    queryset = (
        WsLog.objects.all().prefetch_related("corporation").order_by("-created_at")
    )
    serializer_class = WsLogSerializer
    permission_classes = [AllowAny]
