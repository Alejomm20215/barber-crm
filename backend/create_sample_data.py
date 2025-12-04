"""
Create sample data for testing - Run with: Get-Content backend/create_sample_data.py | docker-compose exec -T backend python manage.py shell
"""

from django.contrib.auth.models import User
from apps.businesses.models import Business
from apps.staff.models import Staff
from apps.customers.models import Customer
from apps.services.models import Service
from apps.appointments.models import Appointment
from datetime import datetime, timedelta

admin_user = User.objects.get(username="admin")

# Create Barbershops
b1, _ = Business.objects.get_or_create(
    name="Downtown Cuts",
    defaults={
        "owner": admin_user,
        "phone": "555-0101",
        "email": "info@downtowncuts.com",
    },
)
b2, _ = Business.objects.get_or_create(
    name="Uptown Styles",
    defaults={
        "owner": admin_user,
        "phone": "555-0202",
        "email": "contact@uptownstyles.com",
    },
)

# Staff
Staff.objects.get_or_create(
    business=b1,
    email="john@downtown.com",
    defaults={"name": "John Smith", "phone": "555-1001", "role": "barber"},
)
Staff.objects.get_or_create(
    business=b1,
    email="mike@downtown.com",
    defaults={"name": "Mike Johnson", "phone": "555-1002", "role": "barber"},
)
Staff.objects.get_or_create(
    business=b2,
    email="sarah@uptown.com",
    defaults={"name": "Sarah Williams", "phone": "555-2001", "role": "stylist"},
)
Staff.objects.get_or_create(
    business=b2,
    email="emma@uptown.com",
    defaults={"name": "Emma Davis", "phone": "555-2002", "role": "stylist"},
)

# Services
Service.objects.get_or_create(
    business=b1, name="Classic Haircut", defaults={"price": 25, "duration": 30}
)
Service.objects.get_or_create(
    business=b1, name="Beard Trim", defaults={"price": 15, "duration": 20}
)
Service.objects.get_or_create(
    business=b1, name="Hot Towel Shave", defaults={"price": 35, "duration": 45}
)
Service.objects.get_or_create(
    business=b2, name="Modern Cut & Style", defaults={"price": 40, "duration": 45}
)
Service.objects.get_or_create(
    business=b2, name="Color Treatment", defaults={"price": 80, "duration": 90}
)
Service.objects.get_or_create(
    business=b2, name="Deluxe Package", defaults={"price": 120, "duration": 120}
)

# Customers
Customer.objects.get_or_create(
    business=b1,
    phone="555-3001",
    defaults={"name": "James Brown", "email": "james@email.com", "total_visits": 5},
)
Customer.objects.get_or_create(
    business=b1,
    phone="555-3002",
    defaults={"name": "Robert Taylor", "email": "robert@email.com", "total_visits": 3},
)
Customer.objects.get_or_create(
    business=b2,
    phone="555-4001",
    defaults={
        "name": "Jennifer Martinez",
        "email": "jennifer@email.com",
        "total_visits": 8,
    },
)
Customer.objects.get_or_create(
    business=b2,
    phone="555-4002",
    defaults={"name": "Lisa Anderson", "email": "lisa@email.com", "total_visits": 12},
)

# Appointments
s1 = Staff.objects.filter(business=b1).first()
c1 = Customer.objects.filter(business=b1).first()
sv1 = Service.objects.filter(business=b1).first()
s2 = Staff.objects.filter(business=b2).first()
c2 = Customer.objects.filter(business=b2).first()
sv2 = Service.objects.filter(business=b2).first()

now = datetime.now()
if s1 and c1 and sv1:
    Appointment.objects.get_or_create(
        business=b1,
        customer=c1,
        staff=s1,
        service=sv1,
        defaults={
            "scheduled_at": now + timedelta(days=1),
            "price": sv1.price,
            "status": "scheduled",
        },
    )
if s2 and c2 and sv2:
    Appointment.objects.get_or_create(
        business=b2,
        customer=c2,
        staff=s2,
        service=sv2,
        defaults={
            "scheduled_at": now + timedelta(days=2),
            "price": sv2.price,
            "status": "scheduled",
        },
    )

print("✅ Sample data created!")
print(f"Businesses: {Business.objects.count()}")
print(f"Staff: {Staff.objects.count()}")
print(f"Services: {Service.objects.count()}")
print(f"Customers: {Customer.objects.count()}")
print(f"Appointments: {Appointment.objects.count()}")
