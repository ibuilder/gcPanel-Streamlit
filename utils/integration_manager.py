"""
Integration Manager for gcPanel.

This module manages connections with external services including project management tools,
calendars, cloud storage, and construction management platforms.
"""

import streamlit as st
import os
import json
from enum import Enum
from datetime import datetime, timedelta
import requests

class IntegrationType(Enum):
    """Types of integrations supported by gcPanel."""
    
    PROJECT_MANAGEMENT = "project_management"
    CALENDAR = "calendar" 
    CLOUD_STORAGE = "cloud_storage"
    CONSTRUCTION_MANAGEMENT = "construction_management"

class IntegrationProvider(Enum):
    """Integration providers supported by gcPanel."""
    
    # Project Management
    JIRA = "jira"
    ASANA = "asana"
    MS_PROJECT = "ms_project"
    
    # Calendar
    GOOGLE_CALENDAR = "google_calendar"
    MS_OUTLOOK = "ms_outlook"
    
    # Cloud Storage
    GOOGLE_DRIVE = "google_drive"
    DROPBOX = "dropbox"
    ONEDRIVE = "onedrive"
    
    # Construction Management
    PROCORE = "procore"

class IntegrationManager:
    """Integration Manager for external services."""
    
    def __init__(self):
        """Initialize the integration manager."""
        # Initialize integrations if not in session state
        if "integrations" not in st.session_state:
            st.session_state.integrations = {}
            
        if "integration_auth_cache" not in st.session_state:
            st.session_state.integration_auth_cache = {}
    
    def get_integration_status(self, provider):
        """
        Get the connection status for a provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            
        Returns:
            dict: Status information for the provider
        """
        # Check if provider is connected
        if provider.value in st.session_state.integrations:
            integration_data = st.session_state.integrations[provider.value]
            
            # Default status shape
            status = {
                "connected": True,
                "provider": provider.value,
                "last_synced": integration_data.get("last_synced", None),
                "connection_info": integration_data.get("connection_info", {}),
                "error": None
            }
            
            return status
        
        return {
            "connected": False,
            "provider": provider.value,
            "last_synced": None,
            "connection_info": {},
            "error": None
        }
    
    def list_integrations(self, integration_type=None):
        """
        List all active integrations, optionally filtered by type.
        
        Args:
            integration_type (IntegrationType, optional): Filter by integration type
            
        Returns:
            dict: Mapping of provider names to status information
        """
        result = {}
        
        # Get all connected providers
        for provider_value in st.session_state.integrations:
            try:
                provider = IntegrationProvider(provider_value)
                
                # Apply type filter if provided
                if integration_type is not None:
                    provider_type = self.get_provider_type(provider)
                    if provider_type != integration_type:
                        continue
                
                # Add to result
                result[provider.value] = self.get_integration_status(provider)
            except ValueError:
                # Invalid provider value in session state
                continue
        
        return result
    
    def get_provider_type(self, provider):
        """
        Get the integration type for a provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            
        Returns:
            IntegrationType: The provider's integration type
        """
        # Project Management
        if provider in [IntegrationProvider.JIRA, IntegrationProvider.ASANA, IntegrationProvider.MS_PROJECT]:
            return IntegrationType.PROJECT_MANAGEMENT
        
        # Calendar
        if provider in [IntegrationProvider.GOOGLE_CALENDAR, IntegrationProvider.MS_OUTLOOK]:
            return IntegrationType.CALENDAR
        
        # Cloud Storage
        if provider in [IntegrationProvider.GOOGLE_DRIVE, IntegrationProvider.DROPBOX, IntegrationProvider.ONEDRIVE]:
            return IntegrationType.CLOUD_STORAGE
        
        # Construction Management
        if provider in [IntegrationProvider.PROCORE]:
            return IntegrationType.CONSTRUCTION_MANAGEMENT
        
        # Unknown provider
        raise ValueError(f"Unknown provider: {provider}")
    
    def connect(self, provider, auth_data):
        """
        Connect to an integration provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            auth_data (dict): Authentication data for the provider
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        # Validate provider
        if not isinstance(provider, IntegrationProvider):
            raise ValueError("Provider must be an IntegrationProvider enum value")
        
        # The implementation would normally perform OAuth or API key validation here
        # For this demonstration, we'll simulate success
        
        # Create connection entry
        st.session_state.integrations[provider.value] = {
            "connected": True,
            "last_synced": datetime.now().isoformat(),
            "connection_info": {
                "user": auth_data.get("user", "Demo User"),
                "organization": auth_data.get("organization", "Demo Org")
            }
        }
        
        # Cache auth data
        st.session_state.integration_auth_cache[provider.value] = auth_data
        
        return True
    
    def disconnect(self, provider):
        """
        Disconnect from an integration provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            
        Returns:
            bool: True if disconnection was successful, False otherwise
        """
        # Validate provider
        if not isinstance(provider, IntegrationProvider):
            raise ValueError("Provider must be an IntegrationProvider enum value")
        
        # Check if connected
        if provider.value not in st.session_state.integrations:
            return False
        
        # Remove from session state
        del st.session_state.integrations[provider.value]
        
        # Remove cached auth data
        if provider.value in st.session_state.integration_auth_cache:
            del st.session_state.integration_auth_cache[provider.value]
        
        return True
    
    def sync(self, provider):
        """
        Sync data with an integration provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            
        Returns:
            bool: True if sync was successful, False otherwise
        """
        # Validate provider
        if not isinstance(provider, IntegrationProvider):
            raise ValueError("Provider must be an IntegrationProvider enum value")
        
        # Check if connected
        if provider.value not in st.session_state.integrations:
            return False
        
        # Update last synced timestamp
        st.session_state.integrations[provider.value]["last_synced"] = datetime.now().isoformat()
        
        return True
    
    def sync_all(self):
        """
        Sync data with all connected integration providers.
        
        Returns:
            dict: Mapping of provider names to sync results
        """
        results = {}
        
        # Sync each connected provider
        for provider_value in st.session_state.integrations:
            try:
                provider = IntegrationProvider(provider_value)
                results[provider.value] = self.sync(provider)
            except ValueError:
                # Invalid provider value in session state
                results[provider_value] = False
        
        return results
    
    def get_data(self, provider, resource_type, params=None):
        """
        Get data from an integration provider.
        
        Args:
            provider (IntegrationProvider): The integration provider
            resource_type (str): The type of resource to get
            params (dict, optional): Parameters for the request
            
        Returns:
            dict: Data from the provider
        """
        # Validate provider
        if not isinstance(provider, IntegrationProvider):
            raise ValueError("Provider must be an IntegrationProvider enum value")
        
        # Check if connected
        if provider.value not in st.session_state.integrations:
            return {"error": "Not connected to provider"}
        
        # In a real implementation, this would call the provider's API
        # For this demonstration, we'll return mock data based on the provider and resource type
        
        # Mock data based on provider and resource type
        mock_data = self._get_mock_data(provider, resource_type, params)
        
        return mock_data
    
    def _get_mock_data(self, provider, resource_type, params=None):
        """
        Get mock data for a provider and resource type.
        
        Args:
            provider (IntegrationProvider): The integration provider
            resource_type (str): The type of resource to get
            params (dict, optional): Parameters for the request
            
        Returns:
            dict: Mock data
        """
        # Jira mock data
        if provider == IntegrationProvider.JIRA:
            if resource_type == "issues":
                return {
                    "issues": [
                        {
                            "id": "HTWR-123",
                            "title": "Update concrete specifications",
                            "status": "In Progress",
                            "assignee": "John Smith",
                            "created": "2025-05-10T14:30:00",
                            "updated": "2025-05-15T09:15:00"
                        },
                        {
                            "id": "HTWR-124",
                            "title": "Review structural drawings for floor 12",
                            "status": "To Do",
                            "assignee": "Sarah Johnson",
                            "created": "2025-05-12T11:00:00",
                            "updated": "2025-05-12T11:00:00"
                        },
                        {
                            "id": "HTWR-125",
                            "title": "Resolve MEP conflict on floor 8",
                            "status": "Done",
                            "assignee": "Mike Chen",
                            "created": "2025-05-08T16:45:00",
                            "updated": "2025-05-14T15:30:00"
                        }
                    ]
                }
        
        # Google Calendar mock data
        if provider == IntegrationProvider.GOOGLE_CALENDAR:
            if resource_type == "events":
                return {
                    "events": [
                        {
                            "id": "ev123",
                            "title": "Weekly Construction Meeting",
                            "start": "2025-05-20T10:00:00",
                            "end": "2025-05-20T11:00:00",
                            "location": "Construction Trailer",
                            "attendees": ["John Smith", "Sarah Johnson", "Mike Chen"]
                        },
                        {
                            "id": "ev124",
                            "title": "Concrete Pour - Floor 12",
                            "start": "2025-05-22T08:00:00",
                            "end": "2025-05-22T17:00:00",
                            "location": "Floor 12",
                            "attendees": ["John Smith", "Concrete Crew"]
                        },
                        {
                            "id": "ev125",
                            "title": "City Inspector Visit",
                            "start": "2025-05-24T13:00:00",
                            "end": "2025-05-24T15:00:00",
                            "location": "Site Office",
                            "attendees": ["Sarah Johnson", "City Inspector"]
                        }
                    ]
                }
        
        # Google Drive mock data
        if provider == IntegrationProvider.GOOGLE_DRIVE:
            if resource_type == "files":
                return {
                    "files": [
                        {
                            "id": "file123",
                            "name": "Highland Tower Specifications.pdf",
                            "type": "application/pdf",
                            "created": "2025-04-15T09:00:00",
                            "updated": "2025-05-10T14:30:00",
                            "size": 2500000
                        },
                        {
                            "id": "file124",
                            "name": "Structural Drawings.dwg",
                            "type": "application/autocad",
                            "created": "2025-04-20T11:15:00",
                            "updated": "2025-05-12T16:45:00",
                            "size": 8500000
                        },
                        {
                            "id": "file125",
                            "name": "Project Schedule.mpp",
                            "type": "application/ms-project",
                            "created": "2025-04-10T08:30:00",
                            "updated": "2025-05-14T10:00:00",
                            "size": 1200000
                        }
                    ]
                }
        
        # Procore mock data
        if provider == IntegrationProvider.PROCORE:
            if resource_type == "projects":
                return {
                    "projects": [
                        {
                            "id": "proj123",
                            "name": "Highland Tower Development",
                            "status": "Active",
                            "start_date": "2024-06-01",
                            "end_date": "2026-08-15",
                            "budget": 45500000
                        }
                    ]
                }
            elif resource_type == "rfi":
                return {
                    "rfi": [
                        {
                            "id": "rfi123",
                            "subject": "Foundation Waterproofing Detail",
                            "status": "Open",
                            "created_by": "John Smith",
                            "assigned_to": "Architect",
                            "date_created": "2025-05-12T09:30:00",
                            "due_date": "2025-05-19T17:00:00"
                        },
                        {
                            "id": "rfi124",
                            "subject": "Curtain Wall Connection Detail",
                            "status": "Answered",
                            "created_by": "Sarah Johnson",
                            "assigned_to": "Structural Engineer",
                            "date_created": "2025-05-10T14:15:00",
                            "due_date": "2025-05-17T17:00:00",
                            "date_answered": "2025-05-15T11:30:00"
                        }
                    ]
                }
        
        # Default empty response
        return {"message": "No data available for this provider and resource type"}

# Provider-specific integration classes would be imported here
# For this demo, we'll just reference them but not implement

def get_jira_integration():
    """
    Get the Jira integration module.
    
    Returns:
        module: Jira integration module
    """
    try:
        import integrations.jira_integration
        return integrations.jira_integration
    except ImportError:
        return None

def get_asana_integration():
    """
    Get the Asana integration module.
    
    Returns:
        module: Asana integration module
    """
    try:
        import integrations.asana_integration
        return integrations.asana_integration
    except ImportError:
        return None

def get_ms_project_integration():
    """
    Get the MS Project integration module.
    
    Returns:
        module: MS Project integration module
    """
    try:
        import integrations.ms_project_integration
        return integrations.ms_project_integration
    except ImportError:
        return None

def get_google_calendar_integration():
    """
    Get the Google Calendar integration module.
    
    Returns:
        module: Google Calendar integration module
    """
    try:
        import integrations.google_calendar_integration
        return integrations.google_calendar_integration
    except ImportError:
        return None

def get_ms_outlook_integration():
    """
    Get the MS Outlook integration module.
    
    Returns:
        module: MS Outlook integration module
    """
    try:
        import integrations.ms_outlook_integration
        return integrations.ms_outlook_integration
    except ImportError:
        return None

def get_google_drive_integration():
    """
    Get the Google Drive integration module.
    
    Returns:
        module: Google Drive integration module
    """
    try:
        import integrations.google_drive_integration
        return integrations.google_drive_integration
    except ImportError:
        return None

def get_dropbox_integration():
    """
    Get the Dropbox integration module.
    
    Returns:
        module: Dropbox integration module
    """
    try:
        import integrations.dropbox_integration
        return integrations.dropbox_integration
    except ImportError:
        return None

def get_onedrive_integration():
    """
    Get the OneDrive integration module.
    
    Returns:
        module: OneDrive integration module
    """
    try:
        import integrations.onedrive_integration
        return integrations.onedrive_integration
    except ImportError:
        return None

def get_procore_integration():
    """
    Get the Procore integration module.
    
    Returns:
        module: Procore integration module
    """
    try:
        import integrations.procore_integration
        return integrations.procore_integration
    except ImportError:
        return None