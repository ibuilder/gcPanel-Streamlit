"""
gcPanel Construction Management Dashboard

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.

The application includes production-ready features:
- Integration with external services
- Advanced analytics with visualization and prediction
- Mobile optimization with PWA support
- Real-time collaboration tools
- AI-powered features
- Improved spacing and UI consistency
- Document management for drawings, specs, and project files
- BIM model visualization and clash detection
- Comprehensive Field Operations tracking
"""

import streamlit as st
from utils.ui_manager import set_page_config
import app_manager

# Import feature showcase
from modules.features_showcase import render_features_showcase
from modules.mobile_field_companion import render_mobile_field_companion

# Import AI features 
# Modified to use modules directly instead of utility functions
from modules.ai_assistant import render_ai_assistant

# Import mobile optimization
from utils.mobile.responsive_layout import add_mobile_styles
from utils.mobile.pwa_support import setup_pwa

# Import improved container styling for better spacing
from assets.container_styles import apply_container_styles

def main():
    """Main application entry point."""
    # Set page configuration with favicon
    set_page_config()
    
    # Enable mobile optimizations and PWA support
    add_mobile_styles()
    setup_pwa()
    
    # Apply improved container styles to fix spacing issues
    apply_container_styles()
    
    # Initialize session state variables if needed
    if "current_menu" not in st.session_state:
        st.session_state["current_menu"] = "Dashboard"
    
    # Add a toggle for mobile field companion view
    is_mobile = False
    if "is_mobile_view" in st.session_state:
        is_mobile = st.session_state.is_mobile_view
    
    # Show appropriate view based on mode
    if is_mobile:
        render_mobile_field_companion()
    else:
        # Check if feature showcase is selected
        if st.session_state.get("current_menu") == "Features Showcase":
            render_features_showcase()
        else:
            # Get current menu selection
            current_menu = st.session_state.get("current_menu", "Dashboard")
            
            # Render the selected module
            app_manager.render_selected_module(current_menu)

if __name__ == "__main__":
    main()