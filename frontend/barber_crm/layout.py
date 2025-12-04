"""Main Application Layout - Premium Barbershop Theme"""

import reflex as rx

from barber_crm import styles
from barber_crm.state import AppState


def nav_item(text: str, icon: str, href: str, is_active: bool = False):
    """Navigation item with hover effects"""
    active_style = (
        {
            "background": "linear-gradient(90deg, rgba(201, 162, 39, 0.15) 0%, transparent 100%)",
            "border_left": f"3px solid {styles.GOLD}",
            "color": styles.GOLD,
        }
        if is_active
        else {}
    )

    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color=styles.GOLD if is_active else styles.GRAY_500),
            rx.text(
                text,
                size="3",
                weight="medium",
                color=styles.WHITE if is_active else styles.GRAY_300,
            ),
            spacing="3",
            align="center",
            width="100%",
            padding="14px 16px",
            border_radius="12px",
            transition="all 0.2s ease",
            _hover={
                "background": styles.GRAY_800,
                "transform": "translateX(4px)",
            },
            style=active_style,
        ),
        href=href,
        width="100%",
        text_decoration="none",
    )


def sidebar():
    """Premium sidebar navigation"""
    return rx.box(
        rx.vstack(
            # Logo Header
            rx.hstack(
                rx.center(
                    rx.image(src="/logo.svg", width="32px", height="32px"),
                    width="48px",
                    height="48px",
                    background="linear-gradient(135deg, rgba(201, 162, 39, 0.2) 0%, rgba(201, 162, 39, 0.05) 100%)",
                    border_radius="14px",
                    border="1px solid rgba(201, 162, 39, 0.3)",
                ),
                rx.vstack(
                    rx.text(
                        "BARBER",
                        size="4",
                        weight="bold",
                        color=styles.WHITE,
                        letter_spacing="2px",
                    ),
                    rx.text(
                        "CRM",
                        size="1",
                        weight="bold",
                        color=styles.GOLD,
                        letter_spacing="4px",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                padding="8px",
                margin_bottom="32px",
            ),
            # Business Selector
            rx.cond(
                AppState.is_master,
                rx.box(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.hstack(
                                rx.icon("building-2", size=18, color=styles.GOLD),
                                rx.text(
                                    AppState.selected_business_name,
                                    size="2",
                                    weight="medium",
                                    color=styles.WHITE,
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                    white_space="nowrap",
                                ),
                                rx.spacer(),
                                rx.icon("chevron-down", size=16, color=styles.GRAY_500),
                                width="100%",
                                align="center",
                                padding="12px 14px",
                                background=styles.GRAY_900,
                                border=styles.BORDER_SUBTLE,
                                border_radius="10px",
                                cursor="pointer",
                                transition="all 0.2s ease",
                                _hover={"border_color": styles.GOLD},
                            ),
                        ),
                        rx.menu.content(
                            rx.foreach(
                                AppState.businesses,
                                lambda b: rx.menu.item(
                                    b.name,
                                    on_click=lambda: AppState.select_business(b.id, b.name),
                                ),
                            ),
                            background=styles.CARD_BG,
                            border=styles.BORDER_SUBTLE,
                        ),
                    ),
                    width="100%",
                    margin_bottom="24px",
                ),
                rx.fragment(),
            ),
            # Navigation Links
            rx.vstack(
                rx.text(
                    "MENU", size="1", weight="bold", color=styles.GRAY_700, letter_spacing="2px", padding_left="16px"
                ),
                nav_item("Dashboard", "layout-dashboard", "/dashboard"),
                nav_item("Appointments", "calendar-clock", "/appointments"),
                nav_item("Customers", "users", "/customers"),
                nav_item("Staff", "user-cog", "/staff"),
                nav_item("Services", "scissors", "/services"),
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            # Decorative Element
            rx.box(
                rx.vstack(
                    rx.icon("sparkles", size=24, color=styles.GOLD),
                    rx.text("Premium", size="2", weight="bold", color=styles.GOLD),
                    rx.text("Barbershop CRM", size="1", color=styles.GRAY_500),
                    spacing="2",
                    align="center",
                ),
                padding="20px",
                background="linear-gradient(180deg, rgba(201, 162, 39, 0.1) 0%, transparent 100%)",
                border="1px solid rgba(201, 162, 39, 0.2)",
                border_radius="16px",
                width="100%",
                text_align="center",
            ),
            # User Profile
            rx.hstack(
                rx.avatar(
                    fallback=rx.cond(
                        AppState.is_authenticated,
                        AppState.user.username[:2].upper(),
                        "?",
                    ),
                    size="3",
                    radius="full",
                    style={
                        "background": styles.GOLD_GRADIENT,
                        "color": styles.BLACK,
                    },
                ),
                rx.vstack(
                    rx.cond(
                        AppState.is_authenticated,
                        rx.text(AppState.user.username, size="2", weight="bold", color=styles.WHITE),
                        rx.link("Sign In", href="/login", size="2", weight="bold", color=styles.GOLD),
                    ),
                    rx.cond(
                        AppState.is_master,
                        rx.text("Master Admin", size="1", color=styles.GOLD),
                        rx.text("Owner", size="1", color=styles.GRAY_500),
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.cond(
                    AppState.is_authenticated,
                    rx.icon_button(
                        rx.icon("log-out", size=16),
                        variant="ghost",
                        color_scheme="gray",
                        size="2",
                        cursor="pointer",
                        on_click=AppState.logout,
                    ),
                    rx.fragment(),
                ),
                width="100%",
                align="center",
                padding="16px",
                margin_top="16px",
                background=styles.GRAY_900,
                border_radius="12px",
                border=styles.BORDER_SUBTLE,
            ),
            height="100%",
            width="100%",
            spacing="2",
        ),
        width="280px",
        height="100vh",
        padding="20px",
        background=styles.DARK_BG,
        border_right=styles.BORDER_SUBTLE,
        position="fixed",
        left="0",
        top="0",
        z_index="100",
        overflow_y="auto",
    )


def notifications():
    """Toast notifications"""
    return rx.fragment(
        rx.cond(
            AppState.success_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle-check", size=20, color=styles.GREEN),
                    rx.text(AppState.success_message, color=styles.WHITE, weight="medium"),
                    rx.icon_button(
                        rx.icon("x", size=14),
                        variant="ghost",
                        size="1",
                        on_click=AppState.clear_messages,
                        cursor="pointer",
                    ),
                    spacing="3",
                    align="center",
                ),
                background=styles.GRAY_900,
                border=f"1px solid {styles.GREEN}",
                border_radius="12px",
                padding="12px 20px",
                position="fixed",
                top="20px",
                right="20px",
                z_index="1000",
                box_shadow=styles.SHADOW_MD,
            ),
        ),
        rx.cond(
            AppState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("circle-alert", size=20, color=styles.RED),
                    rx.text(AppState.error_message, color=styles.WHITE, weight="medium"),
                    rx.icon_button(
                        rx.icon("x", size=14),
                        variant="ghost",
                        size="1",
                        on_click=AppState.clear_messages,
                        cursor="pointer",
                    ),
                    spacing="3",
                    align="center",
                ),
                background=styles.GRAY_900,
                border=f"1px solid {styles.RED}",
                border_radius="12px",
                padding="12px 20px",
                position="fixed",
                top="20px",
                right="20px",
                z_index="1000",
                box_shadow=styles.SHADOW_MD,
            ),
        ),
    )


def layout(content: rx.Component):
    """Main layout wrapper"""
    return rx.box(
        sidebar(),
        rx.box(
            content,
            margin_left="280px",
            padding="32px 40px",
            min_height="100vh",
            background=styles.BLACK,
        ),
        notifications(),
        background=styles.BLACK,
        min_height="100vh",
        color=styles.WHITE,
    )
