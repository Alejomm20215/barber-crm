"""API tests for Appointment endpoints"""

import pytest
from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta


@pytest.mark.django_db
@pytest.mark.integration
class TestAppointmentAPI:
    """Test Appointment API endpoints"""

    def test_list_appointments(self, authenticated_client, appointment):
        """Test listing appointments"""
        url = reverse("appointment-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_appointment(
        self, authenticated_client, business, staff, customer, service
    ):
        """Test creating an appointment"""
        url = reverse("appointment-list")
        scheduled_time = (datetime.now() + timedelta(days=1)).isoformat()
        data = {
            "business": str(business.id),
            "staff": staff.id,
            "customer": customer.id,
            "service": service.id,
            "scheduled_at": scheduled_time,
            "price": "50.00",
            "status": "scheduled",
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_appointment_status(self, authenticated_client, appointment):
        """Test updating appointment status"""
        url = reverse("appointment-detail", kwargs={"pk": appointment.id})
        data = {"status": "confirmed"}
        response = authenticated_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "confirmed"

    def test_appointment_includes_related_data(self, authenticated_client, appointment):
        """Test appointment detail includes related data"""
        url = reverse("appointment-detail", kwargs={"pk": appointment.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "staff_details" in response.data
        assert "customer_details" in response.data
        assert "service_details" in response.data
