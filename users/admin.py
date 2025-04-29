from django.contrib import admin
from .models import DocusignCredentials

# Register your models here.

@admin.register(DocusignCredentials)
class DocusignCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'client_id', 'account_id', 'is_configured', 'token_expiry', 'updated_at')
    list_filter = ('is_configured',)
    search_fields = ('user__username', 'client_id', 'account_id')
    readonly_fields = ('created_at', 'updated_at', 'token_expiry') # Make token fields read-only
    ordering = ('user__username',)
    # Hide sensitive fields like secret/tokens by default unless needed
    # fields = ('user', 'client_id', 'account_id', 'is_configured', 'token_expiry', 'created_at', 'updated_at')
