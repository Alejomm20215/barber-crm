"""Barbershop CRM Frontend - Reflex App Configuration"""

import reflex as rx
import os

# Check if running in Docker
IN_DOCKER = os.environ.get("IN_DOCKER", "false").lower() == "true"

# Configuration
config = rx.Config(
    app_name="barber_crm",
    # Backend configuration - use 0.0.0.0 to accept connections from outside container
    backend_host="0.0.0.0",
    backend_port=8001,
    # Frontend configuration - use 0.0.0.0 for Docker
    frontend_host="0.0.0.0",
    frontend_port=3000,
    # Disable sitemap plugin to avoid warnings
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
