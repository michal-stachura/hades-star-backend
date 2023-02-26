from django.urls import path

from hades_star_backend.utils.views import ShipAttributesApiView

app_name = "utils"

urlpatterns = [
    path("ship-attributes/", ShipAttributesApiView.as_view()),
]
