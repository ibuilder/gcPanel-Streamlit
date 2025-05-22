"""
Simple login form component for gcPanel.

This module provides a basic login form that accepts admin/admin123 and
demo/demo123 credentials for testing purposes.
"""

import streamlit as st
import time

def render_login_form():
    """Render a simple login form with admin and demo account support."""
    
    # Login header
    st.markdown("<h2 style='text-align: center; margin-bottom: 25px; color: #333; font-weight: 600;'>Project Access</h2>", 
                unsafe_allow_html=True)
    
    # Simple login form
    username = st.text_input("Email or Username", help="Try 'admin' or 'demo'")
    password = st.text_input("Password", type="password", help="Try 'admin123' or 'demo123'")
    
    # Remember me checkbox
    remember = st.checkbox("Remember me", value=False)
    
    # Login button outside of a form to avoid any potential issues
    if st.button("Sign In", use_container_width=True, type="primary"):
        if not username or not password:
            st.error("Please enter both username/email and password")
        else:
            # Admin login
            if username.lower() == "admin" and password == "admin123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "admin",
                    "email": "admin@gcpanel.com",
                    "full_name": "Admin User",
                    "role": "admin"
                }
                st.success("Login successful! Redirecting to dashboard...")
                time.sleep(1)
                st.rerun()
            # Demo login
            elif username.lower() == "demo" and password == "demo123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    "username": "demo",
                    "email": "demo@gcpanel.com",
                    "full_name": "Demo User",
                    "role": "viewer"
                }
                st.success("Login successful! Redirecting to dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    # Display "forgot password" link
    st.markdown('<div style="text-align: right;"><a href="#" style="color: #2b579a; font-size: 0.9rem;">Forgot password?</a></div>', 
                unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div style="margin: 25px 0; text-align: center; color: #666; position: relative;">'
                '<hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">'
                '<span style="position: absolute; top: -10px; background: white; padding: 0 10px;">OR</span>'
                '</div>', 
                unsafe_allow_html=True)