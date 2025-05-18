"""
Integration Manager for gcPanel.

This module provides a centralized system for connecting with external services
including project management tools, calendars, and cloud storage.
"""

import os
import logging
import json
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# Constants
INTEGRATION_CONFIG_FILE = "config/integrations.json"
CREDENTIALS_DIR = "config/credentials"

class IntegrationType:
    """Integration type constants."""
    PROJECT_MANAGEMENT = "project_management"
    CALENDAR = "calendar"
    CLOUD_STORAGE = "cloud_storage"
    CONSTRUCTION_MANAGEMENT = "construction_management"

class IntegrationProvider:
    """Integration provider constants."""
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

def ensure_dirs_exist():
    """Ensure integration directories exist."""
    os.makedirs(os.path.dirname(INTEGRATION_CONFIG_FILE), exist_ok=True)
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)

def load_integration_config():
    """
    Load integration configuration.
    
    Returns:
        dict: Integration configuration
    """
    ensure_dirs_exist()
    
    if not os.path.exists(INTEGRATION_CONFIG_FILE):
        # Create default config
        default_config = {
            "enabled": True,
            "integrations": {
                IntegrationType.PROJECT_MANAGEMENT: {
                    "enabled": False,
                    "providers": {
                        IntegrationProvider.JIRA: {
                            "enabled": False,
                            "name": "Jira",
                            "description": "Issue and project tracking",
                            "auth_type": "oauth2",
                            "base_url": "",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        },
                        IntegrationProvider.ASANA: {
                            "enabled": False,
                            "name": "Asana",
                            "description": "Project management",
                            "auth_type": "oauth2",
                            "base_url": "",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        },
                        IntegrationProvider.MS_PROJECT: {
                            "enabled": False,
                            "name": "Microsoft Project",
                            "description": "Project management",
                            "auth_type": "oauth2",
                            "base_url": "",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        }
                    }
                },
                IntegrationType.CALENDAR: {
                    "enabled": False,
                    "providers": {
                        IntegrationProvider.GOOGLE_CALENDAR: {
                            "enabled": False,
                            "name": "Google Calendar",
                            "description": "Calendar and scheduling",
                            "auth_type": "oauth2",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        },
                        IntegrationProvider.MS_OUTLOOK: {
                            "enabled": False,
                            "name": "Microsoft Outlook",
                            "description": "Calendar and scheduling",
                            "auth_type": "oauth2",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        }
                    }
                },
                IntegrationType.CLOUD_STORAGE: {
                    "enabled": False,
                    "providers": {
                        IntegrationProvider.GOOGLE_DRIVE: {
                            "enabled": False,
                            "name": "Google Drive",
                            "description": "Cloud storage",
                            "auth_type": "oauth2",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        },
                        IntegrationProvider.DROPBOX: {
                            "enabled": False,
                            "name": "Dropbox",
                            "description": "Cloud storage",
                            "auth_type": "oauth2",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        },
                        IntegrationProvider.ONEDRIVE: {
                            "enabled": False,
                            "name": "OneDrive",
                            "description": "Cloud storage",
                            "auth_type": "oauth2",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        }
                    }
                },
                IntegrationType.CONSTRUCTION_MANAGEMENT: {
                    "enabled": False,
                    "providers": {
                        IntegrationProvider.PROCORE: {
                            "enabled": False,
                            "name": "Procore",
                            "description": "Construction management",
                            "auth_type": "oauth2",
                            "base_url": "https://api.procore.com",
                            "authenticated": False,
                            "sync_frequency": "hourly",
                            "last_sync": None
                        }
                    }
                }
            }
        }
        
        with open(INTEGRATION_CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    try:
        with open(INTEGRATION_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading integration config: {str(e)}")
        return {}

def save_integration_config(config):
    """
    Save integration configuration.
    
    Args:
        config: Integration configuration to save
    """
    ensure_dirs_exist()
    
    with open(INTEGRATION_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_credentials_path(provider):
    """
    Get the path to credentials for a provider.
    
    Args:
        provider: Integration provider
        
    Returns:
        str: Path to credentials file
    """
    return os.path.join(CREDENTIALS_DIR, f"{provider}.json")

def load_credentials(provider):
    """
    Load credentials for a provider.
    
    Args:
        provider: Integration provider
        
    Returns:
        dict: Provider credentials
    """
    creds_path = get_credentials_path(provider)
    
    if not os.path.exists(creds_path):
        return {}
    
    try:
        with open(creds_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading credentials for {provider}: {str(e)}")
        return {}

def save_credentials(provider, credentials):
    """
    Save credentials for a provider.
    
    Args:
        provider: Integration provider
        credentials: Provider credentials
    """
    ensure_dirs_exist()
    
    creds_path = get_credentials_path(provider)
    
    with open(creds_path, 'w') as f:
        json.dump(credentials, f, indent=2)

def update_integration_status(integration_type, provider, enabled=None, authenticated=None, base_url=None):
    """
    Update the status of an integration.
    
    Args:
        integration_type: Type of integration
        provider: Integration provider
        enabled: Whether the integration is enabled
        authenticated: Whether the integration is authenticated
        base_url: Base URL for the integration
        
    Returns:
        bool: True if successful, False otherwise
    """
    config = load_integration_config()
    
    try:
        provider_config = config["integrations"][integration_type]["providers"][provider]
        
        if enabled is not None:
            provider_config["enabled"] = enabled
        
        if authenticated is not None:
            provider_config["authenticated"] = authenticated
            
            # Update last sync time if authenticated
            if authenticated:
                provider_config["last_sync"] = datetime.now().isoformat()
        
        if base_url is not None:
            provider_config["base_url"] = base_url
        
        # Enable integration type if a provider is enabled
        if enabled:
            config["integrations"][integration_type]["enabled"] = True
        
        save_integration_config(config)
        return True
    
    except Exception as e:
        logger.error(f"Error updating integration status: {str(e)}")
        return False

def get_enabled_integrations():
    """
    Get all enabled integrations.
    
    Returns:
        dict: Enabled integrations by type
    """
    config = load_integration_config()
    
    if not config.get("enabled", True):
        return {}
    
    enabled_integrations = {}
    
    for integration_type, type_config in config.get("integrations", {}).items():
        if not type_config.get("enabled", False):
            continue
        
        enabled_providers = {}
        
        for provider, provider_config in type_config.get("providers", {}).items():
            if provider_config.get("enabled", False):
                enabled_providers[provider] = provider_config
        
        if enabled_providers:
            enabled_integrations[integration_type] = {
                "providers": enabled_providers
            }
    
    return enabled_integrations

def is_integration_configured(integration_type, provider):
    """
    Check if an integration is configured.
    
    Args:
        integration_type: Type of integration
        provider: Integration provider
        
    Returns:
        bool: True if configured, False otherwise
    """
    config = load_integration_config()
    
    try:
        provider_config = config["integrations"][integration_type]["providers"][provider]
        return provider_config.get("enabled", False) and provider_config.get("authenticated", False)
    
    except Exception:
        return False

def initialize_integrations():
    """Initialize all integrations."""
    # Load configuration
    config = load_integration_config()
    
    if not config.get("enabled", True):
        logger.info("Integrations are disabled")
        return
    
    # Initialize enabled integrations
    for integration_type, type_config in config.get("integrations", {}).items():
        if not type_config.get("enabled", False):
            continue
        
        for provider, provider_config in type_config.get("providers", {}).items():
            if not provider_config.get("enabled", False):
                continue
            
            logger.info(f"Initializing integration: {provider_config.get('name', provider)}")
            
            # Initialize specific integration based on provider
            try:
                if provider == IntegrationProvider.JIRA:
                    from integrations.jira_integration import initialize_jira
                    initialize_jira()
                
                elif provider == IntegrationProvider.ASANA:
                    from integrations.asana_integration import initialize_asana
                    initialize_asana()
                
                elif provider == IntegrationProvider.MS_PROJECT:
                    from integrations.ms_project_integration import initialize_ms_project
                    initialize_ms_project()
                
                elif provider == IntegrationProvider.GOOGLE_CALENDAR:
                    from integrations.google_calendar_integration import initialize_google_calendar
                    initialize_google_calendar()
                
                elif provider == IntegrationProvider.MS_OUTLOOK:
                    from integrations.ms_outlook_integration import initialize_ms_outlook
                    initialize_ms_outlook()
                
                elif provider == IntegrationProvider.GOOGLE_DRIVE:
                    from integrations.google_drive_integration import initialize_google_drive
                    initialize_google_drive()
                
                elif provider == IntegrationProvider.DROPBOX:
                    from integrations.dropbox_integration import initialize_dropbox
                    initialize_dropbox()
                
                elif provider == IntegrationProvider.ONEDRIVE:
                    from integrations.onedrive_integration import initialize_onedrive
                    initialize_onedrive()
                
                elif provider == IntegrationProvider.PROCORE:
                    from integrations.procore_integration import initialize_procore
                    initialize_procore()
                
            except Exception as e:
                logger.error(f"Error initializing {provider}: {str(e)}")