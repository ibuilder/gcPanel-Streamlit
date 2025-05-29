"""
Integration Manager for gcPanel.

This module provides tools for managing external service integrations
such as project management platforms, calendar services, cloud storage,
and construction management platforms.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Any
import streamlit as st
import json
import os
import pandas as pd


class IntegrationType(Enum):
    """Enum representing different types of integrations."""
    PROJECT_MANAGEMENT = auto()
    CALENDAR = auto()
    CLOUD_STORAGE = auto()
    CONSTRUCTION_MANAGEMENT = auto()
    DESIGN = auto()


class IntegrationProvider:
    """Class representing a specific integration provider."""
    
    def __init__(
        self, 
        id: str, 
        name: str, 
        description: str, 
        logo_url: Optional[str] = None, 
        auth_type: str = "oauth2",
        auth_fields: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize a new integration provider.
        
        Args:
            id: Unique identifier for the provider
            name: Display name for the provider
            description: Description of the provider
            logo_url: URL to the provider's logo
            auth_type: Authentication type (oauth2, api_key, credentials)
            auth_fields: Fields required for authentication
        """
        self.id = id
        self.name = name
        self.description = description
        self.logo_url = logo_url
        self.auth_type = auth_type
        self.auth_fields = auth_fields or []


class IntegrationManager:
    """Manager for handling external service integrations."""
    
    def __init__(self):
        """Initialize the integration manager."""
        self._initialize_session_state()
        self._load_integrations()
    
    def _initialize_session_state(self):
        """Initialize session state for integrations."""
        if "integrations" not in st.session_state:
            st.session_state.integrations = {}
    
    def _load_integrations(self):
        """
        Load saved integrations from config.
        In a production environment, this would load from a database.
        """
        # In development, we'll use a simplified dictionary in session state
        self.providers = {
            IntegrationType.PROJECT_MANAGEMENT: [
                IntegrationProvider(
                    id="procore",
                    name="Procore",
                    description="Connect with Procore for project management, quality, and safety.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"},
                        {"name": "redirect_uri", "type": "string", "label": "Redirect URI"}
                    ]
                ),
                IntegrationProvider(
                    id="plangrid",
                    name="PlanGrid",
                    description="Connect with PlanGrid for construction document management.",
                    auth_type="api_key",
                    auth_fields=[
                        {"name": "api_key", "type": "password", "label": "API Key"}
                    ]
                ),
                IntegrationProvider(
                    id="ms_project",
                    name="Microsoft Project",
                    description="Connect with Microsoft Project for scheduling and resource planning.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"},
                        {"name": "tenant_id", "type": "string", "label": "Tenant ID"}
                    ]
                )
            ],
            IntegrationType.CALENDAR: [
                IntegrationProvider(
                    id="google_calendar",
                    name="Google Calendar",
                    description="Sync with Google Calendar for scheduling and reminders.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"}
                    ]
                ),
                IntegrationProvider(
                    id="outlook",
                    name="Microsoft Outlook",
                    description="Sync with Outlook Calendar for scheduling and reminders.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"},
                        {"name": "tenant_id", "type": "string", "label": "Tenant ID"}
                    ]
                )
            ],
            IntegrationType.CLOUD_STORAGE: [
                IntegrationProvider(
                    id="dropbox",
                    name="Dropbox",
                    description="Connect to Dropbox for file storage and sharing.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "app_key", "type": "string", "label": "App Key"},
                        {"name": "app_secret", "type": "password", "label": "App Secret"}
                    ]
                ),
                IntegrationProvider(
                    id="google_drive",
                    name="Google Drive",
                    description="Connect to Google Drive for file storage and sharing.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"}
                    ]
                ),
                IntegrationProvider(
                    id="onedrive",
                    name="Microsoft OneDrive",
                    description="Connect to OneDrive for file storage and sharing.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"},
                        {"name": "tenant_id", "type": "string", "label": "Tenant ID"}
                    ]
                )
            ],
            IntegrationType.CONSTRUCTION_MANAGEMENT: [
                IntegrationProvider(
                    id="buildertrend",
                    name="Buildertrend",
                    description="Connect with Buildertrend for residential construction management.",
                    auth_type="api_key",
                    auth_fields=[
                        {"name": "api_key", "type": "password", "label": "API Key"}
                    ]
                ),
                IntegrationProvider(
                    id="fieldwire",
                    name="Fieldwire",
                    description="Connect with Fieldwire for field management and task tracking.",
                    auth_type="api_key",
                    auth_fields=[
                        {"name": "api_key", "type": "password", "label": "API Key"}
                    ]
                )
            ],
            IntegrationType.DESIGN: [
                IntegrationProvider(
                    id="autodesk_bim360",
                    name="Autodesk BIM 360",
                    description="Connect with BIM 360 for design collaboration and model management.",
                    auth_type="oauth2",
                    auth_fields=[
                        {"name": "client_id", "type": "string", "label": "Client ID"},
                        {"name": "client_secret", "type": "password", "label": "Client Secret"}
                    ]
                ),
                IntegrationProvider(
                    id="revit",
                    name="Autodesk Revit",
                    description="Connect with Revit for BIM modeling and coordination.",
                    auth_type="api_key",
                    auth_fields=[
                        {"name": "api_key", "type": "password", "label": "API Key"}
                    ]
                )
            ]
        }
    
    def get_integration_types(self) -> List[IntegrationType]:
        """
        Get all available integration types.
        
        Returns:
            List of integration types
        """
        return list(self.providers.keys())
    
    def get_providers(self, integration_type: IntegrationType) -> List[IntegrationProvider]:
        """
        Get all providers for a specific integration type.
        
        Args:
            integration_type: The type of integration
            
        Returns:
            List of providers for the specified integration type
        """
        return self.providers.get(integration_type, [])
    
    def is_connected(self, integration_type: IntegrationType, provider_id: str) -> bool:
        """
        Check if a provider is connected.
        
        Args:
            integration_type: The type of integration
            provider_id: The provider ID
            
        Returns:
            True if connected, False otherwise
        """
        integrations = st.session_state.integrations
        type_key = integration_type.name
        
        return (
            type_key in integrations and
            provider_id in integrations[type_key] and
            integrations[type_key][provider_id].get("connected", False)
        )
    
    def get_connection_details(
        self, 
        integration_type: IntegrationType, 
        provider_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get connection details for a provider.
        
        Args:
            integration_type: The type of integration
            provider_id: The provider ID
            
        Returns:
            Connection details or None if not connected
        """
        integrations = st.session_state.integrations
        type_key = integration_type.name
        
        if not self.is_connected(integration_type, provider_id):
            return None
        
        return integrations[type_key][provider_id]
    
    def connect(
        self, 
        integration_type: IntegrationType, 
        provider_id: str, 
        credentials: Dict[str, Any]
    ) -> bool:
        """
        Connect to a provider with credentials.
        
        Args:
            integration_type: The type of integration
            provider_id: The provider ID
            credentials: The credentials for authentication
            
        Returns:
            True if connection was successful, False otherwise
        """
        # In a production environment, this would validate the credentials
        # with the provider's API and store tokens securely
        
        # For development, we'll simply store the credentials in session state
        integrations = st.session_state.integrations
        type_key = integration_type.name
        
        if type_key not in integrations:
            integrations[type_key] = {}
        
        # In real implementation, we would validate credentials here
        # and get access tokens from the provider's API
        
        # Store connection details
        integrations[type_key][provider_id] = {
            "connected": True,
            "credentials": credentials,
            "connected_at": str(pd.Timestamp.now())
        }
        
        return True
    
    def disconnect(self, integration_type: IntegrationType, provider_id: str) -> bool:
        """
        Disconnect from a provider.
        
        Args:
            integration_type: The type of integration
            provider_id: The provider ID
            
        Returns:
            True if disconnection was successful, False otherwise
        """
        integrations = st.session_state.integrations
        type_key = integration_type.name
        
        if not self.is_connected(integration_type, provider_id):
            return False
        
        # In a production environment, this would revoke tokens
        # and clean up the connection with the provider's API
        
        # Remove connection details
        if type_key in integrations and provider_id in integrations[type_key]:
            del integrations[type_key][provider_id]
            return True
        
        return False