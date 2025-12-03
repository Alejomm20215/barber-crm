"""Barbershop CRM - Main Application"""

import reflex as rx
from barber_crm.pages import (
    dashboard,
    customers_page,
    staff_page,
    services_page,
    appointments_page,
)


# Create the app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap",
    ],
    theme=rx.theme(
        appearance="dark",
        accent_color="gold",
        radius="large",
    ),
    style={
        "font_family": "'Outfit', sans-serif",
    },
)

# Add pages with navigation
app.add_page(dashboard, route="/", title="Dashboard - Barbershop CRM")
app.add_page(customers_page, route="/customers", title="Customers - Barbershop CRM")
app.add_page(staff_page, route="/staff", title="Staff - Barbershop CRM")
app.add_page(services_page, route="/services", title="Services - Barbershop CRM")
app.add_page(appointments_page, route="/appointments", title="Appointments - Barbershop CRM")
