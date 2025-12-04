"""API tests for Business endpoints"""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.integration
class TestBusinessAPI:
    """Test Business API endpoints"""

    def test_list_businesses_unauthenticated(self, api_client):
        """Test listing businesses without authentication fails"""
        url = reverse("business-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_businesses_authenticated(self, authenticated_client, business):
        """Test listing businesses with authentication"""
        url = reverse("business-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_business(self, authenticated_client, user):
        """Test creating a business"""
        url = reverse("business-list")
        data = {
            "name": "New Barbershop",
            "phone": "555-5678",
            "email": "new@barbershop.com",
            "owner": user.id,
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Barbershop"

    def test_retrieve_business(self, authenticated_client, business):
        """Test retrieving a specific business"""
        url = reverse("business-detail", kwargs={"pk": business.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == business.name

    def test_update_business(self, authenticated_client, business):
        """Test updating a business"""
        url = reverse("business-detail", kwargs={"pk": business.id})
        data = {"name": "Updated Barbershop"}
        response = authenticated_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Barbershop"

    def test_delete_business(self, authenticated_client, business):
        """Test deleting a business"""
        url = reverse("business-detail", kwargs={"pk": business.id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_can_only_see_own_businesses(self, authenticated_client, business):
        """Test users can only see their own businesses"""
        # Create another user's business
        from conftest import UserFactory, BusinessFactory

        other_user = UserFactory()
        other_business = BusinessFactory(owner=other_user)

        url = reverse("business-list")
        response = authenticated_client.get(url)

        business_ids = [b["id"] for b in response.data]
        assert str(business.id) in business_ids
        assert str(other_business.id) not in business_ids
