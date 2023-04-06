from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from hades_star_backend.utils.ship_attributes import ShipAttribute


class ShipAttributesApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(ShipAttribute().get_attributes_json_dict())
