"""Premium Dashboard Page"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout


def quick_action_card(title: str, icon: str, count, subtitle: str, href: str):
    """Quick action card for dashboard"""
    return rx.link(
        styles.premium_card(
            rx.vstack(
                rx.hstack(
                    rx.center(
                        rx.icon(icon, size=28, color=styles.GOLD),
                        width="56px",
                        height="56px",
                        background=f"linear-gradient(135deg, rgba(201, 162, 39, 0.15) 0%, rgba(201, 162, 39, 0.05) 100%)",
                        border_radius="14px",
                        border=f"1px solid rgba(201, 162, 39, 0.2)",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text(
                            count,
                            size="7",
                            weight="bold",
                            color=styles.WHITE,
                        ),
                        rx.text(subtitle, size="1", color=styles.GRAY_500),
                        spacing="0",
                        align="end",
                    ),
                    width="100%",
                    align="start",
                ),
                rx.text(title, size="3", weight="bold", color=styles.WHITE, margin_top="16px"),
                spacing="2",
                width="100%",
            ),
        ),
        href=href,
        text_decoration="none",
    )


def recent_appointment_item(appt):
    """Recent appointment list item"""
    return rx.hstack(
        rx.avatar(
            fallback="?",
            size="3",
            style={
                "background": styles.GOLD_GRADIENT,
                "color": styles.BLACK,
            },
        ),
        rx.vstack(
            rx.text(appt.customer_name, weight="bold", color=styles.WHITE, size="2"),
            rx.hstack(
                rx.icon("scissors", size=12, color=styles.GRAY_500),
                rx.text(appt.service_name, size="1", color=styles.GRAY_500),
                spacing="1",
                align="center",
            ),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.vstack(
            rx.text(appt.scheduled_at, size="1", color=styles.GRAY_500),
            rx.box(
                rx.text(appt.status, size="1", weight="bold", color=styles.GOLD),
                background="rgba(201, 162, 39, 0.1)",
                border=f"1px solid rgba(201, 162, 39, 0.3)",
                border_radius="6px",
                padding="2px 8px",
            ),
            spacing="1",
            align="end",
        ),
        width="100%",
        padding="16px",
        background=styles.GRAY_900,
        border_radius="12px",
        border=styles.BORDER_SUBTLE,
        transition="all 0.2s ease",
        _hover={
            "border_color": styles.GOLD,
            "background": styles.CARD_BG,
        },
    )


def dashboard_content():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.vstack(
                rx.text("Welcome back,", size="2", color=styles.GRAY_500),
                rx.text(
                    "Dashboard",
                    size="8",
                    weight="bold",
                    style={
                        "background": styles.GOLD_GRADIENT,
                        "background_clip": "text",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    },
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.icon("calendar", size=18, color=styles.GOLD),
                rx.text(AppState.selected_business_name, size="2", color=styles.WHITE, weight="medium"),
                padding="10px 16px",
                background=styles.GRAY_900,
                border_radius="10px",
                border=styles.BORDER_SUBTLE,
            ),
            width="100%",
            align="end",
            margin_bottom="32px",
        ),
        
        # Stats Grid
        rx.grid(
            quick_action_card("Total Customers", "users", AppState.total_customers, "clients", "/customers"),
            quick_action_card("Appointments", "calendar-clock", AppState.total_appointments, "bookings", "/appointments"),
            quick_action_card("Staff Members", "user-cog", AppState.total_staff, "team", "/staff"),
            quick_action_card("Services", "scissors", AppState.total_services, "offerings", "/services"),
            columns="4",
            spacing="6",
            width="100%",
        ),
        
        # Recent Activity Section
        rx.hstack(
            rx.vstack(
                rx.text("Recent Appointments", size="5", color=styles.WHITE, weight="bold"),
                rx.text("Latest bookings and activity", size="2", color=styles.GRAY_500),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.link(
                rx.hstack(
                    rx.text("View all", size="2", color=styles.GOLD),
                    rx.icon("arrow-right", size=16, color=styles.GOLD),
                    spacing="2",
                    align="center",
                ),
                href="/appointments",
                text_decoration="none",
            ),
            width="100%",
            align="center",
            margin_top="40px",
            margin_bottom="20px",
        ),
        
        rx.cond(
            AppState.total_appointments > 0,
            rx.vstack(
                rx.foreach(
                    AppState.appointments,
                    recent_appointment_item,
                ),
                spacing="3",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.center(
                        rx.icon("calendar-x", size=48, color=styles.GRAY_700),
                        width="96px",
                        height="96px",
                        background=styles.GRAY_900,
                        border_radius="50%",
                        border=styles.BORDER_SUBTLE,
                    ),
                    rx.text("No appointments yet", size="5", color=styles.GRAY_500, weight="medium"),
                    rx.text("Book your first appointment to get started", color=styles.GRAY_700, size="2"),
                    rx.link(
                        rx.button(
                            rx.hstack(rx.icon("plus", size=18), rx.text("Book Appointment"), spacing="2"),
                            background=styles.GOLD_GRADIENT,
                            color=styles.BLACK,
                            padding="12px 24px",
                            border_radius="12px",
                            cursor="pointer",
                        ),
                        href="/appointments",
                        text_decoration="none",
                    ),
                    spacing="4",
                    align="center",
                    padding="48px",
                ),
                width="100%",
            ),
        ),
        
        width="100%",
        spacing="0",
        on_mount=AppState.load_businesses,
    )


def dashboard():
    return layout(dashboard_content())
