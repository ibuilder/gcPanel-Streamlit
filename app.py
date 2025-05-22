"""
gcPanel Construction Management Dashboard (Production Version)

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.

The application includes production-ready features:
- Integration with external services
- Advanced analytics with visualization and prediction
- Mobile optimization with PWA support
- Real-time collaboration tools
- AI-powered features with Natural Language Processing
- Professional, enterprise-grade UI design system
- Document management for drawings, specs, and project files
- BIM model visualization and clash detection
- Comprehensive Field Operations tracking
- Performance optimizations for production deployment
- Production-ready error handling and logging
- Database connection pooling and query optimization
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

# Import header fixes to remove white box 
from assets.header_fix import apply_header_fixes

# Import enhanced UI components for professional styling
from assets.enhanced_ui import apply_enhanced_styles, create_project_header

def main():
    """Main application entry point."""
    try:
        # Set page configuration with favicon (PWA support is now integrated in set_page_config)
        set_page_config()
        
        # Enable mobile optimizations
        add_mobile_styles()
        
        # Apply enhanced UI styles for professional, enterprise-grade appearance
        apply_enhanced_styles()
        
        # Header is now managed by the app_manager.render_application() function
        # Removed duplicate header creation
        
        # Initialize session state variables from app_manager
        app_manager.initialize_session_state()
        
        # Add a toggle for mobile field companion view
        is_mobile = False
        if "is_mobile_view" in st.session_state:
            is_mobile = st.session_state.is_mobile_view
        
        # Show appropriate view based on mode
        if is_mobile:
            render_mobile_field_companion()
        else:
            # Render the entire application with the app manager
            app_manager.render_application()
            
    except Exception as e:
        # Production error handling
        import traceback
        import logging
        
        # Configure logging
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app_errors.log"),
                logging.StreamHandler()
            ]
        )
        
        # Log the error
        error_details = traceback.format_exc()
        logging.error(f"Application error: {str(e)}\n{error_details}")
        
        # Show user-friendly error page
        st.error("We encountered an unexpected error. Our team has been notified.")
        
        # Only show detailed error in development, not production
        if st.session_state.get('show_debug', False):
            with st.expander("Error Details (Developers Only)"):
                st.code(error_details)

if __name__ == "__main__":
    main()