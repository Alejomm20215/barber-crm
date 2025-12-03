"""Barbershop CRM Frontend - Reflex App Configuration"""

import reflex as rx

# Configuration
config = rx.Config(
    app_name="barber_crm",
    # Backend configuration
    backend_host="127.0.0.1",
    backend_port=8001,
    # Frontend configuration  
    frontend_host="127.0.0.1",
    frontend_port=3000,
    # Disable sitemap plugin to avoid warnings
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
