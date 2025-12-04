"""Serializers for authentication and user management."""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""

    class Meta:
        model = UserProfile
        fields = ["is_master", "phone", "avatar_url"]
        read_only_fields = ["is_master"]  # Only admin can change this


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""

    profile = UserProfileSerializer(read_only=True)
    is_master = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "is_master",
        ]
        read_only_fields = ["id"]

    def get_is_master(self, obj):
        """Get is_master from profile."""
        return obj.profile.is_master if hasattr(obj, "profile") else False


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, label="Confirm Password"
    )
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords don't match."})

        # Check email uniqueness
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already registered."})

        return attrs

    def create(self, validated_data):
        """Create user with profile."""
        phone = validated_data.pop("phone", "")
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # Update profile with phone
        if phone and hasattr(user, "profile"):
            user.profile.phone = phone
            user.profile.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user info."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["is_master"] = (
            user.profile.is_master if hasattr(user, "profile") else False
        )

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user info to response
        data["user"] = UserSerializer(self.user).data

        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
