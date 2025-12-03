"""Staff Page"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout

def staff_content():
    return rx.vstack(
        styles.page_title("Staff Members", "Manage your team"),
        
        rx.cond(
            AppState.staff,
            rx.grid(
                rx.foreach(
                    AppState.staff,
                    lambda member: styles.premium_card(
                        rx.vstack(
                            rx.box(
                                rx.center(
                                    rx.avatar(
                                        fallback=member.name[0], 
                                        size="6", 
                                        radius="full", 
                                        variant="solid",
                                        color_scheme="amber",
                                        border=f"2px solid {styles.accent_color}"
                                    ),
                                    rx.heading(member.name, size="4", color="white", margin_top="3"),
                                    rx.text(member.role, size="2", color=styles.accent_color, weight="medium"),
                                    width="100%",
                                    flex_direction="column",
                                ),
                                padding="20px",
                                background="linear-gradient(180deg, rgba(255,255,255,0.03) 0%, transparent 100%)",
                                border_radius="12px",
                                width="100%",
                                margin_bottom="4",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("mail", size=16, color=styles.text_secondary),
                                    rx.text(member.email, size="2", color=styles.text_secondary),
                                    spacing="3",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.icon("phone", size=16, color=styles.text_secondary),
                                    rx.text(member.phone, size="2", color=styles.text_secondary),
                                    spacing="3",
                                    align="center",
                                ),
                                spacing="3",
                                width="100%",
                                padding_x="2",
                            ),
                            width="100%",
                        )
                    ),
                ),
                columns="4",
                spacing="6",
                width="100%",
            ),
            rx.text("No staff members found.", color="gray"),
        ),
        width="100%",
    )

def staff_page():
    return layout(staff_content())

