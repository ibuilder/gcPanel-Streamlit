"""
Application Manager for gcPanel.

This module manages application initialization, session state, 
and module rendering.
"""

import streamlit as st
from datetime import datetime

# Import app configuration
from app_config import MENU_MAP, DEFAULT_SESSION_STATE, PAGES_WITH_ACTIONS

# Import utility functions
from utils.ui_manager import load_external_resources, render_notification_button

# Import components
from components.action_bar import render_action_bar
from components.simple_breadcrumbs import simple_breadcrumbs, get_breadcrumbs_for_page
from components.header_clean import render_header
from components.notification_center import notification_center

# Import modules
from modules.dashboard import render_dashboard
from modules.settings import render_settings
from modules.project_information import render_project_information
from modules.pdf_viewer.pdf_viewer import render_pdf_viewer
from modules.bim_viewer.basic_viewer import render_basic_bim_viewer
from modules.bim_viewer.advanced_viewer import render_advanced_bim_viewer
from modules.field_operations import render_field_operations
from modules.scheduling import render_scheduling
from modules.safety import render_safety
from modules.contracts import render_contracts
from modules.cost_management import render_cost_management
from modules.closeout import render_closeout
from modules.engineering import render_engineering
from modules.documents import render_documents
from modules.mobile_companion import render_mobile_companion
from modules.analytics import render_analytics
from modules.ai_assistant import render_ai_assistant

# Import feature showcase module
try:
    from modules.features_showcase import render_features_showcase
except ImportError:
    # Define fallback function if module is not found
    def render_features_showcase():
        import streamlit as st
        st.warning("Features showcase module is currently unavailable.")

def initialize_session_state():
    """Initialize session state variables."""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
    # Initialize notifications if not present
    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {
                "id": 1,
                "title": "RFI #123 Response Received",
                "text": "The architect has responded to RFI #123 regarding foundation details.",
                "time": "2 hours ago",
                "read": False,
                "type": "info"
            },
            {
                "id": 2,
                "title": "Change Order #45 Approved",
                "text": "Change order #45 for additional excavation has been approved.",
                "time": "Yesterday",
                "read": True,
                "type": "success"
            },
            {
                "id": 3,
                "title": "Safety Inspection Required",
                "text": "Monthly safety inspection is due by end of week.",
                "time": "2 days ago",
                "read": False,
                "type": "warning"
            }
        ]
    
def render_application():
    """Render the main application interface."""
    # Load external resources
    load_external_resources()
    
    # Initialize core services if they exist
    try:
        from core import initialize_application
        initialize_application()
    except ImportError:
        # Create a placeholder directory if it doesn't exist
        import os
        if not os.path.exists('core'):
            os.makedirs('core', exist_ok=True)
    
    # Render the header with right-aligned navigation
    render_header()
    
    # Main content area
    with st.container():
        # Get current menu selection
        current_menu = st.session_state.get("current_menu", "Dashboard")
        
        # Get breadcrumbs for current page
        breadcrumb_items = get_breadcrumbs_for_page(current_menu)
        
        # CSS is now loaded from external file (breadcrumbs.css)
        
        # Only initialize notification center if needed - we'll handle breadcrumbs elsewhere
        if st.session_state.get("show_notification_center", False):
            notification_center()
        
        # Add action buttons for pages that need them
        if current_menu in PAGES_WITH_ACTIONS:
            page_type = PAGES_WITH_ACTIONS[current_menu]
            action_result = render_action_bar(page_type=page_type)
            
            # Store action results in session state if needed
            if action_result["add_clicked"] or action_result["edit_clicked"]:
                st.session_state[f"{current_menu.lower().replace(' ', '_')}_action"] = action_result
                st.rerun()
        
        # Render the selected module
        render_selected_module(current_menu)

def render_selected_module(current_menu):
    """Render the module selected by the user."""
    if current_menu == "Dashboard":
        render_dashboard()
    elif current_menu == "Project Information":
        render_project_information()
    elif current_menu == "Schedule":
        render_scheduling()
    elif current_menu == "Safety":
        render_safety()
    elif current_menu == "Contracts":
        render_contracts()
    elif current_menu == "Cost Management":
        render_cost_management()
    elif current_menu == "Analytics":
        render_analytics()
    elif current_menu == "Engineering":
        render_engineering()
    elif current_menu == "Field Operations":
        render_field_operations()
    elif current_menu == "Documents":
        render_documents()
    elif current_menu == "AI Assistant":
        render_ai_assistant()
    elif current_menu == "Features Showcase":
        render_features_showcase()
    elif current_menu == "BIM":
        # Provide toggle between basic and advanced viewers
        viewer_type = st.radio(
            "Select BIM Viewer Type", 
            ["Basic Floor Stacks", "Advanced 3D Viewer"],
            horizontal=True
        )
        
        if viewer_type == "Basic Floor Stacks":
            render_basic_bim_viewer()
        else:
            render_advanced_bim_viewer()
    elif current_menu == "Mobile Companion":
        render_mobile_companion()
    elif current_menu == "Closeout":
        render_closeout()
    elif current_menu == "Features Showcase":
        # Import and render the features showcase
        from modules.features_showcase import render_features_showcase
        render_features_showcase()
    elif current_menu == "Settings":
        render_settings()