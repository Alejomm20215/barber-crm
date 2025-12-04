from rest_framework import viewsets, permissions
from .models import Business
from .serializers import BusinessSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business CRUD operations.
    
    - Master users: Can see ALL businesses
    - Regular users: Can only see businesses they own
    - Anonymous users: Can see all (for development, adjust in production)
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        """
        Filter businesses based on user role.
        
        - Master accounts: See all businesses
        - Regular users: See only their own businesses
        - Anonymous: See all (for dev, change in production)
        """
        user = self.request.user
        
        # Anonymous user - return all for development
        if not user.is_authenticated:
            return Business.objects.all()
        
        # Check if user is master
        is_master = False
        if hasattr(user, 'profile'):
            is_master = user.profile.is_master
        
        # Master or staff can see all
        if is_master or user.is_staff:
            return Business.objects.all()
        
        # Regular users see only their businesses
        return Business.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        """Set the owner to the current user."""
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            # For development - use first user or create anonymous
            from django.contrib.auth.models import User
            default_user = User.objects.first()
            serializer.save(owner=default_user)
