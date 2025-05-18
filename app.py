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
from core.digital_signatures.signature import DigitalSignature

# Initialize core application
from core import initialize_application

def local_css():
    """Apply custom CSS for theming"""
    # Define primary color
    primary_color = "#3e79f7"
    secondary_color = "#6c757d"
    success_color = "#38d39f"
    warning_color = "#f9c851"
    danger_color = "#ff5b5b"
    
    # Apply custom CSS
    st.markdown(f"""
    <style>
        /* Base styling */
        .stApp {{
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        /* Dashboard cards */
        .dashboard-card {{
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background-color: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
            border: 1px solid #eef2f7;
        }}
        
        .dashboard-card:hover {{
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }}
        
        /* Counter cards */
        .counter-value {{
            font-size: 2rem;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 0.5rem;
        }}
        
        .counter-label {{
            font-size: 0.9rem;
            color: {secondary_color};
        }}
        
        /* Navigation styling */
        .nav-list {{
            list-style: none;
            padding-left: 0;
            margin-top: 1rem;
        }}
        
        .nav-item {{
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            display: flex;
            align-items: center;
            cursor: pointer;
            color: #6c757d;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.15s ease;
            font-size: 0.95rem;
        }}
        
        .nav-item:hover {{
            background-color: rgba(62, 121, 247, 0.08);
            color: {primary_color};
        }}
        
        .nav-item.active {{
            background-color: rgba(62, 121, 247, 0.1);
            color: {primary_color};
            font-weight: 500;
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
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .status-active {{
            background-color: rgba(56, 211, 159, 0.15);
            color: #38d39f;
        }}
        
        .status-pending {{
            background-color: rgba(249, 200, 81, 0.15);
            color: #f9c851;
        }}
        
        .status-delayed {{
            background-color: rgba(255, 91, 91, 0.15);
            color: #ff5b5b;
        }}
        
        /* Button styling */
        .custom-button {{
            display: inline-block;
            padding: 0.5rem 1rem;
            font-weight: 500;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            cursor: pointer;
            border: 1px solid transparent;
            border-radius: 4px;
            transition: all 0.15s ease;
        }}
        
        .primary-button {{
            color: white;
            background-color: {primary_color};
            border-color: {primary_color};
        }}
        
        .primary-button:hover {{
            background-color: #3267d3;
            border-color: #3267d3;
        }}
        
        /* Form styling */
        div[data-testid="stForm"] {{
            background-color: white;
            padding: 1.5rem;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border: 1px solid #eef2f7;
        }}
        
        /* Table styling */
        div.stDataFrame {{
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid #eef2f7;
            background-color: white;
        }}
        
        div.stDataFrame div[data-testid="stTable"] {{
            border-radius: 6px;
            overflow: hidden;
        }}
        
        div.stDataFrame table {{
            border-collapse: collapse;
            width: 100%;
        }}
        
        div.stDataFrame th {{
            background-color: #f8f9fa;
            border-top: none;
            border-bottom: 2px solid #eef2f7;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            padding: 0.75rem;
        }}
        
        div.stDataFrame td {{
            border-top: 1px solid #eef2f7;
            padding: 0.75rem;
        }}
        
        /* Progress bar styling */
        div.stProgress > div > div > div {{
            background-color: {primary_color};
        }}
        
        /* Tabs styling */
        button[data-baseweb="tab"] {{
            font-size: 1rem;
        }}
        
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {primary_color};
            border-bottom-color: {primary_color};
            font-weight: 600;
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
        
        # Render breadcrumbs
        simple_breadcrumbs(breadcrumb_items)
        
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
        elif current_menu == "Roadmap":
            render_roadmap()
        elif current_menu == "Closeout":
            render_closeout()
        elif current_menu == "Settings":
            render_settings()
        else:
            st.error(f"Unknown menu: {current_menu}")

if __name__ == "__main__":
    main()