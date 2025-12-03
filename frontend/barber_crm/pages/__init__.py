"""Page exports"""

from .dashboard import dashboard
from .customers import customers_page
from .staff import staff_page
from .services import services_page
from .appointments import appointments_page

__all__ = [
    "dashboard",
    "customers_page",
    "staff_page",
    "services_page",
    "appointments_page",
]
