from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer
from apps.businesses.models import Business


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer CRUD operations
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.AllowAny]  # Using global settings
    
    def get_queryset(self):
        """Return all customers for development"""
        return Customer.objects.all()
