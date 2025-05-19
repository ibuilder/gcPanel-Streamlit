"""
Integration settings component for gcPanel.

This module provides the user interface for managing external service integrations
including project management tools, calendars, cloud storage, and construction
management platforms.
"""

import streamlit as st
import os
import json
from datetime import datetime

# Import integration manager
from utils.integration_manager import IntegrationManager, IntegrationType, IntegrationProvider

# Import provider logos from separate file to avoid embedding HTML in Python code
from static.integrations.provider_logos import get_provider_logo

def render_integrations():
    """Render the integrations settings interface."""
    st.subheader("Integrations")
    st.write("Connect gcPanel with your favorite tools and services.")
    
    # Create integration manager instance
    manager = IntegrationManager()
    
    # Create tabs for different integration types
    tabs = st.tabs([
        "Project Management", 
        "Calendars", 
        "Cloud Storage", 
        "Construction Management"
    ])
    
    # Project Management Tab
    with tabs[0]:
        render_integration_type(
            manager, 
            IntegrationType.PROJECT_MANAGEMENT,
            [
                IntegrationProvider.JIRA,
                IntegrationProvider.ASANA,
                IntegrationProvider.MS_PROJECT
            ]
        )
    
    # Calendars Tab
    with tabs[1]:
        render_integration_type(
            manager, 
            IntegrationType.CALENDAR,
            [
                IntegrationProvider.GOOGLE_CALENDAR,
                IntegrationProvider.MS_OUTLOOK
            ]
        )
    
    # Cloud Storage Tab
    with tabs[2]:
        render_integration_type(
            manager, 
            IntegrationType.CLOUD_STORAGE,
            [
                IntegrationProvider.GOOGLE_DRIVE,
                IntegrationProvider.DROPBOX,
                IntegrationProvider.ONEDRIVE
            ]
        )
    
    # Construction Management Tab
    with tabs[3]:
        render_integration_type(
            manager, 
            IntegrationType.CONSTRUCTION_MANAGEMENT,
            [
                IntegrationProvider.PROCORE
            ]
        )

def render_integration_type(manager, integration_type, providers):
    """
    Render integration options for a specific type.
    
    Args:
        manager (IntegrationManager): The integration manager instance
        integration_type (IntegrationType): The type of integration
        providers (list): List of providers for this integration type
    """
    st.write(f"#### {integration_type.value.replace('_', ' ').title()} Integrations")
    
    # Display providers as cards
    cols = st.columns(min(len(providers), 3))
    
    for i, provider in enumerate(providers):
        with cols[i % 3]:
            render_integration_card(manager, integration_type, provider)
    
    # Provide documentation about integration benefits
    with st.expander("Learn more about these integrations"):
        if integration_type == IntegrationType.PROJECT_MANAGEMENT:
            st.markdown("""
            **Project Management integrations** allow you to:
            - Sync tasks and issues between gcPanel and your PM tool
            - Create and assign tasks directly from gcPanel
            - Track project milestones and dependencies
            - Generate reports across all your projects
            """)
        elif integration_type == IntegrationType.CALENDAR:
            st.markdown("""
            **Calendar integrations** allow you to:
            - Schedule meetings and site visits
            - Synchronize project milestones to your calendar
            - Get reminders for important deadlines
            - Share availability with project stakeholders
            """)
        elif integration_type == IntegrationType.CLOUD_STORAGE:
            st.markdown("""
            **Cloud Storage integrations** allow you to:
            - Access project documents from your preferred storage
            - Automatically sync files between systems
            - Maintain version control across platforms
            - Share documents with secure access controls
            """)
        elif integration_type == IntegrationType.CONSTRUCTION_MANAGEMENT:
            st.markdown("""
            **Construction Management integrations** allow you to:
            - Connect with specialized construction software
            - Synchronize RFIs, submittals, and change orders
            - Maintain consistent data across platforms
            - Streamline communications with team members
            """)

def render_integration_card(manager, integration_type, provider):
    """
    Render a card for a specific integration provider.
    
    Args:
        manager (IntegrationManager): The integration manager instance
        integration_type (IntegrationType): The type of integration
        provider (IntegrationProvider): The provider to render
    """
    # Get provider info
    provider_id = provider.value
    provider_name = provider.name.replace('_', ' ').title()
    
    # Get connection status
    is_connected = manager.is_integrated(integration_type, provider)
    status_color = "#4CAF50" if is_connected else "#9E9E9E"
    status_text = "Connected" if is_connected else "Not Connected"
    
    # Get provider logo
    provider_logo = get_provider_logo(provider_id)
    
    # Render card
    st.markdown(f"""
    <div style="border:1px solid #e0e0e0; border-radius:10px; padding:15px; margin-bottom:15px;">
        <div style="display:flex; align-items:center;">
            <div style="margin-right:10px;">
                {provider_logo}
            </div>
            <div style="flex-grow:1;">
                <div style="font-weight:600;">{provider_name}</div>
                <div style="font-size:0.8rem; color:{status_color};">{status_text}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add connect/disconnect button
    if is_connected:
        if st.button(f"Disconnect {provider_name}", key=f"disconnect_{provider_id}"):
            # Disconnect integration
            manager.remove_integration(integration_type, provider)
            st.success(f"Disconnected from {provider_name}")
            st.rerun()
    else:
        if st.button(f"Connect {provider_name}", key=f"connect_{provider_id}"):
            # Show connection form
            render_connection_form(manager, integration_type, provider)

def render_connection_form(manager, integration_type, provider):
    """
    Render a form to connect to a specific provider.
    
    Args:
        manager (IntegrationManager): The integration manager instance
        integration_type (IntegrationType): The type of integration
        provider (IntegrationProvider): The provider to connect to
    """
    provider_name = provider.name.replace('_', ' ').title()
    st.subheader(f"Connect to {provider_name}")
    
    with st.form(f"connect_{provider.value}_form"):
        # Common fields
        api_key = st.text_input(f"{provider_name} API Key", type="password")
        
        # Provider-specific fields
        if provider == IntegrationProvider.JIRA:
            domain = st.text_input("Jira Domain (e.g., yourcompany.atlassian.net)")
            username = st.text_input("Username (Email)")
            
            config = {
                "api_key": api_key,
                "domain": domain,
                "username": username
            }
        elif provider == IntegrationProvider.ASANA:
            workspace = st.text_input("Asana Workspace Name")
            
            config = {
                "api_key": api_key,
                "workspace": workspace
            }
        elif provider == IntegrationProvider.GOOGLE_CALENDAR or provider == IntegrationProvider.GOOGLE_DRIVE:
            client_id = st.text_input("Google Client ID")
            client_secret = st.text_input("Google Client Secret", type="password")
            
            config = {
                "api_key": api_key,
                "client_id": client_id,
                "client_secret": client_secret
            }
        elif provider == IntegrationProvider.PROCORE:
            company_id = st.text_input("Procore Company ID")
            project_id = st.text_input("Procore Project ID")
            
            config = {
                "api_key": api_key,
                "company_id": company_id,
                "project_id": project_id
            }
        else:
            # Default configuration
            config = {
                "api_key": api_key
            }
        
        submitted = st.form_submit_button("Connect")
        if submitted:
            # Add integration
            manager.add_integration(integration_type, provider, config)
            st.success(f"Connected to {provider_name}")
            st.rerun()