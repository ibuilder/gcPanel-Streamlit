"""
gcPanel Construction Management Dashboard

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.
"""

import streamlit as st
from utils.ui_manager import set_page_config
import app_manager

def main():
    """Main application entry point."""
    # Set page configuration with favicon
    set_page_config()
    
    # Initialize session state variables
    app_manager.initialize_session_state()
    
    # Render the main application
    app_manager.render_application()

if __name__ == "__main__":
    main()