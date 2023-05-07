from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hades_star_backend.corporations.views import CorporationViewSet

app_name = "corporations"
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", CorporationViewSet)

urlpatterns = router.urls
