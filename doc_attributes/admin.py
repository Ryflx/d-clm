from django.contrib import admin
from .models import DocumentAttribute

# Register your models here.

@admin.register(DocumentAttribute)
class DocumentAttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_id', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'document_id')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
