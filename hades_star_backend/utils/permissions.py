from rest_framework import permissions

from hades_star_backend.corporations.models import Corporation


class CorporationObjectSecretCheck(permissions.BasePermission):
    def has_object_permission(self, request, view, object) -> bool:
        header_secret = request.headers.get("Corporation-Secret", None)
        corporation_id = request.data.get("corporation_id", None)

        if isinstance(object, Corporation):
            corporation = object
        else:
            try:
                corporation = object.corporation.all().get(id=corporation_id)
            except corporation.DoesNotExist:
                corporation = None

        if corporation:
            return corporation.allow_edit(header_secret)
        return False
