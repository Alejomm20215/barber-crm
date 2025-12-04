"""Authentication pages - Login, Register, and Landing."""

import reflex as rx

from ..state import AppState
from ..styles import (
    BLACK,
    BORDER_SUBTLE,
    CARD_BG,
    DARK_BG,
    GOLD,
    GOLD_GRADIENT,
    GRAY_300,
    GRAY_500,
    GRAY_700,
    GRAY_800,
    SHADOW_GOLD,
    WHITE,
)


def auth_input(
    placeholder: str,
    value: rx.Var,
    on_change: rx.EventHandler,
    input_type: str = "text",
    icon: str = "user",
) -> rx.Component:
    """Styled input for auth forms."""
    return rx.box(
        rx.icon(icon, size=18, color=GRAY_500),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=input_type,
            width="100%",
            background="transparent",
            border="none",
            color=WHITE,
            padding_left="0.5rem",
            _focus={"outline": "none"},
            _placeholder={"color": GRAY_500},
        ),
        display="flex",
        align_items="center",
        gap="0.75rem",
        padding="0.875rem 1rem",
        background=BLACK,
        border=BORDER_SUBTLE,
        border_radius="0.5rem",
        _focus_within={"border_color": GOLD},
    )


def login_page() -> rx.Component:
    """Login page component."""
    return rx.center(
        rx.box(
            # Logo/Brand
            rx.vstack(
                rx.icon("scissors", size=48, color=GOLD),
                rx.heading(
                    "Barber CRM",
                    size="7",
                    color=WHITE,
                    weight="bold",
                ),
                rx.text(
                    "Welcome back! Sign in to continue.",
                    color=GRAY_300,
                    size="2",
                ),
                spacing="2",
                align="center",
                margin_bottom="2rem",
            ),
            # Error message
            rx.cond(
                AppState.auth_error != "",
                rx.box(
                    rx.hstack(
                        rx.icon("circle-alert", size=16, color="#ef4444"),
                        rx.text(AppState.auth_error, color="#ef4444", size="2"),
                        spacing="2",
                    ),
                    padding="0.75rem 1rem",
                    background="rgba(239, 68, 68, 0.1)",
                    border="1px solid rgba(239, 68, 68, 0.3)",
                    border_radius="0.5rem",
                    margin_bottom="1rem",
                    width="100%",
                ),
            ),
            # Login Form
            rx.form(
                rx.vstack(
                    auth_input(
                        placeholder="Username",
                        value=AppState.login_username,
                        on_change=AppState.set_login_username,
                        icon="user",
                    ),
                    auth_input(
                        placeholder="Password",
                        value=AppState.login_password,
                        on_change=AppState.set_login_password,
                        input_type="password",
                        icon="lock",
                    ),
                    rx.button(
                        rx.cond(
                            AppState.auth_loading,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Signing in..."),
                                spacing="2",
                            ),
                            rx.text("Sign In"),
                        ),
                        type="submit",
                        width="100%",
                        padding="0.875rem",
                        background=GOLD,
                        color=BLACK,
                        font_weight="bold",
                        border_radius="0.5rem",
                        cursor="pointer",
                        _hover={"opacity": "0.9"},
                        disabled=AppState.auth_loading,
                    ),
                    spacing="4",
                    width="100%",
                ),
                on_submit=lambda _: AppState.login(),
                width="100%",
            ),
            # Register link
            rx.hstack(
                rx.text("Don't have an account?", color=GRAY_500, size="2"),
                rx.link(
                    "Create one",
                    href="/register",
                    color=GOLD,
                    font_weight="medium",
                    size="2",
                    _hover={"text_decoration": "underline"},
                ),
                spacing="2",
                justify="center",
                margin_top="1.5rem",
            ),
            # Back to landing
            rx.link(
                rx.hstack(
                    rx.icon("arrow-left", size=14, color=GRAY_500),
                    rx.text("Back to home", color=GRAY_500, size="2"),
                    spacing="2",
                ),
                href="/welcome",
                margin_top="1rem",
                _hover={"opacity": "0.8"},
            ),
            width="100%",
            max_width="400px",
            padding="2.5rem",
            background=DARK_BG,
            border=BORDER_SUBTLE,
            border_radius="1rem",
            box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.5)",
        ),
        min_height="100vh",
        background=f"linear-gradient(135deg, {BLACK} 0%, #1a1a2e 100%)",
        padding="1rem",
    )


