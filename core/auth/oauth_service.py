"""
OAuth service for handling authentication with external providers.

This module provides functionality for authenticating users with OAuth providers
including Google, Microsoft Office 365, and Procore.
"""

import logging
import requests
from typing import Optional, Dict, Any, Tuple
from authlib.integrations.requests_client import OAuth2Session

from core.auth.oauth_providers import OAuthProvider, get_oauth_config, is_oauth_configured
from core.auth.user_repository import UserRepository
from core.auth.auth_service import hash_password, generate_tokens
from core.models.user import User, UserStatus

# Set up logging
logger = logging.getLogger(__name__)

def create_oauth_session(provider: OAuthProvider) -> Optional[OAuth2Session]:
    """
    Create an OAuth session for the specified provider.
    
    Args:
        provider: The OAuth provider to create a session for
        
    Returns:
        OAuth2Session: The OAuth session or None if configuration is missing
    """
    if not is_oauth_configured(provider):
        logger.warning(f"OAuth provider {provider.value} is not configured")
        return None
    
    config = get_oauth_config(provider)
    
    # Create OAuth session
    session = OAuth2Session(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope=config.scope,
        **config.client_kwargs
    )
    
    return session

def get_authorization_url(provider: OAuthProvider) -> Tuple[Optional[str], Optional[str]]:
    """
    Get the authorization URL for the specified provider.
    
    Args:
        provider: The OAuth provider to get the authorization URL for
        
    Returns:
        Tuple[str, str]: The authorization URL and state or (None, None) if error
    """
    session = create_oauth_session(provider)
    if not session:
        return None, None
    
    config = get_oauth_config(provider)
    
    try:
        authorization_url, state = session.create_authorization_url(config.authorize_url)
        return authorization_url, state
    except Exception as e:
        logger.error(f"Error creating authorization URL for {provider.value}: {str(e)}")
        return None, None

def get_token(provider: OAuthProvider, authorization_response: str, state: str) -> Optional[Dict[str, Any]]:
    """
    Get an access token from the authorization response.
    
    Args:
        provider: The OAuth provider to get the token from
        authorization_response: The full callback URL with code
        state: The state from the authorization request
        
    Returns:
        Dict[str, Any]: The token response or None if error
    """
    session = create_oauth_session(provider)
    if not session:
        return None
    
    config = get_oauth_config(provider)
    
    try:
        return session.fetch_token(
            config.token_url,
            authorization_response=authorization_response,
            state=state
        )
    except Exception as e:
        logger.error(f"Error fetching token for {provider.value}: {str(e)}")
        return None

def get_user_info(provider: OAuthProvider, token: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get user information from the provider's userinfo endpoint.
    
    Args:
        provider: The OAuth provider to get user info from
        token: The OAuth token
        
    Returns:
        Dict[str, Any]: The user information or None if error
    """
    if not token:
        return None
    
    config = get_oauth_config(provider)
    
    try:
        session = OAuth2Session(token=token)
        response = session.get(config.userinfo_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching user info from {provider.value}: {str(e)}")
        return None

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

def get_name_from_userinfo(provider: OAuthProvider, userinfo: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract first and last name from provider-specific user info response.
    
    Args:
        provider: The OAuth provider
        userinfo: The user info from the provider
        
    Returns:
        Tuple[str, str]: The first and last name or (None, None) if not found
    """
    if not userinfo:
        return None, None
    
    first_name = None
    last_name = None
    
    # Google format
    if provider == OAuthProvider.GOOGLE:
        first_name = userinfo.get("given_name")
        last_name = userinfo.get("family_name")
    
    # Microsoft format
    elif provider == OAuthProvider.MICROSOFT:
        first_name = userinfo.get("givenName")
        last_name = userinfo.get("surname")
    
    # Procore format
    elif provider == OAuthProvider.PROCORE:
        name = userinfo.get("name", "")
        if name:
            name_parts = name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    return first_name, last_name

def authenticate_or_create_user(provider: OAuthProvider, userinfo: Dict[str, Any]) -> Tuple[Optional[User], Optional[Dict[str, Any]], Optional[str]]:
    """
    Authenticate a user with OAuth or create a new user if they don't exist.
    
    Args:
        provider: The OAuth provider
        userinfo: The user info from the provider
        
    Returns:
        Tuple[User, Dict, str]: User object, tokens dict, and error message (if any)
    """
    email = get_email_from_userinfo(provider, userinfo)
    
    if not email:
        return None, None, "Could not retrieve email from OAuth provider"
    
    # Look for existing user by email
    user_repo = UserRepository()
    user = user_repo.get_by_email(email)
    
    # If user exists, authenticate them
    if user:
        # Check if user is active
        if str(user.status.value) != str(UserStatus.ACTIVE.value):
            return None, None, f"User account is {user.status.value}"
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        return user, tokens, None
    
    # User doesn't exist, create a new one
    first_name, last_name = get_name_from_userinfo(provider, userinfo)
    
    # Generate a random password (user will never use this for login)
    import secrets
    import string
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    password_hash = hash_password(password)
    
    # Create new user
    new_user = User(
        username=email.split('@')[0],  # Use first part of email as username
        email=email,
        password_hash=password_hash,
        first_name=first_name,
        last_name=last_name,
        status=UserStatus.ACTIVE
    )
    
    # Save user to database
    try:
        user_id = user_repo.create(new_user)
        if not user_id:
            return None, None, "Failed to create user account"
        
        # Get the created user
        user = user_repo.get_by_id(user_id)
        if not user:
            return None, None, "Failed to retrieve created user"
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        return user, tokens, None
    
    except Exception as e:
        logger.error(f"Error creating user from OAuth: {str(e)}")
        return None, None, "Failed to create user account"