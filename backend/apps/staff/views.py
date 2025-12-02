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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter staff by user's businesses"""
        user_businesses = Business.objects.filter(owner=self.request.user)
        return Staff.objects.filter(business__in=user_businesses)
