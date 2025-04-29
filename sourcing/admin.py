from django.contrib import admin
from .models import SourcingLogin

# Register your models here.

@admin.register(SourcingLogin)
class SourcingLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplier_name', 'supplier_email', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'supplier_name', 'supplier_email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
