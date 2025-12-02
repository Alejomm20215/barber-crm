"""Unit tests for Business model"""

import pytest
from apps.businesses.models import Business


@pytest.mark.django_db
@pytest.mark.unit
class TestBusinessModel:
    """Test Business model"""
    
    def test_create_business(self, user):
        """Test creating a business"""
        business = Business.objects.create(
            name="Test Barbershop",
            owner=user,
            phone="555-1234",
            email="test@barbershop.com"
        )
        
        assert business.name == "Test Barbershop"
        assert business.owner == user
        assert business.phone == "555-1234"
        assert str(business) == "Test Barbershop"
    
    def test_business_str_representation(self, business):
        """Test business string representation"""
        assert str(business) == business.name
    
    def test_business_has_uuid(self, business):
        """Test business has UUID primary key"""
        assert business.id is not None
        assert len(str(business.id)) == 36  # UUID format
    
    def test_business_timestamps(self, business):
        """Test business has timestamps"""
        assert business.created_at is not None
        assert business.updated_at is not None
    
    def test_business_owner_relationship(self, business, user):
        """Test business-owner relationship"""
        assert business.owner == user
        assert business in user.businesses.all()
