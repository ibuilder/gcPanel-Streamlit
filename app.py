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
    primary_color = "#1e3a8a"
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
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
            border: 1px solid #ced4da !important;
            border-radius: 4px !important;
        }}
        .stTextInput > div, .stNumberInput > div, 
        .stDateInput > div, .stSelectbox > div, 
        .stTextArea > div {{
            background-color: transparent !important;
        }}
        /* Select box specific styling */
        .stSelectbox > div > div > div {{
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
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
    
    # Define menu items with icons
    menu_items = {
        "Dashboard": "📊",
        "Projects": "🏗️",
        "Engineering": "📐",
        "Field Operations": "👷",
        "Safety": "⚠️",
        "Contracts": "📝",
        "Cost Management": "💰",
        "BIM": "🏢",
        "Resources": "🔧",
        "Closeout": "✅",
        "Settings": "⚙️",
        "Profile": "👤"
    }
    
    # Add custom styling for the radio buttons
    st.markdown("""
    <style>
    div.row-widget.stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    div.row-widget.stRadio > div > label {
        padding: 10px 15px;
        border-radius: 5px;
        background-color: #f8f9fa;
        border: none;
        box-shadow: none;
        color: #2c3e50;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
    }
    
    div.row-widget.stRadio > div [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0;
    }
    
    div.row-widget.stRadio > div > label:hover {
        background-color: #e9ecef;
    }
    
    div.row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background-color: transparent;
    }
    
    div.row-widget.stRadio > div > label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #1e3a8a;
        color: white;
        font-weight: 500;
    }
    
    /* Hide the actual radio button while preserving functionality */
    div.row-widget.stRadio > div > label > div:first-child {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create radio options with icons
    options = [f"{icon} {name}" for name, icon in menu_items.items()]
    
    # Get the index of the current menu
    current_menu = st.session_state.menu
    current_index = list(menu_items.keys()).index(current_menu) if current_menu in menu_items else 0
    
    # Create the radio buttons
    selected_option = st.radio(
        "Navigation",
        options,
        index=current_index,
        label_visibility="collapsed"
    )
    
    # Extract the menu name (remove the emoji)
    selected_menu = selected_option.split(" ", 1)[1] if " " in selected_option else selected_option
    
    # Update the menu selection if it changed
    if selected_menu != st.session_state.menu:
        st.session_state.menu = selected_menu
        st.rerun()
    
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
    
    # Field Operations tabs
    field_tab = st.tabs(["Daily Reports", "Safety Inspections", "Quality Control", "Site Photos"])
    
    with field_tab[0]:
        st.subheader("Daily Reports")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            project_filter = st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments"])
        with col2:
            date_filter = st.date_input("Date Range (Start)", value=None)
        with col3:
            date_end = st.date_input("Date Range (End)", value=None)
            
        # Add report button
        st.button("Add Daily Report", type="primary", key="add_daily_report")
        
        # Sample data for daily reports
        reports = [
            {"date": "2025-05-15", "project": "Highland Tower", "author": "John Smith", "workers": 23, "weather": "Clear", "temperature": 72},
            {"date": "2025-05-14", "project": "Highland Tower", "author": "John Smith", "workers": 21, "weather": "Partly Cloudy", "temperature": 68},
            {"date": "2025-05-13", "project": "City Center", "author": "Maria Johnson", "workers": 15, "weather": "Rain", "temperature": 65},
            {"date": "2025-05-12", "project": "Riverside Apartments", "author": "Robert Davis", "workers": 12, "weather": "Clear", "temperature": 70}
        ]
        
        # Display reports
        for report in reports:
            with st.expander(f"{report['project']} - {report['date']}"):
                st.write(f"**Author:** {report['author']}")
                st.write(f"**Workers on Site:** {report['workers']}")
                st.write(f"**Weather:** {report['weather']}, {report['temperature']}°F")
                st.write("**Work Completed:**")
                st.write("- Completed foundation pouring for east wing")
                st.write("- Installed temporary power for floors 3-5")
                st.write("- Delivered steel beams for phase 2")
    
    with field_tab[1]:
        st.subheader("Safety Inspections")
        st.info("Safety inspections module is coming soon")
    
    with field_tab[2]:
        st.subheader("Quality Control")
        st.info("Quality control module is coming soon")
        
    with field_tab[3]:
        st.subheader("Site Photos")
        st.info("Site photos gallery is coming soon")

elif st.session_state.menu == "Safety":
    st.header("Safety Management")
    
    # Safety tabs
    safety_tab = st.tabs(["Incident Reports", "Safety Training", "Compliance"])
    
    with safety_tab[0]:
        st.subheader("Incident Reports")
        
        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            project_filter = st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments"], key="safety_project")
        with col2:
            severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Critical"])
            
        # Add incident button
        st.button("Report New Incident", type="primary")
        
        # Sample data for incidents
        incidents = [
            {"date": "2025-05-10", "project": "Highland Tower", "type": "Near Miss", "severity": "Low", "status": "Closed"},
            {"date": "2025-05-05", "project": "City Center", "type": "Property Damage", "severity": "Medium", "status": "Under Investigation"},
            {"date": "2025-04-28", "project": "Riverside Apartments", "type": "Minor Injury", "severity": "Medium", "status": "Closed"},
            {"date": "2025-04-15", "project": "Highland Tower", "type": "Equipment Failure", "severity": "High", "status": "Resolved"}
        ]
        
        # Display incidents
        for incident in incidents:
            status_color = "green" if incident["status"] == "Closed" else "orange" if incident["status"] == "Resolved" else "red"
            severity_color = "green" if incident["severity"] == "Low" else "orange" if incident["severity"] == "Medium" else "red"
            
            with st.expander(f"{incident['date']} - {incident['project']} - {incident['type']}"):
                st.write(f"**Severity:** <span style='color:{severity_color}'>{incident['severity']}</span>", unsafe_allow_html=True)
                st.write(f"**Status:** <span style='color:{status_color}'>{incident['status']}</span>", unsafe_allow_html=True)
                st.write("**Description:**")
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies.")
                st.write("**Actions Taken:**")
                st.write("- Immediate area secured")
                st.write("- Safety briefing conducted")
                st.write("- Equipment inspection scheduled")
    
    with safety_tab[1]:
        st.subheader("Safety Training")
        st.info("Safety training module is coming soon")
    
    with safety_tab[2]:
        st.subheader("Compliance")
        st.info("Safety compliance module is coming soon")

elif st.session_state.menu == "Contracts":
    st.header("Contract Management")
    
    # Contracts tabs
    contracts_tab = st.tabs(["Contracts", "Change Orders", "Purchase Orders"])
    
    with contracts_tab[0]:
        st.subheader("Contracts")
        
        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            project_filter = st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments"], key="contract_project")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Draft", "Under Review", "Executed", "Completed", "Terminated"])
            
        # Add contract button
        st.button("Add Contract", type="primary")
        
        # Sample data for contracts
        contracts = [
            {"number": "C-2025-001", "project": "Highland Tower", "vendor": "ABC Concrete", "type": "Subcontract", "value": "$1,250,000", "status": "Executed"},
            {"number": "C-2025-002", "project": "City Center", "vendor": "XYZ Electrical", "type": "Subcontract", "value": "$875,000", "status": "Under Review"},
            {"number": "C-2025-003", "project": "Riverside Apartments", "vendor": "123 Plumbing", "type": "Subcontract", "value": "$450,000", "status": "Executed"},
            {"number": "C-2025-004", "project": "Highland Tower", "vendor": "Smith & Co. Steel", "type": "Purchase", "value": "$2,100,000", "status": "Executed"}
        ]
        
        # Display contracts
        for contract in contracts:
            with st.expander(f"{contract['number']} - {contract['vendor']} - {contract['project']}"):
                st.write(f"**Type:** {contract['type']}")
                st.write(f"**Value:** {contract['value']}")
                st.write(f"**Status:** {contract['status']}")
                st.write("**Scope:**")
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies.")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("View Contract", key=f"view_{contract['number']}")
                with col2:
                    st.button("Edit", key=f"edit_{contract['number']}")
                with col3:
                    st.button("Download", key=f"download_{contract['number']}")
    
    with contracts_tab[1]:
        st.subheader("Change Orders")
        st.info("Change orders module is coming soon")
    
    with contracts_tab[2]:
        st.subheader("Purchase Orders")
        st.info("Purchase orders module is coming soon")

elif st.session_state.menu == "Cost Management":
    st.header("Cost Management")
    
    # Cost Management tabs
    cost_tab = st.tabs(["Budget", "Cost Tracking", "Invoices", "Forecasting"])
    
    with cost_tab[0]:
        st.subheader("Project Budgets")
        
        # Project selection
        project = st.selectbox("Select Project", ["Highland Tower", "City Center", "Riverside Apartments"], key="budget_project")
        
        # Budget overview
        st.subheader(f"{project} Budget Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Budget", "$12,500,000", "")
        with col2:
            st.metric("Committed", "$8,750,000", "70%")
        with col3:
            st.metric("Spent to Date", "$5,250,000", "42%")
        with col4:
            st.metric("Remaining", "$7,250,000", "")
        
        # Budget breakdown
        st.subheader("Budget Breakdown")
        
        # Sample data for budget categories
        categories = [
            {"name": "General Conditions", "budget": 750000, "committed": 680000, "spent": 450000},
            {"name": "Site Work", "budget": 1250000, "committed": 1200000, "spent": 980000},
            {"name": "Concrete", "budget": 2500000, "committed": 2350000, "spent": 1850000},
            {"name": "Steel", "budget": 3500000, "committed": 3100000, "spent": 1500000},
            {"name": "Mechanical", "budget": 1750000, "committed": 950000, "spent": 250000},
            {"name": "Electrical", "budget": 1250000, "committed": 350000, "spent": 120000},
            {"name": "Finishes", "budget": 1500000, "committed": 120000, "spent": 100000}
        ]
        
        # Create DataFrame
        import pandas as pd
        df = pd.DataFrame(categories)
        df["remaining"] = df["budget"] - df["spent"]
        df["percent_spent"] = (df["spent"] / df["budget"] * 100).round(1).astype(str) + "%"
        
        # Format currency
        for col in ["budget", "committed", "spent", "remaining"]:
            df[col] = df[col].apply(lambda x: f"${x:,.0f}")
        
        # Display table
        st.dataframe(df, use_container_width=True)
        
        # Budget chart
        st.subheader("Budget vs. Actual")
        chart_data = pd.DataFrame({
            "Category": [cat["name"] for cat in categories],
            "Budget": [cat["budget"] for cat in categories],
            "Committed": [cat["committed"] for cat in categories],
            "Actual": [cat["spent"] for cat in categories]
        })
        st.bar_chart(chart_data.set_index("Category"))
    
    with cost_tab[1]:
        st.subheader("Cost Tracking")
        st.info("Cost tracking module is coming soon")
    
    with cost_tab[2]:
        st.subheader("Invoices")
        st.info("Invoices module is coming soon")
        
    with cost_tab[3]:
        st.subheader("Forecasting")
        st.info("Cost forecasting module is coming soon")

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