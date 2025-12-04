"""Authentication pages - Login, Register, and Landing."""

import reflex as rx

from ..state import AppState
from ..styles import (
    BLACK,
    BORDER_SUBTLE,
    DARK_BG,
    GOLD,
    GOLD_GRADIENT,
    GRAY_300,
    GRAY_500,
    GRAY_700,
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
                        placeholder="Business Name",
                        value=AppState.register_business_name,
                        on_change=AppState.set_register_business_name,
                        icon="building-2",
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
    """Public landing page with premium design."""
    return rx.box(
        # Navbar
        rx.hstack(
            rx.hstack(
                rx.icon("scissors", size=24, color=GOLD),
                rx.text("BARBER CRM", size="3", weight="bold", letter_spacing="2px"),
                align="center",
                spacing="2",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Features", href="#features", color=GRAY_300, size="2", weight="medium"),
                rx.link("Pricing", href="#pricing", color=GRAY_300, size="2", weight="medium"),
                rx.link("Sign In", href="/login", color=WHITE, size="2", weight="bold"),
                rx.link(
                    rx.button(
                        "Get Started",
                        background=GOLD,
                        color=BLACK,
                        size="2",
                        radius="full",
                        font_weight="bold",
                        _hover={"opacity": 0.9, "transform": "scale(1.05)"},
                    ),
                    href="/register",
                ),
                spacing="6",
                align="center",
                display=["none", "none", "flex", "flex"],
            ),
            width="100%",
            padding="24px 48px",
            position="absolute",
            top="0",
            z_index="10",
        ),
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Elevate Your Craft",
                    size="9",
                    weight="bold",
                    color=WHITE,
                    line_height="1.1",
                ),
                rx.heading(
                    "Manage Your Business",
                    size="9",
                    weight="bold",
                    style={
                        "background": GOLD_GRADIENT,
                        "background_clip": "text",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    },
                    line_height="1.1",
                ),
                rx.text(
                    "The premium CRM solution designed exclusively for modern barbershops. Streamline appointments, manage staff, and grow your client base.",
                    size="4",
                    color=GRAY_300,
                    max_width="600px",
                    margin_top="24px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Start Free Trial",
                            size="4",
                            background=GOLD,
                            color=BLACK,
                            radius="full",
                            font_weight="bold",
                            padding="24px 48px",
                            _hover={"opacity": 0.9, "transform": "translateY(-2px)"},
                        ),
                        href="/register",
                    ),
                    rx.link(
                        rx.button(
                            "View Demo",
                            size="4",
                            variant="outline",
                            color=WHITE,
                            border_color=WHITE,
                            radius="full",
                            font_weight="bold",
                            padding="24px 48px",
                            _hover={"background": "rgba(255,255,255,0.1)", "transform": "translateY(-2px)"},
                        ),
                        href="#demo",
                    ),
                    spacing="4",
                    margin_top="48px",
                ),
                align="start",
                justify="center",
                height="100vh",
                padding="0 10%",
                max_width="1400px",
                margin="0 auto",
            ),
            background="linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('/hero.png')",
            background_size="cover",
            background_position="center",
            width="100%",
        ),
        # Features Section
        rx.box(
            rx.vstack(
                rx.text("FEATURES", color=GOLD, letter_spacing="2px", weight="bold", size="2"),
                rx.heading("Everything you need to run your shop", size="8", color=WHITE, margin_bottom="48px"),
                rx.grid(
                    feature_card(
                        "calendar-clock",
                        "Smart Scheduling",
                        "Effortless appointment management with automated reminders.",
                    ),
                    feature_card("users", "Client Profiles", "Detailed history and preferences for every client."),
                    feature_card("chart-bar", "Analytics", "Real-time insights into your business performance."),
                    feature_card("smartphone", "Mobile Ready", "Manage your shop from anywhere, on any device."),
                    columns="2",
                    spacing="8",
                    width="100%",
                ),
                max_width="1200px",
                margin="0 auto",
                padding="100px 24px",
            ),
            id="features",
            background=BLACK,
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
            background=BLACK,
        ),
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    """Feature card for landing page."""
    return rx.box(
        rx.vstack(
            rx.icon(icon, size=32, color=GOLD),
            rx.heading(title, size="4", color=WHITE, weight="bold"),
            rx.text(description, size="2", color=GRAY_500, line_height="1.6"),
            spacing="3",
            align="start",
        ),
        padding="2rem",
        background=DARK_BG,
        border=BORDER_SUBTLE,
        border_radius="1rem",
        transition="all 0.3s ease",
        _hover={
            "border_color": GOLD,
            "transform": "translateY(-4px)",
            "box_shadow": SHADOW_GOLD,
        },
    )
