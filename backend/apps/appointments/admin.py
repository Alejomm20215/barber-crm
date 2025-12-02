from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'staff', 'service', 'scheduled_at', 'status', 'price']
    list_filter = ['status', 'scheduled_at', 'created_at']
    search_fields = ['customer__name', 'staff__name', 'service__name', 'business__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'scheduled_at'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('business', 'customer', 'staff', 'service')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'status', 'completed_at')
        }),
        ('Pricing & Notes', {
            'fields': ('price', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related(
            'business', 'customer', 'staff', 'service'
        )
