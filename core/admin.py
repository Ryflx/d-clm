from django.contrib import admin
from .models import Feature

# Register your models here.

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'feature_id', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'feature_id')
    ordering = ('order', 'title')
