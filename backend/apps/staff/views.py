from rest_framework import viewsets, permissions
from .models import Staff
from .serializers import StaffSerializer
from apps.businesses.models import Business


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Staff CRUD operations
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # permission_classes = [permissions.AllowAny]  # Using global settings
    
    def get_queryset(self):
        """Return all staff for development"""
        return Staff.objects.all()
