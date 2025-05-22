"""
OAuth provider configuration for gcPanel.

This module configures OAuth providers for authentication including
Google, Microsoft Office 365, and Procore.
"""

import os
from enum import Enum
from typing import Dict, Any, Optional

class OAuthProvider(Enum):
    """Supported OAuth providers"""
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    PROCORE = "procore"
    
class OAuthConfig:
    """OAuth configuration for a specific provider"""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
        userinfo_url: str,
        scope: str,
        name: str,
        icon: str,
        client_kwargs: Optional[Dict[str, Any]] = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
        self.scope = scope
        self.name = name
        self.icon = icon
        self.client_kwargs = client_kwargs or {}
        
def get_oauth_config(provider: OAuthProvider) -> OAuthConfig:
    """
    Get OAuth configuration for a specific provider.
    
    Args:
        provider: The OAuth provider to get configuration for
        
    Returns:
        OAuthConfig: The provider configuration
    """
    # Google OAuth configuration
    if provider == OAuthProvider.GOOGLE:
        return OAuthConfig(
            client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            token_url="https://oauth2.googleapis.com/token",
            userinfo_url="https://www.googleapis.com/oauth2/v3/userinfo",
            scope="openid email profile",
            name="Google",
            icon="google",
            client_kwargs={
                "redirect_uri": os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/auth/callback/google")
            }
        )
    
    # Microsoft OAuth configuration
    elif provider == OAuthProvider.MICROSOFT:
        return OAuthConfig(
            client_id=os.environ.get("MICROSOFT_CLIENT_ID", ""),
            client_secret=os.environ.get("MICROSOFT_CLIENT_SECRET", ""),
            authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
            userinfo_url="https://graph.microsoft.com/v1.0/me",
            scope="openid email profile User.Read",
            name="Microsoft Office 365",
            icon="microsoft",
            client_kwargs={
                "redirect_uri": os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/auth/callback/microsoft")
            }
        )
    
    # Procore OAuth configuration
    elif provider == OAuthProvider.PROCORE:
        return OAuthConfig(
            client_id=os.environ.get("PROCORE_CLIENT_ID", ""),
            client_secret=os.environ.get("PROCORE_CLIENT_SECRET", ""),
            authorize_url="https://login.procore.com/oauth/authorize",
            token_url="https://login.procore.com/oauth/token",
            userinfo_url="https://api.procore.com/rest/v1.0/me",
            scope="openid email profile",
            name="Procore",
            icon="procore",
            client_kwargs={
                "redirect_uri": os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/auth/callback/procore")
            }
        )
    
    # Default case (should not happen with proper enum usage)
    raise ValueError(f"Unsupported OAuth provider: {provider}")

def is_oauth_configured(provider: OAuthProvider) -> bool:
    """
    Check if an OAuth provider is configured with valid credentials.
    
    Args:
        provider: The OAuth provider to check
        
    Returns:
        bool: True if the provider is configured, False otherwise
    """
    try:
        config = get_oauth_config(provider)
        return bool(config.client_id and config.client_secret)
    except:
        return False