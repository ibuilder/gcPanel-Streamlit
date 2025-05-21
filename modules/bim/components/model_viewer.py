"""
BIM Model Viewer Component for gcPanel.

This component provides functionality to view and interact with BIM models.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render_model_list():
    """Render the list of available BIM models with filtering and search"""
    st.header("BIM Models")
    
    # Create sample model data if not already in session state
    if "bim_models" not in st.session_state:
        # Sample BIM model data for demonstration
        models = [
            {
                "id": 1,
                "name": "Highland Tower - Architectural",
                "type": "IFC",
                "version": "2.0",
                "size_mb": 42.5,
                "uploaded_by": "John Smith",
                "upload_date": "2023-05-15",
                "description": "Complete architectural model for Highland Tower",
                "status": "Current",
                "thumbnail": "architectural_model.png"
            },
            {
                "id": 2,
                "name": "Highland Tower - Structural",
                "type": "IFC",
                "version": "1.5",
                "size_mb": 38.2,
                "uploaded_by": "Sarah Johnson",
                "upload_date": "2023-05-10",
                "description": "Structural engineering model containing all load-bearing elements",
                "status": "Current",
                "thumbnail": "structural_model.png"
            },
            {
                "id": 3,
                "name": "Highland Tower - MEP",
                "type": "IFC",
                "version": "1.3",
                "size_mb": 56.3,
                "uploaded_by": "Mike Davidson",
                "upload_date": "2023-05-12",
                "description": "Mechanical, electrical, and plumbing systems model",
                "status": "Current",
                "thumbnail": "mep_model.png"
            },
            {
                "id": 4,
                "name": "Site Layout",
                "type": "IFC",
                "version": "1.1",
                "size_mb": 12.8,
                "uploaded_by": "Lisa Wang",
                "upload_date": "2023-04-22",
                "description": "Site layout and landscaping model",
                "status": "Current",
                "thumbnail": "site_model.png"
            }
        ]
        st.session_state.bim_models = models
    
    # Filter and search controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search models", placeholder="Enter model name, type, or description...")
    
    with col2:
        model_type = st.selectbox("Filter by type", ["All Types", "IFC", "RVT", "SKP", "Other"])
    
    # Apply filters to the model list
    filtered_models = st.session_state.bim_models
    
    if search_term:
        filtered_models = [m for m in filtered_models if search_term.lower() in m["name"].lower() 
                           or search_term.lower() in m["description"].lower()]
    
    if model_type != "All Types":
        filtered_models = [m for m in filtered_models if m["type"] == model_type]
    
    # Display filtered models in a grid
    if not filtered_models:
        st.info("No models match your search criteria.")
    else:
        st.success(f"Found {len(filtered_models)} models")
        
        # Add new model button 
        if st.button("+ Add New Model", key="add_new_model_btn"):
            st.session_state.bim_view = "upload"
            st.session_state.update_model_id = None
            st.rerun()
        
        # Create a grid of model cards - 2 columns
        for i in range(0, len(filtered_models), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(filtered_models):
                    model = filtered_models[i + j]
                    with cols[j]:
                        with st.container():
                            # Card header with model name
                            st.markdown(f"### {model['name']}")
                            st.markdown(f"**Type:** {model['type']} | **Version:** {model['version']} | **Size:** {model['size_mb']} MB")
                            st.markdown(f"**Uploaded by:** {model['uploaded_by']} on {model['upload_date']}")
                            st.markdown(f"**Status:** {model['status']}")
                            
                            # Description
                            st.markdown(f"{model['description']}")
                            
                            # Model actions
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("View Model", key=f"view_model_{model['id']}"):
                                    st.session_state.bim_view = "view"
                                    st.session_state.selected_model_id = model["id"]
                                    st.rerun()
                            with col2:
                                if st.button("Details", key=f"details_model_{model['id']}"):
                                    st.session_state.bim_view = "details"
                                    st.session_state.selected_model_id = model["id"]
                                    st.rerun()
                            with col3:
                                if st.button("Edit", key=f"edit_model_{model['id']}"):
                                    st.session_state.bim_view = "upload"
                                    st.session_state.update_model_id = model["id"]
                                    st.rerun()
                            
                            # Divider
                            st.markdown("---")

def render_model_viewer():
    """Render the 3D model viewer with controls"""
    # Get the selected model
    selected_model_id = st.session_state.selected_model_id
    model = next((m for m in st.session_state.bim_models if m["id"] == selected_model_id), None)
    
    if not model:
        st.error("Selected model not found.")
        return
    
    st.header(f"Viewing: {model['name']}")
    
    # Model controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        view_mode = st.selectbox("View Mode", ["3D", "Plan", "Section", "Elevation"])
    with col2:
        st.checkbox("Show Dimensions", value=True)
    with col3:
        st.checkbox("Element Selection", value=True)
    
    # Placeholder for actual 3D viewer
    st.image("gcpanel.png", caption=f"{model['name']} - 3D View", use_column_width=True)
    
    # Element information
    st.subheader("Selected Element")
    
    # Placeholder selected element data
    element_data = {
        "ID": "W1234",
        "Type": "Wall",
        "Material": "Concrete",
        "Dimensions": "4.5m x 0.3m x 3.2m",
        "Level": "3rd Floor",
        "Fire Rating": "2 hours",
        "Associated Systems": "Structural"
    }
    
    # Display element properties in columns
    cols = st.columns(3)
    for i, (key, value) in enumerate(element_data.items()):
        with cols[i % 3]:
            st.markdown(f"**{key}:** {value}")
    
    # Element actions
    st.button("Isolate Element")
    st.button("Show Related Elements")

def render_model_details():
    """Render detailed information about a selected model"""
    # Get the selected model
    selected_model_id = st.session_state.selected_model_id
    model = next((m for m in st.session_state.bim_models if m["id"] == selected_model_id), None)
    
    if not model:
        st.error("Selected model not found.")
        return
    
    st.header(f"Model Details: {model['name']}")
    
    # Model metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Information")
        st.markdown(f"**Name:** {model['name']}")
        st.markdown(f"**Type:** {model['type']}")
        st.markdown(f"**Version:** {model['version']}")
        st.markdown(f"**Size:** {model['size_mb']} MB")
        st.markdown(f"**Status:** {model['status']}")
        st.markdown(f"**Description:** {model['description']}")
    
    with col2:
        st.subheader("Upload Information")
        st.markdown(f"**Uploaded by:** {model['uploaded_by']}")
        st.markdown(f"**Upload date:** {model['upload_date']}")
        st.markdown(f"**Last modified:** {model['upload_date']}")
        st.markdown(f"**Revisions:** 3")
    
    # Model statistics
    st.subheader("Model Statistics")
    
    # Create sample statistics
    stats = {
        "Elements": 12450,
        "Floors": 15,
        "Walls": 3210,
        "Doors": 420,
        "Windows": 380,
        "Structural Elements": 1850,
        "MEP Elements": 4900
    }
    
    # Display statistics in columns
    cols = st.columns(4)
    for i, (key, value) in enumerate(stats.items()):
        with cols[i % 4]:
            st.metric(key, value)
    
    # Issues and clashes
    st.subheader("Issues and Clashes")
    
    # Sample issue data
    issues = [
        {"id": "ISS-001", "type": "Clash", "description": "Duct intersects with beam", "status": "Open", "assigned_to": "Mike Davidson", "priority": "High"},
        {"id": "ISS-002", "type": "Missing Element", "description": "Door hardware not specified", "status": "In Progress", "assigned_to": "Sarah Johnson", "priority": "Medium"},
        {"id": "ISS-003", "type": "Clearance", "description": "Insufficient clearance for maintenance", "status": "Resolved", "assigned_to": "John Smith", "priority": "Medium"},
        {"id": "ISS-004", "type": "Clash", "description": "Pipe intersects with column", "status": "Open", "assigned_to": "Lisa Wang", "priority": "High"}
    ]
    
    # Convert to DataFrame and display as table
    issues_df = pd.DataFrame(issues)
    st.dataframe(issues_df, use_container_width=True)

def render_model_upload():
    """Render form for adding or updating a BIM model"""
    # Check if we're updating an existing model
    update_model_id = st.session_state.get("update_model_id")
    
    if update_model_id:
        # Get the model being updated
        model = next((m for m in st.session_state.bim_models if m["id"] == update_model_id), None)
        if not model:
            st.error("Model to update not found.")
            return
        
        st.header(f"Update Model: {model['name']}")
    else:
        st.header("Add New BIM Model")
        # Create an empty model for new uploads
        model = {
            "id": len(st.session_state.bim_models) + 1,
            "name": "",
            "type": "IFC",
            "version": "1.0",
            "size_mb": 0,
            "uploaded_by": "Current User",
            "upload_date": datetime.now().strftime("%Y-%m-%d"),
            "description": "",
            "status": "New",
            "thumbnail": ""
        }
    
    # Model upload form
    with st.form("model_upload_form"):
        name = st.text_input("Model Name", value=model["name"])
        
        col1, col2 = st.columns(2)
        with col1:
            model_type = st.selectbox("Model Type", ["IFC", "RVT", "SKP", "Other"], 
                                    index=["IFC", "RVT", "SKP", "Other"].index(model["type"]) if model["type"] in ["IFC", "RVT", "SKP", "Other"] else 0)
        with col2:
            version = st.text_input("Version", value=model["version"])
        
        # File uploader (note: doesn't actually persist files in this demo)
        uploaded_file = st.file_uploader("Upload Model File", type=["ifc", "rvt", "skp", "zip"])
        
        description = st.text_area("Description", value=model["description"])
        
        status = st.selectbox("Status", ["New", "Current", "Archived", "Superseded"], 
                            index=["New", "Current", "Archived", "Superseded"].index(model["status"]) if model["status"] in ["New", "Current", "Archived", "Superseded"] else 0)
        
        # Submit button
        submitted = st.form_submit_button("Save Model")
        
        if submitted:
            # Update model with form values
            model["name"] = name
            model["type"] = model_type
            model["version"] = version
            model["description"] = description
            model["status"] = status
            
            if uploaded_file:
                # In a real app, save the file and update the model
                model["size_mb"] = round(uploaded_file.size / (1024 * 1024), 1)  # Convert bytes to MB
            
            # Update or add the model in session state
            if update_model_id:
                for i, m in enumerate(st.session_state.bim_models):
                    if m["id"] == update_model_id:
                        st.session_state.bim_models[i] = model
                st.success(f"Model '{name}' updated successfully!")
            else:
                st.session_state.bim_models.append(model)
                st.success(f"Model '{name}' added successfully!")
            
            # Return to list view after short delay
            import time
            time.sleep(1)
            st.session_state.bim_view = "list"
            st.session_state.update_model_id = None
            st.rerun()

def render_model_analytics():
    """Render analytics and insights about the BIM models"""
    st.header("BIM Analytics Dashboard")
    
    # Summary metrics
    st.subheader("Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Models", len(st.session_state.bim_models))
    with col2:
        total_size = sum(m["size_mb"] for m in st.session_state.bim_models)
        st.metric("Total Size", f"{total_size:.1f} MB")
    with col3:
        # Count models by type
        ifc_models = len([m for m in st.session_state.bim_models if m["type"] == "IFC"])
        st.metric("IFC Models", ifc_models)
    with col4:
        # Most recent upload
        latest_date = max(m["upload_date"] for m in st.session_state.bim_models)
        st.metric("Latest Upload", latest_date)
    
    # Models by Type chart
    st.subheader("Models by Type")
    
    # Create a DataFrame of model types
    model_types = [m["type"] for m in st.session_state.bim_models]
    type_counts = pd.Series(model_types).value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    
    # Display chart
    st.bar_chart(type_counts.set_index("Type"))
    
    # Model size comparison
    st.subheader("Model Size Comparison")
    
    # Create a DataFrame of model sizes
    model_sizes = pd.DataFrame({
        "Model": [m["name"] for m in st.session_state.bim_models],
        "Size (MB)": [m["size_mb"] for m in st.session_state.bim_models]
    })
    
    # Display chart
    st.bar_chart(model_sizes.set_index("Model"))
    
    # Element Count Analysis (simulated data)
    st.subheader("Element Count Analysis")
    
    # Create simulated element count data
    element_data = {
        "Model": [],
        "Walls": [],
        "Doors": [],
        "Windows": [],
        "Structural": [],
        "MEP": []
    }
    
    for model in st.session_state.bim_models:
        element_data["Model"].append(model["name"])
        # Generate random element counts for demonstration
        element_data["Walls"].append(random.randint(500, 3000))
        element_data["Doors"].append(random.randint(100, 500))
        element_data["Windows"].append(random.randint(80, 400))
        element_data["Structural"].append(random.randint(300, 2000))
        element_data["MEP"].append(random.randint(1000, 5000))
    
    # Convert to DataFrame
    element_df = pd.DataFrame(element_data)
    
    # Display table
    st.dataframe(element_df, use_container_width=True)
    
    # Display stacked bar chart
    st.subheader("Element Composition by Model")
    
    # Prepare data for stacked bar chart
    chart_data = element_df.set_index("Model")
    
    # Display chart
    st.bar_chart(chart_data)