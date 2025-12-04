import uuid
from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):
    """Business model for multi-tenant barbershop CRM"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="businesses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields for business profile
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "businesses"
        verbose_name_plural = "Businesses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
