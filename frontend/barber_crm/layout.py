"""Main Application Layout"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles

def sidebar_item(text: str, icon: str, href: str):
    return rx.link(
        rx.box(
            rx.icon(icon, size=20),
            rx.text(text, size="3", weight="medium"),
            style=styles.nav_link_style,
        ),
        href=href,
        width="100%",
        text_decoration="none",
    )

def sidebar():
    return rx.box(
        rx.vstack(
            # Logo / Brand
            rx.hstack(
                rx.box(
                    rx.icon("scissors", size=24, color=styles.accent_color),
                    padding="10px",
                    background="rgba(212, 175, 55, 0.1)",
                    border_radius="12px",
                    border=f"1px solid {styles.accent_color}20",
                ),
                rx.heading("BarberCRM", size="5", color="white", font_family="Outfit", letter_spacing="-0.5px"),
                spacing="3",
                align="center",
                margin_bottom="8",
                padding_x="2",
                width="100%",
            ),
            
            # Navigation
            rx.vstack(
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                sidebar_item("Appointments", "calendar", "/appointments"),
                sidebar_item("Customers", "users", "/customers"),
                sidebar_item("Staff", "user-check", "/staff"),
                sidebar_item("Services", "scissors", "/services"),
                spacing="2",
                width="100%",
            ),
            
            rx.spacer(),
            
            # User Profile / Logout
            rx.box(
                rx.hstack(
                    rx.avatar(fallback="AD", size="3", radius="full", variant="soft", color_scheme="gray"),
                    rx.vstack(
                        rx.text("Admin User", size="2", weight="bold", color="white"),
                        rx.text("admin@barber.com", size="1", color="gray"),
                        spacing="0",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="16px",
                background="rgba(255, 255, 255, 0.03)",
                border_radius="12px",
                border="1px solid rgba(255, 255, 255, 0.05)",
                width="100%",
            ),
            
            height="100%",
            width="100%",
        ),
        style=styles.sidebar_style,
    )

def layout(content: rx.Component):
    return rx.box(
        sidebar(),
        rx.box(
            content,
            style=styles.content_style,
        ),
        background=styles.bg_gradient,
        min_height="100vh",
    )
