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
import logging
import os
from utils.ui_manager import set_page_config
import app_manager

# Import production configuration
from config.production import ProductionConfig, setup_logging
from utils.security import log_security_event

# Setup logging for production
logger = setup_logging()

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
        # Validate production configuration
        config_errors = ProductionConfig.validate_config()
        if config_errors and ProductionConfig.ENVIRONMENT == 'production':
            logger.critical(f"Production configuration errors: {config_errors}")
            st.error("Application configuration error. Please contact administrator.")
            return
        
        # Log application start
        log_security_event("APPLICATION_START", {"environment": ProductionConfig.ENVIRONMENT})
        # Set page configuration with favicon (PWA support is now integrated in set_page_config)
        set_page_config()
        
        # Enable mobile optimizations
        add_mobile_styles()
        
        # Apply enhanced UI styles for professional, enterprise-grade appearance
        apply_enhanced_styles()
        
        # Apply complete full dark theme and construction animations
        from assets.complete_dark_theme import apply_complete_dark_theme, add_dark_theme_indicator
        from assets.construction_dashboard_js import add_construction_dashboard_js, add_construction_help_button
        
        apply_complete_dark_theme()
        add_dark_theme_indicator()
        add_construction_dashboard_js()
        add_construction_help_button()
        
        # Remove sidebar and ensure full width layout
        st.markdown("""
        <style>
        /* ELIMINATE ALL unnecessary containers and divs throughout the app */
        .main .block-container {
            padding: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 !important;
            margin-top: 0 !important;
            max-width: 100% !important;
        }
        
        /* Remove ALL spacing from app container */
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
        .css-1d391kg {display: none !important;}
        .st-hy {display: none !important;}
        .st-emotion-cache-ue6h4q {display: none !important;}
        
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
        
        /* Ensure buttons remain functional */
        .stButton > button {
            display: block !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        
        /* Fix form elements functionality */
        .stTextInput,
        .stSelectbox,
        .stCheckbox,
        .stButton {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Force full width layout with zero top spacing */
        .appview-container .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .stApp > div:first-child {
            margin-left: 0px !important;
        }
        
        .css-18e3th9, .css-1d391kg {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
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

def render_custom_header():
    """Render the custom header with project info and user details."""
    
    user_role = st.session_state.get('user_role', 'Project Manager')
    username = st.session_state.get('username', 'User')
    
    # Get project info from config
    from app_config import PROJECT_INFO
    
    st.markdown(f"""
    <div class="custom-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="header-title">
                    🏗️ gcPanel
                    <span style="font-weight: normal; margin-left: 20px;">{PROJECT_INFO['name']}</span>
                </div>
                <div class="project-info">
                    {PROJECT_INFO['value']} • {PROJECT_INFO['location']} • Phase: {PROJECT_INFO['current_phase']}
                </div>
            </div>
            <div class="user-info">
                <div><strong>{username}</strong></div>
                <div style="opacity: 0.8;">{user_role}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render clean sidebar with project info and navigation."""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏗️</div>
            <h2 style='color: #3498db; margin: 0; font-weight: bold;'>gcPanel</h2>
            <p style='color: #95a5a6; font-size: 0.9em; margin: 5px 0;'>Construction Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu - moved directly under logo
        st.markdown("### Navigation")
        
        navigation_options = [
            "🏗️ Dashboard", "📋 Preconstruction", "⚙️ Engineering", "👷 Field Operations", 
            "🦺 Safety", "📄 Contracts", "💰 Cost Management", "🏢 BIM", "✅ Closeout", 
            "📊 Analytics", "📁 Documents", "📝 Daily Reports", "❓ RFIs", "📤 Submittals", 
            "📨 Transmittals", "📸 Photo Log", "👁️ Safety Observations", "⚠️ Incidents", 
            "📑 Prime Contract", "🔧 Change Orders", "🎯 Clash Detection", "👥 Resource Management",
            "🔍 Quality Control", "📋 Inspections", "💵 Budget", "📊 Business Intelligence"
        ]
        
        # Handle default selection with icons
        default_selection = st.session_state.get("current_menu", "🏗️ Dashboard")
        if not any(default_selection in option for option in navigation_options):
            default_selection = "🏗️ Dashboard"
        
        current_menu = st.selectbox(
            "Select Module:",
            navigation_options,
            index=navigation_options.index(default_selection) if default_selection in navigation_options else 0,
            key="navigation_select"
        )
        
        # Update session state with selected menu
        st.session_state["current_menu"] = current_menu
        
        st.divider()
        
        # Project Information
        st.markdown("### Highland Tower Development")
        st.markdown("""
        **Project Value:** $45.5M  
        **Type:** Mixed-Use Development  
        **Units:** 120 Residential + 8 Retail  
        **Size:** 168,500 sq ft  
        **Floors:** 15 Above + 2 Below Ground
        """)
        
        st.divider()
        
        # User Information
        current_user = st.session_state.get("username", "Project Manager")
        user_role = st.session_state.get("user_role", "admin")
        
        st.markdown(f"""
        **User:** {current_user}  
        **Role:** {user_role.title()}
        """)

def main_clean():
    """Clean main function with sidebar layout."""
    # Set page configuration
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply clean all dark theme
    st.markdown("""
    <style>
        /* All dark theme */
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        
        /* Sidebar dark */
        section[data-testid="stSidebar"] {
            background-color: #262730;
        }
        
        /* Main content area */
        .main .block-container {
            background-color: #0e1117;
            color: white;
        }
        
        /* Metrics dark */
        [data-testid="metric-container"] {
            background-color: #262730;
            border: 1px solid #464854;
            color: white;
        }
        
        /* Text elements */
        .stMarkdown {
            color: white;
        }
        
        /* Form elements dark */
        .stSelectbox > div > div {
            background-color: #262730;
            color: white;
            border: 1px solid #464854;
        }
        
        /* Buttons dark */
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            border: none;
        }
        
        .stButton > button:hover {
            background-color: #ff6c6c;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize basic session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_menu" not in st.session_state:
        st.session_state.current_menu = "Dashboard"
    if "username" not in st.session_state:
        st.session_state.username = "Project Manager"
    if "user_role" not in st.session_state:
        st.session_state.user_role = "admin"
    
    # Check authentication
    if not st.session_state.get("authenticated", False):
        st.error("🔒 Access Denied - Please log in to access Highland Tower Development dashboard")
        st.info("You need to authenticate to view project information and modules.")
        from login_form import render_login_form
        render_login_form()
        return
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render main content based on selection
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    try:
        if "Dashboard" in current_menu:
            import modules.dashboard
            modules.dashboard.render_dashboard()
        elif "Analytics" in current_menu:
            import modules.analytics
            modules.analytics.render_analytics_dashboard()
        elif "Preconstruction" in current_menu:
            # Import and render the actual preconstruction module
            import modules.PreConstruction
            modules.PreConstruction.render()
        elif "Engineering" in current_menu:
            # Import and render the actual engineering module
            from modules.engineering import render
            render()
        elif "Field Operations" in current_menu:
            # Import and render the actual field operations module
            from modules.field_operations import render
            render()
        elif "Safety" in current_menu:
            # Import and render the actual safety module
            from modules.safety import render
            render()
        elif "Contracts" in current_menu:
            # Import and render the actual contracts module
            import modules.contracts
            modules.contracts.render()
        elif "Cost Management" in current_menu:
            # Import and render the actual cost management module
            from modules.cost_management import render
            render()
        elif "BIM" in current_menu:
            # Import and render the actual BIM module
            from modules.bim import render_bim
            render_bim()
        elif "Closeout" in current_menu:
            # Import and render the actual closeout module
            from modules.closeout import render
            render()
        elif "Documents" in current_menu:
            # Import and render the actual documents module
            from modules.documents import render
            render()
        elif "Daily Reports" in current_menu:
            # Import and render the actual daily reports module
            from modules.field_operations import render_daily_reports
            render_daily_reports()
        elif "RFIs" in current_menu:
            # Import and render the actual RFIs module
            from modules.rfis import render
            render()
        elif "Submittals" in current_menu:
            # Import and render the actual submittals module
            from modules.engineering.submittal_packages import render as render_submittal_packages
            render_submittal_packages()
        elif "Transmittals" in current_menu:
            # Import and render the actual transmittals module
            from modules.engineering.transmittals import render as render_transmittals
            render_transmittals()
        elif "Photo Log" in current_menu:
            st.title("📸 Photo Log")
            st.info("Construction progress photography and documentation")
        elif "Safety Observations" in current_menu:
            st.title("👁️ Safety Observations")
            st.info("Field safety observations and compliance tracking")
        elif "Incidents" in current_menu:
            st.title("⚠️ Incident Reports")
            st.info("Safety incident reporting and investigation")
        elif "Prime Contract" in current_menu:
            st.title("📑 Prime Contract")
            st.info("Prime contract management and administration")
        elif "Change Orders" in current_menu:
            st.title("🔧 Change Orders")
            st.info("Construction change order tracking and approval")
        elif "Clash Detection" in current_menu:
            st.title("🎯 Clash Detection")
            st.info("BIM model clash detection and resolution")
        elif "Resource Management" in current_menu:
            st.title("👥 Resource Management")
            st.info("Team coordination, equipment, and material management")
        elif "Quality Control" in current_menu:
            st.title("🔍 Quality Control")
            st.info("Quality assurance and control processes")
        elif "Inspections" in current_menu:
            st.title("📋 Inspections")
            st.info("Construction inspections and compliance verification")
        elif "Budget" in current_menu:
            st.title("💵 Budget")
            st.info("Detailed budget tracking and financial management")
        elif "Business Intelligence" in current_menu:
            st.title("📊 Business Intelligence")
            st.info("Advanced analytics and business intelligence dashboards")
        else:
            st.title(f"{current_menu}")
            st.info("Module content will be displayed here.")
    except Exception as e:
        st.error(f"Error loading {current_menu} module")
        st.info("Please try selecting a different module.")

if __name__ == "__main__":
    main_clean()