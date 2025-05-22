"""
Application Manager for gcPanel.

This module manages application initialization, session state, 
and module rendering.
"""

import streamlit as st
from datetime import datetime
import importlib
import os

# Import app configuration
from app_config import MENU_MAP, DEFAULT_SESSION_STATE, PAGES_WITH_ACTIONS

# Import utility functions
from utils.ui_manager import load_external_resources, render_notification_button

# Import components
from components.action_bar import render_action_bar
from components.simple_breadcrumbs import simple_breadcrumbs, get_breadcrumbs_for_page
from components.header_clean import render_header
from components.notification_center import notification_center

# Import modules directly
from modules.dashboard import render_dashboard
from modules.settings import render_settings
from modules.project_information import render_project_information
from modules.pdf_viewer.pdf_viewer import render_pdf_viewer
from modules.bim_viewer.basic_viewer import render_basic_bim_viewer
from modules.bim_viewer.advanced_viewer import render_advanced_bim_viewer
from modules.bim import render_bim
from modules.standalone_bim import render_bim_standalone
from modules.field_operations import render as render_field_operations
from modules.scheduling import render_scheduling
from modules.safety import render as render_safety
from modules.cost_management import render as render_cost_management
from modules.closeout import render as render_closeout
from modules.engineering import render as render_engineering
from modules.documents import render_documents
from modules.mobile_companion import render_mobile_companion
from modules.analytics import render as render_analytics
from modules.ai_assistant import render_ai_assistant
from modules.integrations import render_integrations
from modules.preconstruction import render as render_preconstruction

# Import Admin module features
import modules.contracts
import modules.admin

def initialize_session_state():
    """
    Initialize session state variables from config and set up required app state.
    
    This function initializes:
    1. Default session state variables from app_config
    2. Notification system state
    3. Any other required application state variables
    """
    _initialize_default_state()
    _initialize_notifications()
    
def _initialize_default_state():
    """Initialize the basic session state variables from configuration."""
    # Iterate through the default session state and initialize any missing values
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

def _initialize_notifications():
    """Initialize the notification system state if not already present."""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    if 'show_notifications' not in st.session_state:
        st.session_state.show_notifications = False
    
    if 'unread_count' not in st.session_state:
        st.session_state.unread_count = 0

# Import CRUD demo and newly added CRUD modules
import modules.crud_demo
import modules.field_issues
import modules.equipment

def initialize_session_state():
    """
    Initialize session state variables from config and set up required app state.
    
    This function initializes:
    1. Default session state variables from app_config
    2. Notification system state
    3. Any other required application state variables
    """
    # Initialize default session state from configuration
    _initialize_default_state()
    
    # Initialize notification system
    _initialize_notifications()
    
def _initialize_default_state():
    """Initialize the basic session state variables from configuration."""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

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

def _setup_application_environment():
    """Set up the application environment and initialize core services."""
    # Load external resources (CSS, JS)
    load_external_resources()
    
    # Initialize database connection pool if in production
    _setup_database_connection_pool()
    
    # Set up caching for performance in production
    _configure_caching()
    
    # Initialize core services if they exist
    try:
        from core import initialize_application
        initialize_application()
    except ImportError:
        # Create a placeholder directory if it doesn't exist
        if not os.path.exists('core'):
            os.makedirs('core', exist_ok=True)
            
def _setup_database_connection_pool():
    """Initialize database connection pool for production use."""
    if 'db_pool' not in st.session_state:
        try:
            import os
            from sqlalchemy import create_engine, text
            from sqlalchemy.pool import QueuePool
            
            # Check if we have a database connection string
            database_url = os.environ.get('DATABASE_URL')
            if database_url and not database_url.startswith('https://'):
                # Create connection pool with appropriate settings for production
                engine = create_engine(
                    database_url,
                    poolclass=QueuePool,
                    pool_size=10,
                    max_overflow=20,
                    pool_timeout=30,
                    pool_recycle=1800  # Recycle connections after 30 minutes
                )
                
                # Store in session state for reuse
                st.session_state.db_pool = engine
                
                # Test connection with proper SQLAlchemy 2.0 syntax
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
        except Exception as e:
            import logging
            logging.error(f"Database connection pool initialization error: {str(e)}")
            # Don't fail if DB connection fails - app can still function with files