def register_page() -> rx.Component:
    """Register page component."""
    return rx.center(
        rx.box(
            # Logo/Brand
            rx.vstack(
                rx.icon("scissors", size=48, color=GOLD),
                rx.heading(
                    "Create Account",
                    size="7",
                    color=WHITE,
                    weight="bold",
                ),
                rx.text(
                    "Start managing your barbershop today.",
                    color=GRAY_300,
                    size="2",
                ),
                spacing="2",
                align="center",
                margin_bottom="2rem",
            ),
            # Error message
            rx.cond(
                AppState.auth_error != "",
                rx.box(
                    rx.hstack(
                        rx.icon("circle-alert", size=16, color="#ef4444"),
                        rx.text(AppState.auth_error, color="#ef4444", size="2"),
                        spacing="2",
                    ),
                    padding="0.75rem 1rem",
                    background="rgba(239, 68, 68, 0.1)",
                    border="1px solid rgba(239, 68, 68, 0.3)",
                    border_radius="0.5rem",
                    margin_bottom="1rem",
                    width="100%",
                ),
            ),
            # Register Form
            rx.form(
                rx.vstack(
                    # Name row
                    rx.hstack(
                        auth_input(
                            placeholder="First Name",
                            value=AppState.register_first_name,
                            on_change=AppState.set_register_first_name,
                            icon="user",
                        ),
                        auth_input(
                            placeholder="Last Name",
                            value=AppState.register_last_name,
                            on_change=AppState.set_register_last_name,
                            icon="user",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    auth_input(
                        placeholder="Username",
                        value=AppState.register_username,
                        on_change=AppState.set_register_username,
                        icon="at-sign",
                    ),
                    auth_input(
                        placeholder="Email",
                        value=AppState.register_email,
                        on_change=AppState.set_register_email,
                        input_type="email",
                        icon="mail",
                    ),
                    auth_input(
                        placeholder="Phone (optional)",
                        value=AppState.register_phone,
                        on_change=AppState.set_register_phone,
                        icon="phone",
                    ),
                    auth_input(
                        placeholder="Password",
                        value=AppState.register_password,
                        on_change=AppState.set_register_password,
                        input_type="password",
                        icon="lock",
                    ),
                    auth_input(
                        placeholder="Confirm Password",
                        value=AppState.register_password2,
                        on_change=AppState.set_register_password2,
                        input_type="password",
                        icon="lock",
                    ),
                    rx.button(
                        rx.cond(
                            AppState.auth_loading,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Creating account..."),
                                spacing="2",
                            ),
                            rx.text("Create Account"),
                        ),
                        type="submit",
                        width="100%",
                        padding="0.875rem",
                        background=GOLD,
                        color=BLACK,
                        font_weight="bold",
                        border_radius="0.5rem",
                        cursor="pointer",
                        _hover={"opacity": "0.9"},
                        disabled=AppState.auth_loading,
                    ),
                    spacing="3",
                    width="100%",
                ),
                on_submit=lambda _: AppState.register(),
                width="100%",
            ),
            # Login link
            rx.hstack(
                rx.text("Already have an account?", color=GRAY_500, size="2"),
                rx.link(
                    "Sign in",
                    href="/login",
                    color=GOLD,
                    font_weight="medium",
                    size="2",
                    _hover={"text_decoration": "underline"},
                ),
                spacing="2",
                justify="center",
                margin_top="1.5rem",
            ),
            width="100%",
            max_width="480px",
            padding="2.5rem",
            background=DARK_BG,
            border=BORDER_SUBTLE,
            border_radius="1rem",
            box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.5)",
        ),
        min_height="100vh",
        background=f"linear-gradient(135deg, {BLACK} 0%, #1a1a2e 100%)",
        padding="1rem",
    )


