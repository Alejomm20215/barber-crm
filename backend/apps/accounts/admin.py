"""Admin configuration for accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""

    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile."""

    inlines = [UserProfileInline]
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_is_master",
    ]

    def get_is_master(self, obj):
        return obj.profile.is_master if hasattr(obj, "profile") else False

    get_is_master.short_description = "Master"
    get_is_master.boolean = True


# Re-register User with new admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile."""

    list_display = ["user", "is_master", "phone", "created_at"]
    list_filter = ["is_master", "created_at"]
    search_fields = ["user__username", "user__email", "phone"]
    readonly_fields = ["created_at", "updated_at"]
