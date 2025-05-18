"""
gcPanel Construction Management Dashboard

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.
"""

import streamlit as st
import os
import pandas as pd
from datetime import datetime

# Import modules
from modules.dashboard import render_dashboard
from modules.settings import render_settings
from modules.project_information import render_project_information
from modules.pdf_viewer.pdf_viewer import render_pdf_viewer
from modules.bim_viewer.ifc_viewer import render_bim_viewer
from modules.field_operations import render_field_operations
from modules.scheduling import render_scheduling
from modules.safety import render_safety
from modules.contracts import render_contracts
from modules.cost_management import render_cost_management
from modules.closeout import render_closeout
from modules.engineering import render_engineering
from modules.documents import render_documents
from modules.roadmap import render_roadmap

# Import components
from components.simple_breadcrumbs import simple_breadcrumbs, get_breadcrumbs_for_page
from components.sidebar import render_sidebar
from components.notification_center import notification_center
from core.digital_signatures.signature import DigitalSignature

# Initialize core application
from core import initialize_application

def local_css():
    """Apply custom CSS for theming"""
    # Define color palette
    primary_color = "#3e79f7"
    secondary_color = "#6c757d"
    success_color = "#38d39f"
    warning_color = "#f9c851"
    danger_color = "#ff5b5b"
    light_bg = "#f8f9fa"
    dark_bg = "#313a46"
    border_color = "#eef2f7"
    text_color = "#2c3e50"
    text_muted = "#6c757d"
    
    # Apply custom CSS
    st.markdown(f"""
    <style>
        /* Base styling */
        .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            color: {text_color};
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            color: {text_color};
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
            line-height: 1.3;
        }}
        
        h1 {{
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
        }}
        
        h2 {{
            font-size: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        h3 {{
            font-size: 1.25rem;
        }}
        
        p {{
            margin-bottom: 1rem;
            line-height: 1.6;
        }}
        
        a {{
            color: {primary_color};
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Layout and Spacing */
        .stApp > header {{
            background-color: white;
            border-bottom: 1px solid {border_color};
        }}
        
        section[data-testid="stSidebarContent"] {{
            padding-top: 2rem;
        }}
        
        .main .block-container {{
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1200px;
        }}
        
        /* Dashboard cards */
        .dashboard-card {{
            background-color: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            margin-bottom: 1.5rem;
            transition: all 0.2s ease;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        }}
        
        .dashboard-card h3 {{
            margin-top: 0;
            font-size: 1.2rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }}
        
        .dashboard-card h3 svg, 
        .dashboard-card h3 i {{
            margin-right: 0.5rem;
            color: {primary_color};
        }}
        
        .dashboard-card p {{
            color: {text_muted};
            margin-bottom: 0.75rem;
        }}
        
        /* Counter cards */
        .counter-value {{
            font-size: 2.25rem;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }}
        
        .counter-label {{
            font-size: 0.9rem;
            color: {secondary_color};
            font-weight: 500;
        }}
        
        /* Navigation styling */
        .nav-list {{
            list-style: none;
            padding-left: 0;
            margin-top: 1.5rem;
        }}
        
        .nav-item {{
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            display: flex;
            align-items: center;
            cursor: pointer;
            color: #9097a7;
            border-radius: 6px;
            text-decoration: none;
            transition: all 0.15s ease;
            font-size: 0.95rem;
        }}
        
        .nav-item:hover {{
            background-color: rgba(62, 121, 247, 0.08);
            color: white;
        }}
        
        .nav-item.active {{
            background-color: rgba(62, 121, 247, 0.15);
            color: white;
            font-weight: 500;
        }}
        
        .nav-item i, 
        .nav-item svg {{
            margin-right: 0.75rem;
            font-size: 1.25rem;
        }}
        
        .nav-icon {{
            display: inline-block;
            width: 22px;
            margin-right: 10px;
            text-align: center;
            font-size: 18px;
        }}
        
        /* Status indicators */
        .status-pill {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            letter-spacing: 0.01em;
            line-height: 1.4;
            margin-right: 0.5rem;
        }}
        
        .status-pill i, 
        .status-pill svg {{
            margin-right: 0.35rem;
            font-size: 0.85rem;
        }}
        
        .status-active, .status-complete, .status-approved {{
            background-color: rgba(56, 211, 159, 0.15);
            color: #38d39f;
        }}
        
        .status-pending, .status-in-progress, .status-scheduled {{
            background-color: rgba(249, 200, 81, 0.15);
            color: #f9c851;
        }}
        
        .status-delayed, .status-canceled, .status-rejected {{
            background-color: rgba(255, 91, 91, 0.15);
            color: #ff5b5b;
        }}
        
        /* Button styling */
        .custom-button,
        div.stButton > button,
        div.stDownloadButton > button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.5rem 1rem;
            font-weight: 500;
            text-align: center;
            white-space: nowrap;
            cursor: pointer;
            border: 1px solid transparent;
            border-radius: 6px;
            transition: all 0.15s ease;
            font-size: 0.9rem;
            gap: 0.5rem;
        }}
        
        .primary-button,
        div.stButton > button[kind="primary"] {{
            color: white;
            background-color: {primary_color};
            border-color: {primary_color};
        }}
        
        .primary-button:hover,
        div.stButton > button[kind="primary"]:hover {{
            background-color: #3267d3;
            border-color: #3267d3;
            box-shadow: 0 2px 5px rgba(62, 121, 247, 0.2);
        }}
        
        .secondary-button,
        div.stButton > button:not([kind="primary"]) {{
            color: {text_color};
            background-color: white;
            border-color: {border_color};
        }}
        
        .secondary-button:hover,
        div.stButton > button:not([kind="primary"]):hover {{
            border-color: {primary_color};
            color: {primary_color};
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        /* Form styling */
        div[data-testid="stForm"] {{
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            margin-bottom: 1.5rem;
        }}
        
        div[data-testid="stForm"] > div > div > div {{
            gap: 1.25rem;
        }}
        
        /* Form input elements */
        input, select, textarea, div[data-baseweb="input"] input {{
            border-radius: 6px !important;
            border: 1px solid {border_color} !important;
            padding: 0.6rem 0.75rem !important;
            font-size: 0.95rem !important;
            transition: all 0.15s ease;
            background-color: white;
        }}
        
        input:focus, select:focus, textarea:focus, div[data-baseweb="input"] input:focus {{
            border-color: {primary_color} !important;
            box-shadow: 0 0 0 3px rgba(62, 121, 247, 0.15) !important;
            outline: none;
        }}
        
        /* Labels */
        label {{
            font-weight: 500;
            margin-bottom: 0.35rem;
            color: {text_color};
            font-size: 0.95rem;
        }}
        
        /* Table styling */
        div.stDataFrame, div[data-testid="stTable"] {{
            padding: 0;
            border-radius: 8px;
            border: 1px solid {border_color};
            background-color: white;
            overflow: hidden;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }}
        
        div.stDataFrame table, div[data-testid="stTable"] table {{
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
        }}
        
        div.stDataFrame th, div[data-testid="stTable"] th {{
            background-color: {light_bg};
            padding: 0.75rem 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {text_muted};
            border-bottom: 1px solid {border_color};
        }}
        
        div.stDataFrame td, div[data-testid="stTable"] td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid {border_color};
            vertical-align: middle;
            font-size: 0.95rem;
        }}
        
        div.stDataFrame tr:last-child td, div[data-testid="stTable"] tr:last-child td {{
            border-bottom: none;
        }}
        
        div.stDataFrame tr:hover td, div[data-testid="stTable"] tr:hover td {{
            background-color: rgba(0,0,0,0.01);
        }}
        
        /* Progress bar styling */
        div.stProgress > div > div > div {{
            background-color: {primary_color};
        }}
        
        /* Tabs styling */
        div.stTabs {{
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            margin-bottom: 1.5rem;
        }}
        
        button[data-baseweb="tab"] {{
            padding: 0.75rem 1.25rem;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.15s ease;
        }}
        
        button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: transparent;
            border-bottom: 2px solid {primary_color};
            color: {primary_color};
            font-weight: 600;
        }}
        
        div[data-testid="stTabContent"] {{
            padding: 1.5rem;
            background-color: white;
        }}
        
        /* Breadcrumbs */
        .breadcrumb {{
            display: flex;
            flex-wrap: wrap;
            padding: 0.5rem 1rem;
            margin-bottom: 1rem;
            list-style: none;
            background-color: #f8f9fa;
            border-radius: 0.25rem;
        }}
        
        .breadcrumb-item {{
            display: flex;
            align-items: center;
        }}
        
        .breadcrumb-item + .breadcrumb-item {{
            padding-left: 0.5rem;
        }}
        
        .breadcrumb-item + .breadcrumb-item::before {{
            display: inline-block;
            padding-right: 0.5rem;
            color: #6c757d;
            content: "/";
        }}
        
        .breadcrumb-item.active {{
            color: {primary_color};
            font-weight: 500;
        }}
        
        /* Custom widget styling */
        div.stSlider {{
            margin-bottom: 1.5rem;
        }}
        
        div.stDateInput > div > div {{
            border-radius: 4px;
        }}
        
        div.stTextInput > div > div {{
            border-radius: 4px;
        }}
        
        div.stTextArea > div > div {{
            border-radius: 4px;
        }}
        
        div.stSelectbox > div > div {{
            border-radius: 4px;
        }}
        
        div.stMultiselect > div > div {{
            border-radius: 4px;
        }}
        
        /* Markdown text styling */
        .info-text {{
            color: {secondary_color};
            font-size: 0.9rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Include Material Icons
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'menu' not in st.session_state:
        st.session_state.menu = "Dashboard"
    
    if 'theme_color' not in st.session_state:
        st.session_state.theme_color = "#3e79f7"
    
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "light"
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = "Highland Tower Development"
    
    if 'edit_project' not in st.session_state:
        st.session_state.edit_project = False

def main():
    """Main application entry point."""
    
    # Set page configuration
    st.set_page_config(
        page_title="gcPanel Construction Dashboard",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    local_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize database and authentication
    initialize_application()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    with st.container():
        # Get current menu selection
        current_menu = st.session_state.get("menu", "Dashboard")
        
        # Get breadcrumbs for current page
        breadcrumb_items = get_breadcrumbs_for_page(current_menu)
        
        # Create a header row with breadcrumbs and notification center
        header_col1, header_col2 = st.columns([7, 3])
        
        with header_col1:
            # Render breadcrumbs
            simple_breadcrumbs(breadcrumb_items)
        
        with header_col2:
            # Initialize notification center
            if st.session_state.get("show_notification_center", False):
                notification_center()
            
            # Add notification center toggle button
            show_notifications = st.button("📋 Notifications", key="show_notifications_btn")
            if show_notifications:
                st.session_state.show_notification_center = not st.session_state.get("show_notification_center", False)
                st.rerun()
        
        # Render selected module
        if current_menu == "Dashboard":
            render_dashboard()
        elif current_menu == "Project Information":
            render_project_information()
        elif current_menu == "Engineering":
            render_engineering()
        elif current_menu == "Documents":
            render_documents()
        elif current_menu == "BIM":
            render_bim_viewer()
        elif current_menu == "Field Operations":
            render_field_operations()
        elif current_menu == "Safety":
            render_safety()
        elif current_menu == "Contracts":
            render_contracts()
        elif current_menu == "Cost Management":
            render_cost_management()
        elif current_menu == "Schedule":
            render_scheduling()
        # Roadmap functionality has been integrated into Schedule module
        elif current_menu == "Closeout":
            render_closeout()
        elif current_menu == "Settings":
            render_settings()
        else:
            st.error(f"Unknown menu: {current_menu}")

if __name__ == "__main__":
    main()