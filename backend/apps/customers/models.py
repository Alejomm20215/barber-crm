from django.db import models
from apps.businesses.models import Business


class Customer(models.Model):
    """Customer model for barbershop clients"""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="customers"
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)

    # Customer notes and preferences
    notes = models.TextField(blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)

    # Customer stats
    total_visits = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["business", "phone"]),
            models.Index(fields=["business", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone})"
