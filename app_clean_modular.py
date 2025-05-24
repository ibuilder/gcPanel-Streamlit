"""
Highland Tower Development - Clean Modular gcPanel
Completely refactored for independent component loading and debugging
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "guest", 
        "current_menu": "Dashboard",
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def apply_theme():
    """Apply theme based on user selection"""
    current_theme = st.session_state.get("theme", "dark")
    
    if current_theme == "dark":
        st.markdown("""
        <style>
            .stApp { background-color: #0e1117; color: white; }
            section[data-testid="stSidebar"] { background-color: #262730; }
            .main .block-container { background-color: #0e1117; color: white; padding-top: 1rem; }
            [data-testid="metric-container"] { background-color: #262730; border: 1px solid #464854; color: white; }
            .stButton > button { background-color: #ff4b4b; color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #262730; }
            section[data-testid="stSidebar"] { background-color: #f0f2f6; }
            .main .block-container { background-color: #ffffff; color: #262730; padding-top: 1rem; }
            [data-testid="metric-container"] { background-color: #f0f2f6; border: 1px solid #d1d5db; color: #262730; }
            .stButton > button { background-color: #3498db; color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render the complete sidebar"""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏗️</div>
            <h2 style='color: #3498db; margin: 0; font-weight: bold;'>gcPanel</h2>
            <p style='color: #95a5a6; font-size: 0.9em; margin: 5px 0;'>Construction Management</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # User info or About section
        is_authenticated = st.session_state.get("authenticated", False)
        
        if is_authenticated:
            current_user = st.session_state.get("username", "Project Manager")
            user_role = st.session_state.get("user_role", "admin")
            st.markdown(f"**User:** {current_user}  \n**Role:** {user_role.title()}")
        else:
            st.markdown("### About gcPanel")
            st.markdown("""
            **gcPanel** is the industry-leading construction management platform.
            
            🏗️ **Features:**
            • Project Dashboard & Analytics
            • BIM Integration & Visualization  
            • Safety Management & Compliance
            • Cost Control & Budget Tracking
            • Document Management
            • Field Operations Support
            
            💼 **Perfect for:**
            • General Contractors • Project Managers
            • Construction Teams • Development Companies
            """)
            
            if st.button("🌐 Visit www.gcpanel.co", use_container_width=True, type="primary"):
                st.markdown("[Visit gcPanel.co](https://www.gcpanel.co)")
        
        st.divider()
        
        # Navigation Menu
        if is_authenticated:
            st.markdown("### Navigation")
            navigation_options = [
                "Dashboard", "Preconstruction", "Engineering", "Field Operations", 
                "Safety", "Contracts", "Cost Management", "BIM", "Closeout", 
                "Analytics", "Documents"
            ]
            
            current_menu = st.selectbox(
                "Select Module:",
                navigation_options,
                index=navigation_options.index(st.session_state.get("current_menu", "Dashboard")),
                key="navigation_select"
            )
            
            st.session_state["current_menu"] = current_menu
            
            st.divider()
            
            # Quick Actions
            st.markdown("### Quick Actions")
            if st.button("📊 View Reports", use_container_width=True):
                st.session_state["current_menu"] = "Analytics"
                st.rerun()
            
            if st.button("📋 Safety Check", use_container_width=True):
                st.session_state["current_menu"] = "Safety"
                st.rerun()
            
            if st.button("💰 Budget Review", use_container_width=True):
                st.session_state["current_menu"] = "Cost Management"
                st.rerun()
        
        st.divider()
        
        # Theme Toggle
        st.markdown("### 🎨 Theme")
        current_theme = st.session_state.get("theme", "dark")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", 
                        type="primary" if current_theme == "dark" else "secondary",
                        use_container_width=True):
                st.session_state.theme = "dark"
                st.rerun()
        
        with col2:
            if st.button("☀️ Light", 
                        type="primary" if current_theme == "light" else "secondary", 
                        use_container_width=True):
                st.session_state.theme = "light"
                st.rerun()

def render_login():
    """Render login form"""
    st.title("🏗️ gcPanel Login")
    st.subheader("Highland Tower Development")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            if username and password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = "admin"
                st.rerun()
            else:
                st.error("Please enter username and password")
    
    # Demo accounts
    st.divider()
    st.subheader("Demo Accounts")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💼 Project Manager", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Project Manager"
            st.session_state.user_role = "admin"
            st.rerun()
    
    with col2:
        if st.button("👷‍♂️ Superintendent", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Superintendent"
            st.session_state.user_role = "field"
            st.rerun()

def render_dashboard():
    """Render the main dashboard"""
    st.title("🏗️ Highland Tower Development Dashboard")
    
    # Project Overview Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Value", "$45.5M", "On Budget")
    with col2:
        st.metric("Progress", "67%", "2% this week")
    with col3:
        st.metric("Units Complete", "81/128", "5 this week")
    with col4:
        st.metric("Safety Score", "98%", "0.5% improvement")
    
    st.divider()
    
    # Recent Activity and Action Items
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Recent Activity")
        st.write("• Foundation inspection completed - Unit 12A")
        st.write("• MEP rough-in approved - Floors 8-10")
        st.write("• Concrete pour scheduled - Level B2")
        st.write("• Fire safety inspection passed - Retail spaces")
        st.write("• Final electrical inspection - Units 45-50")
    
    with col2:
        st.subheader("⚠️ Action Items")
        st.warning("🔧 HVAC system calibration due - Floor 15")
        st.info("📋 Weekly safety meeting - Tomorrow 9 AM")
        st.success("✅ Permit renewal submitted - On track")
        st.error("🚨 Weather delay possible - Monitor forecast")
    
    st.divider()
    
    # Progress Chart
    st.subheader("📊 Construction Progress")
    progress_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Interior', 'Exterior'],
        'Planned': [100, 100, 85, 45, 30],
        'Actual': [100, 98, 82, 42, 25]
    })
    
    fig = px.bar(progress_data, x='Phase', y=['Planned', 'Actual'], 
                title='Project Phase Progress (%)', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def render_main_content():
    """Render main content based on selected module"""
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    if current_menu == "Dashboard":
        render_dashboard()
    else:
        st.title(f"🔧 {current_menu}")
        st.info(f"The {current_menu} module is being developed. Coming soon!")
        
        # Module-specific placeholder content
        if current_menu == "Safety":
            st.subheader("Safety Overview")
            st.success("Zero incidents this month")
            st.write("Last safety meeting: January 15, 2025")
        elif current_menu == "Analytics":
            st.subheader("Project Analytics")
            st.write("Performance metrics and reporting tools")
        elif current_menu == "BIM":
            st.subheader("BIM Integration")
            st.write("3D model viewing and collaboration tools")

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply theme
    apply_theme()
    
    # Check authentication and render appropriate content
    if not st.session_state.get("authenticated", False):
        # Show sidebar for non-authenticated users
        render_sidebar()
        
        # Show login in main content
        render_login()
    else:
        # Show sidebar for authenticated users
        render_sidebar()
        
        # Show main content
        render_main_content()
        
        # Logout button in main area
        if st.button("🚪 Logout", key="logout_main"):
            for key in ["authenticated", "username", "user_role"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()