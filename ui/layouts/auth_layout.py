"""
Authentication Layout for gcPanel
Clean login interface with Highland Tower branding
"""

import streamlit as st
from core.app_state import AppStateManager

def render_login_page():
    """Render clean, professional login page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #60a5fa; font-size: 3rem; margin-bottom: 0.5rem;">gcPanel</h1>
        <h2 style="color: #94a3b8; font-size: 1.5rem; margin-bottom: 2rem;">Highland Tower Development</h2>
        <p style="color: #64748b; font-size: 1.1rem;">Enterprise Construction Management Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Project Access")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.form_submit_button("Access Project Dashboard", use_container_width=True)
            
            if login_button:
                state_manager = AppStateManager()
                if state_manager.authenticate_user(username, password):
                    st.success("✅ Access granted! Loading project dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        # Login help
        with st.expander("Login Information"):
            st.markdown("""
            **Available Access Levels:**
            - **admin** / admin123 - Full system access
            - **manager** / manager123 - Project management access  
            - **user** / user123 - Standard user access
            
            **Project Details:**
            - Highland Tower Development
            - $45.5M Mixed-Use Project
            - 120 Residential + 8 Retail Units
            """)