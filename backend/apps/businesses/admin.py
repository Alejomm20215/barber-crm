from django.contrib import admin
from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'phone', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'owner__username', 'phone', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner')
        }),
        ('Contact Details', {
            'fields': ('address', 'phone', 'email', 'logo_url')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
