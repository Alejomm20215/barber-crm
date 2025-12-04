from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "business",
            "name",
            "phone",
            "email",
            "role",
            "role_display",
            "schedule",
            "photo_url",
            "is_active",
            "hire_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
