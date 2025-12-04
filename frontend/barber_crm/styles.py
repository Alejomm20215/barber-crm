"""Premium Barbershop Design System - Dark & Gold Aesthetic"""

import reflex as rx

# ============ COLOR PALETTE ============
# Inspired by classic barbershops with modern dark UI
BLACK = "#0a0a0a"
DARK_BG = "#111111"
CARD_BG = "#1a1a1a"
CARD_HOVER = "#222222"
GOLD = "#c9a227"
GOLD_LIGHT = "#e8d48b"
GOLD_DARK = "#9a7b1a"
RED = "#dc2626"
GREEN = "#22c55e"
BLUE = "#3b82f6"
WHITE = "#ffffff"
GRAY_100 = "#f5f5f5"
GRAY_300 = "#d4d4d4"
GRAY_500 = "#737373"
GRAY_700 = "#404040"
GRAY_800 = "#262626"
GRAY_900 = "#171717"

# ============ GRADIENTS ============
GOLD_GRADIENT = f"linear-gradient(135deg, {GOLD} 0%, {GOLD_LIGHT} 50%, {GOLD} 100%)"
DARK_GRADIENT = f"linear-gradient(180deg, {DARK_BG} 0%, {BLACK} 100%)"
CARD_GRADIENT = f"linear-gradient(145deg, {CARD_BG} 0%, {GRAY_900} 100%)"
SHIMMER = "linear-gradient(90deg, transparent 0%, rgba(201, 162, 39, 0.1) 50%, transparent 100%)"

# ============ SHADOWS ============
SHADOW_SM = "0 2px 8px rgba(0,0,0,0.3)"
SHADOW_MD = "0 4px 16px rgba(0,0,0,0.4)"
SHADOW_LG = "0 8px 32px rgba(0,0,0,0.5)"
SHADOW_GOLD = "0 4px 20px rgba(201, 162, 39, 0.2)"

# ============ BORDERS ============
BORDER_SUBTLE = f"1px solid {GRAY_800}"
BORDER_GOLD = f"1px solid {GOLD}"
BORDER_GOLD_SUBTLE = "1px solid rgba(201, 162, 39, 0.3)"


# ============ COMPONENT STYLES ============
def premium_card(*children, **props):
    """Premium glass-effect card"""
    default_style = {
        "background": CARD_BG,
        "border": BORDER_SUBTLE,
        "border_radius": "16px",
        "padding": "24px",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "position": "relative",
        "overflow": "hidden",
        "_hover": {
            "border_color": GOLD,
            "box_shadow": SHADOW_GOLD,
            "transform": "translateY(-2px)",
        },
    }
    return rx.box(
        *children, style={**default_style, **props.get("style", {})}, **{k: v for k, v in props.items() if k != "style"}
    )


def gold_button(text: str, icon: str | None = None, **props):
    """Primary gold action button"""
    children = []
    if icon:
        children.append(rx.icon(icon, size=18))
    children.append(rx.text(text, weight="bold"))

    return rx.button(
        rx.hstack(*children, spacing="2", align="center"),
        background=GOLD_GRADIENT,
        color=BLACK,
        padding="12px 24px",
        border_radius="12px",
        border="none",
        cursor="pointer",
        font_weight="bold",
        transition="all 0.2s ease",
        _hover={
            "transform": "scale(1.02)",
            "box_shadow": SHADOW_GOLD,
        },
        _active={
            "transform": "scale(0.98)",
        },
        **props,
    )


def ghost_button(text: str, icon: str | None = None, **props):
    """Secondary ghost button"""
    children = []
    if icon:
        children.append(rx.icon(icon, size=16, color=GRAY_500))
    children.append(rx.text(text, color=GRAY_300))

    return rx.button(
        rx.hstack(*children, spacing="2", align="center"),
        background="transparent",
        border=BORDER_SUBTLE,
        padding="10px 20px",
        border_radius="10px",
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background": GRAY_800,
            "border_color": GRAY_700,
        },
        **props,
    )


def danger_button(text: str, **props):
    """Danger/delete button"""
    return rx.button(
        rx.hstack(rx.icon("trash-2", size=16), rx.text(text), spacing="2", align="center"),
        background="transparent",
        color=RED,
        border=f"1px solid {RED}",
        padding="8px 16px",
        border_radius="8px",
        cursor="pointer",
        font_size="14px",
        transition="all 0.2s ease",
        _hover={
            "background": RED,
            "color": WHITE,
        },
        **props,
    )


