"""
OAuth callback handler for gcPanel.

This module handles OAuth callbacks from providers including Google,
Microsoft Office 365, and Procore, providing user authentication and
automatic account creation for project directory members.
"""

import logging
import streamlit as st
from typing import Optional, Dict, Any, Tuple

from core.auth.oauth_providers import OAuthProvider, is_oauth_configured
from core.auth.oauth_service import get_token, get_user_info, authenticate_or_create_user
from core.auth.auth_service import generate_tokens
from core.repository.project_directory_repository import ProjectDirectoryRepository
from core.auth.user_repository import UserRepository

# Set up logging
logger = logging.getLogger(__name__)

def handle_oauth_callback(provider: OAuthProvider, code: str, state: str) -> Tuple[bool, Optional[str]]:
    """
    Handle the OAuth callback for the specified provider.
    
    Args:
        provider: The OAuth provider
        code: The authorization code
        state: The state from the authorization request
        
    Returns:
        Tuple[bool, str]: Success status and error message (if any)
    """
    try:
        # Check if we have stored state to compare against
        if "oauth_states" not in st.session_state or provider.value not in st.session_state.oauth_states:
            return False, "Invalid OAuth state. Please try again."
        
        # Verify state matches
        stored_state = st.session_state.oauth_states[provider.value]
        if stored_state != state:
            return False, "State mismatch in OAuth callback. Please try again."
        
        # Get full callback URL
        callback_url = build_callback_url(provider, code, state)
        
        # Exchange code for access token
        token = get_token(provider, callback_url, state)
        if not token:
            return False, f"Failed to get access token from {provider.value}. Please try again."
        
        # Get user info
        userinfo = get_user_info(provider, token)
        if not userinfo:
            return False, f"Failed to get user information from {provider.value}. Please try again."
        
        # Authenticate or create user
        user, tokens, error = authenticate_or_create_user(provider, userinfo)
        if error:
            return False, error
        
        # Authentication successful, store in session state
        st.session_state.authenticated = True
        st.session_state.user = user
        
        if tokens and "access_token" in tokens:
            st.session_state.token = tokens["access_token"]
        
        st.session_state.current_menu = "Dashboard"
        
        # If user came from project directory, check for project access
        email = get_email_from_userinfo(provider, userinfo)
        if email:
            check_and_update_project_access(email, user.id)
        
        return True, None
    
    except Exception as e:
        logger.error(f"Error in OAuth callback: {str(e)}")
        return False, f"An error occurred during authentication: {str(e)}"

def build_callback_url(provider: OAuthProvider, code: str, state: str) -> str:
    """
    Build the full callback URL for the OAuth provider.
    
    Args:
        provider: The OAuth provider
        code: The authorization code
        state: The state parameter
        
    Returns:
        str: The full callback URL
    """
    base_url = st.get_option("server.baseUrlPath", "http://localhost:5000")
    
    # Add provider-specific path
    provider_path = f"/auth/callback/{provider.value}"
    
    # Construct the full URL
    return f"{base_url}{provider_path}?code={code}&state={state}"

def get_email_from_userinfo(provider: OAuthProvider, userinfo: Dict[str, Any]) -> Optional[str]:
    """
    Extract email from provider-specific user info response.
    
    Args:
        provider: The OAuth provider
        userinfo: The user info from the provider
        
    Returns:
        str: The email address or None if not found
    """
    if not userinfo:
        return None
    
    # Google returns email directly
    if provider == OAuthProvider.GOOGLE:
        return userinfo.get("email")
    
    # Microsoft Graph API returns email directly
    elif provider == OAuthProvider.MICROSOFT:
        return userinfo.get("mail") or userinfo.get("userPrincipalName")
    
    # Procore has a specific format
    elif provider == OAuthProvider.PROCORE:
        return userinfo.get("email")
    
    return None

def check_and_update_project_access(email: str, user_id: int) -> None:
    """
    Check if the email exists in project directory and update user access.
    
    Args:
        email: The user's email address
        user_id: The user's ID
    """
    try:
        # Check if email is in project directory
        dir_repo = ProjectDirectoryRepository()
        project_ids = dir_repo.get_projects_for_email(email)
        
        if not project_ids:
            logger.info(f"Email {email} not found in any project directory")
            return
        
        # Grant access to projects
        user_repo = UserRepository()
        for project_id in project_ids:
            # This would add appropriate roles or permissions for the project
            # Actual implementation depends on how project access is defined in the system
            
            # For example, adding a project_member role
            user_repo.add_role_to_user(user_id, "project_member")
            
            logger.info(f"Granted access to project {project_id} for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error updating project access for {email}: {str(e)}")
        # Don't raise exception, just log it - authentication has already succeeded