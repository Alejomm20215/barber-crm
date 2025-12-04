from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service CRUD operations
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    # permission_classes = [permissions.AllowAny]  # Using global settings

    def get_queryset(self):
        """Return all services for development"""
        return Service.objects.all()
