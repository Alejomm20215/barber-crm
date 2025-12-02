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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter customers by user's businesses"""
        user_businesses = Business.objects.filter(owner=self.request.user)
        return Customer.objects.filter(business__in=user_businesses)
