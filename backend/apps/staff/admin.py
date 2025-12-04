from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["name", "business", "role", "phone", "is_active", "created_at"]
    list_filter = ["role", "is_active", "created_at"]
    search_fields = ["name", "phone", "email", "business__name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("business", "name", "role")}),
        ("Contact Details", {"fields": ("phone", "email", "photo_url")}),
        ("Employment", {"fields": ("is_active", "hire_date", "schedule")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
