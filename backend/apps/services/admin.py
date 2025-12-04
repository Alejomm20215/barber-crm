from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "business", "price", "duration", "category", "is_active"]
    list_filter = ["is_active", "category", "created_at"]
    search_fields = ["name", "description", "business__name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("business", "name", "description", "category")},
        ),
        ("Pricing & Duration", {"fields": ("price", "duration")}),
        ("Settings", {"fields": ("is_active",)}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
