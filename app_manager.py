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
from utils.cache_manager import CacheManager
from utils.responsive_ui import apply_all_responsive_styles, detect_mobile
from utils.search_manager import SearchManager

# Import enhanced core system
from core.app_core import app_core

# Import modules for standalone functionality
import modules.daily_reports
import modules.rfis
import modules.submittals
import modules.transmittals
import modules.meetings

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
from modules.collaboration import render_collaboration_hub  # Import the collaboration module function
from modules.bim_viewer.advanced_viewer import render_advanced_bim_viewer
from modules.bim import render_bim
from modules.standalone_bim import render_bim_standalone
from modules.field_operations import render as render_field_operations
from modules.scheduling import render_scheduling
from modules.safety import render as render_safety
from modules.cost_management import render as render_cost_management
from modules.closeout import render as render_closeout
from modules.engineering import render as render_engineering
from modules.documents import render as render_documents
from modules.mobile_companion import render_mobile_companion
from modules.analytics import render as render_analytics
from modules.ai_assistant import render_ai_assistant
from modules.integrations import render_integrations

# Import Admin module features
import modules.contracts
import modules.admin

# Import PreConstruction module
import modules.PreConstruction

def initialize_session_state():
    """
    Initialize enhanced session state with enterprise features.
    
    This function initializes:
    1. Default session state variables from app_config
    2. Enhanced notification system with real-time alerts
    3. Advanced caching and performance optimization
    4. Global search and filtering system
    5. Real-time collaboration features
    6. Audit logging and security monitoring
    """
    _initialize_default_state()
    _initialize_notifications()
    _initialize_cache_system()
    
    # Initialize enhanced core system
    app_core.initialize_application()
    
    # Initialize search system
    SearchManager.initialize()
    
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
    
    # Initialize notification toggle state if not already present
    if 'show_notifications' not in st.session_state:
        st.session_state.show_notifications = False
        
def _initialize_cache_system():
    """Initialize the application cache for improved performance."""
    # Use the cache manager to initialize the cache system
    CacheManager.initialize_cache()
    
    # Run cache cleanup on startup to ensure a clean state
    CacheManager.cleanup_cache(force=True)

def render_application():
    """
    Render the main application interface.
    
    This function orchestrates the application rendering process through several steps:
    1. Load external resources (CSS, JS)
    2. Initialize core services
    3. Render the application UI components
    """
    # Set up application environment and initialize services
    _setup_application_environment()
    
    # Render the UI framework (header, navigation, content area)
    _render_ui_framework()
    
def _setup_application_environment():
    """Set up the application environment and initialize core services."""
    # Load CSS and JavaScript files
    load_external_resources()
    
    # Apply responsive UI improvements
    apply_all_responsive_styles()
    
    # Initialize screen size tracking
    if "_screen_width" not in st.session_state:
        st.session_state._screen_width = 1200  # Default desktop width
    
    # Track if device is mobile
    st.session_state.is_mobile = detect_mobile()
    
    # Initialize database connection pool for production
    _setup_database_connection_pool()
    
    # Configure caching
    _configure_caching()

def _setup_database_connection_pool():
    """Initialize database connection pool for production use."""
    # This is a placeholder for the actual database connection pool setup
    # In a production environment, this would initialize connection pooling
    pass

def _configure_caching():
    """Configure caching for improved performance in production."""
    # This is a placeholder for caching configuration
    # In a production environment, this would set up caching policies
    pass

