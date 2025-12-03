"""Appointments Page with Creation Modal"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout

def appointment_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("New Appointment", color="white"),
            rx.dialog.description("Schedule a new appointment for a customer.", color=styles.text_secondary),
            
            rx.vstack(
                rx.text("Customer", size="2", weight="bold", color="white"),
                rx.select.root(
                    rx.select.trigger(placeholder="Select Customer", width="100%"),
                    rx.select.content(
                        rx.select.group(
                            rx.foreach(
                                AppState.customers,
                                lambda c: rx.select.item(c.name, value=c.id)
                            )
                        ),
                    ),
                    on_change=AppState.set_new_appointment_customer,
                    value=AppState.new_appointment_customer,
                ),
                
                rx.text("Staff Member", size="2", weight="bold", color="white"),
                rx.select.root(
                    rx.select.trigger(placeholder="Select Staff", width="100%"),
                    rx.select.content(
                        rx.select.group(
                            rx.foreach(
                                AppState.staff,
                                lambda s: rx.select.item(s.name, value=s.id)
                            )
                        ),
                    ),
                    on_change=AppState.set_new_appointment_staff,
                    value=AppState.new_appointment_staff,
                ),
                
                rx.text("Service", size="2", weight="bold", color="white"),
                rx.select.root(
                    rx.select.trigger(placeholder="Select Service", width="100%"),
                    rx.select.content(
                        rx.select.group(
                            rx.foreach(
                                AppState.services,
                                lambda s: rx.select.item(s.name, value=s.id)
                            )
                        ),
                    ),
                    on_change=AppState.set_new_appointment_service,
                    value=AppState.new_appointment_service,
                ),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Date", size="2", weight="bold", color="white"),
                        rx.input(
                            type="date",
                            on_change=AppState.set_new_appointment_date,
                            width="100%",
                            variant="soft",
                            color_scheme="gray",
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Time", size="2", weight="bold", color="white"),
                        rx.input(
                            type="time",
                            on_change=AppState.set_new_appointment_time,
                            width="100%",
                            variant="soft",
                            color_scheme="gray",
                        ),
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                
                spacing="4",
                margin_top="4",
            ),
            
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                ),
                rx.button(
                    "Create Appointment", 
                    on_click=AppState.create_appointment,
                    loading=AppState.is_loading,
                    background=styles.accent_gradient,
                    color="black",
                    _hover={"opacity": 0.9},
                ),
                spacing="3",
                margin_top="6",
                justify="end",
            ),
            style={
                "max_width": "500px",
                "background": "#1a1a1a",
                "border": f"1px solid {styles.border_color}",
            },
        ),
        open=AppState.is_appointment_modal_open,
        on_open_change=AppState.toggle_appointment_modal,
    )

def appointments_content():
    return rx.vstack(
        styles.page_title("Appointments", "Manage your schedule"),
        
        # Actions Bar
        rx.hstack(
            rx.button(
                rx.icon("plus", size=18),
                "New Appointment",
                on_click=AppState.toggle_appointment_modal,
                background=styles.accent_gradient,
                color="black",
                size="3",
                _hover={"transform": "scale(1.02)"},
            ),
            rx.spacer(),
            rx.select(
                ["All", "Scheduled", "Completed", "Cancelled"],
                default_value="All",
                variant="soft",
                color_scheme="gray",
            ),
            width="100%",
            margin_bottom="6",
        ),
        
        # Appointments List
        rx.cond(
            AppState.appointments,
            rx.vstack(
                rx.foreach(
                    AppState.appointments,
                    lambda appt: styles.premium_card(
                        rx.hstack(
                            # Time Column
                            rx.vstack(
                                rx.text(appt.scheduled_at, size="2", color=styles.text_secondary, weight="bold"),
                                align="center",
                                min_width="100px",
                                border_right=f"1px solid {styles.border_color}",
                                padding_right="4",
                            ),
                            
                            # Details Column
                            rx.vstack(
                                rx.heading(appt.customer_name, size="4", color="white"),
                                rx.hstack(
                                    rx.icon("scissors", size=14, color=styles.accent_color),
                                    rx.text(appt.service_name, size="2", color=styles.text_secondary),
                                    rx.icon("user", size=14, color=styles.accent_color),
                                    rx.text(appt.staff_name, size="2", color=styles.text_secondary),
                                    spacing="2",
                                    align="center",
                                ),
                                align="start",
                                padding_left="4",
                            ),
                            
                            rx.spacer(),
                            
                            # Status Badge
                            rx.badge(
                                appt.status,
                                color_scheme=rx.cond(
                                    appt.status == "scheduled", "blue",
                                    rx.cond(appt.status == "completed", "green", "gray")
                                ),
                                size="2",
                                variant="soft",
                            ),
                            
                            width="100%",
                            align="center",
                        ),
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            rx.center(
                rx.text("No appointments found.", color="gray"),
                padding="10",
            ),
        ),
        
        appointment_modal(),
        width="100%",
    )

def appointments_page():
    return layout(appointments_content())
