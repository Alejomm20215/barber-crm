"""Appointments Page with CRUD Operations"""

import reflex as rx

from barber_crm import styles
from barber_crm.layout import layout
from barber_crm.state import AppState


def appointment_modal():
    """Modal for creating new appointment"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("calendar-plus", size=24, color=styles.GOLD),
                        rx.heading("Book Appointment", size="5", color=styles.WHITE, weight="bold"),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        on_click=AppState.toggle_appointment_modal,
                        cursor="pointer",
                    ),
                    width="100%",
                ),
                rx.divider(color=styles.GRAY_800, margin_y="16px"),
                rx.vstack(
                    # Customer Select
                    rx.vstack(
                        rx.text("Customer", size="2", weight="medium", color=styles.GRAY_300),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Select customer...",
                                width="100%",
                                style={
                                    "background": styles.GRAY_900,
                                    "border": styles.BORDER_SUBTLE,
                                    "border_radius": "10px",
                                },
                            ),
                            rx.select.content(
                                rx.foreach(
                                    AppState.customers,
                                    lambda c: rx.select.item(c.name, value=c.id),
                                ),
                                background=styles.CARD_BG,
                            ),
                            value=AppState.form_appt_customer,
                            on_change=AppState.set_form_appt_customer,
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    # Staff Select
                    rx.vstack(
                        rx.text("Barber / Staff", size="2", weight="medium", color=styles.GRAY_300),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Select barber...",
                                width="100%",
                                style={
                                    "background": styles.GRAY_900,
                                    "border": styles.BORDER_SUBTLE,
                                    "border_radius": "10px",
                                },
                            ),
                            rx.select.content(
                                rx.foreach(
                                    AppState.staff,
                                    lambda s: rx.select.item(s.name, value=s.id),
                                ),
                                background=styles.CARD_BG,
                            ),
                            value=AppState.form_appt_staff,
                            on_change=AppState.set_form_appt_staff,
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    # Service Select
                    rx.vstack(
                        rx.text("Service", size="2", weight="medium", color=styles.GRAY_300),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Select service...",
                                width="100%",
                                style={
                                    "background": styles.GRAY_900,
                                    "border": styles.BORDER_SUBTLE,
                                    "border_radius": "10px",
                                },
                            ),
                            rx.select.content(
                                rx.foreach(
                                    AppState.services,
                                    lambda s: rx.select.item(s.name, value=s.id),
                                ),
                                background=styles.CARD_BG,
                            ),
                            value=AppState.form_appt_service,
                            on_change=AppState.set_form_appt_service,
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    # Date & Time
                    rx.hstack(
                        rx.vstack(
                            rx.text("Date", size="2", weight="medium", color=styles.GRAY_300),
                            rx.input(
                                type="date",
                                value=AppState.form_appt_date,
                                on_change=AppState.set_form_appt_date,
                                background=styles.GRAY_900,
                                border=styles.BORDER_SUBTLE,
                                border_radius="10px",
                                padding="12px 16px",
                                color=styles.WHITE,
                                width="100%",
                                _focus={"border_color": styles.GOLD, "outline": "none"},
                            ),
                            spacing="2",
                            flex="1",
                        ),
                        rx.vstack(
                            rx.text("Time", size="2", weight="medium", color=styles.GRAY_300),
                            rx.input(
                                type="time",
                                value=AppState.form_appt_time,
                                on_change=AppState.set_form_appt_time,
                                background=styles.GRAY_900,
                                border=styles.BORDER_SUBTLE,
                                border_radius="10px",
                                padding="12px 16px",
                                color=styles.WHITE,
                                width="100%",
                                _focus={"border_color": styles.GOLD, "outline": "none"},
                            ),
                            spacing="2",
                            flex="1",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        variant="outline",
                        color_scheme="gray",
                        on_click=AppState.toggle_appointment_modal,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(AppState.is_loading, rx.spinner(size="1"), rx.icon("calendar-check", size=16)),
                            rx.text("Book Appointment"),
                            spacing="2",
                        ),
                        background=styles.GOLD_GRADIENT,
                        color=styles.BLACK,
                        on_click=AppState.create_appointment,
                        cursor="pointer",
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="24px",
                ),
                spacing="0",
                width="100%",
            ),
            style={
                "background": styles.CARD_BG,
                "border": "1px solid rgba(201, 162, 39, 0.3)",
                "border_radius": "20px",
                "padding": "24px",
                "max_width": "480px",
                "width": "100%",
            },
        ),
        open=AppState.show_appointment_modal,
    )


def status_badge(status: str):
    """Status badge with color coding"""
    colors = {
        "scheduled": styles.BLUE,
        "completed": styles.GREEN,
        "cancelled": styles.RED,
    }
    color = colors.get(status.lower(), styles.GRAY_500) if isinstance(status, str) else styles.GOLD

    return rx.box(
        rx.text(status, size="1", weight="bold", color=color),
        background="rgba(201, 162, 39, 0.1)",
        border=f"1px solid {color}",
        border_radius="6px",
        padding="4px 10px",
    )


def appointment_card(appt):
    """Individual appointment card"""
    return styles.premium_card(
        rx.hstack(
            # Time Column
            rx.vstack(
                rx.text(
                    appt.scheduled_at,
                    size="2",
                    weight="bold",
                    color=styles.GOLD,
                ),
                rx.text(
                    appt.status,
                    size="2",
                    weight="medium",
                    color=styles.WHITE,
                ),
                align="center",
                min_width="80px",
                padding_right="20px",
                border_right=styles.BORDER_SUBTLE,
            ),
            # Customer & Service Info
            rx.hstack(
                rx.avatar(
                    fallback="?",
                    size="3",
                    style={
                        "background": styles.GOLD_GRADIENT,
                        "color": styles.BLACK,
                    },
                ),
                rx.vstack(
                    rx.text(appt.customer_name, weight="bold", color=styles.WHITE, size="3"),
                    rx.hstack(
                        rx.icon("scissors", size=12, color=styles.GRAY_500),
                        rx.text(appt.service_name, size="2", color=styles.GRAY_500),
                        rx.text("•", color=styles.GRAY_700),
                        rx.icon("user", size=12, color=styles.GRAY_500),
                        rx.text(appt.staff_name, size="2", color=styles.GRAY_500),
                        spacing="2",
                        align="center",
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="center",
                flex="1",
                padding_left="20px",
            ),
            rx.spacer(),
            # Status Badge
            rx.box(
                rx.text(appt.status, size="1", weight="bold", color=styles.GOLD),
                background="rgba(201, 162, 39, 0.1)",
                border="1px solid rgba(201, 162, 39, 0.3)",
                border_radius="6px",
                padding="4px 12px",
            ),
            # Actions
            rx.menu.root(
                rx.menu.trigger(
                    rx.icon_button(
                        rx.icon("ellipsis-vertical", size=18),
                        variant="ghost",
                        color_scheme="gray",
                        cursor="pointer",
                    ),
                ),
                rx.menu.content(
                    rx.menu.item(
                        rx.hstack(rx.icon("circle-x", size=14), rx.text("Cancel")),
                        color="red",
                        on_click=lambda: AppState.delete_appointment(appt.id),
                    ),
                    background=styles.CARD_BG,
                    border=styles.BORDER_SUBTLE,
                ),
            ),
            width="100%",
            align="center",
        ),
    )


def appointments_content():
    return rx.vstack(
        # Header
        styles.page_header(
            "Appointments",
            f"{AppState.total_appointments} bookings",
            styles.gold_button("Book Appointment", "calendar-plus", on_click=AppState.toggle_appointment_modal),
        ),
        # Quick Stats
        rx.hstack(
            rx.hstack(
                rx.icon("calendar-clock", size=18, color=styles.GOLD),
                rx.text("Today", size="2", weight="medium", color=styles.WHITE),
                rx.text("0 appointments", size="2", color=styles.GRAY_500),
                spacing="2",
                align="center",
                padding="12px 20px",
                background=styles.GRAY_900,
                border_radius="10px",
                border=styles.BORDER_SUBTLE,
            ),
            rx.hstack(
                rx.icon("calendar", size=18, color=styles.BLUE),
                rx.text("This Week", size="2", weight="medium", color=styles.WHITE),
                rx.text(f"{AppState.total_appointments} appointments", size="2", color=styles.GRAY_500),
                spacing="2",
                align="center",
                padding="12px 20px",
                background=styles.GRAY_900,
                border_radius="10px",
                border=styles.BORDER_SUBTLE,
            ),
            spacing="4",
            margin_bottom="24px",
        ),
        # Appointments List
        rx.cond(
            AppState.total_appointments > 0,
            rx.vstack(
                rx.foreach(AppState.appointments, appointment_card),
                spacing="3",
                width="100%",
            ),
            styles.empty_state(
                "calendar-x",
                "No appointments yet",
                "Book your first appointment to get started",
                styles.gold_button("Book Appointment", "calendar-plus", on_click=AppState.toggle_appointment_modal),
            ),
        ),
        appointment_modal(),
        width="100%",
    )


def appointments_page():
    return layout(appointments_content())
