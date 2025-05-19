"""
Integration settings component for gcPanel.

This module provides the user interface for managing external service integrations
including project management tools, calendars, cloud storage, and construction
management platforms.
"""

import streamlit as st
from utils.integration_manager import IntegrationManager, IntegrationType, IntegrationProvider
from static.integrations.provider_logos import get_provider_logo


def render_integrations():
    """Render the integrations settings interface."""
    st.header("External Service Integrations")
    
    st.write("""
    Connect gcPanel with your essential construction management tools.
    Integrations allow you to seamlessly work with other platforms in your tech stack.
    """)
    
    # Initialize integration manager
    manager = IntegrationManager()
    
    # Create tabs for different integration types
    integration_types = manager.get_integration_types()
    
    # Friendly names for integration types
    type_names = {
        IntegrationType.PROJECT_MANAGEMENT: "Project Management",
        IntegrationType.CALENDAR: "Calendar & Scheduling",
        IntegrationType.CLOUD_STORAGE: "Cloud Storage",
        IntegrationType.CONSTRUCTION_MANAGEMENT: "Construction Management",
        IntegrationType.DESIGN: "BIM & Design"
    }
    
    # Create tabs with friendly names
    tab_labels = [type_names[t] for t in integration_types]
    tabs = st.tabs(tab_labels)
    
    # Project Management Tab
    with tabs[0]:
        render_project_management_integrations(manager)
    
    # Calendar Tab
    with tabs[1]:
        render_calendar_integrations(manager)
    
    # Cloud Storage Tab
    with tabs[2]:
        render_cloud_storage_integrations(manager)
    
    # Construction Management Tab
    with tabs[3]:
        render_construction_integrations(manager)
    
    # Design Tab
    with tabs[4]:
        render_design_integrations(manager)


def render_project_management_integrations(manager):
    """Render project management integrations."""
    st.subheader("Project Management Integrations")
    
    st.write("""
    Connect with your project management tools to sync tasks, issues, and project updates.
    """)
    
    # Get available providers
    providers = manager.get_providers(IntegrationType.PROJECT_MANAGEMENT)
    
    # Create a grid for provider cards
    cols = st.columns(3)
    
    for i, provider in enumerate(providers):
        with cols[i % 3]:
            render_integration_card(manager, IntegrationType.PROJECT_MANAGEMENT, provider)


def render_calendar_integrations(manager):
    """Render calendar integrations."""
    st.subheader("Calendar & Scheduling Integrations")
    
    st.write("""
    Sync project schedules, meetings, and deadlines with your calendar applications.
    """)
    
    # Get available providers
    providers = manager.get_providers(IntegrationType.CALENDAR)
    
    # Create a grid for provider cards
    cols = st.columns(2)
    
    for i, provider in enumerate(providers):
        with cols[i % 2]:
            render_integration_card(manager, IntegrationType.CALENDAR, provider)


def render_cloud_storage_integrations(manager):
    """Render cloud storage integrations."""
    st.subheader("Cloud Storage Integrations")
    
    st.write("""
    Connect with your file storage platforms to access and share project documents.
    """)
    
    # Get available providers
    providers = manager.get_providers(IntegrationType.CLOUD_STORAGE)
    
    # Create a grid for provider cards
    cols = st.columns(3)
    
    for i, provider in enumerate(providers):
        with cols[i % 3]:
            render_integration_card(manager, IntegrationType.CLOUD_STORAGE, provider)


def render_construction_integrations(manager):
    """Render construction management integrations."""
    st.subheader("Construction Management Integrations")
    
    st.write("""
    Connect with specialized construction management platforms.
    """)
    
    # Get available providers
    providers = manager.get_providers(IntegrationType.CONSTRUCTION_MANAGEMENT)
    
    # Create a grid for provider cards
    cols = st.columns(2)
    
    for i, provider in enumerate(providers):
        with cols[i % 2]:
            render_integration_card(manager, IntegrationType.CONSTRUCTION_MANAGEMENT, provider)


def render_design_integrations(manager):
    """Render design software integrations."""
    st.subheader("BIM & Design Integrations")
    
    st.write("""
    Connect with Building Information Modeling (BIM) and design software.
    """)
    
    # Get available providers
    providers = manager.get_providers(IntegrationType.DESIGN)
    
    # Create a grid for provider cards
    cols = st.columns(2)
    
    for i, provider in enumerate(providers):
        with cols[i % 2]:
            render_integration_card(manager, IntegrationType.DESIGN, provider)


