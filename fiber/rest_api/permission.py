from rest_framework.permissions import BasePermission

from fiber.utils import class_loader
from fiber.app_settings import PERMISSION_CLASS


PERMISSIONS = class_loader.load_class(PERMISSION_CLASS)


class RestApiPermission(BasePermission):
    """
    Handle rest api permissions
    """
    def has_permission(self, request, view):
        # todo: handle more permissions here
        return PERMISSIONS.is_fiber_editor(request.user)