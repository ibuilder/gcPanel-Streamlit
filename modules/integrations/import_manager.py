"""
Integration Import Manager for gcPanel.

This module provides functionality to import data from external platforms into gcPanel.
It serves as the main interface for users to connect with construction management
platforms, import project data, and keep information synchronized.

# Features:
- Platform connection management through authenticated API connections
- Data preview for imported information
- Flexible import strategies (merge or replace)
- Import history tracking and reporting
- Synchronization monitoring and management
- Automatic persistence of imported data

# Components:
- Import Manager: User interface for data import operations
- Import History: Tracking and management of past imports
- Sync Status: Interface for monitoring and triggering synchronization

# Supported Platforms:
- Procore: Full-featured construction management platform
- PlanGrid: Field-focused document and task management
- FieldWire: Mobile-first field operations platform
- BuildingConnected: Preconstruction and bidding platform

# Data Types:
Different platforms support various data types for import:
- Documents: Project files, drawings, and specifications
- Bids: Bidding information and contractor submissions
- Daily Reports: Field observations and progress tracking
- Budget: Financial information and cost tracking
- Schedule: Project timeline and task scheduling
- Incidents: Safety incidents and related information

# Usage:
This module is designed to be used through the Streamlit UI interface.
Access it through the "Integrations" section of the application.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Import functions from other modules
from modules.integrations.importers import (
    import_documents, import_specifications, import_bids,
    import_daily_reports, import_budget, import_schedule, import_incidents
)

# Import authentication module
from modules.integrations.authentication import (
    initialize_integrations, get_credentials, test_connection, 
    store_credentials, get_platform_name, get_auth_fields,
    is_connected, disconnect_platform
)

# Import data persistence module
from modules.integrations.data_persistence import (
    save_imported_data, get_imported_data, delete_imported_data,
    get_import_history, initialize_database
)

def render_import_manager():
    """Render the integration import manager interface."""
    st.title("Integration Data Import")
    
    st.write("""
    Import data from your connected platforms into gcPanel. Select the platform and 
    data type to import, then review and confirm the import.
    """)
    
    # Initialize database and authentication
    initialize_database()
    initialize_integrations()
    
    # Check which integrations are available
    available_platforms = []
    for platform in ["procore", "plangrid", "fieldwire", "buildingconnected"]:
        if is_connected(platform):
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
        
        # Convert import method option to simple string
        import_method_value = "merge" if "Merge" in import_method else "replace"
        
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
                            awarded_bids = sum(1 for bid in data if isinstance(bid, dict) and bid.get("status") == "Awarded")
                            
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
                        if isinstance(data, dict) and "items" in data:
                            st.subheader("Budget Categories")
                            budget_items = data.get("items", [])
                            budget_df = pd.DataFrame(budget_items)
                            st.dataframe(budget_df, use_container_width=True)
                            
                            st.subheader("Budget Summary")
                            summary = data.get("summary", {})
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Budget", summary.get("total_current", "N/A"))
                            col2.metric("Total Spent", summary.get("total_spent", "N/A"))
                            col3.metric("Remaining", summary.get("total_remaining", "N/A"))
                    
                    elif data_type_key == "schedule":
                        # Display schedule with summary
                        if isinstance(data, dict) and "tasks" in data:
                            st.subheader("Schedule Tasks")
                            schedule_tasks = data.get("tasks", [])
                            schedule_df = pd.DataFrame(schedule_tasks)
                            st.dataframe(schedule_df, use_container_width=True)
                            
                            st.subheader("Schedule Summary")
                            summary = data.get("summary", {})
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Start Date", summary.get("start_date", "N/A"))
                            col2.metric("End Date", summary.get("end_date", "N/A"))
                            col3.metric("Completion", summary.get("percent_complete", "N/A"))
                    
                    # Add import confirmation if there's valid data
                    if data and start_import:
                        with st.spinner("Importing data..."):
                            # Save data using our persistence module
                            dataset_id = save_imported_data(
                                platform=selected_platform,
                                data_type=data_type_key,
                                data=data,
                                import_method=import_method_value,
                                user_id=st.session_state.get("user_id")
                            )
                            
                            if dataset_id:
                                st.success(f"Successfully imported {data_type_key} from {selected_platform_name}!")
                            else:
                                st.warning(f"Data was imported to temporary storage. Database persistence is not available.")
                                st.success(f"Successfully imported {data_type_key} to temporary storage.")
                            
                            # Show additional import options
                            st.subheader("Next Steps")
                            st.write("Select your next action:")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Import Another Data Type"):
                                    st.rerun()
                            with col2:
                                if st.button("View Imported Data"):
                                    st.session_state["import_view_tab"] = 1  # Switch to history tab
                                    st.rerun()

def render_import_history():
    """Render the import history interface."""
    st.subheader("Import History")
    
    # Get import history from the database or session state
    history_df = get_import_history()
    
    # Check if we have any import history
    if history_df.empty:
        st.info("No import history available. Import data from external platforms to see history here.")
        return
    
    # Add actions column
    st.dataframe(history_df, use_container_width=True)
    
    # Action buttons for managing imported data
    st.subheader("Manage Imported Data")
    
    # Allow deleting imports
    with st.form("delete_import_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            # Get list of import IDs and formats
            import_options = history_df.apply(
                lambda row: f"{row['Data Type']} from {row['Platform']} ({row['Import Date']})",
                axis=1
            ).tolist()
            
            if import_options:
                selected_import = st.selectbox(
                    "Select Import to Delete",
                    options=import_options,
                    index=0
                )
                
                # Get the ID of the selected import
                selected_index = import_options.index(selected_import)
                selected_id = history_df.iloc[selected_index]["ID"] if not history_df.empty else None
            else:
                st.write("No imports available to delete.")
                selected_id = None
        
        with col2:
            delete_submitted = st.form_submit_button("Delete Selected Import")
            
        if delete_submitted and selected_id:
            # Delete the selected import
            if delete_imported_data(selected_id):
                st.success("Import deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete import. It may be referenced by other data.")
    
    # Export functionality
    st.subheader("Export Data")
    
    with st.form("export_data_form"):
        export_options = history_df.apply(
            lambda row: f"{row['Data Type']} from {row['Platform']} ({row['Import Date']})",
            axis=1
        ).tolist()
        
        if export_options:
            selected_export = st.selectbox(
                "Select Data to Export",
                options=export_options,
                index=0
            )
            
            # Get the details of the selected export
            selected_export_index = export_options.index(selected_export)
            export_details = history_df.iloc[selected_export_index] if not history_df.empty else None
            
            export_formats = ["CSV", "JSON", "Excel"]
            export_format = st.selectbox("Export Format", export_formats)
            
            export_submitted = st.form_submit_button("Export Data")
            
            if export_submitted and export_details is not None:
                # In a real application, this would retrieve and export the data
                # For this demo, we'll simulate it
                st.success(f"Data exported as {export_format}!")
                
                # Display a download button (in a real app, this would be connected to the actual file)
                filename = f"{export_details['Data Type']}_{export_details['Platform']}_{export_details['Import Date']}.{export_format.lower()}"
                st.download_button(
                    label=f"Download {export_format} File",
                    data="Sample export data",
                    file_name=filename,
                    mime="text/plain"
                )
        else:
            st.write("No imports available to export.")
            st.form_submit_button("Export Data", disabled=True)

def render_sync_status():
    """Render the synchronization status interface."""
    st.subheader("Synchronization Status")
    
    # Initialize database and authentication
    initialize_database()
    initialize_integrations()
    
    # Check for connected platforms
    platforms = ["procore", "plangrid", "fieldwire", "buildingconnected"]
    connected_platforms = []
    
    for platform in platforms:
        if is_connected(platform):
            connected_platforms.append(platform)
    
    if not connected_platforms:
        st.warning("No connected platforms found. Please set up integrations in Settings > Integrations.")
        return
    
    # Display sync status for each connected platform
    for platform in connected_platforms:
        platform_name = get_platform_name(platform)
        
        st.write(f"### {platform_name}")
        
        # Get connection status and last sync info
        platform_info = st.session_state.integrations.get(platform, {})
        last_connected = platform_info.get("last_connected", "Never")
        if isinstance(last_connected, str) and last_connected != "Never":
            try:
                # Try to parse and format the date
                last_connected_date = datetime.fromisoformat(last_connected)
                last_connected_str = last_connected_date.strftime("%Y-%m-%d %H:%M")
            except:
                last_connected_str = last_connected
        else:
            last_connected_str = "Never connected"
        
        # Get imported data counts
        history_df = get_import_history(50)
        platform_data = history_df[history_df["Platform"] == platform] if not history_df.empty else pd.DataFrame()
        
        # Display platform status
        st.info(f"Connected: Yes | Last connection: {last_connected_str}")
        
        # Create columns for data status
        if not platform_data.empty:
            # Group by data type and count using pandas methods
            data_type_series = platform_data["Data Type"]
            
            # Use dictionary comprehension instead of Series.value_counts() to avoid LSP issues
            data_types = {}
            for data_type in data_type_series:
                if data_type in data_types:
                    data_types[data_type] += 1
                else:
                    data_types[data_type] = 1
            
            # Show metrics for data types
            cols = st.columns(min(4, len(data_types) + 1))
            
            for i, (data_type, count) in enumerate(data_types.items()):
                with cols[i % 4]:
                    # Find the last import date for this data type more safely
                    filtered_data = platform_data[platform_data["Data Type"] == data_type]
                    
                    # Handle empty case explicitly by checking length
                    if len(filtered_data) == 0:
                        last_import = "Never"
                    else:
                        # Convert to list and find max value manually to avoid Series.max() LSP issues
                        import_dates = filtered_data["Import Date"].tolist()
                        last_import = max(import_dates) if import_dates else "Never"
                    
                    st.metric(
                        data_type, 
                        f"{count} import{'' if count == 1 else 's'}", 
                        f"Last sync: {last_import}"
                    )
        else:
            st.write("No data has been imported from this platform yet.")
                
        # Add a sync button
        col1, col2 = st.columns([3, 1])
        with col1:
            sync_data_types = []
            
            if platform == "procore":
                sync_data_types = ["Documents", "Specifications", "Bids", "Daily Reports", "Budget", "Schedule", "Incidents"]
            elif platform == "plangrid":
                sync_data_types = ["Documents", "Daily Reports"]
            elif platform == "fieldwire":
                sync_data_types = ["Documents", "Daily Reports"]
            elif platform == "buildingconnected":
                sync_data_types = ["Bids"]
            
            selected_sync_type = st.selectbox(
                f"Select data to sync from {platform_name}",
                options=sync_data_types,
                key=f"sync_type_{platform}"
            )
        
        with col2:
            if st.button(f"Sync Now", key=f"sync_{platform}"):
                with st.spinner(f"Syncing {selected_sync_type} from {platform_name}..."):
                    # Convert data type to key format
                    data_type_key = selected_sync_type.lower().replace(" ", "_")
                    
                    # Import data based on selection
                    if data_type_key == "documents":
                        result = import_documents(platform)
                    elif data_type_key == "specifications":
                        result = import_specifications(platform)
                    elif data_type_key == "bids":
                        result = import_bids(platform)
                    elif data_type_key == "daily_reports":
                        result = import_daily_reports(platform)
                    elif data_type_key == "budget":
                        result = import_budget(platform)
                    elif data_type_key == "schedule":
                        result = import_schedule(platform)
                    elif data_type_key == "incidents":
                        result = import_incidents(platform)
                    else:
                        result = {"error": f"Unknown data type: {data_type_key}"}
                    
                    # Save the data
                    if "error" not in result:
                        # Save data using our persistence module
                        data = result.get("data", [])
                        dataset_id = save_imported_data(
                            platform=platform,
                            data_type=data_type_key,
                            data=data,
                            import_method="merge",
                            user_id=st.session_state.get("user_id")
                        )
                        
                        st.success(f"Successfully synced {selected_sync_type} from {platform_name}!")
                    else:
                        st.error(result["error"])
        
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