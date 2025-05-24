"""
Sidebar-based layout for Highland Tower Development gcPanel.

This module provides a clean, stable sidebar layout using Streamlit's
default components to eliminate customization issues.
"""

import streamlit as st

def render_sidebar():
    """Render the sidebar with logo, project info, and navigation."""
    
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
        
        # User Information
        current_user = st.session_state.get("username", "Project Manager")
        user_role = st.session_state.get("user_role", "admin")
        
        st.markdown(f"""
        **User:** {current_user}  
        **Role:** {user_role.title()}
        """)
        
        st.divider()
        
        # Navigation Menu
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
        
        # Update session state with selected menu
        st.session_state["current_menu"] = current_menu
        
        st.divider()
        
        # Quick Actions
        st.markdown("### Quick Actions")
        if st.button("📊 View Reports", use_container_width=True, key="sidebar_reports"):
            st.session_state["current_menu"] = "Analytics"
            st.rerun()
        
        if st.button("📋 Safety Check", use_container_width=True, key="sidebar_safety"):
            st.session_state["current_menu"] = "Safety"
            st.rerun()
        
        if st.button("💰 Budget Review", use_container_width=True, key="sidebar_budget"):
            st.session_state["current_menu"] = "Cost Management"
            st.rerun()
        
        st.divider()
        
        # Light/Dark Theme Toggle at bottom of sidebar
        st.markdown("### 🎨 Theme")
        
        current_theme = st.session_state.get("theme", "dark")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌙 Dark", 
                        type="primary" if current_theme == "dark" else "secondary",
                        use_container_width=True,
                        key="theme_dark"):
                st.session_state.theme = "dark"
                st.rerun()
        
        with col2:
            if st.button("☀️ Light", 
                        type="primary" if current_theme == "light" else "secondary", 
                        use_container_width=True,
                        key="theme_light"):
                st.session_state.theme = "light"
                st.rerun()

def apply_sidebar_theme():
    """Apply theme styling based on user selection."""
    current_theme = st.session_state.get("theme", "dark")
    
    if current_theme == "dark":
        st.markdown("""
        <style>
            /* Dark theme */
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
                padding-top: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
                max-width: 100%;
            }
            
            /* Button styling */
            .stButton > button {
                background-color: #ff4b4b;
                color: white;
                border: none;
                border-radius: 5px;
                width: 100%;
            }
            
            .stButton > button:hover {
                background-color: #ff6c6c;
            }
            
            /* Form elements dark */
            .stSelectbox > div > div {
                background-color: #262730;
                color: white;
                border: 1px solid #464854;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Light theme */
            .stApp {
                background-color: #ffffff;
                color: #262730;
            }
            
            /* Sidebar light */
            section[data-testid="stSidebar"] {
                background-color: #f0f2f6;
            }
            
            /* Main content area */
            .main .block-container {
                background-color: #ffffff;
                color: #262730;
                padding-top: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
                max-width: 100%;
            }
            
            /* Button styling */
            .stButton > button {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                width: 100%;
            }
            
            .stButton > button:hover {
                background-color: #2980b9;
            }
            
            /* Form elements light */
            .stSelectbox > div > div {
            background-color: #34495e;
            color: white;
            border: 1px solid #3498db;
        }
        
        /* Metrics styling */
        [data-testid="metric-container"] {
            background-color: #2d3e50;
            border: 1px solid #34495e;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)