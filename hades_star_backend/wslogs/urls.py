from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hades_star_backend.wslogs.views import WSLogsViewSet

app_name = "wslogs"
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", WSLogsViewSet)

urlpatterns = router.urls
