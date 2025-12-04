from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentListSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations
    """

    queryset = Appointment.objects.all()
    # permission_classes = [permissions.AllowAny]  # Using global settings

    def get_serializer_class(self):
        """Use lighter serializer for list view"""
        if self.action == "list":
            return AppointmentListSerializer
        return AppointmentSerializer

    def get_queryset(self):
        """Return all appointments for development"""
        return Appointment.objects.all().select_related(
            "staff", "customer", "service", "business"
        )
