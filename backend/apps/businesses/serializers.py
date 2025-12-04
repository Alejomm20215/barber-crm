from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "owner",
            "owner_username",
            "address",
            "phone",
            "email",
            "logo_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
