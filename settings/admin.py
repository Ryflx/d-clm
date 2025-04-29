from django.contrib import admin
from .models import AppSettings

# Register your models here.

@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('sourcing_login_title',)
    # Since it's a singleton, disable add/delete
    def has_add_permission(self, request):
        return not AppSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
