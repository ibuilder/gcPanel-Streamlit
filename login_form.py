"""
Login form component for gcPanel.

This module provides a comprehensive login form that supports multiple user roles
with different permission levels for testing the application.
"""

import streamlit as st
import time

def render_login_form():
    """Render a login form with multi-role support."""
    
    # Login header
    st.markdown("<h2 style='text-align: center; margin-bottom: 25px; color: #333; font-weight: 600;'>Project Access</h2>", 
                unsafe_allow_html=True)
    
    # Multi-tab interface with demo accounts first
    demo_tab, login_tab = st.tabs(["Demo Accounts", "Login"])
    
    with login_tab:
        # Standard login form
        username = st.text_input("Email or Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        
        # Remember me checkbox
        remember = st.checkbox("Remember me", value=False)
        
        # Login button
        if st.button("Sign In", use_container_width=True, type="primary", key="signin_btn"):
            if not username or not password:
                st.error("Please enter both username/email and password")
            else:
                # Store the form submission in session state for processing in the main app
                st.session_state.login_username = username
                st.session_state.login_password = password
                st.session_state.login_form_submitted = True
                
                # Show a loading message
                st.success("Authenticating... Please wait.")
                time.sleep(0.5)
                st.rerun()
        
        # Display "forgot password" link
        st.markdown('<div style="text-align: right;"><a href="#" style="color: #2b579a; font-size: 0.9rem;">Forgot password?</a></div>', 
                    unsafe_allow_html=True)
    
    with demo_tab:
        st.markdown("### Demo Account Options")
        st.markdown("Use these accounts to test different permission levels:")
        
        # Create a clean table for demo accounts
        demo_accounts = [
            {"Role": "Admin", "Username": "admin", "Password": "admin123", "Access": "Full system access"},
            {"Role": "Project Manager", "Username": "pm", "Password": "pm123", "Access": "Full project access"},
            {"Role": "Superintendent", "Username": "super", "Password": "super123", "Access": "Field operations focus"},
            {"Role": "Estimator", "Username": "estimator", "Password": "est123", "Access": "Cost management focus"},
            {"Role": "Architect", "Username": "architect", "Password": "arch123", "Access": "Design focus"},
            {"Role": "Engineer", "Username": "engineer", "Password": "eng123", "Access": "Engineering focus"},
            {"Role": "Subcontractor", "Username": "sub", "Password": "sub123", "Access": "Limited access"},
            {"Role": "Owner", "Username": "owner", "Password": "owner123", "Access": "Owner view"},
            {"Role": "Viewer", "Username": "demo", "Password": "demo123", "Access": "View-only access"}
        ]
        
        # Display as a more compact clickable cards
        cols = st.columns(3)
        for i, account in enumerate(demo_accounts):
            with cols[i % 3]:
                card_html = f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f8f9fa;">
                    <strong style="color: #333;">{account['Role']}</strong><br>
                    <span style="color: #666; font-size: 0.9rem;">User: <code>{account['Username']}</code><br>
                    Pass: <code>{account['Password']}</code></span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(f"Login as {account['Role']}", key=f"demo_login_{i}", use_container_width=True):
                    # Store the form submission in session state for processing in the main app
                    st.session_state.login_username = account['Username']
                    st.session_state.login_password = account['Password']
                    st.session_state.login_form_submitted = True
                    
                    # Show a loading message
                    st.success(f"Logging in as {account['Role']}... Please wait.")
                    time.sleep(0.5)
                    st.rerun()
    
    # Divider
    st.markdown('<div style="margin: 25px 0; text-align: center; color: #666; position: relative;">'
                '<hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">'
                '<span style="position: absolute; top: -10px; background: white; padding: 0 10px;">OR</span>'
                '</div>', 
                unsafe_allow_html=True)
                
    # OAuth buttons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <button style="width: 100%; padding: 10px; background-color: #4285F4; color: white; border: none; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" style="height: 18px; margin-right: 10px;">
                Sign in with Google
            </button>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <button style="width: 100%; padding: 10px; background-color: #0A66C2; color: white; border: none; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" style="height: 18px; margin-right: 10px; background: white; border-radius: 2px;">
                Sign in with LinkedIn
            </button>
            """,
            unsafe_allow_html=True
        )