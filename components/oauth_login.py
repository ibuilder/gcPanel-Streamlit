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
            "bgcolor": "#4285F4",
            "color": "white",
            "icon": "https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
        },
        "microsoft": {
            "bgcolor": "#2F2F2F",
            "color": "white",
            "icon": "https://logincdn.msauth.net/shared/1.0/content/images/favicon_a_eupayfgghqiai7k9sol6eih2.ico"
        },
        "procore": {
            "bgcolor": "#F56B46",
            "color": "white",
            "icon": "https://cdn.procore.com/images/favicon.ico"
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
                           border: none; padding: 10px 15px; border-radius: 5px; width: 100%;
                           cursor: pointer; display: flex; align-items: center; justify-content: center;"
                >
                    <img src="{style['icon']}" style="height: 20px; margin-right: 10px;"/>
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
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-header img {
        max-width: 200px;
        margin-bottom: 1rem;
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
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login container
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <img src="https://gcpanel.com/logo" alt="gcPanel Logo">
            <h2>Welcome to gcPanel</h2>
            <p>Sign in to access your construction management dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Email and password form
        with st.form("login_form"):
            st.text_input("Email", placeholder="Enter your email")
            st.text_input("Password", placeholder="Enter your password", type="password")
            
            # Remember me and forgot password
            cols = st.columns([1, 1])
            with cols[0]:
                st.checkbox("Remember me")
            with cols[1]:
                st.markdown('<div style="text-align: right;"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)
            
            # Submit button
            st.form_submit_button("Sign In", use_container_width=True)
        
        # Divider
        st.markdown('<div class="divider"><span>OR</span></div>', unsafe_allow_html=True)
        
        # OAuth buttons
        render_oauth_buttons()
        
        # Registration link
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p>Don't have an account? <a href="#">Contact your project administrator</a></p>
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