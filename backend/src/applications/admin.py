from django.contrib import admin
from django.contrib.auth.models import User

from django.db.models import QuerySet

from .models import Application


def refresh_key(modeladmin, request, queryset):
    for app in queryset:
        app.refresh_key()


refresh_key.short_description = "Обновить ключи API"


class ApplicationsAdmin(admin.ModelAdmin):
    fields = ('owner', 'name', 'api_key', 'created', 'updated',)
    readonly_fields = ('api_key', 'created', 'updated',)
    list_filter = ('created', 'updated',)
    list_display = ('owner', 'name', 'api_key', 'created', 'updated',)
    actions = (refresh_key,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        Clean owners depend on request.user
        if user is not superuser he can see and chuse only himself in owner field
        '''
        user = request.user
        if db_field.name == "owner" and not user.is_superuser:
            kwargs["queryset"] = User.objects.filter(pk=user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request, *args, **kwargs) -> 'QuerySet[Application]':
        '''
        If user is superuser return all applications
        else filter by owner.
        Not superuser can't chuse another users as owners
        '''
        user = request.user
        queryset = super().get_queryset(request, *args, **kwargs)

        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=user)

    def save_model(self, request, obj, form, change):
        '''
        if request.user is not superuser owner can be only request.user
        '''
        user = request.user
        if not user.is_superuser:
            obj.owner = user
        super().save_model(request, obj, form, change)


admin.site.register(Application, ApplicationsAdmin)
