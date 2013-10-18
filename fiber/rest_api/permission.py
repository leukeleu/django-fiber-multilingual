from rest_framework.permissions import BasePermission

from fiber.utils import class_loader
from fiber.app_settings import PERMISSION_CLASS


PERMISSIONS = class_loader.load_class(PERMISSION_CLASS)


class RestApiPermission(BasePermission):
    """
    Handle rest api permissions for 'GET' request. Other request types are handled in the restapi views
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            # The user must be fiber editor
            return PERMISSIONS.is_fiber_editor(request.user)
        else:
            # Other methods are handled in the restapi views
            return True