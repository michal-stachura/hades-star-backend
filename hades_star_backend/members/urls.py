from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hades_star_backend.members.views import MemberViewSet

app_name = "corporations"
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", MemberViewSet)

urlpatterns = router.urls
