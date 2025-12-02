from rest_framework import viewsets, permissions
from .models import Business
from .serializers import BusinessSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business CRUD operations
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter businesses by owner"""
        return Business.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Set the owner to the current user"""
        serializer.save(owner=self.request.user)
