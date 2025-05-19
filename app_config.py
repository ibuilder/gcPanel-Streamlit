"""
Application configuration for gcPanel.

This module contains centralized application settings and configuration options.
The configuration is organized into logical sections to improve maintainability:

- Navigation: Menu options and mapping
- Session State: Default session values
- UI Configuration: Pages with action buttons, theme settings
- Project Information: Global project data

To extend the application, developers can modify the appropriate section
without affecting other parts of the configuration.
"""

import streamlit as st

# ============================================================================
# NAVIGATION CONFIGURATION
# ============================================================================

# All available modules with their display names (including icons)
MENU_OPTIONS = [
    "📊 Dashboard", 
    "📋 Project Information",
    "📅 Schedule",
    "⚠️ Safety",
    "📝 Contracts", 
    "💰 Cost Management",
    "📈 Analytics",
    "🔧 Engineering",
    "🚧 Field Operations",
    "📄 Documents",
    "🏢 BIM Viewer",
    "📱 Mobile Companion",
    "✅ Closeout",
    "🤖 AI Assistant",
    "✨ Features Showcase",
    "⚙️ Settings"
]

# Mapping from display names (with icons) to internal module names
MENU_MAP = {
    "📊 Dashboard": "Dashboard", 
    "📋 Project Information": "Project Information",
    "📅 Schedule": "Schedule",
    "⚠️ Safety": "Safety",
    "📝 Contracts": "Contracts", 
    "💰 Cost Management": "Cost Management",
    "📈 Analytics": "Analytics",
    "🔧 Engineering": "Engineering",
    "🚧 Field Operations": "Field Operations",
    "📄 Documents": "Documents",
    "🏢 BIM Viewer": "BIM",
    "📱 Mobile Companion": "Mobile Companion",
    "✅ Closeout": "Closeout",
    "🤖 AI Assistant": "AI Assistant",
    "✨ Features Showcase": "Features Showcase",
    "⚙️ Settings": "Settings"
}

# ============================================================================
# SESSION STATE CONFIGURATION
# ============================================================================

# Default values for session state variables
DEFAULT_SESSION_STATE = {
    "current_menu": "Dashboard",  # Default landing page
    "user": None,                 # User information when logged in
    "theme": "light",             # UI theme (light/dark)
    "show_notifications": False,  # Notification panel visibility
    "mobile_page": "dashboard"    # Current page in mobile view
}

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Pages that should display action buttons (Add/Edit/Delete)
# The value is the item type label used in the buttons
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

# ============================================================================
# PROJECT INFORMATION
# ============================================================================

# Global project information used throughout the application
PROJECT_INFO = {
    "name": "Highland Tower Development",
    "value": "$45.5M",
    "size": "168,500 sq ft",
    "floors": "15 stories above ground, 2 below",
    "units": "120 residential, 8 retail",
    "location": "Downtown Highland District",
    "client": "Highland Properties LLC",
    "start_date": "2025-01-15",
    "completion_date": "2027-06-30"
}