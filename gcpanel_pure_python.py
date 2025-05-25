"""
Highland Tower Development - gcPanel Pure Python
Clean, performant construction management platform with zero HTML dependencies
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="gcPanel - Highland Tower",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_user_permissions():
    """Define clean role-based permissions"""
    return {
        "admin": {
            "name": "Administrator",
            "modules": ["Dashboard", "Unit Prices", "Deliveries", "Safety", "Contracts", 
                       "Cost Management", "Daily Reports", "BIM", "Analytics", "Documents"],
            "can_manage_users": True
        },
        "manager": {
            "name": "Project Manager", 
            "modules": ["Dashboard", "Unit Prices", "Deliveries", "Safety", "Daily Reports", 
                       "Cost Management", "BIM", "Analytics"],
            "can_manage_users": False
        },
        "user": {
            "name": "Standard User",
            "modules": ["Dashboard", "Daily Reports"],
            "can_manage_users": False
        }
    }

def check_access(module_name):
    """Check if user has access to module"""
    if not st.session_state.get("authenticated", False):
        return False
    
    user_role = st.session_state.get("user_role", "user")
    permissions = get_user_permissions()
    
    if user_role in permissions:
        return module_name in permissions[user_role]["modules"]
    return False

def initialize_session():
    """Initialize session state"""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "",
        "current_menu": "Dashboard"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_login():
    """Clean login interface"""
    st.title("🏗️ Highland Tower Development")
    st.subheader("gcPanel Construction Management")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.form_submit_button("🔐 Login", use_container_width=True):
            # Simple authentication logic
            if username and password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = "admin" if username == "admin" else "manager" if username == "manager" else "user"
                st.rerun()
            else:
                st.error("Please enter both username and password")

def render_profile_section():
    """Clean profile section"""
    if not st.session_state.get("authenticated"):
        return
    
    username = st.session_state.get("username", "")
    user_role = st.session_state.get("user_role", "")
    permissions = get_user_permissions()
    role_info = permissions.get(user_role, {"name": "Unknown"})
    
    # Profile display
    st.markdown(f"### 👤 {username}")
    st.caption(f"**{role_info['name']}**")
    st.info("🏗️ Highland Tower Development")
    
    # User actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚙️ Settings", use_container_width=True):
            st.success("Settings panel opened")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.rerun()

def render_navigation():
    """Clean sidebar navigation"""
    st.sidebar.markdown("## 🎯 Core Management")
    
    modules = [
        ("📊 Dashboard", "Dashboard"),
        ("💲 Unit Prices", "Unit Prices"),
        ("🚛 Deliveries", "Deliveries"),
        ("🦺 Safety", "Safety"),
        ("📋 Contracts", "Contracts"),
        ("💰 Cost Management", "Cost Management"),
        ("📊 Daily Reports", "Daily Reports"),
        ("🏢 BIM", "BIM"),
        ("📈 Analytics", "Analytics"),
        ("📄 Documents", "Documents")
    ]
    
    for display_name, module_name in modules:
        if check_access(module_name):
            if st.sidebar.button(display_name, key=f"nav_{module_name}", use_container_width=True):
                st.session_state.current_menu = module_name
                st.rerun()

def render_dashboard():
    """Clean dashboard interface"""
    st.title("📊 Highland Tower Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Progress", "87%", "3% this week")
    with col2:
        st.metric("Active Workers", "89", "+12 vs last week") 
    with col3:
        st.metric("Budget Status", "$42.1M", "On track")
    with col4:
        st.metric("Safety Score", "98.2%", "Excellent")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Weekly Progress")
        progress_data = pd.DataFrame({
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Progress": [75, 81, 84, 87]
        })
        fig = px.line(progress_data, x="Week", y="Progress", title="Project Progress Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👷 Workforce Distribution")
        workforce_data = pd.DataFrame({
            "Role": ["Structural", "MEP", "Interior", "Site Management"],
            "Count": [35, 28, 18, 8]
        })
        fig = px.pie(workforce_data, values="Count", names="Role", title="Current Workforce")
        st.plotly_chart(fig, use_container_width=True)

def render_unit_prices():
    """Clean unit prices interface"""
    st.title("💲 Unit Prices Intelligence")
    
    tab1, tab2, tab3 = st.tabs(["📊 Materials", "🚜 Equipment", "👷 Labor"])
    
    with tab1:
        st.subheader("Material Cost Analysis")
        
        materials_data = pd.DataFrame({
            "Material": ["Steel Beams", "Concrete", "Rebar", "Drywall"],
            "Unit": ["LF", "CY", "TON", "SF"],
            "Budget_Price": [45.80, 125.00, 850.00, 2.45],
            "Current_Price": [47.20, 128.50, 875.00, 2.50],
            "Variance": [3.1, 2.8, 2.9, 2.0]
        })
        
        st.dataframe(materials_data, use_container_width=True)
        
        # Cost variance chart
        fig = px.bar(materials_data, x="Material", y="Variance", 
                    title="Material Cost Variance (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Equipment Utilization")
        
        equipment_data = pd.DataFrame({
            "Equipment": ["Tower Crane", "Concrete Pump", "Excavator", "Forklift"],
            "Daily_Rate": [2850, 1200, 800, 350],
            "Utilization": [94.5, 87.2, 76.8, 91.3],
            "Status": ["Active", "Active", "Maintenance", "Active"]
        })
        
        st.dataframe(equipment_data, use_container_width=True)
    
    with tab3:
        st.subheader("Labor Rates")
        
        labor_data = pd.DataFrame({
            "Trade": ["Iron Workers", "Concrete Finishers", "Electricians", "Plumbers"],
            "Hourly_Rate": [42.50, 38.75, 45.20, 44.80],
            "Hours_This_Week": [320, 280, 240, 200],
            "Efficiency": [96.2, 94.1, 98.5, 92.8]
        })
        
        st.dataframe(labor_data, use_container_width=True)

def render_deliveries():
    """Clean deliveries interface"""
    st.title("🚛 Highland Tower Deliveries")
    
    # Today's deliveries
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Scheduled Today", "12", "3 more than yesterday")
    with col2:
        st.metric("Completed", "8", "On schedule")
    with col3:
        st.metric("In Transit", "3", "Real-time tracking")
    with col4:
        st.metric("Delayed", "1", "-2 vs last week")
    
    # Delivery schedule
    st.subheader("📅 Today's Schedule")
    
    deliveries = pd.DataFrame({
        "Time": ["8:00 AM", "10:30 AM", "2:00 PM", "3:30 PM"],
        "Material": ["Steel Beams - Level 14", "Concrete Mix - Level 13", 
                    "MEP Equipment", "Drywall Supplies"],
        "Supplier": ["Steel Fabricators Inc", "Highland Concrete", 
                    "Advanced Building Systems", "Interior Solutions"],
        "Status": ["En Route", "Loading", "Confirmed", "Pending"]
    })
    
    st.dataframe(deliveries, use_container_width=True)
    
    # Schedule new delivery
    with st.expander("➕ Schedule New Delivery"):
        with st.form("new_delivery"):
            col1, col2 = st.columns(2)
            
            with col1:
                delivery_date = st.date_input("Date")
                material_type = st.selectbox("Material", 
                    ["Steel Beams", "Concrete", "MEP Equipment", "Drywall"])
            
            with col2:
                delivery_time = st.time_input("Time")
                supplier = st.text_input("Supplier")
            
            if st.form_submit_button("📅 Schedule Delivery"):
                st.success("Delivery scheduled successfully!")

def render_daily_reports():
    """Clean daily reports interface"""
    st.title("📊 Daily Reports")
    
    # Quick status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("📍 Highland Tower Development")
    with col2:
        st.info("🏗️ Level 13 Active")
    with col3:
        st.info("👷 89 Workers")
    with col4:
        st.info("🌤️ 72°F Clear")
    
    # Report creation
    st.subheader("📝 Create Daily Report")
    
    with st.form("daily_report"):
        col1, col2 = st.columns(2)
        
        with col1:
            work_performed = st.text_area("Work Performed Today", height=100)
            crew_count = st.number_input("Crew Count", value=89)
        
        with col2:
            safety_issues = st.text_area("Safety Issues", height=100)
            weather_conditions = st.selectbox("Weather", 
                ["Clear", "Partly Cloudy", "Cloudy", "Rain", "Snow"])
        
        if st.form_submit_button("📊 Submit Report"):
            st.success("Daily report submitted successfully!")

def render_main_content():
    """Render main content based on selected menu"""
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    content_functions = {
        "Dashboard": render_dashboard,
        "Unit Prices": render_unit_prices,
        "Deliveries": render_deliveries,
        "Daily Reports": render_daily_reports
    }
    
    if current_menu in content_functions:
        content_functions[current_menu]()
    else:
        st.title(f"{current_menu}")
        st.info(f"The {current_menu} module is being developed with enterprise features.")
        
        # Module previews
        if current_menu == "Safety":
            st.subheader("🦺 Safety Management")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Safety Score", "98.2%", "Excellent")
                st.metric("Days Without Incident", "127", "+1")
            with col2:
                st.metric("Safety Inspections", "15", "This week")
                st.metric("Training Completed", "94%", "+2%")
        
        elif current_menu == "BIM":
            st.subheader("🏢 BIM Integration")
            st.info("3D model viewer and clash detection capabilities")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Model Accuracy", "99.7%", "High precision")
            with col2:
                st.metric("Clashes Resolved", "156", "This month")

def main():
    """Main application entry point"""
    initialize_session()
    
    if not st.session_state.get("authenticated", False):
        render_login()
    else:
        # Sidebar
        with st.sidebar:
            render_profile_section()
            st.markdown("---")
            render_navigation()
        
        # Main content
        render_main_content()

if __name__ == "__main__":
    main()