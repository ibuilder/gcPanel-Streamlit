"""
gcPanel Construction Management Dashboard

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
"""

import streamlit as st
import os
from datetime import datetime

# Initialize core application
from core import initialize_application

# Import components
from components.auth import (
    login_component, register_component, check_authentication,
    logout, user_profile_component
)
from components.project import (
    project_list_component, project_details_component,
    project_create_component
)
from components.engineering import (
    submittals_list_component, submittal_details_component,
    rfi_list_component, rfi_details_component
)

# Page configuration
st.set_page_config(
    page_title="gcPanel Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize application
if not hasattr(st.session_state, 'app_initialized'):
    if initialize_application():
        st.session_state.app_initialized = True
    else:
        st.error("Failed to initialize application")
        st.stop()

# Setup theme
def local_css():
    """Apply custom CSS for theming"""
    # Light theme colors by default
    bg_color = "#ffffff"
    text_color = "#2c3e50"
    primary_color = "#4caf50"
    secondary_color = "#2a9fd6"
    accent_color = "#26a69a"
    
    # Apply CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        /* Button styling */
        .stButton button {{
            background-color: {secondary_color} !important;
            color: #ecf0f1 !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            margin: 0.25rem 0 !important;
            transition: all 0.2s !important;
        }}
        .stButton button:hover {{
            background-color: {secondary_color} !important;
            box-shadow: 0 3px 5px rgba(0,0,0,0.2) !important;
        }}
        /* Form input styling */
        .stTextInput input, .stNumberInput input, .stDateInput input, 
        .stSelectbox select, .stTextArea textarea {{
            background-color: #2c3e50 !important;
            color: #ecf0f1 !important;
            border: 1px solid #4a6572 !important;
            border-radius: 4px !important;
        }}
        .stTextInput > div, .stNumberInput > div, 
        .stDateInput > div, .stSelectbox > div, 
        .stTextArea > div {{
            background-color: transparent !important;
        }}
        /* Select box specific styling */
        .stSelectbox > div > div > div {{
            background-color: #2c3e50 !important;
            color: #ecf0f1 !important;
        }}
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom-color: {secondary_color}40 !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding: 8px 16px;
            border-radius: 4px 4px 0 0;
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background-color: {secondary_color} !important;
            color: white !important;
        }}
        /* Radio button styling */
        .stRadio > div {{
            gap: 1rem !important;
        }}
        .stRadio label {{
            padding: 0.5rem 1rem !important;
            background-color: #2c3e50 !important;
            border-radius: 4px !important;
            transition: all 0.2s !important;
        }}
        .stRadio label:has(input:checked) {{
            background-color: {secondary_color} !important;
            box-shadow: 0 3px 5px rgba(0,0,0,0.2) !important;
        }}
        /* Enhanced dashboard cards */
        .dashboard-card {{
            background-color: #2c3e50;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid {secondary_color}40;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        /* Main title */
        .main-title {{
            color: {primary_color};
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        /* Counter styles */
        .counter-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {accent_color};
        }}
        .counter-label {{
            font-size: 0.9rem;
            color: {text_color}90;
            text-transform: uppercase;
        }}
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {{
            background-color: #1a2433 !important;
        }}
        /* Status indicators */
        .status-pill {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            color: white;
            background-color: var(--pill-color, #555);
        }}
    </style>
    """, unsafe_allow_html=True)

# Apply CSS theme
local_css()

# Title and main header
title_col1, title_col2 = st.columns([3, 1])
with title_col1:
    st.markdown('<div class="main-title">gcPanel Construction Management Dashboard</div>', unsafe_allow_html=True)
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"<div>{current_date}</div>", unsafe_allow_html=True)

# No theme toggle - using Superhero theme consistently

# Authentication check
if not check_authentication():
    # Show login/register tabs if not authenticated
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        login_component()
    with register_tab:
        register_component()
    st.stop()

# User greeting in sidebar
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user.full_name}")
    
    # Safely get roles
    try:
        from core.database.config import get_db_session
        from core.models.user import User
        with get_db_session() as db:
            # Refresh user from database to get associated roles
            user = db.query(User).filter(User.id == st.session_state.user.id).first()
            if user and user.roles:
                roles_text = ', '.join([role.name for role in user.roles])
                st.markdown(f"**Role:** {roles_text}")
            else:
                st.markdown("**Role:** Standard User")
    except Exception as e:
        st.markdown("**Role:** Standard User")
    
    # Navigation
    st.markdown("## Navigation")
    
    # Check if menu is in session state, if not initialize to Dashboard
    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"
        
    # Create radio buttons for menu selection and update session state
    selected = st.radio("", [
        "Dashboard", 
        "Projects", 
        "Engineering",
        "Field Operations",
        "Cost Management",
        "Settings",
        "Profile"
    ], index=["Dashboard", "Projects", "Engineering", "Field Operations", 
              "Cost Management", "Settings", "Profile"].index(st.session_state.menu))
    
    # Update session state when menu selection changes
    if selected != st.session_state.menu:
        st.session_state.menu = selected
    
    if st.button("Logout"):
        logout()
        st.rerun()

# Main content based on navigation
if st.session_state.menu == "Dashboard":
    st.header("Dashboard")
    st.write("Welcome to gcPanel Construction Management Dashboard")
    
    # Project stats
    st.subheader("Project Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">12</div>'
                   '<div class="counter-label">Active Projects</div>'
                   '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">45</div>'
                   '<div class="counter-label">Open RFIs</div>'
                   '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">28</div>'
                   '<div class="counter-label">Pending Submittals</div>'
                   '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">8</div>'
                   '<div class="counter-label">Overdue Tasks</div>'
                   '</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    # Placeholder for recent activity feed
    activities = [
        {"type": "RFI", "project": "Highland Tower", "description": "RFI #123 was answered", "time": "2 hours ago"},
        {"type": "Submittal", "project": "City Center", "description": "Submittal #45 was approved", "time": "Yesterday"},
        {"type": "Project", "project": "Riverside Apartments", "description": "New milestone added", "time": "2 days ago"},
        {"type": "Task", "project": "Highland Tower", "description": "Task assigned to John Smith", "time": "3 days ago"}
    ]
    
    for activity in activities:
        st.markdown(f"**{activity['type']}** - {activity['project']}: {activity['description']} · {activity['time']}")

elif st.session_state.menu == "Projects":
    # Project sub-navigation
    project_action = st.sidebar.radio("Project Actions", ["View Projects", "Create Project"])
    
    if project_action == "View Projects":
        if "selected_project_code" in st.session_state:
            project_details_component()
        else:
            project_list_component()
    elif project_action == "Create Project":
        project_create_component()

elif st.session_state.menu == "Engineering":
    # Engineering sub-navigation
    engineering_tab = st.sidebar.radio("Engineering Documents", ["Submittals", "RFIs"])
    
    if engineering_tab == "Submittals":
        if "selected_submittal_id" in st.session_state:
            submittal_details_component()
        elif "create_submittal_project_id" in st.session_state:
            st.warning("Submittal creation form not yet implemented")
            if st.button("Back to Submittals"):
                del st.session_state.create_submittal_project_id
                st.rerun()
        else:
            submittals_list_component()
    
    elif engineering_tab == "RFIs":
        if "selected_rfi_id" in st.session_state:
            rfi_details_component()
        elif "create_rfi_project_id" in st.session_state:
            st.warning("RFI creation form not yet implemented")
            if st.button("Back to RFIs"):
                del st.session_state.create_rfi_project_id
                st.rerun()
        else:
            rfi_list_component()

elif st.session_state.menu == "Field Operations":
    st.header("Field Operations")
    st.info("Field Operations module is under development")

elif st.session_state.menu == "Cost Management":
    st.header("Cost Management")
    st.info("Cost Management module is under development")

elif st.session_state.menu == "Settings":
    st.header("Settings")
    
    # Settings tabs
    settings_tab = st.radio("Settings", ["General", "Users", "Permissions"])
    
    if settings_tab == "General":
        st.subheader("General Settings")
        company_name = st.text_input("Company Name", "Your Construction Company")
        logo_upload = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")
    
    elif settings_tab == "Users":
        st.subheader("User Management")
        st.info("User management interface is under development")
    
    elif settings_tab == "Permissions":
        st.subheader("Role Permissions")
        st.info("Role permissions interface is under development")

elif st.session_state.menu == "Profile":
    user_profile_component()

# Clear navigation state if we've changed main menu
if st.session_state.menu == "Projects" and "selected_project_code" in st.session_state:
    # Keep project selection state only in project section
    pass
elif st.session_state.menu != "Projects" and "selected_project_code" in st.session_state:
    del st.session_state.selected_project_code

if st.session_state.menu == "Engineering" and "selected_submittal_id" in st.session_state:
    # Keep submittal selection state only in engineering section
    pass
elif st.session_state.menu != "Engineering" and "selected_submittal_id" in st.session_state:
    del st.session_state.selected_submittal_id

if st.session_state.menu == "Engineering" and "selected_rfi_id" in st.session_state:
    # Keep RFI selection state only in engineering section
    pass
elif st.session_state.menu != "Engineering" and "selected_rfi_id" in st.session_state:
    del st.session_state.selected_rfi_id