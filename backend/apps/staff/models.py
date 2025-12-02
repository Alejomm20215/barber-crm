from django.db import models
from apps.businesses.models import Business


class Staff(models.Model):
    """Staff members working at a barbershop"""
    ROLE_CHOICES = [
        ('barber', 'Barber'),
        ('stylist', 'Stylist'),
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
    ]
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='staff_members')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='barber')
    
    # Schedule stored as JSON (can be improved with a separate Schedule model)
    schedule = models.JSONField(default=dict, blank=True)
    
    # Additional fields
    photo_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    hire_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff'
        verbose_name_plural = 'Staff'
        ordering = ['name']
        indexes = [
            models.Index(fields=['business', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
