"""Services Page with CRUD Operations"""

import reflex as rx
from barber_crm.state import AppState
from barber_crm import styles
from barber_crm.layout import layout


def service_modal():
    """Modal for creating new service"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.icon("scissors", size=24, color=styles.GOLD),
                        rx.heading("Add New Service", size="5", color=styles.WHITE, weight="bold"),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        on_click=AppState.toggle_service_modal,
                        cursor="pointer",
                    ),
                    width="100%",
                ),
                
                rx.divider(color=styles.GRAY_800, margin_y="16px"),
                
                rx.vstack(
                    rx.vstack(
                        rx.text("Service Name", size="2", weight="medium", color=styles.GRAY_300),
                        rx.input(
                            placeholder="Classic Haircut",
                            value=AppState.form_service_name,
                            on_change=AppState.set_form_service_name,
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
                        rx.text("Description", size="2", weight="medium", color=styles.GRAY_300),
                        rx.text_area(
                            placeholder="A timeless haircut with precision styling...",
                            value=AppState.form_service_description,
                            on_change=AppState.set_form_service_description,
                            background=styles.GRAY_900,
                            border=styles.BORDER_SUBTLE,
                            border_radius="10px",
                            padding="12px 16px",
                            color=styles.WHITE,
                            width="100%",
                            min_height="80px",
                            _focus={"border_color": styles.GOLD, "outline": "none"},
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Price ($)", size="2", weight="medium", color=styles.GRAY_300),
                            rx.input(
                                placeholder="25.00",
                                type="number",
                                value=AppState.form_service_price,
                                on_change=AppState.set_form_service_price,
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
                            rx.text("Duration (min)", size="2", weight="medium", color=styles.GRAY_300),
                            rx.input(
                                placeholder="30",
                                type="number",
                                value=AppState.form_service_duration,
                                on_change=AppState.set_form_service_duration,
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
                        on_click=AppState.toggle_service_modal,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(AppState.is_loading, rx.spinner(size="1"), rx.icon("plus", size=16)),
                            rx.text("Add Service"),
                            spacing="2",
                        ),
                        background=styles.GOLD_GRADIENT,
                        color=styles.BLACK,
                        on_click=AppState.create_service,
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
                "max_width": "480px",
                "width": "100%",
            },
        ),
        open=AppState.show_service_modal,
    )


def service_card(service):
    """Individual service card"""
    return styles.premium_card(
        rx.hstack(
            # Icon
            rx.center(
                rx.icon("scissors", size=24, color=styles.GOLD),
                width="56px",
                height="56px",
                background="rgba(201, 162, 39, 0.1)",
                border_radius="14px",
                border=f"1px solid rgba(201, 162, 39, 0.2)",
                flex_shrink="0",
            ),
            
            # Service Info
            rx.vstack(
                rx.heading(service.name, size="4", color=styles.WHITE, weight="bold"),
                rx.text(
                    service.description,
                    size="2",
                    color=styles.GRAY_500,
                    overflow="hidden",
                    text_overflow="ellipsis",
                    style={"display": "-webkit-box", "-webkit-line-clamp": "2", "-webkit-box-orient": "vertical"},
                ),
                spacing="1",
                align="start",
                flex="1",
            ),
            
            # Price & Duration
            rx.vstack(
                rx.heading(
                    "$", service.price,
                    size="6",
                    weight="bold",
                    style={
                        "background": styles.GOLD_GRADIENT,
                        "background_clip": "text",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    },
                ),
                rx.hstack(
                    rx.icon("clock", size=14, color=styles.GRAY_500),
                    rx.text(service.duration, " min", size="2", color=styles.GRAY_500),
                    spacing="1",
                    align="center",
                ),
                align="end",
                spacing="1",
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
                        rx.hstack(rx.icon("trash-2", size=14), rx.text("Delete")),
                        color="red",
                        on_click=lambda: AppState.delete_service(service.id),
                    ),
                    background=styles.CARD_BG,
                    border=styles.BORDER_SUBTLE,
                ),
            ),
            
            width="100%",
            spacing="4",
            align="center",
        ),
    )


def services_content():
    return rx.vstack(
        # Header
        styles.page_header(
            "Services",
            f"{AppState.total_services} services available",
            styles.gold_button("Add Service", "plus", on_click=AppState.toggle_service_modal),
        ),
        
        # Services List
        rx.cond(
            AppState.total_services > 0,
            rx.vstack(
                rx.foreach(AppState.services, service_card),
                spacing="4",
                width="100%",
            ),
            styles.empty_state(
                "scissors",
                "No services yet",
                "Add your first service to start taking bookings",
                styles.gold_button("Add Service", "plus", on_click=AppState.toggle_service_modal),
            ),
        ),
        
        service_modal(),
        width="100%",
    )


def services_page():
    return layout(services_content())
