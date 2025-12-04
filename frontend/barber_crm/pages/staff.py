"""Staff Page with CRUD Operations"""

import reflex as rx

from barber_crm import styles
from barber_crm.layout import layout
from barber_crm.state import AppState


def staff_modal():
    """Modal for creating new staff member"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("user-cog", size=24, color=styles.GOLD),
                        rx.heading("Add Staff Member", size="5", color=styles.WHITE, weight="bold"),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        on_click=AppState.toggle_staff_modal,
                        cursor="pointer",
                    ),
                    width="100%",
                ),
                rx.divider(color=styles.GRAY_800, margin_y="16px"),
                rx.vstack(
                    rx.vstack(
                        rx.text("Full Name", size="2", weight="medium", color=styles.GRAY_300),
                        rx.input(
                            placeholder="Mike Johnson",
                            value=AppState.form_staff_name,
                            on_change=AppState.set_form_staff_name,
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
                            placeholder="mike@barbershop.com",
                            type="email",
                            value=AppState.form_staff_email,
                            on_change=AppState.set_form_staff_email,
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
                            placeholder="+1 (555) 987-6543",
                            type="tel",
                            value=AppState.form_staff_phone,
                            on_change=AppState.set_form_staff_phone,
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
                        rx.text("Role", size="2", weight="medium", color=styles.GRAY_300),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Select role",
                                width="100%",
                                style={
                                    "background": styles.GRAY_900,
                                    "border": styles.BORDER_SUBTLE,
                                    "border_radius": "10px",
                                },
                            ),
                            rx.select.content(
                                rx.select.item("Barber", value="Barber"),
                                rx.select.item("Senior Barber", value="Senior Barber"),
                                rx.select.item("Manager", value="Manager"),
                                rx.select.item("Receptionist", value="Receptionist"),
                                background=styles.CARD_BG,
                            ),
                            value=AppState.form_staff_role,
                            on_change=AppState.set_form_staff_role,
                            width="100%",
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
                        on_click=AppState.toggle_staff_modal,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(AppState.is_loading, rx.spinner(size="1"), rx.icon("plus", size=16)),
                            rx.text("Add Staff"),
                            spacing="2",
                        ),
                        background=styles.GOLD_GRADIENT,
                        color=styles.BLACK,
                        on_click=AppState.create_staff,
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
                "max_width": "440px",
                "width": "100%",
            },
        ),
        open=AppState.show_staff_modal,
    )


def staff_card(member):
    """Individual staff card"""
    return styles.premium_card(
        rx.vstack(
            # Header with avatar
            rx.center(
                rx.vstack(
                    rx.avatar(
                        fallback="ST",
                        size="6",
                        style={
                            "background": styles.GOLD_GRADIENT,
                            "color": styles.BLACK,
                            "font_weight": "700",
                            "font_size": "18px",
                        },
                    ),
                    rx.heading(member.name, size="4", color=styles.WHITE, weight="bold", margin_top="12px"),
                    rx.box(
                        rx.text(member.role, size="1", weight="bold", color=styles.GOLD),
                        background="rgba(201, 162, 39, 0.1)",
                        border="1px solid rgba(201, 162, 39, 0.3)",
                        border_radius="20px",
                        padding="4px 12px",
                    ),
                    align="center",
                    spacing="2",
                ),
                padding="20px",
                background="linear-gradient(180deg, rgba(201, 162, 39, 0.08) 0%, transparent 100%)",
                border_radius="12px",
                width="100%",
            ),
            rx.divider(color=styles.GRAY_800, margin_y="16px"),
            # Contact info
            rx.vstack(
                rx.hstack(
                    rx.icon("mail", size=16, color=styles.GRAY_500),
                    rx.text(member.email, size="2", color=styles.GRAY_300),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                rx.hstack(
                    rx.icon("phone", size=16, color=styles.GRAY_500),
                    rx.text(member.phone, size="2", color=styles.GRAY_300),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            # Actions
            rx.hstack(
                rx.spacer(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.hstack(
                                rx.text("Actions", size="1"),
                                rx.icon("chevron-down", size=14),
                                spacing="1",
                            ),
                            variant="outline",
                            color_scheme="gray",
                            size="1",
                            cursor="pointer",
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            rx.hstack(rx.icon("trash-2", size=14), rx.text("Delete")),
                            color="red",
                            on_click=lambda: AppState.delete_staff(member.id),
                        ),
                        background=styles.CARD_BG,
                        border=styles.BORDER_SUBTLE,
                    ),
                ),
                width="100%",
                margin_top="12px",
            ),
            spacing="0",
            width="100%",
        ),
    )


def staff_content():
    return rx.vstack(
        # Header
        styles.page_header(
            "Staff",
            f"{AppState.total_staff} team members",
            styles.gold_button("Add Staff", "user-plus", on_click=AppState.toggle_staff_modal),
        ),
        # Staff Grid
        rx.cond(
            AppState.total_staff > 0,
            rx.grid(
                rx.foreach(AppState.staff, staff_card),
                columns="4",
                spacing="5",
                width="100%",
            ),
            styles.empty_state(
                "user-cog",
                "No staff members yet",
                "Add your team to start scheduling appointments",
                styles.gold_button("Add Staff Member", "user-plus", on_click=AppState.toggle_staff_modal),
            ),
        ),
        staff_modal(),
        width="100%",
    )


def staff_page():
    return layout(staff_content())
