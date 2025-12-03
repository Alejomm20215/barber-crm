"""Customers Page"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout

def customers_content():
    return rx.vstack(
        styles.page_title("Customers", "Manage your client base"),
        
        rx.cond(
            AppState.customers,
            rx.grid(
                rx.foreach(
                    AppState.customers,
                    lambda customer: styles.premium_card(
                        rx.vstack(
                            rx.hstack(
                                rx.avatar(
                                    fallback=customer.name[0], 
                                    size="4", 
                                    radius="full",
                                    variant="soft",
                                    color_scheme="gray"
                                ),
                                rx.vstack(
                                    rx.text(customer.name, weight="bold", color="white"),
                                    rx.text(customer.email, size="2", color=styles.text_secondary),
                                    spacing="0",
                                ),
                                rx.spacer(),
                                rx.icon_button(
                                    rx.icon("ellipsis", size=16), 
                                    variant="ghost", 
                                    size="2",
                                    color="white"
                                ),
                                width="100%",
                                align="center",
                            ),
                            rx.divider(margin_y="3", color="rgba(255,255,255,0.1)"),
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Phone", size="1", color=styles.text_secondary),
                                    rx.text(customer.phone, size="2", color="white"),
                                    spacing="0",
                                ),
                                rx.spacer(),
                                rx.vstack(
                                    rx.text("Visits", size="1", color=styles.text_secondary),
                                    rx.text(customer.total_visits.to_string(), size="2", color=styles.accent_color, weight="bold"),
                                    spacing="0",
                                    align="end",
                                ),
                                width="100%",
                            ),
                            width="100%",
                        )
                    ),
                ),
                columns="3",
                spacing="6",
                width="100%",
            ),
            rx.text("No customers found.", color="gray"),
        ),
        width="100%",
    )

def customers_page():
    return layout(customers_content())
