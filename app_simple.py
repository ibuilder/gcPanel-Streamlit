"""
Highland Tower Development - Simplified Sidebar Layout

Clean, stable version using Streamlit's default sidebar components.
"""

import streamlit as st
from login_form import render_login_form
from app_sidebar import render_sidebar, apply_sidebar_theme
import modules

def initialize_session_state():
    """Initialize session state with default values."""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "guest",
        "current_menu": "Dashboard",
        "current_project": "Highland Tower Development",
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_main_content():
    """Render the main content area based on selected module."""
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Module mapping
    module_mapping = {
        "Dashboard": modules.dashboard.render_dashboard,
        "Preconstruction": modules.preconstruction.render,
        "Engineering": modules.engineering.render_engineering,
        "Field Operations": modules.field_operations.render,
        "Safety": modules.safety.render,
        "Contracts": modules.contracts.render,
        "Cost Management": modules.cost_management.render,
        "BIM": modules.bim.render,
        "Closeout": modules.closeout.render,
        "Analytics": modules.analytics.render_analytics_dashboard,
        "Documents": modules.documents.render
    }
    
    # Render selected module
    if current_menu in module_mapping:
        try:
            module_mapping[current_menu]()
        except Exception as e:
            st.error(f"Error loading {current_menu} module: {str(e)}")
            st.info("Please try refreshing the page or selecting a different module.")
    else:
        st.error(f"Module '{current_menu}' not found.")

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply theme
    apply_sidebar_theme()
    
    # Check authentication
    if not st.session_state.get("authenticated", False):
        render_login_form()
        return
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render main content
    render_main_content()

if __name__ == "__main__":
    main()