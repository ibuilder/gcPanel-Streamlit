"""
Login page for gcPanel with OAuth support.

This module provides a dedicated login page that includes support for
OAuth authentication with Google, Microsoft Office 365, and Procore.
"""

import streamlit as st
import os
from urllib.parse import parse_qs, urlparse

from components.oauth_login import render_oauth_login_page, handle_oauth_callback
from core.auth.oauth_providers import OAuthProvider

def login_page():
    """Render the login page with OAuth options."""
    
    # Note: page config is now set in the main app.py file
    # We don't need to set it again here
    
    # Apply custom styles
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    /* Hide default header, footer, and sidebar */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    
    /* Improve form spacing */
    div.stForm > div {
        padding-bottom: 10px;
    }
    button[kind="primaryFormSubmit"] {
        margin-top: 10px;
    }
    /* Better layout for the login page */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if this is an OAuth callback
    query_params = st.query_params
    if "code" in query_params and "state" in query_params:
        # Determine which provider this is based on URL path components
        current_url = st.get_option("server.baseUrlPath", "")
        provider = None
        
        if "google" in current_url:
            provider = OAuthProvider.GOOGLE
        elif "microsoft" in current_url:
            provider = OAuthProvider.MICROSOFT
        elif "procore" in current_url:
            provider = OAuthProvider.PROCORE
            
        if provider:
            code = query_params.get("code", [""])[0]
            state = query_params.get("state", [""])[0]
            
            from core.auth.oauth_callback_handler import handle_oauth_callback
            success, error = handle_oauth_callback(provider, code, state)
            
            if success:
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error(f"Login failed: {error}")
            
            return
    
    # Regular login page
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://i.imgur.com/XYYzKKy.png" alt="gcPanel Logo" style="max-width: 200px;">
        <h1 style="font-size: 2.5rem; margin-top: 10px;">Welcome to gcPanel</h1>
        <p style="font-size: 1.2rem; color: #666;">Construction Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main login container
    tabs = st.tabs(["Login", "Register"])
    
    with tabs[0]:
        # Use a simplified version without nested columns
        render_oauth_login_page()
    
    with tabs[1]:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2>Request Access</h2>
            <p>Registration for gcPanel is managed by your project administrator.</p>
            <p>If you need access, please contact your project manager or administrator with your:</p>
            <ul style="text-align: left;">
                <li>Full name</li>
                <li>Company</li>
                <li>Position/role</li>
                <li>Corporate email address</li>
            </ul>
            <p>Once added to the project directory, you'll be able to sign in using your corporate email address.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #999; font-size: 0.8rem;">
        <p>© 2025 gcPanel Construction Management. All rights reserved.</p>
        <p><a href="#" style="color: #999;">Privacy Policy</a> | <a href="#" style="color: #999;">Terms of Service</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()