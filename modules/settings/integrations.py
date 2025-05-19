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
    "Document Management": [
        {"id": "onedrive", "name": "Microsoft OneDrive", "logo": "onedrive_logo.png", "status": False},
        {"id": "google_drive", "name": "Google Drive", "logo": "google_drive_logo.png", "status": False},
        {"id": "dropbox", "name": "Dropbox", "logo": "dropbox_logo.png", "status": False},
        {"id": "sharepoint", "name": "SharePoint", "logo": "sharepoint_logo.png", "status": False}
    ],
    "Project Management": [
        {"id": "procore", "name": "Procore", "logo": "procore_logo.png", "status": False},
        {"id": "plangrid", "name": "PlanGrid", "logo": "plangrid_logo.png", "status": False},
        {"id": "asana", "name": "Asana", "logo": "asana_logo.png", "status": False},
        {"id": "monday", "name": "Monday.com", "logo": "monday_logo.png", "status": False}
    ],
    "Communication": [
        {"id": "outlook", "name": "Microsoft Outlook", "logo": "outlook_logo.png", "status": False},
        {"id": "gmail", "name": "Gmail", "logo": "gmail_logo.png", "status": True},
        {"id": "slack", "name": "Slack", "logo": "slack_logo.png", "status": False},
        {"id": "teams", "name": "Microsoft Teams", "logo": "teams_logo.png", "status": False}
    ],
    "Weather & Environmental": [
        {"id": "weather_api", "name": "Weather API", "logo": "weather_api_logo.png", "status": True},
        {"id": "noaa", "name": "NOAA Weather", "logo": "noaa_logo.png", "status": False},
        {"id": "air_quality", "name": "Air Quality Index", "logo": "aqi_logo.png", "status": False}
    ],
    "AI & Data Services": [
        {"id": "openai", "name": "OpenAI", "logo": "openai_logo.png", "status": False},
        {"id": "anthropic", "name": "Anthropic Claude", "logo": "anthropic_logo.png", "status": False},
        {"id": "google_ai", "name": "Google AI", "logo": "google_ai_logo.png", "status": False}
    ],
    "BIM & Design": [
        {"id": "autodesk_bim360", "name": "Autodesk BIM 360", "logo": "bim360_logo.png", "status": False},
        {"id": "revit_cloud", "name": "Revit Cloud", "logo": "revit_logo.png", "status": False},
        {"id": "sketchup", "name": "SketchUp", "logo": "sketchup_logo.png", "status": False},
        {"id": "trimble_connect", "name": "Trimble Connect", "logo": "trimble_logo.png", "status": False}
    ],
    "Accounting & Finance": [
        {"id": "quickbooks", "name": "QuickBooks", "logo": "quickbooks_logo.png", "status": False},
        {"id": "sage", "name": "Sage", "logo": "sage_logo.png", "status": False},
        {"id": "xero", "name": "Xero", "logo": "xero_logo.png", "status": False}
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
            
            # Status indicator
            if integration_data["status"]:
                st.markdown("<span style='color:#38d39f;'>● Connected</span>", unsafe_allow_html=True)
                st.caption(f"Last sync: {integration_data['last_sync']}")
            else:
                st.markdown("<span style='color:#6c757d;'>● Not Connected</span>", unsafe_allow_html=True)
                
        # Connection controls
        if integration_data["status"]:
            if st.button(f"Disconnect", key=f"disconnect_{service_id}"):
                save_integration_status(service_id, False)
                st.success(f"Disconnected from {service_name}")
                st.rerun()
        else:
            # Show connection form
            with st.expander(f"Connect to {service_name}"):
                with st.form(key=f"connect_form_{service_id}"):
                    api_key = st.text_input("API Key or Access Token", type="password")
                    
                    # Some services might need additional fields
                    if service_id in ["google_drive", "onedrive", "dropbox"]:
                        st.text_input("Client ID")
                        st.text_input("Client Secret", type="password")
                    
                    connect_submitted = st.form_submit_button("Connect")
                    
                    if connect_submitted:
                        if api_key:
                            save_integration_status(service_id, True, api_key)
                            st.success(f"Connected to {service_name}")
                            st.rerun()
                        else:
                            st.error("API Key or Access Token is required")
        
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