def stat_card(title: str, value, icon: str, color: str = GOLD):
    """Dashboard stat card"""
    return premium_card(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(icon, size=24, color=color),
                    width="48px",
                    height="48px",
                    background="rgba(201, 162, 39, 0.1)",
                    border_radius="12px",
                    border="1px solid rgba(201, 162, 39, 0.2)",
                ),
                rx.spacer(),
                rx.text(title, color=GRAY_500, size="2", weight="medium"),
                width="100%",
                align="center",
            ),
            rx.heading(
                value,
                size="8",
                color=WHITE,
                weight="bold",
                style={"font_variant_numeric": "tabular-nums"},
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        style={"min_width": "200px"},
    )


def page_header(title: str, subtitle: str = "", action_button=None):
    """Page header with title and optional action"""
    return rx.hstack(
        rx.vstack(
            rx.heading(
                title,
                size="8",
                weight="bold",
                style={
                    "background": GOLD_GRADIENT,
                    "background_clip": "text",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                },
            ),
            rx.text(subtitle, color=GRAY_500, size="3") if subtitle else rx.fragment(),
            spacing="1",
            align="start",
        ),
        rx.spacer(),
        action_button if action_button else rx.fragment(),
        width="100%",
        align="center",
        margin_bottom="32px",
    )


def input_field(placeholder: str, icon: str | None = None, **props):
    """Styled input field"""
    return rx.input(
        placeholder=placeholder,
        background=GRAY_900,
        border=BORDER_SUBTLE,
        border_radius="10px",
        padding="12px 16px",
        color=WHITE,
        width="100%",
        _focus={
            "border_color": GOLD,
            "box_shadow": "0 0 0 2px rgba(201, 162, 39, 0.2)",
            "outline": "none",
        },
        _placeholder={"color": GRAY_500},
        **props,
    )


def select_field(placeholder: str, **props):
    """Styled select trigger"""
    return rx.select.root(
        rx.select.trigger(
            placeholder=placeholder,
            style={
                "background": GRAY_900,
                "border": BORDER_SUBTLE,
                "border_radius": "10px",
                "padding": "12px 16px",
                "color": WHITE,
                "width": "100%",
                "cursor": "pointer",
            },
        ),
        **props,
    )


def modal_container(title: str, children, is_open, on_close):
    """Styled modal dialog"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.heading(title, size="5", color=WHITE, weight="bold"),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=20),
                        variant="ghost",
                        color_scheme="gray",
                        on_click=on_close,
                        cursor="pointer",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.divider(color=GRAY_800, margin_y="16px"),
                children,
                spacing="4",
                width="100%",
            ),
            style={
                "background": CARD_BG,
                "border": BORDER_GOLD_SUBTLE,
                "border_radius": "20px",
                "padding": "24px",
                "max_width": "480px",
                "width": "100%",
                "box_shadow": SHADOW_LG,
            },
        ),
        open=is_open,
    )


def empty_state(icon: str, title: str, subtitle: str, action=None):
    """Empty state placeholder"""
    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(icon, size=48, color=GRAY_700),
                width="96px",
                height="96px",
                background=GRAY_900,
                border_radius="50%",
                border=BORDER_SUBTLE,
            ),
            rx.heading(title, size="5", color=GRAY_500, weight="medium"),
            rx.text(subtitle, color=GRAY_700, size="2", text_align="center"),
            action if action else rx.fragment(),
            spacing="4",
            align="center",
            padding="48px",
        ),
        width="100%",
    )


def toast_success(message: str):
    """Success toast notification"""
    return rx.box(
        rx.hstack(
            rx.icon("circle-check", size=20, color=GREEN),
            rx.text(message, color=WHITE, weight="medium"),
            spacing="3",
            align="center",
        ),
        background=GRAY_900,
        border=f"1px solid {GREEN}",
        border_radius="12px",
        padding="12px 20px",
        position="fixed",
        top="20px",
        right="20px",
        z_index="1000",
        box_shadow=SHADOW_MD,
    )


def toast_error(message: str):
    """Error toast notification"""
    return rx.box(
        rx.hstack(
            rx.icon("circle-alert", size=20, color=RED),
            rx.text(message, color=WHITE, weight="medium"),
            spacing="3",
            align="center",
        ),
        background=GRAY_900,
        border=f"1px solid {RED}",
        border_radius="12px",
        padding="12px 20px",
        position="fixed",
        top="20px",
        right="20px",
        z_index="1000",
        box_shadow=SHADOW_MD,
    )


def badge(text: str, color: str = GOLD):
    """Status badge"""
    return rx.box(
        rx.text(text, size="1", weight="bold", color=color),
        background="rgba(201, 162, 39, 0.1)",
        border=f"1px solid {color}",
        border_radius="6px",
        padding="4px 10px",
    )
