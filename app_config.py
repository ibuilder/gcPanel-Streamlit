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
    "🏗️ PreConstruction",
    "📈 Analytics",
    "🔧 Engineering",
    "🚧 Field Operations",
    "📄 Documents",
    "🏢 BIM",
    "✅ Closeout",
    "👥 Collaboration",  # New collaboration module
    "🤖 AI Assistant",
    "📱 Mobile Companion",
    "🔄 Integrations",
    "⚙️ Settings",
    "👨‍💻 Admin"  # Admin section at the end
]

# Mapping from display names (with icons) to internal module names
MENU_MAP = {
    "📊 Dashboard": "Dashboard", 
    "📋 Project Information": "Project Information",
    "📅 Schedule": "Schedule",
    "⚠️ Safety": "Safety",
    "📝 Contracts": "Contracts", 
    "💰 Cost Management": "Cost Management",
    "🏗️ PreConstruction": "PreConstruction",
    "📈 Analytics": "Analytics",
    "🔧 Engineering": "Engineering",
    "🚧 Field Operations": "Field Operations",
    "📄 Documents": "Documents",
    "🏢 BIM": "BIM",
    "✅ Closeout": "Closeout",
    "👥 Collaboration": "Collaboration",
    "🤖 AI Assistant": "AI Assistant",
    "📱 Mobile Companion": "Mobile Companion",
    "🔄 Integrations": "Integrations",
    "⚙️ Settings": "Settings",
    "👨‍💻 Admin": "Admin"  # Admin section
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
# We're removing all action buttons since they've been replaced with the CRUD functionality
PAGES_WITH_ACTIONS = {}

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