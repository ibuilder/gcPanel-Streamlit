"""
External Services Integration Manager for gcPanel.

This module provides a comprehensive interface for managing integrations 
with external services, APIs, and third-party tools used by the application.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Define integration categories and available services
INTEGRATION_CATEGORIES = {
    "Construction Management": [
        {"id": "procore", "name": "Procore", "logo": "procore_logo.png", "status": False, 
         "description": "Bidirectional sync for RFIs, submittals, and change orders between gcPanel and Procore",
         "required_fields": ["client_id", "client_secret", "redirect_uri", "company_id"]},
        {"id": "plangrid", "name": "PlanGrid", "logo": "plangrid_logo.png", "status": False,
         "description": "Drawing management, field reports, and punch lists integration",
         "required_fields": ["api_key", "username", "password"]},
        {"id": "fieldwire", "name": "FieldWire", "logo": "fieldwire_logo.png", "status": False,
         "description": "Task management, field reporting, and drawing annotation synchronization",
         "required_fields": ["api_key", "account_id"]},
        {"id": "buildingconnected", "name": "BuildingConnected", "logo": "buildingconnected_logo.png", "status": False,
         "description": "Bid management workflow and subcontractor database integration",
         "required_fields": ["api_key", "client_id", "client_secret"]}
    ],
    "Document Management": [
        {"id": "onedrive", "name": "Microsoft OneDrive", "logo": "onedrive_logo.png", "status": False,
         "description": "Store and access project documents in Microsoft OneDrive",
         "required_fields": ["client_id", "client_secret", "redirect_uri"]},
        {"id": "google_drive", "name": "Google Drive", "logo": "google_drive_logo.png", "status": False,
         "description": "Store and access project documents in Google Drive",
         "required_fields": ["client_id", "client_secret", "redirect_uri"]},
        {"id": "dropbox", "name": "Dropbox", "logo": "dropbox_logo.png", "status": False,
         "description": "Store and access project documents in Dropbox",
         "required_fields": ["app_key", "app_secret", "redirect_uri"]},
        {"id": "sharepoint", "name": "SharePoint", "logo": "sharepoint_logo.png", "status": False,
         "description": "Store and access project documents in SharePoint",
         "required_fields": ["tenant_id", "client_id", "client_secret"]}
    ],
    "Project Management": [
        {"id": "asana", "name": "Asana", "logo": "asana_logo.png", "status": False,
         "description": "Sync tasks and projects with Asana",
         "required_fields": ["access_token", "workspace_id"]},
        {"id": "monday", "name": "Monday.com", "logo": "monday_logo.png", "status": False,
         "description": "Sync projects and tasks with Monday.com",
         "required_fields": ["api_key", "board_id"]},
        {"id": "jira", "name": "Jira", "logo": "jira_logo.png", "status": False,
         "description": "Issue tracking and project management integration",
         "required_fields": ["url", "username", "api_token"]}
    ],
    "Communication": [
        {"id": "outlook", "name": "Microsoft Outlook", "logo": "outlook_logo.png", "status": False,
         "description": "Email integration with Microsoft Outlook",
         "required_fields": ["client_id", "client_secret", "tenant_id"]},
        {"id": "gmail", "name": "Gmail", "logo": "gmail_logo.png", "status": True,
         "description": "Email integration with Gmail",
         "required_fields": ["client_id", "client_secret", "redirect_uri"]},
        {"id": "slack", "name": "Slack", "logo": "slack_logo.png", "status": False,
         "description": "Real-time messaging and notifications",
         "required_fields": ["client_id", "client_secret", "signing_secret"]},
        {"id": "teams", "name": "Microsoft Teams", "logo": "teams_logo.png", "status": False,
         "description": "Team collaboration and messaging integration",
         "required_fields": ["client_id", "client_secret", "tenant_id"]}
    ],
    "Weather & Environmental": [
        {"id": "weather_api", "name": "Weather API", "logo": "weather_api_logo.png", "status": True,
         "description": "Retrieve current and forecasted weather conditions",
         "required_fields": ["api_key"]},
        {"id": "noaa", "name": "NOAA Weather", "logo": "noaa_logo.png", "status": False,
         "description": "Official weather data from the National Oceanic and Atmospheric Administration",
         "required_fields": ["token"]},
        {"id": "air_quality", "name": "Air Quality Index", "logo": "aqi_logo.png", "status": False,
         "description": "Monitor air quality at project sites",
         "required_fields": ["api_key"]}
    ],
    "AI & Data Services": [
        {"id": "openai", "name": "OpenAI", "logo": "openai_logo.png", "status": False,
         "description": "AI-powered document analysis and drafting assistance",
         "required_fields": ["api_key", "organization_id"]},
        {"id": "anthropic", "name": "Anthropic Claude", "logo": "anthropic_logo.png", "status": False,
         "description": "Generate construction documentation and analyze project data",
         "required_fields": ["api_key"]},
        {"id": "google_ai", "name": "Google AI", "logo": "google_ai_logo.png", "status": False,
         "description": "AI services for document processing and data analysis",
         "required_fields": ["api_key", "project_id"]}
    ],
    "BIM & Design": [
        {"id": "autodesk_bim360", "name": "Autodesk BIM 360", "logo": "bim360_logo.png", "status": False,
         "description": "BIM model management and collaboration",
         "required_fields": ["client_id", "client_secret", "account_id"]},
        {"id": "revit_cloud", "name": "Revit Cloud", "logo": "revit_logo.png", "status": False,
         "description": "Access and manage Revit models",
         "required_fields": ["api_key", "account_id"]},
        {"id": "sketchup", "name": "SketchUp", "logo": "sketchup_logo.png", "status": False,
         "description": "3D modeling integration for construction planning",
         "required_fields": ["api_key", "client_id"]},
        {"id": "trimble_connect", "name": "Trimble Connect", "logo": "trimble_logo.png", "status": False,
         "description": "Project collaboration platform for construction data",
         "required_fields": ["client_id", "client_secret", "project_id"]}
    ],
    "Accounting & Finance": [
        {"id": "quickbooks", "name": "QuickBooks", "logo": "quickbooks_logo.png", "status": False,
         "description": "Financial tracking and accounting integration",
         "required_fields": ["client_id", "client_secret", "realm_id"]},
        {"id": "sage", "name": "Sage", "logo": "sage_logo.png", "status": False,
         "description": "Construction-specific accounting and financial management",
         "required_fields": ["api_key", "company_id"]},
        {"id": "xero", "name": "Xero", "logo": "xero_logo.png", "status": False,
         "description": "Cloud-based accounting system integration",
         "required_fields": ["client_id", "client_secret", "tenant_id"]}
    ]
}

def load_integration_status():
    """Load integration status from session state or initialize defaults."""
    if "integrations" not in st.session_state:
        st.session_state.integrations = {}
        
        # Initialize integration status from the INTEGRATION_CATEGORIES dictionary
        for category, services in INTEGRATION_CATEGORIES.items():
            for service in services:
                service_id = service["id"]
                st.session_state.integrations[service_id] = {
                    "name": service["name"],
                    "status": service["status"],
                    "category": category,
                    "last_sync": "Never" if not service["status"] else "Today",
                    "api_key": "" if not service["status"] else "••••••••••••••••"
                }

def save_integration_status(service_id, status, api_key=""):
    """Save integration status to session state."""
    if "integrations" in st.session_state and service_id in st.session_state.integrations:
        st.session_state.integrations[service_id]["status"] = status
        
        if status:
            st.session_state.integrations[service_id]["last_sync"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if api_key:
                # In a real application, this would be securely stored
                st.session_state.integrations[service_id]["api_key"] = "••••••••••••••••"
        else:
            # If disconnecting, reset API key
            st.session_state.integrations[service_id]["api_key"] = ""

def render_integration_manager():
    """Render the integration manager interface."""
    st.header("External Services Integration")
    
    # Load integration status
    load_integration_status()
    
    # Introduction
    st.markdown("""
    Connect gcPanel with external services to enhance functionality and streamline workflows. 
    These integrations allow you to seamlessly sync data, access external resources, and 
    automate processes across your construction projects.
    """)
    
    # Create tabs for each integration category
    tabs = st.tabs(list(INTEGRATION_CATEGORIES.keys()))
    
    for idx, (category, services) in enumerate(INTEGRATION_CATEGORIES.items()):
        with tabs[idx]:
            st.subheader(f"{category} Integrations")
            
            # Display integrations in a grid with 2 columns
            cols = st.columns(2)
            for i, service in enumerate(services):
                service_id = service["id"]
                with cols[i % 2]:
                    render_integration_card(service_id, service["name"], service["logo"])

def render_integration_card(service_id, service_name, logo_path):
    """Render an individual integration card."""
    # Find the service definition to get description and required fields
    service_def = None
    for category, services in INTEGRATION_CATEGORIES.items():
        for service in services:
            if service["id"] == service_id:
                service_def = service
                break
        if service_def:
            break
    
    integration_data = st.session_state.integrations.get(service_id, {
        "status": False,
        "last_sync": "Never",
        "api_key": ""
    })
    
    # Card container
    with st.container():
        # Use columns for layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Try to display the logo if it exists
            try:
                st.image(f"static/integrations/logos/{logo_path}", width=60)
            except:
                # Fallback if logo doesn't exist
                st.markdown(f"<div style='width:60px;height:60px;background:#f0f2f5;display:flex;justify-content:center;align-items:center;border-radius:5px;'>{service_name[0]}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**{service_name}**")
            
            # Display description if available
            if service_def and "description" in service_def:
                st.caption(service_def["description"])
            
            # Status indicator
            if integration_data["status"]:
                st.markdown("<span style='color:#38d39f;'>● Connected</span>", unsafe_allow_html=True)
                st.caption(f"Last sync: {integration_data['last_sync']}")
            else:
                st.markdown("<span style='color:#6c757d;'>● Not Connected</span>", unsafe_allow_html=True)
                
        # Connection controls
        if integration_data["status"]:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.button(f"Sync Now", key=f"sync_{service_id}")
            with col2:
                if st.button(f"Disconnect", key=f"disconnect_{service_id}"):
                    save_integration_status(service_id, False)
                    st.success(f"Disconnected from {service_name}")
                    st.rerun()
            
            # Show additional options for connected services
            with st.expander("Connection Details"):
                st.json({
                    "Status": "Connected",
                    "Service": service_name,
                    "Last Sync": integration_data['last_sync'],
                    "Connection Type": "OAuth" if service_id in ["google_drive", "onedrive", "dropbox", "procore"] else "API Key"
                })
                
                if service_id == "procore":
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Projects Synced", "7")
                    with col2:
                        st.metric("RFIs Synced", "24")
        else:
            # Show connection form
            with st.expander(f"Connect to {service_name}"):
                with st.form(key=f"connect_form_{service_id}"):
                    # Display all required fields from the service definition
                    form_fields = {}
                    if service_def and "required_fields" in service_def:
                        for field in service_def["required_fields"]:
                            # Format field name for display (e.g., client_id -> Client ID)
                            display_name = " ".join(word.capitalize() for word in field.split("_"))
                            
                            # Determine if field should be password type
                            is_secret = "secret" in field.lower() or "password" in field.lower() or "key" in field.lower() or "token" in field.lower()
                            
                            # Create the input field
                            form_fields[field] = st.text_input(display_name, type="password" if is_secret else "text")
                    else:
                        # Fallback for services without defined fields
                        form_fields["api_key"] = st.text_input("API Key or Access Token", type="password")
                    
                    connect_submitted = st.form_submit_button("Connect")
                    
                    if connect_submitted:
                        # Check if all required fields are filled
                        if service_def and "required_fields" in service_def:
                            if all(form_fields[field] for field in service_def["required_fields"]):
                                save_integration_status(service_id, True, form_fields.get("api_key", ""))
                                st.success(f"Connected to {service_name}")
                                st.rerun()
                            else:
                                st.error("All fields are required")
                        elif form_fields.get("api_key"):
                            save_integration_status(service_id, True, form_fields["api_key"])
                            st.success(f"Connected to {service_name}")
                            st.rerun()
                        else:
                            st.error("API Key or Access Token is required")
        
        # Display special section for featured integrations
        if service_id in ["procore", "plangrid", "fieldwire", "buildingconnected"]:
            with st.expander("Integration Details", expanded=False):
                if service_id == "procore":
                    st.markdown("""
                    ### Procore API Integration Features
                    
                    - **Bidirectional Sync**: RFIs, submittals, and change orders sync between gcPanel and Procore
                    - **Document Management**: Access all project documents from either platform 
                    - **Project Directory**: Keep team contacts and responsibilities in sync
                    - **Schedule Integration**: Link Procore tasks with gcPanel schedule items
                    - **Financial Tools**: Connect budget tracking and cost management
                    """)
                elif service_id == "plangrid":
                    st.markdown("""
                    ### PlanGrid Integration Features
                    
                    - Drawing management and version control
                    - Field reports and punch lists
                    - RFI integration
                    - Sheet linking with BIM models
                    """)
                elif service_id == "fieldwire":
                    st.markdown("""
                    ### FieldWire Integration Features
                    
                    - Task management integration
                    - Field reporting
                    - Drawing annotation sync
                    - Mobile-first workflow
                    """)
                elif service_id == "buildingconnected":
                    st.markdown("""
                    ### BuildingConnected Integration Features
                    
                    - Bid management workflow
                    - Prequalification data sync
                    - Subcontractor database
                    - Cost benchmarking
                    """)
        
        # Divider
        st.markdown("---")

def render_integration_settings():
    """Render integration settings page with all integration options."""
    st.header("Integration Settings")
    
    # Load integration status
    load_integration_status()
    
    # Display active integrations
    st.subheader("Active Integrations")
    
    active_integrations = []
    for service_id, data in st.session_state.integrations.items():
        if data["status"]:
            active_integrations.append({
                "Service": data["name"],
                "Category": data["category"],
                "Last Sync": data["last_sync"]
            })
    
    if active_integrations:
        st.dataframe(pd.DataFrame(active_integrations), use_container_width=True)
    else:
        st.info("No active integrations. Connect to external services below.")
    
    # Option to manage integrations
    if st.button("Manage Integrations"):
        st.session_state.show_integration_manager = True
        st.rerun()
    
    # Show integration manager if requested
    if st.session_state.get("show_integration_manager", False):
        render_integration_manager()
        
        # Option to hide integration manager
        if st.button("Hide Integration Manager"):
            st.session_state.show_integration_manager = False
            st.rerun()