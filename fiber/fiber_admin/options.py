from django.contrib.admin import ModelAdmin as DjangoModelAdmin

from mptt.admin import MPTTModelAdmin as DjangoMPTTModelAdmin

from multilingual.admin.options import MultilingualModelAdmin as DjangoMultilingualModelAdmin


class ModelAdmin(DjangoModelAdmin):
    pass


class MPTTModelAdmin(DjangoMPTTModelAdmin):
    pass


class MultilingualModelAdmin(DjangoMultilingualModelAdmin):
    pass