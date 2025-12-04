"""Barbershop CRM - Premium Appointment Management"""

import reflex as rx

from barber_crm.pages import (
    appointments_page,
    customers_page,
    dashboard,
    landing_page,
    login_page,
    register_page,
    services_page,
    staff_page,
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
    head_components=[
        rx.el.link(rel="icon", href="/logo.svg"),
    ],
)

# Public Routes
app.add_page(landing_page, route="/", title="Welcome | BarberCRM")
app.add_page(landing_page, route="/welcome", title="Welcome | BarberCRM")
app.add_page(login_page, route="/login", title="Login | BarberCRM")
app.add_page(register_page, route="/register", title="Register | BarberCRM")

# App Routes (protected)
app.add_page(dashboard, route="/dashboard", title="Dashboard | BarberCRM")
app.add_page(customers_page, route="/customers", title="Customers | BarberCRM")
app.add_page(staff_page, route="/staff", title="Staff | BarberCRM")
app.add_page(services_page, route="/services", title="Services | BarberCRM")
app.add_page(appointments_page, route="/appointments", title="Appointments | BarberCRM")
