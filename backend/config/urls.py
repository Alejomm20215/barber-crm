from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.businesses.views import BusinessViewSet
from apps.staff.views import StaffViewSet
from apps.customers.views import CustomerViewSet
from apps.services.views import ServiceViewSet
from apps.appointments.views import AppointmentViewSet
from config.health import healthz, livez, readyz

# Create API router
router = DefaultRouter()
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r"staff", StaffViewSet, basename="staff")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("apps.accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # Health checks
    path("healthz/", healthz, name="healthz"),
    path("livez/", livez, name="livez"),
    path("readyz/", readyz, name="readyz"),
]
