from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentListSerializer
from apps.businesses.models import Business


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations
    """
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use lighter serializer for list view"""
        if self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        """Filter appointments by user's businesses"""
        user_businesses = Business.objects.filter(owner=self.request.user)
        return Appointment.objects.filter(business__in=user_businesses).select_related(
            'staff', 'customer', 'service', 'business'
        )
