"""
OAuth login component for gcPanel.

This module provides a login interface with OAuth provider buttons
for Google, Microsoft Office 365, and Procore.
"""

import streamlit as st
from typing import Dict, Optional
import os

from core.auth.oauth_providers import OAuthProvider, is_oauth_configured
from core.auth.oauth_service import get_authorization_url

def render_oauth_buttons():
    """
    Render OAuth login buttons for configured providers.
    
    Displays login buttons for Google, Microsoft Office 365, and Procore
    if they are configured in the environment.
    """
    # Check which providers are configured
    providers = [
        (OAuthProvider.GOOGLE, "Google", "google"),
        (OAuthProvider.MICROSOFT, "Microsoft Office 365", "microsoft"),
        (OAuthProvider.PROCORE, "Procore", "procore")
    ]
    
    # Define button styles
    button_styles = {
        "google": {
            "bgcolor": "#FFFFFF",
            "color": "#757575",
            "border": "1px solid #DADCE0",
            "icon": "https://developers.google.com/identity/images/g-logo.png",
            "hover": "background-color: #F5F5F5"
        },
        "microsoft": {
            "bgcolor": "#2F2F2F",
            "color": "white",
            "border": "none",
            "icon": "https://logincdn.msauth.net/shared/1.0/content/images/microsoft_logo_ee5c8d9fb6248c938fd0dc19370e90bd.svg",
            "hover": "background-color: #444444"
        },
        "procore": {
            "bgcolor": "#F9A01B",
            "color": "white",
            "border": "none",
            "icon": "https://assets.procore.com/images/favicon.ico",
            "hover": "background-color: #E99010"
        }
    }
    
    # Container for the OAuth buttons
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <p>Or sign in with:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the configured provider buttons
    for provider, name, key in providers:
        if is_oauth_configured(provider):
            render_oauth_button(provider, name, button_styles[key])
        else:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 10px; opacity: 0.5;">
                <button 
                    style="background-color: #f0f0f0; color: #666; border: none; padding: 10px 15px; 
                           border-radius: 5px; width: 100%; cursor: not-allowed; display: flex; 
                           align-items: center; justify-content: center;"
                    disabled
                >
                    <span>{name} (Not Configured)</span>
                </button>
            </div>
            """, unsafe_allow_html=True)

def render_oauth_button(provider: OAuthProvider, name: str, style: Dict[str, str]):
    """
    Render a single OAuth button with proper styling.
    
    Args:
        provider: The OAuth provider
        name: Display name for the button
        style: Dictionary with style information
    """
    # Get the authorization URL
    auth_url, state = get_authorization_url(provider)
    
    if auth_url and state:
        # Store state in session for validation in callback
        if "oauth_states" not in st.session_state:
            st.session_state.oauth_states = {}
        st.session_state.oauth_states[provider.value] = state
        
        # Render the button
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;">
            <a href="{auth_url}" target="_self" style="text-decoration: none; width: 100%;">
                <button 
                    style="background-color: {style['bgcolor']}; color: {style['color']}; 
                           border: {style.get('border', 'none')}; padding: 12px 15px; 
                           border-radius: 4px; width: 100%; font-weight: 500;
                           cursor: pointer; display: flex; align-items: center; 
                           justify-content: center; transition: all 0.2s ease;
                           box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
                    onmouseover="this.style.{style.get('hover', 'opacity: 0.9')}"
                    onmouseout="this.style.backgroundColor='{style['bgcolor']}'"
                >
                    <img src="{style['icon']}" style="height: 20px; margin-right: 10px; vertical-align: middle;"/>
                    <span>Continue with {name}</span>
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Could not generate authentication URL for {name}")

def render_oauth_login_page():
    """
    Render a complete login page with OAuth options.
    
    This displays a professionally styled login page with both
    traditional login form and OAuth login buttons.
    """
    # Apply custom styling
    st.markdown("""
    <style>
    .login-container {
        padding: 1rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .divider {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e0e0e0;
    }
    .divider span {
        padding: 0 1rem;
        color: #666;
        font-size: 0.875rem;
        background-color: white;
    }
    
    /* Construction-themed elements */
    .construction-icon {
        display: inline-block;
        margin-right: 5px;
        vertical-align: middle;
    }
    
    /* Form styling */
    input[type="text"], input[type="password"] {
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        padding: 12px 10px !important;
        background-color: #f9f9f9 !important;
    }
    
    input[type="text"]:focus, input[type="password"]:focus {
        border-color: #f9a01b !important;
        box-shadow: 0 0 0 1px #f9a01b !important;
    }
    
    .oauth-button {
        margin-bottom: 10px;
        padding: 10px;
        transition: all 0.2s ease;
    }
    
    .oauth-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login header - simplified without icon
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 25px; color: #333; font-weight: 600;">Project Access</h2>
    """, unsafe_allow_html=True)
    
    # Email and password form with functional login
    with st.form("login_form"):
        username = st.text_input("Email or Username", key="login_username", placeholder="Enter your email or username")
        password = st.text_input("Password", key="login_password", placeholder="Enter your password", type="password")
        
        # Remember me and forgot password in a single row
        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me", key="remember_me")
        with col2:
            st.markdown('<div style="text-align: right;"><a href="#" style="color: #2b579a;">Forgot password?</a></div>', unsafe_allow_html=True)
        
        # Submit button 
        submit_clicked = st.form_submit_button("Sign In", use_container_width=True)
        
        # Process form submission
        if submit_clicked:
            if not username or not password:
                st.error("Please enter both username/email and password")
            else:
                # Store credentials in session state for processing
                st.session_state.login_username = username
                st.session_state.login_password = password
                st.session_state.login_form_submitted = True
                
                # Show a message and trigger the rerun
                st.success("Signing in...")
                st.rerun()
    
    # Divider with construction theme
    st.markdown("""
    <div class="divider">
        <span style="display: flex; align-items: center;">
            <svg class="construction-icon" width="16" height="16" viewBox="0 0 24 24" fill="#666">
                <path d="M6,2C4.89,2 4,2.89 4,4V20A2,2 0 0,0 6,22H10V20.09L12.09,18H16.9L19,15.9V4C19,2.89 18.1,2 17,2H6M6,4H17V16H11.91L10,17.91V16H6V4M8,6V12H16V6H8Z" />
            </svg>
            CORPORATE LOGIN
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # OAuth buttons
    render_oauth_buttons()
    
    # Project access info with construction theme
    st.markdown("""
    <div style="text-align: center; margin-top: 25px; padding: 15px; background-color: #f7f7f7; border-radius: 6px; border-left: 4px solid #f9a01b;">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#555" style="margin-right: 8px;">
                <path d="M13,9H11V7H13V9M13,17H11V11H13V17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
            </svg>
            <span style="font-weight: 600; color: #444;">New to Highland Tower Development?</span>
        </div>
        <p style="color: #666; font-size: 0.9rem;">Contact your project manager to request access credentials</p>
    </div>
    """, unsafe_allow_html=True)

def handle_oauth_callback():
    """
    Handle the OAuth callback from the provider.
    
    This function processes the callback URL and exchanges the authorization code
    for an access token, then retrieves the user information and creates or
    logs in the user.
    """
    import streamlit as st
    from urllib.parse import urlparse, parse_qs
    
    # Get the current URL
    query_params = st.experimental_get_query_params()
    
    # Check if this is a callback (has code and state)
    if "code" in query_params and "state" in query_params:
        code = query_params["code"][0]
        state = query_params["state"][0]
        
        # Determine which provider this is for
        provider = None
        path = urlparse(st.get_option("server.baseUrlPath")).path
        
        if path.endswith("/google"):
            provider = OAuthProvider.GOOGLE
        elif path.endswith("/microsoft"):
            provider = OAuthProvider.MICROSOFT
        elif path.endswith("/procore"):
            provider = OAuthProvider.PROCORE
        
        if provider:
            # Check if state matches what we stored
            if "oauth_states" in st.session_state:
                stored_state = st.session_state.oauth_states.get(provider.value)
                
                if stored_state != state:
                    st.error("Invalid OAuth state. Please try again.")
                    return
            else:
                st.error("OAuth state not found. Please try again.")
                return
            
            # Process the OAuth flow
            from core.auth.oauth_service import get_token, get_user_info, authenticate_or_create_user
            
            # Get the full callback URL
            full_url = f"{st.get_option('server.baseUrlPath')}?{st.get_option('server.queryString')}"
            
            # Get access token
            token = get_token(provider, full_url, state)
            
            if not token:
                st.error(f"Failed to get access token from {provider.value}. Please try again.")
                return
            
            # Get user info
            userinfo = get_user_info(provider, token)
            
            if not userinfo:
                st.error(f"Failed to get user information from {provider.value}. Please try again.")
                return
            
            # Authenticate or create user
            user, tokens, error = authenticate_or_create_user(provider, userinfo)
            
            if error:
                st.error(error)
                return
            
            # Store authentication in session state
            st.session_state.authenticated = True
            st.session_state.user = user
            if tokens and "access_token" in tokens:
                st.session_state.token = tokens["access_token"]
            st.session_state.current_menu = "Dashboard"
            
            # Clear query parameters by redirecting
            st.query_params.clear()
            st.rerun()