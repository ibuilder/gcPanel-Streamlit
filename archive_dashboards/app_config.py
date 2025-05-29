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
    "🤝 Meeting Management",
    "⚠️ Safety",
    "📝 Contracts", 
    "💰 Cost Management",
    "🏗️ PreConstruction",
    "🏢 BIM Collaboration",
    "📈 Analytics",
    "❓ RFIs",
    "📦 Submittals",
    "📤 Transmittals",
    "📝 Daily Reports",
    "🚧 Field Operations",
    "📄 Documents",
    "🏗️ Subcontractor Management",
    "📸 Progress Photos",
    "🔍 Inspections",
    "⚠️ Issues & Risks",
    "📊 Performance Snapshot",
    "💼 Companies Database",
    "✅ Prequalifications",
    "📋 Budget Management",
    "📑 Schedule of Values",
    "📄 File Explorer",
    "📈 Reports Generation",
    "👥 User Profiles",
    "🔧 General Conditions",
    "🏷️ Cost Codes",
    "✅ Closeout",
    "👥 Collaboration",
    "🤖 AI Assistant",
    "📱 Mobile Companion",
    "🔄 Integrations",
    "⚙️ Settings",
    "👨‍💻 Admin"
]

# Mapping from display names (with icons) to internal module names
MENU_MAP = {
    "📊 Dashboard": "Dashboard", 
    "📋 Project Information": "Project Information",
    "📅 Schedule": "Schedule",
    "🤝 Meeting Management": "meetings",
    "⚠️ Safety": "Safety",
    "📝 Contracts": "Contracts", 
    "💰 Cost Management": "Cost Management",
    "🏗️ PreConstruction": "PreConstruction",
    "🏢 BIM Collaboration": "BIM",
    "📈 Analytics": "Analytics",
    "❓ RFIs": "RFIs",
    "📦 Submittals": "Submittals",
    "📤 Transmittals": "Transmittals",
    "📝 Daily Reports": "Daily Reports",
    "🚧 Field Operations": "Field Operations",
    "📄 Documents": "Documents",
    "🏗️ Subcontractor Management": "Subcontractor Management",
    "📸 Progress Photos": "Progress Photos",
    "🔍 Inspections": "Inspections",
    "⚠️ Issues & Risks": "Issues & Risks",
    "📊 Performance Snapshot": "Performance Snapshot",
    "💼 Companies Database": "Companies Database",
    "✅ Prequalifications": "Prequalifications",
    "📋 Budget Management": "Budget Management",
    "📑 Schedule of Values": "Schedule of Values",
    "📄 File Explorer": "File Explorer",
    "📈 Reports Generation": "Reports Generation",
    "👥 User Profiles": "User Profiles",
    "🔧 General Conditions": "General Conditions",
    "🏷️ Cost Codes": "Cost Codes",
    "✅ Closeout": "Closeout",
    "👥 Collaboration": "Collaboration",
    "🤖 AI Assistant": "AI Assistant",
    "📱 Mobile Companion": "Mobile Companion",
    "🔄 Integrations": "Integrations",
    "⚙️ Settings": "Settings",
    "👨‍💻 Admin": "Admin"
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

# ============================================================================
# COMPANY INFORMATION
# ============================================================================

# Project companies information
PROJECT_COMPANIES = [
    {
        "id": "comp_001",
        "name": "Highland Properties LLC",
        "role": "Owner/Developer",
        "contact_name": "Jessica Taylor",
        "contact_email": "jtaylor@highlandproperties.com",
        "contact_phone": "555-123-4567",
        "address": "100 Main Street, Highland, CA 92346"
    },
    {
        "id": "comp_002",
        "name": "GC Prime Contractors",
        "role": "General Contractor",
        "contact_name": "John Smith",
        "contact_email": "jsmith@gcprime.com",
        "contact_phone": "555-987-6543",
        "address": "200 Construction Way, Highland, CA 92346"
    },
    {
        "id": "comp_003",
        "name": "Design Partners",
        "role": "Architecture",
        "contact_name": "Sarah Johnson",
        "contact_email": "sjohnson@designpartners.com",
        "contact_phone": "555-456-7890",
        "address": "300 Design Boulevard, Highland, CA 92346"
    },
    {
        "id": "comp_004",
        "name": "Structure Solutions",
        "role": "Structural Engineering",
        "contact_name": "Michael Chen",
        "contact_email": "mchen@structuresolutions.com",
        "contact_phone": "555-789-0123",
        "address": "400 Engineering Lane, Highland, CA 92346"
    },
    {
        "id": "comp_005",
        "name": "Power Systems Inc.",
        "role": "Electrical Contractor",
        "contact_name": "Robert Williams",
        "contact_email": "rwilliams@powersystems.com",
        "contact_phone": "555-234-5678",
        "address": "500 Energy Street, Highland, CA 92346"
    }
]