"""Pages module exports"""

from barber_crm.pages.dashboard import dashboard
from barber_crm.pages.customers import customers_page
from barber_crm.pages.staff import staff_page
from barber_crm.pages.services import services_page
from barber_crm.pages.appointments import appointments_page

__all__ = [
    "dashboard",
    "customers_page",
    "staff_page",
    "services_page",
    "appointments_page",
]
