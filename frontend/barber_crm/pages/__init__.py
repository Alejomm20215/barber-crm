"""Pages module exports"""

from barber_crm.pages.appointments import appointments_page
from barber_crm.pages.auth import landing_page, login_page, register_page
from barber_crm.pages.customers import customers_page
from barber_crm.pages.dashboard import dashboard
from barber_crm.pages.services import services_page
from barber_crm.pages.staff import staff_page

__all__ = [
    "appointments_page",
    "customers_page",
    "dashboard",
    "landing_page",
    "login_page",
    "register_page",
    "services_page",
    "staff_page",
]
