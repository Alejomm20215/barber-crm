from rest_framework import serializers
from .models import Appointment
from apps.staff.serializers import StaffSerializer
from apps.customers.serializers import CustomerSerializer
from apps.services.serializers import ServiceSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    staff_details = StaffSerializer(source='staff', read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'business', 'staff', 'customer', 'service',
            'staff_details', 'customer_details', 'service_details',
            'scheduled_at', 'status', 'status_display', 'price', 'notes',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Auto-fill price from service if not provided."""
        if 'price' not in validated_data or validated_data.get('price') is None:
            service = validated_data.get('service')
            if service:
                validated_data['price'] = service.price
            else:
                validated_data['price'] = 0
        return super().create(validated_data)


class AppointmentListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'business', 'staff', 'staff_name', 'customer', 'customer_name',
            'service', 'service_name', 'scheduled_at', 'status', 'status_display',
            'price', 'created_at'
        ]
