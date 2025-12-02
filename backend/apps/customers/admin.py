from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'phone', 'total_visits', 'total_spent', 'last_visit']
    list_filter = ['created_at', 'last_visit']
    search_fields = ['name', 'phone', 'email', 'business__name']
    readonly_fields = ['total_visits', 'total_spent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business', 'name')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email')
        }),
        ('Customer Data', {
            'fields': ('notes', 'preferences', 'total_visits', 'total_spent', 'last_visit')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
