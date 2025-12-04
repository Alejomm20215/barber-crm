"""Test fixtures for the entire test suite"""

import pytest
from django.contrib.auth.models import User
from apps.businesses.models import Business
from apps.staff.models import Staff
from apps.customers.models import Customer
from apps.services.models import Service
from apps.appointments.models import Appointment
from datetime import datetime, timedelta
import factory
from factory.django import DjangoModelFactory


# Factories
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class BusinessFactory(DjangoModelFactory):
    class Meta:
        model = Business

    name = factory.Faker("company")
    owner = factory.SubFactory(UserFactory)
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    address = factory.Faker("address")


class StaffFactory(DjangoModelFactory):
    class Meta:
        model = Staff

    business = factory.SubFactory(BusinessFactory)
    name = factory.Faker("name")
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    role = "barber"
    is_active = True


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    business = factory.SubFactory(BusinessFactory)
    name = factory.Faker("name")
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    business = factory.SubFactory(BusinessFactory)
    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    duration = 30
    is_active = True


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment

    business = factory.SubFactory(BusinessFactory)
    staff = factory.SubFactory(StaffFactory)
    customer = factory.SubFactory(CustomerFactory)
    service = factory.SubFactory(ServiceFactory)
    scheduled_at = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    status = "scheduled"


# Fixtures
@pytest.fixture
def user():
    """Create a test user"""
    return UserFactory()


@pytest.fixture
def business(user):
    """Create a test business"""
    return BusinessFactory(owner=user)


@pytest.fixture
def staff(business):
    """Create a test staff member"""
    return StaffFactory(business=business)


@pytest.fixture
def customer(business):
    """Create a test customer"""
    return CustomerFactory(business=business)


@pytest.fixture
def service(business):
    """Create a test service"""
    return ServiceFactory(business=business)


@pytest.fixture
def appointment(business, staff, customer, service):
    """Create a test appointment"""
    return AppointmentFactory(
        business=business, staff=staff, customer=customer, service=service
    )


@pytest.fixture
def api_client():
    """Create an API client"""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(user, api_client):
    """Create an authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client
