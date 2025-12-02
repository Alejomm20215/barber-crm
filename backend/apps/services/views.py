from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer
from apps.businesses.models import Business


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service CRUD operations
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter services by user's businesses"""
        user_businesses = Business.objects.filter(owner=self.request.user)
        return Service.objects.filter(business__in=user_businesses)
