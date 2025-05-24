"""
gcPanel Construction Management Dashboard - Fixed Layout Version
Highland Tower Development - $45.5M Mixed-Use Project
"""

import streamlit as st
import logging
import os
from utils.ui_manager import set_page_config
import app_manager

# Setup page configuration
set_page_config()

def main():
    """Main application with fixed layout."""
    
    # Initialize session state
    app_manager.initialize_session_state()
    
    # Check authentication status
    is_authenticated = st.session_state.get("authenticated", False)
    
    # Apply clean layout CSS based on authentication status
    if is_authenticated:
        # Clean layout with visible sidebar for authenticated users
        st.markdown("""
        <style>
        /* Remove empty divs and clean spacing */
        .main .block-container {
            padding-top: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Hide empty containers that create extra spacing */
        .stApp > div:empty {
            display: none !important;
        }
        
        .stApp > div > div:empty {
            display: none !important;
        }
        
        /* Ensure sidebar is visible and properly styled */
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
        
        .css-1d391kg {
            background-color: #1e2228 !important;
            padding-top: 1rem !important;
        }
        
        /* Clean header area */
        .stApp > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Dark theme styling */
        .stApp {
            background-color: #0e1117 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Hide sidebar on login page
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        
        .main .block-container {
            padding-top: 0rem !important;
            max-width: 100% !important;
        }
        
        .stApp > div:empty {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Handle authentication
    if not is_authenticated:
        render_login_page()
    else:
        render_authenticated_app()

def render_login_page():
    """Render clean login page."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e2228 0%, #2d3748 100%); 
                padding: 40px; border-radius: 15px; margin: 2rem auto; 
                max-width: 500px; text-align: center;">
        <h1 style="color: #4CAF50; margin-bottom: 30px;">🏗️ gcPanel</h1>
        <h2 style="color: white; margin-bottom: 20px;">Highland Tower Development</h2>
        <p style="color: #B0BEC5;">$45.5M Mixed-Use Development | 120 Units + 8 Retail</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple login form
    with st.form("login_form"):
        st.markdown("### Login to Continue")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_button = st.form_submit_button("🔑 Login", use_container_width=True)
        
        if login_button:
            if username and password:
                # Simple authentication (replace with real auth)
                if username.lower() in ["admin", "demo", "user"]:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = "admin" if username.lower() == "admin" else "user"
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Please enter both username and password")

def render_authenticated_app():
    """Render the main authenticated application."""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e2228 0%, #2d3748 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; color: #4CAF50;">🏗️ gcPanel - Highland Tower Development</h1>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div>
                <span style="color: #B0BEC5;">Progress: 72.3% | Budget: 96.8% | Safety: 98.2%</span>
            </div>
            <div style="color: #B0BEC5;">
                👤 {st.session_state.get('username', 'User')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="background: #1e2228; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #4CAF50; margin: 0 0 10px 0;">Highland Tower</h3>
            <p style="color: #B0BEC5; margin: 0; font-size: 14px;">
                📍 Highland District<br>
                🏢 15 Floors + 2 Basement<br>
                🏠 120 Units + 8 Retail<br>
                💰 $45.5M Project Value
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Navigation")
        
        # Navigation buttons
        menu_options = [
            "🏗️ Dashboard",
            "📊 Analytics", 
            "📋 Preconstruction",
            "⚙️ Engineering",
            "🏗️ Field Operations",
            "⚠️ Safety Management",
            "📄 Contracts",
            "💰 Cost Management",
            "🏢 BIM & 3D Models",
            "✅ Project Closeout",
            "📁 Document Center"
        ]
        
        for option in menu_options:
            if st.button(option, key=f"nav_{option}", use_container_width=True):
                st.session_state.current_menu = option
                st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content area
    current_menu = st.session_state.get('current_menu', '🏗️ Dashboard')
    
    if current_menu == '🏗️ Dashboard':
        render_dashboard()
    else:
        st.markdown(f"## {current_menu}")
        st.info(f"This is the {current_menu} module. Content will be loaded here.")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Progress", "72.3%", "2.1%")
        with col2:
            st.metric("Budget Status", "96.8%", "-1.2%") 
        with col3:
            st.metric("Safety Score", "98.2", "0.5")
        with col4:
            st.metric("Active Items", "12", "+3")

def render_dashboard():
    """Render the main dashboard."""
    st.markdown("## 🏗️ Project Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Progress", "72.3%", "2.1%")
    with col2:
        st.metric("Budget Efficiency", "96.8%", "-1.2%")
    with col3:
        st.metric("Safety Rating", "98.2", "0.5")
    with col4:
        st.metric("Active RFIs", "12", "+3")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Recent Activity")
        activities = [
            "🆕 RFI-2025-045: Electrical outlet placement - Floor 12",
            "✅ Quality check completed: Floor 14 concrete pour",
            "📦 Material delivery: Steel beams for Floor 15",
            "⚠️ Safety inspection: All areas passed"
        ]
        
        for activity in activities:
            st.markdown(f"• {activity}")
    
    with col2:
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("📝 New Daily Report", use_container_width=True):
            st.success("Opening Daily Report form...")
        
        if st.button("❓ Submit RFI", use_container_width=True):
            st.success("Opening RFI submission form...")
        
        if st.button("📸 Photo Documentation", use_container_width=True):
            st.success("Opening photo documentation...")
        
        if st.button("📊 View Reports", use_container_width=True):
            st.success("Opening analytics dashboard...")

if __name__ == "__main__":
    main()