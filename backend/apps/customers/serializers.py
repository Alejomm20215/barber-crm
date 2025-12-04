from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "business",
            "name",
            "phone",
            "email",
            "notes",
            "preferences",
            "total_visits",
            "total_spent",
            "last_visit",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "total_visits",
            "total_spent",
            "created_at",
            "updated_at",
        ]
