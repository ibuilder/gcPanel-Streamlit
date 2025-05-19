"""
Integration Import Manager for gcPanel.

This module provides functionality to import data from external platforms into gcPanel.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Import functions from importers.py
from modules.integrations.importers import (
    import_documents, import_specifications, import_bids,
    import_daily_reports, import_budget, import_schedule, import_incidents,
    get_integration_credentials
)

def render_import_manager():
    """Render the integration import manager interface."""
    st.title("Integration Data Import")
    
    st.write("""
    Import data from your connected platforms into gcPanel. Select the platform and 
    data type to import, then review and confirm the import.
    """)
    
    # Check which integrations are available
    available_platforms = []
    for platform in ["procore", "plangrid", "fieldwire", "buildingconnected"]:
        if get_integration_credentials(platform):
            available_platforms.append(platform)
    
    if not available_platforms:
        st.warning("No connected platforms found. Please set up integrations in Settings > Integrations first.")
        
        # Add quick links to integration settings
        if st.button("Go to Integration Settings"):
            st.session_state.current_menu = "Settings"
            st.session_state.show_integration_manager = True
            st.rerun()
        return
    
    # Set up columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Import Source")
        
        # Platform selection
        platform_names = {
            "procore": "Procore",
            "plangrid": "PlanGrid",
            "fieldwire": "FieldWire",
            "buildingconnected": "BuildingConnected"
        }
        
        platform_options = [platform_names[p] for p in available_platforms]
        selected_platform_name = st.selectbox("Select Platform", platform_options)
        selected_platform = next((p for p, name in platform_names.items() if name == selected_platform_name), None)
        
        # Data type selection based on platform
        if selected_platform == "procore":
            data_types = [
                "Documents", "Specifications", "Bids", 
                "Daily Reports", "Budget", "Schedule", "Incidents"
            ]
        elif selected_platform == "plangrid":
            data_types = ["Documents", "Daily Reports"]
        elif selected_platform == "fieldwire":
            data_types = ["Documents", "Daily Reports"]
        elif selected_platform == "buildingconnected":
            data_types = ["Bids"]
        else:
            data_types = []
        
        selected_data_type = st.selectbox("Select Data Type", data_types)
        
        # Import options
        st.subheader("Import Options")
        
        import_options = {
            "Merge with existing data": "Newly imported data will be added to existing data. Duplicates will be updated.",
            "Replace existing data": "All existing data of this type will be replaced with imported data."
        }
        
        import_method = st.radio(
            "Import Method", 
            list(import_options.keys()),
            index=0
        )
        
        st.info(import_options[import_method])
        
        # Start import button
        start_import = st.button("Start Import", type="primary")
        
    with col2:
        st.subheader("Data Preview")
        
        # Only show preview if user has selected both platform and data type
        if selected_platform and selected_data_type:
            with st.spinner(f"Fetching data from {selected_platform_name}..."):
                # Convert data type to lowercase with underscores
                data_type_key = selected_data_type.lower().replace(" ", "_")
                
                # Import data based on selection
                if data_type_key == "documents":
                    result = import_documents(selected_platform)
                elif data_type_key == "specifications":
                    result = import_specifications(selected_platform)
                elif data_type_key == "bids":
                    result = import_bids(selected_platform)
                elif data_type_key == "daily_reports":
                    result = import_daily_reports(selected_platform)
                elif data_type_key == "budget":
                    result = import_budget(selected_platform)
                elif data_type_key == "schedule":
                    result = import_schedule(selected_platform)
                elif data_type_key == "incidents":
                    result = import_incidents(selected_platform)
                else:
                    result = {"error": f"Unknown data type: {data_type_key}"}
                
                # Display result
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Show source info
                    st.success(f"Successfully retrieved data from {result.get('source', selected_platform_name)}")
                    
                    # Show data preview based on data type
                    data = result.get("data", [])
                    
                    if data_type_key in ["documents", "specifications", "incidents"]:
                        # Display as a table
                        if data:
                            df = pd.DataFrame(data)
                            st.dataframe(df, use_container_width=True)
                            
                            st.metric("Total Items", len(data))
                    
                    elif data_type_key == "bids":
                        # Display bids with a summary
                        if data:
                            df = pd.DataFrame(data)
                            st.dataframe(df, use_container_width=True)
                            
                            # Calculate some metrics
                            total_bids = len(data)
                            awarded_bids = sum(1 for bid in data if bid.get("status") == "Awarded")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Bids", total_bids)
                            col2.metric("Awarded", awarded_bids)
                            col3.metric("Pending Decision", total_bids - awarded_bids)
                    
                    elif data_type_key == "daily_reports":
                        # Display daily reports
                        if data:
                            df = pd.DataFrame(data)
                            st.dataframe(df, use_container_width=True)
                            
                            st.metric("Total Reports", len(data))
                    
                    elif data_type_key == "budget":
                        # Display budget with summary
                        if "items" in data:
                            st.subheader("Budget Categories")
                            budget_df = pd.DataFrame(data["items"])
                            st.dataframe(budget_df, use_container_width=True)
                            
                            st.subheader("Budget Summary")
                            summary = data["summary"]
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Budget", summary["total_current"])
                            col2.metric("Total Spent", summary["total_spent"])
                            col3.metric("Remaining", summary["total_remaining"])
                    
                    elif data_type_key == "schedule":
                        # Display schedule with summary
                        if "tasks" in data:
                            st.subheader("Schedule Tasks")
                            schedule_df = pd.DataFrame(data["tasks"])
                            st.dataframe(schedule_df, use_container_width=True)
                            
                            st.subheader("Schedule Summary")
                            summary = data["summary"]
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Start Date", summary["start_date"])
                            col2.metric("End Date", summary["end_date"])
                            col3.metric("Completion", summary["percent_complete"])
                    
                    # Add import confirmation if there's valid data
                    if data and start_import:
                        with st.spinner("Importing data..."):
                            # Simulate import process (in real app, this would save to database)
                            import time
                            time.sleep(2)
                            
                            st.session_state[f"imported_{data_type_key}"] = {
                                "data": data,
                                "source": result.get('source', selected_platform_name),
                                "import_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "count": len(data) if not isinstance(data, dict) else 
                                         (len(data.get("items", [])) if "items" in data else 
                                          len(data.get("tasks", [])))
                            }
                            
                            st.success(f"Successfully imported {data_type_key} from {selected_platform_name}!")
                            
                            # Show additional import options
                            st.subheader("Next Steps")
                            st.write("Select your next action:")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Import Another Data Type"):
                                    st.rerun()
                            with col2:
                                if st.button("View Imported Data"):
                                    # In a real app, this would navigate to the relevant section
                                    pass

def render_import_history():
    """Render the import history interface."""
    st.subheader("Import History")
    
    # Check if any data has been imported
    has_imported_data = any(key.startswith("imported_") for key in st.session_state.keys())
    
    if not has_imported_data:
        st.info("No import history available. Import data from external platforms to see history here.")
        return
    
    # Gather import history from session state
    import_history = []
    for key, value in st.session_state.items():
        if key.startswith("imported_"):
            data_type = key.replace("imported_", "").replace("_", " ").title()
            import_history.append({
                "Data Type": data_type,
                "Source": value.get("source", "Unknown"),
                "Import Date": value.get("import_date", "Unknown"),
                "Count": value.get("count", 0)
            })
    
    # Display import history
    if import_history:
        history_df = pd.DataFrame(import_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No import history available.")

def render_sync_status():
    """Render the synchronization status interface."""
    st.subheader("Synchronization Status")
    
    # Check for connected platforms
    platforms = ["procore", "plangrid", "fieldwire", "buildingconnected"]
    connected_platforms = []
    
    for platform in platforms:
        if get_integration_credentials(platform):
            connected_platforms.append(platform)
    
    if not connected_platforms:
        st.warning("No connected platforms found. Please set up integrations in Settings > Integrations.")
        return
    
    # Display sync status for each connected platform
    for platform in connected_platforms:
        platform_name = {
            "procore": "Procore",
            "plangrid": "PlanGrid",
            "fieldwire": "FieldWire",
            "buildingconnected": "BuildingConnected"
        }.get(platform, platform.capitalize())
        
        st.write(f"### {platform_name}")
        
        # Create columns for each data type
        if platform == "procore":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Documents", "42", "Last sync: Today")
            with col2:
                st.metric("RFIs", "18", "Last sync: Today")
            with col3:
                st.metric("Submittals", "24", "Last sync: Yesterday")
            with col4:
                st.metric("Daily Logs", "35", "Last sync: Today")
                
            # Add a sync button
            if st.button(f"Sync {platform_name} Now", key=f"sync_{platform}"):
                with st.spinner(f"Syncing with {platform_name}..."):
                    # Simulate sync process
                    import time
                    time.sleep(2)
                    st.success(f"Synchronized with {platform_name}!")
        else:
            # For other platforms, just show basic status
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Last Sync", "Today")
            with col2:
                st.button(f"Sync {platform_name} Now", key=f"sync_{platform}")
        
        st.divider()

def render_integration_import_interface():
    """Render the main integration import interface."""
    st.title("External Data Integration")
    
    # Create tabs for different sections
    tabs = st.tabs(["Import Data", "Import History", "Sync Status"])
    
    with tabs[0]:
        render_import_manager()
    
    with tabs[1]:
        render_import_history()
    
    with tabs[2]:
        render_sync_status()