from rest_framework import permissions

from hades_star_backend.corporations.models import Corporation


class CorporationObjectSecretCheck(permissions.BasePermission):
    def has_object_permission(self, request, view, object) -> bool:
        header_secret = request.headers.get("Corporation-Secret", None)
        corporation = None

        if isinstance(object, Corporation):
            corporation = object
        else:
            corporation_id = request.data.get("corporation", None)
            if corporation_id:
                try:
                    corporation = Corporation.objects.get(id=corporation_id)
                except Corporation.DoesNotExist:
                    pass

        if corporation:
            return corporation.allow_edit(header_secret)
        return False