def render_integration_card(manager, integration_type, provider):
    """
    Render a card for a specific integration provider.
    
    Args:
        manager (IntegrationManager): The integration manager instance
        integration_type (IntegrationType): The type of integration
        provider (IntegrationProvider): The provider to render
    """
    # Check if this provider is connected
    is_connected = manager.is_connected(integration_type, provider.id)
    
    # Create a card with border
    card_style = """
    <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
    """
    
    # Provider title with logo (if available)
    logo_html = ""
    if hasattr(provider, 'logo_url') and provider.logo_url:
        logo_html = f'<img src="{provider.logo_url}" style="height: 30px; margin-right: 10px; vertical-align: middle;">'
    elif provider.id in ["procore", "plangrid", "google_calendar", "outlook", "dropbox", "google_drive", "onedrive"]:
        # Try to get logo from our static provider_logos module
        logo_svg = get_provider_logo(provider.id)
        if logo_svg:
            logo_html = f'<span style="margin-right: 10px; vertical-align: middle;">{logo_svg}</span>'
    
    # Status indicator
    status_color = "#4CAF50" if is_connected else "#9E9E9E"
    status_text = "Connected" if is_connected else "Not Connected"
    
    card_html = f"""
    {card_style}
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            {logo_html}
            <h3 style="margin: 0;">{provider.name}</h3>
            <div style="margin-left: auto; display: flex; align-items: center;">
                <span style="width: 10px; height: 10px; background-color: {status_color}; border-radius: 50%; display: inline-block; margin-right: 5px;"></span>
                <span style="color: {status_color}; font-size: 0.8em;">{status_text}</span>
            </div>
        </div>
        <p>{provider.description}</p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Connection button
    if is_connected:
        if st.button(f"Disconnect {provider.name}", key=f"disconnect_{provider.id}"):
            if manager.disconnect(integration_type, provider.id):
                st.success(f"Successfully disconnected from {provider.name}.")
                st.rerun()
            else:
                st.error(f"Failed to disconnect from {provider.name}.")
    else:
        if st.button(f"Connect {provider.name}", key=f"connect_{provider.id}"):
            st.session_state.show_connection_form = provider.id
    
    # Show connection form if requested
    if getattr(st.session_state, 'show_connection_form', '') == provider.id:
        render_connection_form(manager, integration_type, provider)


def render_connection_form(manager, integration_type, provider):
    """
    Render a form to connect to a specific provider.
    
    Args:
        manager (IntegrationManager): The integration manager instance
        integration_type (IntegrationType): The type of integration
        provider (IntegrationProvider): The provider to connect to
    """
    st.subheader(f"Connect to {provider.name}")
    
    # Create a form based on the provider's authentication type
    with st.form(key=f"connect_form_{provider.id}"):
        credentials = {}
        
        # Render form fields based on auth_fields
        for field in provider.auth_fields:
            field_name = field.get('name', '')
            field_label = field.get('label', field_name.replace('_', ' ').title())
            field_type = field.get('type', 'string')
            
            if field_type == 'password':
                credentials[field_name] = st.text_input(field_label, type="password", key=f"{provider.id}_{field_name}")
            else:
                credentials[field_name] = st.text_input(field_label, key=f"{provider.id}_{field_name}")
        
        # Submit button
        submitted = st.form_submit_button("Connect")
        
        if submitted:
            # Handle form submission
            if all(credentials.values()):  # Ensure all fields are filled
                if manager.connect(integration_type, provider.id, credentials):
                    st.success(f"Successfully connected to {provider.name}!")
                    # Reset the form visibility flag
                    st.session_state.show_connection_form = ''
                    st.rerun()
                else:
                    st.error(f"Failed to connect to {provider.name}. Please check your credentials.")
            else:
                st.warning("Please fill in all required fields.")
    
    # Cancel button (outside the form)
    if st.button("Cancel", key=f"cancel_{provider.id}"):
        st.session_state.show_connection_form = ''
        st.rerun()


def get_mock_usage_data(provider_id):
    """
    Get mock usage data for a provider.
    This would be replaced with real usage data in production.
    
    Args:
        provider_id (str): The provider ID
        
    Returns:
        dict: Usage data for the provider
    """
    # Sample data for different providers
    if provider_id == "procore":
        return {
            "active_projects": 3,
            "documents_synced": 127,
            "last_sync": "2025-05-18 14:32:21",
            "usage_chart": [10, 25, 18, 32, 45, 37, 29]
        }
    elif provider_id in ["google_calendar", "outlook"]:
        return {
            "events_synced": 24,
            "upcoming_events": 8,
            "last_sync": "2025-05-19 09:15:42"
        }
    elif provider_id in ["dropbox", "google_drive", "onedrive"]:
        return {
            "files_synced": 89,
            "storage_used": "1.2 GB",
            "last_sync": "2025-05-19 10:45:18"
        }
    
    # Default data
    return {
        "connections": 1,
        "last_sync": "2025-05-19 08:00:00"
    }