def _configure_caching():
    """Configure caching for improved performance in production."""
    # Set up cache TTL for various function types
    try:
        # For data-loading functions, cache for a moderate time
        st.cache_data.clear()
        
        # For resource functions, cache longer
        st.cache_resource.clear()
        
        # Configure global cache settings if needed
        # This code can be extended to set more specific cache policies
    except Exception as e:
        import logging
        logging.error(f"Cache configuration error: {str(e)}")

def _render_ui_framework():
    """Render the main UI framework including navigation and content."""
    # Main content area
    with st.container():
        # Get current menu selection
        current_menu = st.session_state.get("current_menu", "Dashboard")
        
        # Handle notification center
        _handle_notification_display()
        
        # Handle action buttons for appropriate pages
        _handle_action_buttons(current_menu)
        
        # Render the selected module's content
        render_selected_module(current_menu)

def _handle_notification_display():
    """Display notification center if toggled by user."""
    if st.session_state.get("show_notification_center", False):
        notification_center()

def _handle_action_buttons(current_menu):
    """Handle rendering and processing of action buttons for specific pages."""
    if current_menu in PAGES_WITH_ACTIONS:
        page_type = PAGES_WITH_ACTIONS[current_menu]
        action_result = render_action_bar(page_type=page_type)
        
        # Store action results in session state if needed
        if action_result["add_clicked"] or action_result["edit_clicked"]:
            st.session_state[f"{current_menu.lower().replace(' ', '_')}_action"] = action_result
            st.rerun()

def render_selected_module(current_menu):
    """
    Render the module selected by the user.
    
    Uses a module mapping approach for cleaner code organization and easier maintenance.
    Special cases like BIM with multiple view options are handled separately.
    """
    # Define a mapping of menu items to their rendering functions
    # This makes it easy to add new modules without modifying the if/elif chain
    module_mapping = {
        # Main Navigation
        "Dashboard": render_dashboard,
        "Project Information": render_project_information,
        "Schedule": render_scheduling,
        "Safety": render_safety,
        "Contracts": lambda: modules.contracts.render(),
        "Cost Management": render_cost_management,
        "Pre-Construction": lambda: modules.preconstruction.render(),
        "Analytics": render_analytics,
        "Engineering": render_engineering,
        "Field Operations": render_field_operations,
        "Documents": render_documents,
        "BIM": render_bim,
        "Closeout": render_closeout,
        "Mobile Companion": render_mobile_companion,
        "AI Assistant": render_ai_assistant,
        "Integrations": render_integrations,
        "Settings": render_settings,
        
        # Admin Section (hidden from main navigation)
        "Admin": lambda: modules.admin.render(),
        
        # Legacy modules that will be removed or redirected
        "Equipment": lambda: modules.equipment.render()
    }
    
    # Handle special case for BIM with multiple view options
    if current_menu == "BIM":
        viewer_type = st.radio(
            "Select BIM Viewer Type", 
            ["Enhanced 3D Model Viewer", "Basic Floor Stacks", "Advanced 3D Viewer"],
            horizontal=True,
            index=0
        )
        
        # Check which option was selected and render appropriate viewer
        if viewer_type == "Enhanced 3D Model Viewer":
            try:
                render_bim()
            except Exception as e:
                st.error(f"Error loading BIM viewer: {str(e)}")
                st.info("Try selecting a different viewer type above.")
        elif viewer_type == "Basic Floor Stacks":
            try:
                render_basic_bim_viewer()
            except Exception as e:
                st.error(f"Error loading basic BIM viewer: {str(e)}")
                st.info("Try selecting a different viewer type above.")
        else:
            try:
                render_advanced_bim_viewer()
            except Exception as e:
                st.error(f"Error loading advanced BIM viewer: {str(e)}")
                st.info("Try selecting a different viewer type above.")
    # Handle our new standalone BIM viewer
    elif current_menu == "StandaloneBIM":
        try:
            render_bim_standalone()
        except Exception as e:
            st.error(f"Error loading standalone BIM viewer: {str(e)}")
            st.info("The standalone BIM viewer may require additional setup.")
    # For regular modules, use the mapping to find and call the appropriate function
    elif current_menu in module_mapping:
        module_mapping[current_menu]()
    else:
        st.error(f"Module '{current_menu}' not found. Please select a valid module.")