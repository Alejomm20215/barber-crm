"""Dashboard Page"""

import reflex as rx
from barber_crm.state import DashboardState


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    """Create a stat card component"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icon, size=32, color=color),
                rx.spacer(),
            ),
            rx.heading(value, size="8", weight="bold"),
            rx.text(title, size="2", color="gray"),
            spacing="2",
            align="start",
        ),
        width="100%",
    )


def dashboard() -> rx.Component:
    """Main dashboard page"""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("Barbershop CRM Dashboard", size="9", weight="bold"),
            rx.text("Manage your barbershop business", size="4", color="gray"),
            
            # Stats Grid
            rx.grid(
                stat_card(
                    "Total Customers",
                    DashboardState.total_customers,
                    "users",
                    "blue"
                ),
                stat_card(
                    "Total Appointments",
                    DashboardState.total_appointments,
                    "calendar",
                    "green"
                ),
                stat_card(
                    "Staff Members",
                    DashboardState.total_staff,
                    "user-check",
                    "purple"
                ),
                stat_card(
                    "Services",
                    rx.text(f"{len(DashboardState.services)}"),
                    "scissors",
                    "orange"
                ),
                columns="4",
                spacing="4",
                width="100%",
            ),
            
            # Quick Actions
            rx.heading("Quick Actions", size="6", margin_top="8"),
            rx.hstack(
                rx.button(
                    rx.icon("plus", margin_right="2"),
                    "New Appointment",
                    color_scheme="blue",
                    size="3",
                ),
                rx.button(
                    rx.icon("user-plus", margin_right="2"),
                    "Add Customer",
                    color_scheme="green",
                    size="3",
                ),
                rx.button(
                    rx.icon("users", margin_right="2"),
                    "Manage Staff",
                    color_scheme="purple",
                    size="3",
                ),
                spacing="4",
            ),
            
            # Recent Appointments
            rx.heading("Recent Appointments", size="6", margin_top="8"),
            rx.cond(
                DashboardState.is_loading,
                rx.spinner(size="3"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Customer"),
                            rx.table.column_header_cell("Staff"),
                            rx.table.column_header_cell("Service"),
                            rx.table.column_header_cell("Date"),
                            rx.table.column_header_cell("Status"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            DashboardState.appointments[:10],
                            lambda appt: rx.table.row(
                                rx.table.cell(appt["customer_name"]),
                                rx.table.cell(appt["staff_name"]),
                                rx.table.cell(appt["service_name"]),
                                rx.table.cell(appt["scheduled_at"]),
                                rx.table.cell(
                                    rx.badge(appt["status_display"], color_scheme="blue")
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            
            # Error message
            rx.cond(
                DashboardState.error_message != "",
                rx.callout(
                    DashboardState.error_message,
                    icon="alert-circle",
                    color_scheme="red",
                ),
            ),
            
            spacing="6",
            padding="8",
            width="100%",
        ),
        on_mount=DashboardState.load_dashboard_data,
    )
