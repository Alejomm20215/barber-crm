from django.db import models
from apps.businesses.models import Business
from apps.staff.models import Staff
from apps.customers.models import Customer
from apps.services.models import Service


class Appointment(models.Model):
    """Appointment booking model"""

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("confirmed", "Confirmed"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="appointments"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="appointments"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="appointments"
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, related_name="appointments"
    )

    # Appointment details
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    # Pricing (can override service price)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Notes
    notes = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "appointments"
        ordering = ["-scheduled_at"]
        indexes = [
            models.Index(fields=["business", "scheduled_at"]),
            models.Index(fields=["staff", "scheduled_at"]),
            models.Index(fields=["customer", "scheduled_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.customer.name} with {self.staff.name} at {self.scheduled_at}"
