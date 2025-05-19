"""
Authentication module for external service integrations.

This module handles secure authentication with external construction management
platforms such as Procore, PlanGrid, FieldWire, and BuildingConnected.

# Usage Example:
```python
from modules.integrations.authentication import (
    initialize_integrations, 
    store_credentials, 
    test_connection,
    is_connected
)

# Initialize the authentication system
initialize_integrations()

# Store credentials for a platform
credentials = {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}
success = store_credentials("procore", credentials)

# Test the connection with the stored credentials
is_successful, message = test_connection("procore", credentials)

# Check if a platform is connected
if is_connected("procore"):
    # Perform actions with the connected platform
    pass
```

# Supported Platforms:
- Procore: OAuth 2.0 authentication (client_id, client_secret)
- PlanGrid: API key authentication (api_key)
- FieldWire: API key authentication (api_key, email)
- BuildingConnected: OAuth 2.0 authentication (client_id, client_secret)

# Security Notes:
- In production, credentials should be stored securely using encryption
- OAuth tokens should be refreshed automatically when expired
- API keys should be rotated periodically for security
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import requests
import base64
from typing import Dict, Optional, Any, Tuple

# Define API configuration for supported platforms
PLATFORM_CONFIG = {
    "procore": {
        "name": "Procore",
        "auth_type": "oauth2",
        "client_id_field": "client_id",
        "client_secret_field": "client_secret",
        "base_url": "https://api.procore.com/rest/v1.0",
        "auth_url": "https://login.procore.com/oauth/authorize",
        "token_url": "https://login.procore.com/oauth/token",
        "scope": "openid email profile offline_access",
        "logo": "🏗️"
    },
    "plangrid": {
        "name": "PlanGrid",
        "auth_type": "api_key",
        "key_field": "api_key",
        "base_url": "https://io.plangrid.com/api/v2",
        "logo": "📐"
    },
    "fieldwire": {
        "name": "FieldWire",
        "auth_type": "api_key",
        "key_field": "api_key",
        "email_field": "email",
        "base_url": "https://api.fieldwire.com/api/v3",
        "logo": "📱"
    },
    "buildingconnected": {
        "name": "BuildingConnected",
        "auth_type": "oauth2",
        "client_id_field": "client_id",
        "client_secret_field": "client_secret",
        "base_url": "https://api.buildingconnected.com/v1",
        "auth_url": "https://api.buildingconnected.com/oauth/authorize",
        "token_url": "https://api.buildingconnected.com/oauth/token",
        "scope": "read write",
        "logo": "🔄"
    }
}

# Initialize integrations in session state if needed
def initialize_integrations():
    """Initialize integrations container in session state."""
    if "integrations" not in st.session_state:
        st.session_state.integrations = {}
    
    # Initialize each platform if not already present
    for platform_id in PLATFORM_CONFIG:
        if platform_id not in st.session_state.integrations:
            st.session_state.integrations[platform_id] = {
                "status": False,
                "credentials": {},
                "last_connected": None,
                "token_info": None
            }

def store_credentials(platform_id: str, credentials: Dict[str, Any]) -> bool:
    """
    Store credentials for a platform.
    
    Args:
        platform_id: ID of the platform
        credentials: Dictionary of credentials
    
    Returns:
        bool: True if successful, False otherwise
    """
    if platform_id not in PLATFORM_CONFIG:
        return False
    
    initialize_integrations()
    
    # Store the credentials
    st.session_state.integrations[platform_id]["credentials"] = credentials
    st.session_state.integrations[platform_id]["last_connected"] = datetime.now().isoformat()
    st.session_state.integrations[platform_id]["status"] = True
    
    # In a real app with proper security, we'd store these securely
    # For example, using encrypted storage or a secure vault
    
    return True

def get_credentials(platform_id: str) -> Optional[Dict[str, Any]]:
    """
    Get stored credentials for a platform.
    
    Args:
        platform_id: ID of the platform
    
    Returns:
        Optional[Dict[str, Any]]: Credentials if available, None otherwise
    """
    initialize_integrations()
    
    platform_info = st.session_state.integrations.get(platform_id, {})
    if not platform_info.get("status", False):
        return None
    
    return platform_info.get("credentials", None)

def test_connection(platform_id: str, credentials: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Test connection to a platform API.
    
    Args:
        platform_id: ID of the platform
        credentials: Credentials for the platform
    
    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    if platform_id not in PLATFORM_CONFIG:
        return False, f"Unknown platform: {platform_id}"
    
    platform_config = PLATFORM_CONFIG[platform_id]
    auth_type = platform_config.get("auth_type")
    
    # In a real implementation, we would make API calls to the actual service
    # For demonstration purposes, we'll pretend the test was successful
    
    # This simulates a successful connection
    if auth_type == "oauth2":
        # Get fields with safer default values to avoid None issues
        client_id_field = "client_id"
        if "client_id_field" in platform_config:
            client_id_field = platform_config["client_id_field"]
            
        client_secret_field = "client_secret"
        if "client_secret_field" in platform_config:
            client_secret_field = platform_config["client_secret_field"]
        
        # Check credentials with safer access
        has_client_id = client_id_field in credentials and credentials[client_id_field]
        has_client_secret = client_secret_field in credentials and credentials[client_secret_field]
        
        if not has_client_id or not has_client_secret:
            return False, "Missing client ID or client secret"
            
        # In a real implementation, we would make an OAuth token request
        # For this demo, we'll simulate it
        simulated_token = {
            "access_token": "simulated_access_token",
            "refresh_token": "simulated_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": platform_config.get("scope", "")
        }
        
        # Store token info
        st.session_state.integrations[platform_id]["token_info"] = {
            "token": simulated_token,
            "expires_at": (datetime.now() + timedelta(seconds=3600)).isoformat()
        }
        
        return True, f"Successfully connected to {platform_config['name']}"
        
    elif auth_type == "api_key":
        # Get the key field with safer default values
        key_field = "api_key"
        if "key_field" in platform_config:
            key_field = platform_config["key_field"]
        
        # Check credentials safely
        has_key = key_field in credentials and credentials[key_field]
        if not has_key:
            return False, "Missing API key"
            
        # In a real implementation, we would verify the API key
        # For this demo, we'll assume it's valid
        
        return True, f"Successfully connected to {platform_config['name']}"
    
    return False, "Unknown authentication type"

def get_platform_name(platform_id: str) -> str:
    """Get the human-readable name of a platform from its ID."""
    if platform_id not in PLATFORM_CONFIG:
        return platform_id.capitalize()
    
    return PLATFORM_CONFIG[platform_id]["name"]

def get_platform_logo(platform_id: str) -> str:
    """Get the logo for a platform."""
    if platform_id not in PLATFORM_CONFIG:
        return "🔗"
    
    # Safely get logo with explicit None check
    logo = None
    if "logo" in PLATFORM_CONFIG[platform_id]:
        logo = PLATFORM_CONFIG[platform_id]["logo"]
    
    return logo if logo is not None else "🔗"

def get_auth_fields(platform_id: str) -> Dict[str, str]:
    """
    Get the authentication fields required for a platform.
    
    Args:
        platform_id: ID of the platform
    
    Returns:
        Dict[str, str]: Dictionary of field IDs and labels
    """
    if platform_id not in PLATFORM_CONFIG:
        return {}
    
    platform_config = PLATFORM_CONFIG[platform_id]
    auth_type = platform_config.get("auth_type")
    
    if auth_type == "oauth2":
        return {
            platform_config.get("client_id_field", "client_id"): "Client ID",
            platform_config.get("client_secret_field", "client_secret"): "Client Secret"
        }
    elif auth_type == "api_key":
        fields = {platform_config.get("key_field", "api_key"): "API Key"}
        
        # Add email field if required
        if "email_field" in platform_config:
            fields[platform_config["email_field"]] = "Email"
            
        return fields
    
    return {}

def is_connected(platform_id: str) -> bool:
    """Check if a platform is connected."""
    initialize_integrations()
    
    platform_info = st.session_state.integrations.get(platform_id, {})
    return platform_info.get("status", False)

def disconnect_platform(platform_id: str) -> None:
    """Disconnect from a platform."""
    initialize_integrations()
    
    if platform_id in st.session_state.integrations:
        st.session_state.integrations[platform_id] = {
            "status": False,
            "credentials": {},
            "last_connected": None,
            "token_info": None
        }

def get_connection_status(platform_id: str) -> Dict[str, Any]:
    """
    Get detailed connection status information for a platform.
    
    Args:
        platform_id: ID of the platform
        
    Returns:
        Dict[str, Any]: Connection status information including:
            - last_sync: timestamp of last data sync
            - connection_time: when the connection was established
            - auth_type: type of authentication (oauth, api_key)
            - scopes: authorized access scopes (for OAuth)
    """
    initialize_integrations()
    
    platform_info = st.session_state.integrations.get(platform_id, {})
    
    if not platform_info.get("status", False):
        return {"connected": False}
        
    platform_config = PLATFORM_CONFIG.get(platform_id, {})
    auth_type = platform_config.get("auth_type", "unknown")
    
    # Build connection status information without including sensitive credentials
    status = {
        "connected": True,
        "last_sync": platform_info.get("last_sync", "Never"),
        "connection_time": platform_info.get("last_connected", "Unknown"),
        "auth_type": auth_type
    }
    
    # Add OAuth-specific information if applicable
    if auth_type == "oauth2":
        token_info = platform_info.get("token_info", {})
        if token_info:
            status.update({
                "scopes": token_info.get("scope", []),
                "expires": token_info.get("expires", "Unknown")
            })
    
    return status

def get_authorized_headers(platform_id: str) -> Optional[Dict[str, str]]:
    """
    Get authorized headers for API requests.
    
    Args:
        platform_id: ID of the platform
    
    Returns:
        Optional[Dict[str, str]]: Headers if available, None otherwise
    """
    initialize_integrations()
    
    platform_info = st.session_state.integrations.get(platform_id, {})
    if not platform_info.get("status", False):
        return None
    
    platform_config = PLATFORM_CONFIG.get(platform_id, {})
    auth_type = platform_config.get("auth_type")
    
    if auth_type == "oauth2":
        token_info = platform_info.get("token_info", {})
        if not token_info:
            return None
        
        token = token_info.get("token", {})
        access_token = token.get("access_token")
        
        if not access_token:
            return None
        
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    elif auth_type == "api_key":
        credentials = platform_info.get("credentials", {})
        api_key = credentials.get(platform_config.get("key_field", "api_key"))
        
        if not api_key:
            return None
        
        # Different platforms have different ways of handling API keys
        # For simplicity, we'll use a common approach here
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    return None