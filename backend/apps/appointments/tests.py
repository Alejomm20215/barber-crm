"""Unit tests for Appointment model"""

import pytest
from apps.appointments.models import Appointment
from datetime import datetime, timedelta


@pytest.mark.django_db
@pytest.mark.unit
class TestAppointmentModel:
    """Test Appointment model"""
    
    def test_create_appointment(self, business, staff, customer, service):
        """Test creating an appointment"""
        scheduled_time = datetime.now() + timedelta(days=1)
        appointment = Appointment.objects.create(
            business=business,
            staff=staff,
            customer=customer,
            service=service,
            scheduled_at=scheduled_time,
            price=50.00,
            status='scheduled'
        )
        
        assert appointment.business == business
        assert appointment.staff == staff
        assert appointment.customer == customer
        assert appointment.service == service
        assert appointment.price == 50.00
        assert appointment.status == 'scheduled'
    
    def test_appointment_str_representation(self, appointment):
        """Test appointment string representation"""
        expected = f"{appointment.customer.name} with {appointment.staff.name} at {appointment.scheduled_at}"
        assert str(appointment) == expected
    
    def test_appointment_status_choices(self, appointment):
        """Test appointment status choices"""
        valid_statuses = ['scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show']
        
        for status in valid_statuses:
            appointment.status = status
            appointment.save()
            assert appointment.status == status
    
    def test_appointment_timestamps(self, appointment):
        """Test appointment has timestamps"""
        assert appointment.created_at is not None
        assert appointment.updated_at is not None
