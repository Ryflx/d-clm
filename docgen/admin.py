from django.contrib import admin
from .models import DocGenConfiguration, DocLauncherTask

# Register your models here.

@admin.register(DocGenConfiguration)
class DocGenConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'href', 'account_id')
    search_fields = ('name', 'href', 'account_id')

@admin.register(DocLauncherTask)
class DocLauncherTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'configuration', 'status', 'created_at')
    list_filter = ('status', 'user', 'configuration')
    search_fields = ('user__username', 'configuration__name', 'result_url')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
