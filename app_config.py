"""
Application configuration for gcPanel.

This module contains centralized application settings and configuration options.
"""

import streamlit as st

# Menu options for the application
MENU_OPTIONS = [
    "📊 Dashboard", 
    "📋 Project Information",
    "📅 Schedule",
    "⚠️ Safety",
    "📝 Contracts", 
    "💰 Cost Management",
    "🔧 Engineering",
    "🚧 Field Operations",
    "📄 Documents",
    "🏢 BIM Viewer",
    "📱 Mobile Companion",
    "✅ Closeout",
    "⚙️ Settings"
]

# Mapping from display names to internal names
MENU_MAP = {
    "📊 Dashboard": "Dashboard", 
    "📋 Project Information": "Project Information",
    "📅 Schedule": "Schedule",
    "⚠️ Safety": "Safety",
    "📝 Contracts": "Contracts", 
    "💰 Cost Management": "Cost Management",
    "🔧 Engineering": "Engineering",
    "🚧 Field Operations": "Field Operations",
    "📄 Documents": "Documents",
    "🏢 BIM Viewer": "BIM",
    "📱 Mobile Companion": "Mobile Companion",
    "✅ Closeout": "Closeout",
    "⚙️ Settings": "Settings"
}

# Default session state values
DEFAULT_SESSION_STATE = {
    "current_menu": "Dashboard",
    "user": None,
    "theme": "light",
    "show_notifications": False,
    "mobile_page": "dashboard"
}

# Pages that should have Add/Edit buttons
PAGES_WITH_ACTIONS = {
    "Project Information": "Information", 
    "Schedule": "Schedule Item",
    "Safety": "Safety Item",
    "Contracts": "Contract", 
    "Cost Management": "Cost Item",
    "Engineering": "Drawing",
    "Field Operations": "Field Item",
    "Documents": "Document",
    "Mobile Companion": "Feature",
    "Closeout": "Closeout Item"
}