def landing_page() -> rx.Component:
    """Public landing page."""
    return rx.box(
        # Hero Section
        rx.center(
            rx.vstack(
                # Animated scissors icon
                rx.center(
                    rx.icon("scissors", size=64, color=GOLD),
                    width="120px",
                    height="120px",
                    background="linear-gradient(135deg, rgba(201, 162, 39, 0.2) 0%, rgba(201, 162, 39, 0.05) 100%)",
                    border_radius="50%",
                    border="2px solid rgba(201, 162, 39, 0.4)",
                    margin_bottom="2rem",
                ),
                # Main heading
                rx.heading(
                    "BARBER CRM",
                    size="9",
                    weight="bold",
                    style={
                        "background": GOLD_GRADIENT,
                        "background_clip": "text",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                        "letter_spacing": "4px",
                    },
                ),
                rx.text(
                    "Premium Barbershop Management",
                    size="5",
                    color=GRAY_300,
                    margin_top="0.5rem",
                ),
                rx.text(
                    "Streamline appointments, manage staff, and grow your business",
                    size="3",
                    color=GRAY_500,
                    text_align="center",
                    max_width="400px",
                    margin_top="1rem",
                ),
                # CTA Buttons
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.text("Get Started", weight="bold"),
                                rx.icon("arrow-right", size=18),
                                spacing="2",
                            ),
                            background=GOLD_GRADIENT,
                            color=BLACK,
                            padding="1rem 2rem",
                            border_radius="0.75rem",
                            cursor="pointer",
                            font_size="1rem",
                            _hover={"transform": "scale(1.02)", "box_shadow": SHADOW_GOLD},
                        ),
                        href="/register",
                    ),
                    rx.link(
                        rx.button(
                            rx.text("Sign In", weight="medium"),
                            background="transparent",
                            color=WHITE,
                            border=BORDER_SUBTLE,
                            padding="1rem 2rem",
                            border_radius="0.75rem",
                            cursor="pointer",
                            font_size="1rem",
                            _hover={"background": GRAY_800, "border_color": GOLD},
                        ),
                        href="/login",
                    ),
                    spacing="4",
                    margin_top="2.5rem",
                ),
                spacing="1",
                align="center",
            ),
            min_height="70vh",
        ),
        # Features Section
        rx.box(
            rx.vstack(
                rx.text("FEATURES", size="1", color=GOLD, weight="bold", letter_spacing="3px"),
                rx.heading("Everything you need", size="7", color=WHITE, weight="bold"),
                rx.grid(
                    feature_card("calendar-clock", "Appointments", "Easy booking and scheduling for your clients"),
                    feature_card("users", "Customer Management", "Track visits, preferences, and history"),
                    feature_card("user-cog", "Staff Management", "Manage your team and their schedules"),
                    feature_card("scissors", "Services", "Define services, pricing, and durations"),
                    feature_card("chart-bar", "Analytics", "Insights to grow your business"),
                    feature_card("shield-check", "Secure", "Your data is safe and protected"),
                    columns="3",
                    spacing="6",
                    width="100%",
                ),
                spacing="6",
                align="center",
                max_width="1000px",
                margin="0 auto",
            ),
            padding="4rem 2rem",
            background=DARK_BG,
        ),
        # Footer
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.icon("scissors", size=20, color=GOLD),
                    rx.text("BARBER CRM", size="2", color=WHITE, weight="bold", letter_spacing="2px"),
                    spacing="2",
                ),
                rx.text("© 2025 Barber CRM. All rights reserved.", size="1", color=GRAY_700),
                spacing="2",
                align="center",
            ),
            padding="2rem",
            border_top=BORDER_SUBTLE,
        ),
        min_height="100vh",
        background=f"linear-gradient(180deg, {BLACK} 0%, {DARK_BG} 50%, {BLACK} 100%)",
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    """Feature card for landing page."""
    return rx.box(
        rx.vstack(
            rx.center(
                rx.icon(icon, size=28, color=GOLD),
                width="56px",
                height="56px",
                background="rgba(201, 162, 39, 0.1)",
                border_radius="12px",
                border="1px solid rgba(201, 162, 39, 0.2)",
            ),
            rx.text(title, size="3", color=WHITE, weight="bold"),
            rx.text(description, size="2", color=GRAY_500, text_align="center"),
            spacing="3",
            align="center",
        ),
        padding="1.5rem",
        background=CARD_BG,
        border=BORDER_SUBTLE,
        border_radius="1rem",
        transition="all 0.3s ease",
        _hover={
            "border_color": GOLD,
            "transform": "translateY(-4px)",
            "box_shadow": SHADOW_GOLD,
        },
    )

