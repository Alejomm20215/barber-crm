"""Barbershop CRM - Premium Appointment Management"""

import reflex as rx
from barber_crm.pages import (
    dashboard,
    customers_page,
    staff_page,
    services_page,
    appointments_page,
)

# App Configuration
app = rx.App(
    stylesheets=[
        # Premium fonts
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap",
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap",
    ],
    theme=rx.theme(
        appearance="dark",
        accent_color="amber",
        radius="large",
        scaling="100%",
    ),
    style={
        "font_family": "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
        "background": "#0a0a0a",
        "color": "#ffffff",
    },
)

# Routes
app.add_page(dashboard, route="/", title="Dashboard | BarberCRM")
app.add_page(customers_page, route="/customers", title="Customers | BarberCRM")
app.add_page(staff_page, route="/staff", title="Staff | BarberCRM")
app.add_page(services_page, route="/services", title="Services | BarberCRM")
app.add_page(appointments_page, route="/appointments", title="Appointments | BarberCRM")
