from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# from hades_star_backend.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)

urlpatterns = router.urls
