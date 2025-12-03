"""Services Page"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout

def services_content():
    return rx.vstack(
        styles.page_title("Services", "Manage service menu"),
        
        rx.cond(
            AppState.services,
            rx.vstack(
                rx.foreach(
                    AppState.services,
                    lambda service: styles.premium_card(
                        rx.hstack(
                            rx.center(
                                rx.icon("scissors", size=20, color=styles.accent_color),
                                background="rgba(212, 175, 55, 0.1)",
                                padding="12px",
                                border_radius="12px",
                                border=f"1px solid {styles.accent_color}20",
                                margin_right="4",
                            ),
                            rx.vstack(
                                rx.heading(service.name, size="4", color="white"),
                                rx.text(service.description, size="2", color=styles.text_secondary),
                                spacing="1",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.vstack(
                                rx.heading(f"${service.price}", size="5", color=styles.accent_color),
                                rx.text(f"{service.duration} min", size="2", color=styles.text_secondary),
                                align="end",
                                spacing="0",
                            ),
                            width="100%",
                            align="center",
                        )
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            rx.text("No services found.", color="gray"),
        ),
        width="100%",
    )

def services_page():
    return layout(services_content())