def _render_ui_framework():
    """Render the main UI framework including navigation, and content."""
    # Get current menu from session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # No need to render header here - it's now handled in app.py
    # This prevents duplicate headers
    
    # Apply aggressive div removal for dashboard and all modules
    st.markdown("""
    <style>
        /* ELIMINATE ALL unnecessary containers and divs throughout dashboard */
        .main .block-container {
            padding: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 !important;
            margin-top: 0 !important;
            max-width: 100% !important;
        }
        
        /* Bring header to absolute top */
        .stApp {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Target every possible container that creates top spacing */
        .stApp > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .stApp > div > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        section.main {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .main > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Proper content spacing */
        .streamlit-container {
            padding-top: 0 !important;
        }
        
        /* Target specific container classes that create extra divs */
        .css-1rs6os {display: none !important;}
        .css-17ziqus {display: none !important;}
        .css-12oz5g7 {display: none !important;}
        .css-1y4p8pa {display: none !important;}
        .css-91z34k {display: none !important;}
        .css-1wrcr25 {display: none !important;}
        .css-18e3th9 {display: none !important;}
        .css-k1vhr4 {display: none !important;}
        .css-1avcm0n {display: none !important;}
        
        /* Remove element containers and spacing BUT preserve charts */
        .element-container:not([data-testid*="chart"]) {
            margin: 0 !important; 
            padding: 0 !important;
            border: none !important;
        }
        
        div[data-testid="element-container"]:not([data-testid*="chart"]) {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Ensure charts and plotly graphs are visible */
        .js-plotly-plot, .plotly, [data-testid*="chart"] {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Preserve chart containers */
        div[data-testid*="metric"], 
        div[data-testid*="plotly"], 
        .stPlotlyChart,
        .stMetric {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Fix navigation dropdown positioning and dark theme styling */
        .stSelectbox {
            margin-top: 0 !important;
        }
        
        /* Dark theme for selectbox dropdown */
        .stSelectbox > div > div {
            background-color: rgba(30, 34, 42, 0.95) !important;
            color: #ffffff !important;
            border: 2px solid #667eea !important;
        }
        
        .stSelectbox > div > div > div {
            background-color: rgba(30, 34, 42, 0.95) !important;
            color: #ffffff !important;
        }
        
        /* Dropdown options styling */
        .stSelectbox [data-baseweb="select"] > div {
            background-color: rgba(30, 34, 42, 0.95) !important;
            color: #ffffff !important;
        }
        
        .stSelectbox [data-baseweb="popover"] {
            background-color: rgba(30, 34, 42, 0.98) !important;
        }
        
        .stSelectbox [role="option"] {
            background-color: rgba(30, 34, 42, 0.98) !important;
            color: #ffffff !important;
        }
        
        .stSelectbox [role="option"]:hover {
            background-color: rgba(102, 126, 234, 0.3) !important;
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Always render breadcrumbs for navigation context
    # Pass the menu directly instead of a list to avoid showing brackets
    simple_breadcrumbs(current_menu)
    
    # Handle notifications display
    _handle_notification_display()
    
    # Handle action buttons for specific pages
    _handle_action_buttons(current_menu)
    
    # Render the selected module
    render_selected_module(current_menu)

def _handle_notification_display():
    """Display notification center if toggled by user."""
    if st.session_state.get("show_notifications", False):
        notification_center()

def _handle_action_buttons(current_menu):
    """Handle rendering and processing of action buttons for specific pages."""
    if current_menu in PAGES_WITH_ACTIONS:
        render_action_bar(current_menu)



def render_selected_module(current_menu):
    """
    Render the module selected by the user.
    
    Uses a module mapping approach for cleaner code organization and easier maintenance.
    Special cases like BIM with multiple view options are handled separately.
    """
    # Special case for the standalone BIM viewer
    if current_menu == "BIM Standalone":
        render_bim_standalone()
        return
    
    # Special case for PDF viewer
    if current_menu == "PDF Viewer":
        render_pdf_viewer()
        return
    
    # BIM module with multiple view options
    if current_menu == "BIM":
        # Check for specific BIM view selection
        bim_view = st.session_state.get("bim_view", "default")
        
        if bim_view == "basic":
            render_basic_bim_viewer()
        elif bim_view == "advanced":
            render_advanced_bim_viewer()
        else:
            render_bim()
        return
    
    # Define a mapping of menu items to their rendering functions
    # This makes it easy to add new modules without modifying the if/elif chain
    module_mapping = {
        # Main Navigation
        "📊 Dashboard": render_dashboard,
        "Dashboard": render_dashboard,
        "📋 Project Information": render_project_information,
        "Project Information": render_project_information,
        "📅 Schedule": render_scheduling,
        "Schedule": render_scheduling,
        "🤝 Meeting Management": modules.meetings.render,
        "Meeting Management": modules.meetings.render,
        "⚠️ Safety": render_safety,
        "Safety": render_safety,
        "📝 Contracts": lambda: modules.contracts.render(),
        "Contracts": lambda: modules.contracts.render(),
        "💰 Cost Management": render_cost_management,
        "Cost Management": render_cost_management,
        "🏗️ PreConstruction": lambda: modules.PreConstruction.render(),
        "PreConstruction": lambda: modules.PreConstruction.render(),
        "📈 Analytics": render_analytics,
        "Analytics": render_analytics,
        "❓ RFIs": modules.rfis.render,
        "RFIs": modules.rfis.render,
        "📦 Submittals": modules.submittals.render,
        "Submittals": modules.submittals.render,
        "📤 Transmittals": modules.transmittals.render,
        "Transmittals": modules.transmittals.render,
        "📝 Daily Reports": modules.daily_reports.render,
        "Daily Reports": modules.daily_reports.render,
        "🚧 Field Operations": render_field_operations,
        "Field Operations": render_field_operations,
        "📄 Documents": render_documents,
        "Documents": render_documents,
        "🏢 BIM": render_bim,
        "BIM": render_bim,
        "✅ Closeout": render_closeout,
        "Closeout": render_closeout,
        "👥 Collaboration": render_collaboration_hub,
        "Collaboration": render_collaboration_hub,
        "📱 Mobile Companion": render_mobile_companion,
        "Mobile Companion": render_mobile_companion,
        "🤖 AI Assistant": render_ai_assistant,
        "AI Assistant": render_ai_assistant,
        "🔄 Integrations": render_integrations,
        "Integrations": render_integrations,
        "⚙️ Settings": render_settings,
        "Settings": render_settings,
        "👨‍💻 Admin": lambda: modules.admin.render(),
        "Admin": lambda: modules.admin.render()
    }
    
    # Enhanced module rendering with fallback handling
    module_rendered = False
    
    # First try direct mapping
    if current_menu in module_mapping:
        try:
            module_mapping[current_menu]()
            module_rendered = True
        except Exception as e:
            st.error(f"Error loading {current_menu}: {str(e)}")
    
    # If not found, try finding the display name from MENU_MAP
    if not module_rendered:
        from app_config import MENU_MAP, MENU_OPTIONS
        
        # Try to find matching display name
        for display_name in MENU_OPTIONS:
            if MENU_MAP.get(display_name) == current_menu and display_name in module_mapping:
                try:
                    module_mapping[display_name]()
                    module_rendered = True
                    break
                except Exception as e:
                    st.error(f"Error loading {display_name}: {str(e)}")
    
    # Final fallback
    if not module_rendered:
        st.warning(f"Module '{current_menu}' not available")
        st.info("Please select a module from the navigation dropdown above")