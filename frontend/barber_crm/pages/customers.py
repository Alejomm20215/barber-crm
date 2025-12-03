"""Customers Page with CRUD Operations"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout


def customer_modal():
    """Modal for creating new customer"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("user-plus", size=24, color=styles.GOLD),
                        rx.heading("Add New Customer", size="5", color=styles.WHITE, weight="bold"),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        on_click=AppState.toggle_customer_modal,
                        cursor="pointer",
                    ),
                    width="100%",
                ),
                
                rx.divider(color=styles.GRAY_800, margin_y="16px"),
                
                rx.vstack(
                    rx.vstack(
                        rx.text("Full Name", size="2", weight="medium", color=styles.GRAY_300),
                        rx.input(
                            placeholder="John Smith",
                            value=AppState.form_customer_name,
                            on_change=AppState.set_form_customer_name,
                            background=styles.GRAY_900,
                            border=styles.BORDER_SUBTLE,
                            border_radius="10px",
                            padding="12px 16px",
                            color=styles.WHITE,
                            width="100%",
                            _focus={"border_color": styles.GOLD, "outline": "none"},
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Email Address", size="2", weight="medium", color=styles.GRAY_300),
                        rx.input(
                            placeholder="john@example.com",
                            type="email",
                            value=AppState.form_customer_email,
                            on_change=AppState.set_form_customer_email,
                            background=styles.GRAY_900,
                            border=styles.BORDER_SUBTLE,
                            border_radius="10px",
                            padding="12px 16px",
                            color=styles.WHITE,
                            width="100%",
                            _focus={"border_color": styles.GOLD, "outline": "none"},
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Phone Number", size="2", weight="medium", color=styles.GRAY_300),
                        rx.input(
                            placeholder="+1 (555) 123-4567",
                            type="tel",
                            value=AppState.form_customer_phone,
                            on_change=AppState.set_form_customer_phone,
                            background=styles.GRAY_900,
                            border=styles.BORDER_SUBTLE,
                            border_radius="10px",
                            padding="12px 16px",
                            color=styles.WHITE,
                            width="100%",
                            _focus={"border_color": styles.GOLD, "outline": "none"},
                        ),
                        spacing="2",
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
                        on_click=AppState.toggle_customer_modal,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(AppState.is_loading, rx.spinner(size="1"), rx.icon("plus", size=16)),
                            rx.text("Add Customer"),
                            spacing="2",
                        ),
                        background=styles.GOLD_GRADIENT,
                        color=styles.BLACK,
                        on_click=AppState.create_customer,
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
                "border": f"1px solid rgba(201, 162, 39, 0.3)",
                "border_radius": "20px",
                "padding": "24px",
                "max_width": "440px",
                "width": "100%",
            },
        ),
        open=AppState.show_customer_modal,
    )


def customer_card(customer):
    """Individual customer card"""
    return styles.premium_card(
        rx.vstack(
            rx.hstack(
                rx.avatar(
                    fallback="?",
                    size="4",
                    style={
                        "background": styles.GOLD_GRADIENT,
                        "color": styles.BLACK,
                        "font_weight": "700",
                    },
                ),
                rx.vstack(
                    rx.text(customer.name, weight="bold", color=styles.WHITE, size="3"),
                    rx.text(customer.email, size="1", color=styles.GRAY_500),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
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
                            rx.hstack(rx.icon("trash-2", size=14), rx.text("Delete")),
                            color="red",
                            on_click=lambda: AppState.delete_customer(customer.id),
                        ),
                        background=styles.CARD_BG,
                        border=styles.BORDER_SUBTLE,
                    ),
                ),
                width="100%",
                align="center",
            ),
            rx.divider(color=styles.GRAY_800, margin_y="12px"),
            rx.hstack(
                rx.hstack(
                    rx.icon("phone", size=14, color=styles.GRAY_500),
                    rx.text(customer.phone, size="2", color=styles.GRAY_300),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon("calendar-check", size=14, color=styles.GOLD),
                    rx.text(customer.total_visits, " visits", size="2", color=styles.GOLD, weight="medium"),
                    spacing="2",
                    align="center",
                ),
                width="100%",
            ),
            spacing="0",
            width="100%",
        ),
    )


def customers_content():
    return rx.vstack(
        # Header
        styles.page_header(
            "Customers",
            f"{AppState.total_customers} total clients",
            styles.gold_button("Add Customer", "user-plus", on_click=AppState.toggle_customer_modal),
        ),
        
        # Customer Grid
        rx.cond(
            AppState.total_customers > 0,
            rx.grid(
                rx.foreach(AppState.customers, customer_card),
                columns="3",
                spacing="5",
                width="100%",
            ),
            styles.empty_state(
                "users",
                "No customers yet",
                "Add your first customer to start tracking visits",
                styles.gold_button("Add Customer", "user-plus", on_click=AppState.toggle_customer_modal),
            ),
        ),
        
        customer_modal(),
        width="100%",
    )


def customers_page():
    return layout(customers_content())
