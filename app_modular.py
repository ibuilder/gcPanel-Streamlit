"""
gcPanel Construction Management Dashboard (Modular Version)

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.

This modular version uses the new module loader system for better code
organization and independent module development.
"""

import streamlit as st
import os
from utils.ui_manager import set_page_config

# Import improved container styling for better spacing
from assets.container_styles import apply_container_styles

# Import header fixes to remove white box 
from assets.header_fix import apply_header_fixes

# Import mobile optimization
from utils.mobile.responsive_layout import add_mobile_styles
from utils.mobile.pwa_support import setup_pwa

# Import from shared state manager
from utils.shared_state import initialize_base_session_state

# Import module loader
from modules.module_loader import (
    get_all_modules,
    get_modules_by_category,
    render_module,
    get_module_metadata,
    get_modules_requiring_action_buttons
)

# Import components
from components.header_modular import render_header
from components.action_bar import render_action_bar
from components.notification_center import notification_center

def _initialize_notifications():
    """Initialize the notification system state if not already present."""
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

def _setup_application_environment():
    """Set up the application environment and initialize core services."""
    # Load external resources (CSS, JS)
    _load_external_resources()
    
    # Initialize core services if they exist
    try:
        from core import initialize_application
        initialize_application()
    except ImportError:
        # Create a placeholder directory if it doesn't exist
        if not os.path.exists('core'):
            os.makedirs('core', exist_ok=True)

def _load_external_resources():
    """Load external resources like CSS and JavaScript files."""
    # Add Material Icons for better UI elements
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
    
    # Add custom CSS for styling improvements
    st.markdown(
        """
        <style>
        /* Base font and spacing improvements */
        * {font-family: 'Inter', sans-serif;}
        
        /* Improve container spacing */
        .main .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        
        /* Improve header and navigation */
        header {visibility: hidden; height: 0px;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

def _handle_notification_display():
    """Display notification center if toggled by user."""
    if st.session_state.get("show_notification_center", False):
        notification_center()

def _handle_action_buttons(current_module):
    """Handle rendering and processing of action buttons for specific pages."""
    # Get modules that require action buttons
    modules_with_actions = get_modules_requiring_action_buttons()
    
    if current_module in modules_with_actions:
        # Get module metadata for page type information
        metadata = get_module_metadata(current_module)
        page_type = metadata.get("page_type", current_module.replace("_", " ").title())
        
        action_result = render_action_bar(page_type=page_type)
        
        # Store action results in session state if needed
        if action_result["add_clicked"] or action_result["edit_clicked"]:
            st.session_state[f"{current_module.lower()}_action"] = action_result
            st.rerun()

def render_application():
    """
    Render the main application interface.
    
    This function orchestrates the application rendering process through several steps:
    1. Load external resources (CSS, JS)
    2. Initialize core services
    3. Render the application UI components
    """
    # Setup application environment
    _setup_application_environment()
    
    # Render UI components
    _render_ui_framework()

def _render_ui_framework():
    """Render the main UI framework including header, navigation, and content."""
    # Get all registered modules
    modules = get_all_modules()
    
    # Get current module selection
    current_module = st.session_state.get("current_module", "dashboard")
    
    # Render the application header with navigation
    render_header(modules, current_module)
    
    # Main content area
    with st.container():
        # Handle notification center
        _handle_notification_display()
        
        # Handle action buttons for appropriate modules
        _handle_action_buttons(current_module)
        
        # Render the selected module's content
        render_module(current_module)

def initialize_session_state():
    """
    Initialize session state variables from config and set up required app state.
    
    This function initializes:
    1. Default session state variables
    2. Notification system state
    3. Any other required application state variables
    """
    # Initialize shared base session state
    initialize_base_session_state()
    
    # Initialize notification system
    _initialize_notifications()

def main():
    """Main application entry point."""
    # Set page configuration with favicon
    set_page_config()
    
    # Enable mobile optimizations and PWA support
    add_mobile_styles()
    setup_pwa()
    
    # Apply improved container styles to fix spacing issues
    apply_container_styles()
    
    # Apply header fixes to remove white box at the top
    apply_header_fixes()
    
    # Initialize session state variables
    initialize_session_state()
    
    # Add a toggle for mobile field companion view
    is_mobile = False
    if "is_mobile_view" in st.session_state:
        is_mobile = st.session_state.is_mobile_view
    
    # Show appropriate view based on mode
    if is_mobile:
        # Render mobile view if available
        from modules.mobile_field_companion import render_mobile_field_companion
        render_mobile_field_companion()
    else:
        # Render the entire application with the app manager
        render_application()

if __name__ == "__main__":
    main()