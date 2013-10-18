# MPTTModelAdmin is unused, but should stay since its import from here
# has been referenced in documentation.
from django.contrib import admin
from django.http.response import HttpResponseForbidden
from .options import ModelAdmin, MPTTModelAdmin


class FiberAdminSite(admin.AdminSite):

    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelAdmin
        return super(FiberAdminSite, self).register(model_or_iterable, admin_class=admin_class, **options)

    def login(self, request, extra_context=None):
        # The user is not allowed to login using this url
        return HttpResponseForbidden()

site = FiberAdminSite(name='fiber_admin')
