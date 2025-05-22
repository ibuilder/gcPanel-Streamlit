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
        background-color: #f7f7f7;
        background-image: url('https://www.transparenttextures.com/patterns/concrete-wall-2.png');
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
        background-color: #f9a01b !important;
        color: white !important;
        font-weight: 600 !important;
    }
    button[kind="primaryFormSubmit"]:hover {
        background-color: #e99010 !important;
    }
    /* Better layout for the login page */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    
    /* Construction-themed elements */
    .login-card {
        background-color: white;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-top: 5px solid #f9a01b;
    }
    
    /* Custom tabs styling */
    button[role="tab"] {
        font-weight: 600 !important;
        color: #555 !important;
    }
    button[role="tab"][aria-selected="true"] {
        color: #f9a01b !important;
    }
    [data-testid="stTabContent"] {
        padding: 20px;
        background-color: white;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
    
    # Regular login page with construction theme
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="position: relative; display: inline-block;">
            <img src="https://i.imgur.com/XYYzKKy.png" alt="gcPanel Logo" style="max-width: 200px;">
            <div style="position: absolute; top: -20px; right: -15px;">
                <svg width="50" height="50" viewBox="0 0 24 24" fill="#f9a01b">
                    <path d="M19.92,9.27C19.97,9.14 20,9 20,8.86C20,8.69 19.96,8.53 19.88,8.4C19.74,8.17 19.49,8 19.2,8H19V7.79C19,7.35 18.65,7 18.21,7H5.79C5.35,7 5,7.35 5,7.79V8H4.8C4.34,8 3.97,8.37 3.97,8.83C3.97,9 4.02,9.18 4.12,9.34C4.25,9.53 4.46,9.67 4.7,9.7V10H4.8C4.42,10 4.12,10.3 4.12,10.68C4.12,10.83 4.17,10.98 4.26,11.1C4.42,11.29 4.65,11.4 4.9,11.4V13.06C4.5,13.13 4.22,13.5 4.22,13.91C4.22,14.28 4.43,14.59 4.74,14.71C4.85,14.76 4.96,14.78 5.08,14.78H5.91V15H5.25C4.84,15 4.5,15.34 4.5,15.75C4.5,16.16 4.84,16.5 5.25,16.5H8L8.05,19.04L9.55,19L9.5,16.5H14.5L14.45,19.04L15.95,19L16,16.5H19.5C19.91,16.5 20.25,16.16 20.25,15.75C20.25,15.34 19.91,15 19.5,15H18.75V14.78H19.95C20.36,14.78 20.7,14.44 20.7,14.03C20.7,13.62 20.36,13.28 19.95,13.28H19V11.4C19.35,11.4 19.63,11.12 19.63,10.77C19.63,10.58 19.54,10.41 19.41,10.3C19.31,10.21 19.18,10.16 19.04,10.15C19.04,10.1 19,10.05 19,10H19.2C19.54,10 19.81,9.73 19.81,9.39C19.81,9.34 19.83,9.32 19.82,9.27H19.92M17.5,15H7.5V10H17.5V15Z" />
                </svg>
            </div>
        </div>
        <h1 style="font-size: 2.5rem; margin-top: 10px;">
            <span style="color: #2b579a; font-weight: 700;">gc</span><span style="color: #333; font-weight: 700;">Panel</span>
        </h1>
        <div style="display: flex; justify-content: center; margin-top: -5px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; background-color: #f9a01b; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                <svg style="margin-right: 5px;" width="16" height="16" viewBox="0 0 24 24" fill="white">
                    <path d="M14,6L10.25,11L13.1,14.8L11.5,16L7,11L11,6H14M19,6L14.7,11L13.1,14.8L14.7,16L19,11L19,6H19M6.83,16H19V18H6.83L6.83,16Z"/>
                </svg>
                Highland Tower Development
            </div>
        </div>
        <p style="font-size: 1.2rem; color: #666; max-width: 450px; margin: 0 auto;">Your centralized platform for construction project management and collaboration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main login container
    tabs = st.tabs(["Login", "Register"])
    
    with tabs[0]:
        # Use the simple login form instead of the nested columns version
        from login_form import render_login_form
        render_login_form()
        
        # Add OAuth buttons directly
        from components.oauth_login import render_oauth_buttons
        render_oauth_buttons()
        
        # Add the gcPanel information
        st.markdown("""
        <div style="text-align: center; margin-top: 25px; padding: 15px; background-color: #f7f7f7; border-radius: 6px; border-left: 4px solid #f9a01b;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="#555" style="margin-right: 8px;">
                    <path d="M13,9H11V7H13V9M13,17H11V11H13V17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
                </svg>
                <span style="font-weight: 600; color: #444;">New to gcPanel?</span>
            </div>
            <p style="color: #666; font-size: 0.9rem;">Get more information at <a href="http://www.gcpanel.co" target="_blank" style="color: #2b579a; font-weight: 500;">www.gcPanel.co</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("""
        <div style="padding: 20px 15px; background-color: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.07);">
            <!-- Construction-themed icon for registration -->
            <div style="text-align: center; margin-bottom: 25px;">
                <div style="display: inline-block; background-color: #2b579a; color: white; border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
                        <path d="M12,15C7.58,15 4,16.79 4,19V21H20V19C20,16.79 16.42,15 12,15M8,9A4,4 0 0,0 12,13A4,4 0 0,0 16,9M11.5,2C11.2,2 11,2.21 11,2.5V5.5H10V3C10,2.45 10.45,2 11,2H13C13.55,2 14,2.45 14,3V5.5H13V2.5C13,2.21 12.8,2 12.5,2H11.5Z" />
                    </svg>
                </div>
            </div>

            <h2 style="text-align: center; color: #333; font-weight: 600; margin-bottom: 20px;">Request Project Access</h2>
            
            <div style="background-color: #f5f5f5; border-left: 4px solid #2b579a; padding: 15px; margin-bottom: 20px; border-radius: 0 4px 4px 0;">
                <p style="margin: 0; color: #555;"><strong>Note:</strong> Registration for Highland Tower Development is managed by your project administrator.</p>
            </div>
            
            <p style="color: #444;">To request access, please contact your project manager with the following information:</p>
            
            <div style="background-color: #f9f9f9; border-radius: 6px; padding: 15px; margin-top: 10px;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; justify-content: center; background-color: #f9a01b; width: 24px; height: 24px; border-radius: 50%; margin-right: 10px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
                            <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
                        </svg>
                    </div>
                    <div><strong>Full Name & Professional Credentials</strong></div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; justify-content: center; background-color: #f9a01b; width: 24px; height: 24px; border-radius: 50%; margin-right: 10px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
                            <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z" />
                        </svg>
                    </div>
                    <div><strong>Company Name & Address</strong></div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; justify-content: center; background-color: #f9a01b; width: 24px; height: 24px; border-radius: 50%; margin-right: 10px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
                            <path d="M12,15C13.66,15 15,13.66 15,12C15,10.34 13.66,9 12,9C10.34,9 9,10.34 9,12C9,13.66 10.34,15 12,15M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z" />
                        </svg>
                    </div>
                    <div><strong>Project Role & Responsibilities</strong></div>
                </div>
                
                <div style="display: flex; align-items: center;">
                    <div style="display: flex; align-items: center; justify-content: center; background-color: #f9a01b; width: 24px; height: 24px; border-radius: 50%; margin-right: 10px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
                            <path d="M20,8L12,13L4,8V6L12,11L20,6M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4Z" />
                        </svg>
                    </div>
                    <div><strong>Corporate Email Address</strong></div>
                </div>
            </div>
            
            <div style="margin-top: 25px; text-align: center;">
                <div style="display: inline-block; background-color: #f5f5f5; padding: 12px 20px; border-radius: 6px; border: 1px dashed #ccc;">
                    <div style="display: flex; align-items: center; color: #555;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="#555" style="margin-right: 8px;">
                            <path d="M12,3C7.46,3 3.34,4.78 0.29,7.67C0.11,7.85 0,8.1 0,8.38C0,8.66 0.11,8.91 0.29,9.09L2.77,11.57C2.95,11.75 3.2,11.86 3.5,11.86C3.75,11.86 4,11.75 4.18,11.58C4.97,10.84 5.87,10.22 6.84,9.73C7.17,9.57 7.4,9.23 7.4,8.83V5.73C8.85,5.25 10.39,5 12,5C13.59,5 15.14,5.25 16.59,5.72V8.82C16.59,9.21 16.82,9.56 17.15,9.72C18.13,10.21 19,10.84 19.82,11.57C20,11.75 20.25,11.85 20.5,11.85C20.8,11.85 21.05,11.74 21.23,11.56L23.71,9.08C23.89,8.9 24,8.65 24,8.37C24,8.09 23.88,7.85 23.7,7.67C20.65,4.78 16.53,3 12,3M9,7V10C9,10 3,15 3,18V22H21V18C21,15 15,10 15,10V7H13V9H11V7H9Z" />
                        </svg>
                        Once approved, you'll receive login credentials via email
                    </div>
                </div>
            </div>
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