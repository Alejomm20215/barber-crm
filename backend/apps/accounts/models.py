"""User Profile model for extended user functionality."""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile with role management.
    
    - is_master: Can see ALL barbershops in the system
    - Regular users: Can only see barbershops they own or are assigned to
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_master = models.BooleanField(default=False, help_text="Master accounts can see all barbershops")
    phone = models.CharField(max_length=20, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        role = "Master" if self.is_master else "Owner"
        return f"{self.user.username} ({role})"
    
    @property
    def is_admin(self):
        """Check if user is admin (staff or master)."""
        return self.user.is_staff or self.is_master


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Auto-save profile when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
