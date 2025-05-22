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

# Import new fixed header component that positions correctly
from components.fixed_header import render_fixed_header

# Import enhanced UI components for professional styling
from assets.enhanced_ui import apply_enhanced_styles

def main():
    """Main application entry point."""
    try:
        # Set page configuration with favicon (PWA support is now integrated in set_page_config)
        set_page_config()
        
        # Enable mobile optimizations
        add_mobile_styles()
        
        # Apply enhanced UI styles for professional, enterprise-grade appearance
        apply_enhanced_styles()
        
        # Remove sidebar completely from the entire application
        st.markdown("""
        <style>
        /* Completely hide all sidebar elements and controls from all pages */
        [data-testid="stSidebar"] {display: none !important;}
        .st-emotion-cache-1c7y2kd {display: none !important;}
        button[kind="headerNoPadding"] {display: none !important;}
        section[data-testid="stSidebarContent"] {display: none !important;}
        .st-emotion-cache-z5fcl4 {display: none !important;}
        section[data-testid="stSidebarUserContent"] {display: none !important;}
        .st-emotion-cache-10oheav {visibility: hidden !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        #Sidebar {display: none !important;}
        nav[data-testid="stSidebar"] {display: none !important;}
        nav.st-emotion-cache-zq5wmm.ezrtsby0 {display: none !important;}
        /* Hide more aggressively with additional selectors */
        .css-1d391kg {display: none !important;}
        .st-hy {display: none !important;}
        .st-emotion-cache-ue6h4q {display: none !important;}
        </style>
        """, unsafe_allow_html=True)
        
        # Initialize session state variables from app_manager
        app_manager.initialize_session_state()
        
        # Check authentication
        is_authenticated = False
        if "authenticated" in st.session_state:
            is_authenticated = st.session_state.authenticated
        
        # Handle the admin and demo login credentials for quick testing
        if "login_form_submitted" in st.session_state and st.session_state.login_form_submitted:
            username = st.session_state.get("login_username", "")
            password = st.session_state.get("login_password", "")
            
            # Reset the form submission flag
            st.session_state.login_form_submitted = False
            
            # Check user credentials for various roles
            # Admin - Full system access
            if username.lower() == "admin" and password == "admin123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "admin",
                    "email": "admin@gcpanel.com",
                    "full_name": "Admin User",
                    "role": "admin",
                    "company": "GC Prime Contractors",
                    "access_level": "full"
                }
                is_authenticated = True
            
            # Project Manager - Full project access
            elif username.lower() == "pm" and password == "pm123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "pm",
                    "email": "pm@gcpanel.com",
                    "full_name": "Project Manager",
                    "role": "project_manager",
                    "company": "GC Prime Contractors",
                    "access_level": "full_project"
                }
                is_authenticated = True
            
            # Superintendent - Field operations focus
            elif username.lower() == "super" and password == "super123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "super",
                    "email": "super@gcpanel.com",
                    "full_name": "Site Superintendent",
                    "role": "superintendent",
                    "company": "GC Prime Contractors",
                    "access_level": "field_ops"
                }
                is_authenticated = True
            
            # Estimator - Preconstruction and cost focus
            elif username.lower() == "estimator" and password == "est123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "estimator",
                    "email": "estimator@gcpanel.com",
                    "full_name": "Senior Estimator",
                    "role": "estimator",
                    "company": "GC Prime Contractors",
                    "access_level": "cost_precon"
                }
                is_authenticated = True
            
            # Architect - Design focus
            elif username.lower() == "architect" and password == "arch123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "architect",
                    "email": "arch@designpartners.com",
                    "full_name": "Design Architect",
                    "role": "architect",
                    "company": "Design Partners",
                    "access_level": "design"
                }
                is_authenticated = True
            
            # Engineer - Engineering focus
            elif username.lower() == "engineer" and password == "eng123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "engineer",
                    "email": "engineer@structuresolutions.com",
                    "full_name": "Structural Engineer",
                    "role": "engineer",
                    "company": "Structure Solutions",
                    "access_level": "engineering"
                }
                is_authenticated = True
            
            # Subcontractor - Limited access
            elif username.lower() == "sub" and password == "sub123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "sub",
                    "email": "foreman@powersystems.com",
                    "full_name": "Electrical Foreman",
                    "role": "subcontractor",
                    "company": "Power Systems Inc.",
                    "access_level": "limited"
                }
                is_authenticated = True
            
            # Owner - Owner view
            elif username.lower() == "owner" and password == "owner123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "owner",
                    "email": "owner@highlandproperties.com",
                    "full_name": "Project Owner",
                    "role": "owner",
                    "company": "Highland Properties LLC",
                    "access_level": "owner_view"
                }
                is_authenticated = True
            
            # Demo User - Viewer access (kept for backward compatibility)
            elif username.lower() == "demo" and password == "demo123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "demo",
                    "email": "demo@gcpanel.com",
                    "full_name": "Demo User",
                    "role": "viewer",
                    "company": "GC Prime Contractors",
                    "access_level": "view_only"
                }
                is_authenticated = True
        
        # Show login page if not authenticated
        if not is_authenticated:
            
            # Import and render login page
            from pages.login import login_page
            login_page()
            return
            
        # User is authenticated, continue with regular app
        
        # Render the fixed header at the top of the page
        render_fixed_header()
        
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
        # In production, this should be False by default
        is_development = False
        if st.session_state.get('show_debug', is_development):
            with st.expander("Error Details (Developers Only)"):
                st.code(error_details)

if __name__ == "__main__":
    main()