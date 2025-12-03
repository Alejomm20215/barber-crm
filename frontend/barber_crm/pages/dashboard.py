"""Premium Dashboard Page"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout

def stat_card(title: str, value: rx.Var, icon: str):
    return styles.premium_card(
        rx.hstack(
            rx.vstack(
                rx.text(title, size="2", color=styles.text_secondary, weight="medium"),
                rx.heading(value, size="8", color="white", letter_spacing="-1px"),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.center(
                rx.icon(icon, size=24, color=styles.accent_color),
                background=f"rgba(212, 175, 55, 0.1)",
                padding="12px",
                border_radius="12px",
                border=f"1px solid {styles.accent_color}20",
                box_shadow=f"0 0 20px -5px {styles.accent_color}30",
            ),
            align="center",
            width="100%",
        )
    )

def dashboard_content():
    return rx.vstack(
        # Header
        rx.hstack(
            styles.page_title("Dashboard", f"Overview for {AppState.selected_business_name}"),
            rx.spacer(),
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.hstack(
                            rx.text(AppState.selected_business_name),
                            rx.icon("chevron-down", size=16),
                        ),
                        variant="outline",
                        color_scheme="gray",
                    ),
                ),
                rx.menu.content(
                    rx.foreach(
                        AppState.businesses,
                        lambda business: rx.menu.item(
                            business.name,
                            on_click=AppState.select_business(business.id, business.name),
                        ),
                    ),
                ),
            ),
            width="100%",
            align="start",
        ),
        
        # Stats Grid
        rx.grid(
            stat_card("Total Customers", AppState.total_customers, "users"),
            stat_card("Appointments", AppState.total_appointments, "calendar"),
            stat_card("Staff Members", AppState.total_staff, "user-check"),
            stat_card("Services", AppState.total_services, "scissors"),
            columns="4",
            spacing="6",
            width="100%",
        ),
        
        # Recent Activity Section
        rx.heading("Recent Activity", size="5", color="white", margin_top="8", margin_bottom="4"),
        
        rx.cond(
            AppState.appointments,
            rx.vstack(
                rx.foreach(
                    AppState.appointments,  # Slicing might be limited, just showing all for now or first few if supported
                    lambda appt: styles.premium_card(
                        rx.hstack(
                            rx.avatar(fallback="?", size="3"),
                            rx.vstack(
                                rx.text(appt.customer_name, weight="bold", color="white"),
                                rx.text("Booked ", appt.service_name, size="2", color="gray"),
                                spacing="0",
                            ),
                            rx.spacer(),
                            rx.text(appt.scheduled_at, size="2", color="gray"),
                            width="100%",
                            align="center",
                        ),
                        padding="4",
                    ),
                ),
                spacing="3",
                width="100%",
            ),
            rx.text("No recent activity", color="gray"),
        ),
        
        width="100%",
        on_mount=AppState.load_businesses,
    )

def dashboard():
    return layout(dashboard_content())
