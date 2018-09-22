from django.conf import settings
from django.contrib import admin

from parler.admin import TranslatableAdmin


class AbstractTimeStampModelAdmin(admin.ModelAdmin):
    list_display = ['created_ts', 'last_changed_ts', ]
    list_filter = ['last_changed_ts', 'created_ts', ]
    date_hierarchy = 'last_changed_ts'


class AbstractNameSlugAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']


class AbstractOwnedModelAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'last_changed_by']
    list_filter = ['created_by', 'last_changed_by']

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.owner = obj.owner or user
        obj.created_by = obj.created_by or user
        obj.last_changed_by = user
        super().save_model(request, obj, form, change)


class AbstractBaseModelAdmin(AbstractNameSlugAdmin, AbstractTimeStampModelAdmin, AbstractOwnedModelAdmin):
    list_display = AbstractNameSlugAdmin.list_display +\
        AbstractTimeStampModelAdmin.list_display + AbstractOwnedModelAdmin.list_display
    list_filter = AbstractTimeStampModelAdmin.list_filter + AbstractOwnedModelAdmin.list_filter


class AbstractVisibleModelAdmin(TranslatableAdmin, AbstractBaseModelAdmin):
    list_display = AbstractBaseModelAdmin.list_display + ['visible']
    list_filter = AbstractBaseModelAdmin.list_filter + ['visible']


class AllFieldsReadOnlyMixin(object):
    """
    read only fieldset in admin
    """
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in obj._meta.fields]


class ProductionAllFieldsReadOnlyMixin(object):
    """
    read only fieldset in admin
    """
    def get_readonly_fields(self, request, obj=None):
        if obj and not settings.DEBUG:
            return [f.name for f in obj._meta.fields]
        return []


class ReadOnlyAdminMixin(AllFieldsReadOnlyMixin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DeletableForSuperUserMixin(ReadOnlyAdminMixin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ProductionReadOnlyAdminMixin(ProductionAllFieldsReadOnlyMixin):
    """
    makes a model readonly in admin if DEBUG=False
    """
    def has_add_permission(self, request):
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return settings.DEBUG
