"""Premium Design System for Barbershop CRM"""

import reflex as rx

# Color Palette
bg_dark = "#050505"  # Deep black
bg_sidebar = "#0a0a0a"
bg_card = "rgba(20, 20, 20, 0.7)"
accent_color = "#D4AF37"  # Classic Gold
accent_gradient = "linear-gradient(135deg, #D4AF37 0%, #F2D06B 100%)"
text_primary = "#FFFFFF"
text_secondary = "#A1A1AA"
border_color = "rgba(255, 255, 255, 0.1)"

# Glassmorphism
glass_style = {
    "background": bg_card,
    "backdrop_filter": "blur(10px)",
    "border": f"1px solid {border_color}",
    "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
}

# Layout Styles
sidebar_style = {
    **glass_style,
    "width": "280px",
    "height": "100vh",
    "padding": "24px",
    "position": "fixed",
    "left": "0",
    "top": "0",
    "z_index": "100",
    "display": "flex",
    "flex_direction": "column",
}

bg_gradient = f"linear-gradient(to bottom right, {bg_dark}, #1b1b1b)"

content_style = {
    "margin_left": "280px",
    "padding": "40px",
    "min_height": "100vh",
    "color": text_primary,
}

# Component Styles
card_style = {
    **glass_style,
    "border_radius": "16px",
    "padding": "24px",
    "transition": "all 0.3s ease",
    "_hover": {
        "transform": "translateY(-4px)",
        "box_shadow": f"0 12px 40px -10px {accent_color}20",
        "border_color": f"{accent_color}40",
    },
}

nav_link_style = {
    "color": text_secondary,
    "text_decoration": "none",
    "padding": "12px 16px",
    "border_radius": "12px",
    "width": "100%",
    "display": "flex",
    "align_items": "center",
    "gap": "12px",
    "transition": "all 0.2s ease",
    "font_weight": "500",
    "_hover": {
        "background": "rgba(255, 255, 255, 0.05)",
        "color": text_primary,
        "transform": "translateX(4px)",
    },
}

active_nav_link_style = {
    **nav_link_style,
    "background": f"linear-gradient(90deg, {accent_color}20 0%, transparent 100%)",
    "color": accent_color,
    "border_left": f"3px solid {accent_color}",
}

def premium_card(*children, **props):
    return rx.box(
        *children,
        **{**card_style, **props}
    )

def page_title(title: str, subtitle: str = ""):
    return rx.vstack(
        rx.heading(
            title, 
            size="8", 
            color=text_primary, 
            weight="bold",
            letter_spacing="-0.02em",
            style={
                "background": accent_gradient,
                "-webkit-background-clip": "text",
                "-webkit-text-fill-color": "transparent",
            }
        ),
        rx.text(subtitle, size="4", color=text_secondary),
        spacing="2",
        margin_bottom="8",
        align="start",
    )
