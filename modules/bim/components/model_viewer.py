"""
BIM Model Viewer component using Streamlit Elements.

This module provides a 3D model viewer for BIM models using Three.js 
integrated through Streamlit Elements.
"""

import streamlit as st
import json
import os
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# Import Streamlit Elements
from streamlit_elements import elements, dashboard, mui, html

# Sample data for demonstration
def generate_sample_models():
    """Generate sample BIM model data for demonstration"""
    models = [
        {
            "id": "model-001",
            "name": "Highland Tower - Full Model",
            "description": "Complete architectural and structural model for Highland Tower project",
            "type": "Architectural",
            "format": "IFC",
            "version": "2.0",
            "upload_date": "2025-01-10",
            "last_modified": "2025-04-15",
            "size": "245 MB",
            "author": "Design Team",
            "path": "TallBuilding.ifc",
            "thumbnail": "gcpanel.png"
        },
        {
            "id": "model-002",
            "name": "Highland Tower - MEP Model",
            "description": "Mechanical, electrical, and plumbing systems for Highland Tower",
            "type": "MEP",
            "format": "IFC",
            "version": "1.3",
            "upload_date": "2025-01-15",
            "last_modified": "2025-03-20",
            "size": "180 MB",
            "author": "MEP Engineering Team",
            "path": "TallBuilding.ifc",
            "thumbnail": "gcpanel.png"
        },
        {
            "id": "model-003",
            "name": "Highland Tower - Site Model",
            "description": "Site layout, grading, and utilities for Highland Tower project",
            "type": "Civil",
            "format": "IFC",
            "version": "1.2",
            "upload_date": "2025-01-12",
            "last_modified": "2025-02-28",
            "size": "95 MB",
            "author": "Site Development Team",
            "path": "TallBuilding.ifc",
            "thumbnail": "gcpanel.png"
        },
        {
            "id": "model-004",
            "name": "Highland Tower - Structural Model",
            "description": "Detailed structural elements for Highland Tower",
            "type": "Structural",
            "format": "IFC",
            "version": "1.5",
            "upload_date": "2025-01-18",
            "last_modified": "2025-04-02",
            "size": "165 MB",
            "author": "Structural Engineering Team",
            "path": "TallBuilding.ifc",
            "thumbnail": "gcpanel.png"
        },
        {
            "id": "model-005",
            "name": "Highland Tower - Facade Model",
            "description": "Exterior facade systems and details",
            "type": "Architectural",
            "format": "IFC",
            "version": "1.1",
            "upload_date": "2025-02-05",
            "last_modified": "2025-03-10",
            "size": "120 MB",
            "author": "Facade Consultant",
            "path": "TallBuilding.ifc",
            "thumbnail": "gcpanel.png"
        }
    ]
    return models

def generate_sample_issues():
    """Generate sample BIM issues data for demonstration"""
    status_options = ["Open", "In Progress", "Resolved", "Verified"]
    priority_options = ["Low", "Medium", "High", "Critical"]
    discipline_options = ["Architectural", "Structural", "MEP", "Civil", "General"]
    location_options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5",
                      "Level 6", "Level 7", "Level 8", "Level 9", "Level 10",
                      "Level 11", "Level 12", "Level 13", "Level 14", "Level 15"]
    
    issues = []
    
    for i in range(1, 31):
        # Create random dates within a reasonable range
        created_date = datetime.now() - timedelta(days=random.randint(1, 120))
        
        # Some issues are resolved, some are not
        status = random.choice(status_options)
        
        if status in ["Resolved", "Verified"]:
            # Resolution date is after creation date
            resolution_date = created_date + timedelta(days=random.randint(1, 30))
            resolution_days = (resolution_date - created_date).days
        else:
            resolution_date = None
            resolution_days = None
        
        # Generate clash description based on disciplines
        discipline = random.choice(discipline_options)
        if discipline == "Architectural":
            other_discipline = random.choice(["Structural", "MEP"])
        elif discipline == "Structural":
            other_discipline = random.choice(["Architectural", "MEP"])
        elif discipline == "MEP":
            other_discipline = random.choice(["Architectural", "Structural"])
        else:
            other_discipline = random.choice(["Architectural", "Structural", "MEP"])
        
        # Format dates as strings for display
        created_date_str = created_date.strftime("%Y-%m-%d")
        resolution_date_str = resolution_date.strftime("%Y-%m-%d") if resolution_date else ""
        
        # Create issue record
        issue = {
            "id": f"BIM-{i:03d}",
            "title": f"{discipline}/{other_discipline} Clash on {random.choice(location_options)}",
            "description": f"{discipline} and {other_discipline} elements intersect creating a clash",
            "status": status,
            "priority": random.choice(priority_options),
            "discipline": discipline,
            "location": random.choice(location_options),
            "created_date": created_date_str,
            "resolution_date": resolution_date_str,
            "resolution_days": resolution_days,
            "assigned_to": random.choice(["J. Smith", "L. Johnson", "A. Martinez", "K. Wong", "S. Davis"]),
            "model_id": random.choice(["model-001", "model-002", "model-003", "model-004", "model-005"]),
            "coordinates": f"X: {random.randint(100, 999)}, Y: {random.randint(100, 999)}, Z: {random.randint(100, 999)}"
        }
        
        issues.append(issue)
    
    return issues

def render_model_list():
    """Render the BIM model list view with filtering and sorting"""
    st.subheader("BIM Models")
    
    # Get sample data
    models = generate_sample_models()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Model type filter
            model_types = ["All Types"] + sorted(list(set(model["type"] for model in models)))
            selected_type = st.selectbox("Model Type", model_types, key="model_type_filter")
            
            # Format filter
            formats = ["All Formats"] + sorted(list(set(model["format"] for model in models)))
            selected_format = st.selectbox("Format", formats, key="model_format_filter")
        
        with col2:
            # Author filter
            authors = ["All Authors"] + sorted(list(set(model["author"] for model in models)))
            selected_author = st.selectbox("Author", authors, key="model_author_filter")
            
            # Search field
            search_term = st.text_input("Search", key="model_search", placeholder="Search models...")
    
    # Filter the data based on selections
    filtered_models = models
    
    # Filter by model type
    if selected_type != "All Types":
        filtered_models = [model for model in filtered_models if model["type"] == selected_type]
    
    # Filter by format
    if selected_format != "All Formats":
        filtered_models = [model for model in filtered_models if model["format"] == selected_format]
    
    # Filter by author
    if selected_author != "All Authors":
        filtered_models = [model for model in filtered_models if model["author"] == selected_author]
    
    # Filter by search term
    if search_term:
        filtered_models = [model for model in filtered_models if 
                          search_term.lower() in model["id"].lower() or
                          search_term.lower() in model["name"].lower() or
                          search_term.lower() in model["description"].lower()]
    
    # Layout for action buttons
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        # Show item count
        st.caption(f"Showing {len(filtered_models)} models")
    
    with col2:
        # Add button
        if st.button("⬆️ Upload Model", use_container_width=True):
            st.session_state.bim_view = "upload"
            st.rerun()
    
    # Analysis button
    if st.button("📊 View Analytics", use_container_width=True):
        st.session_state.bim_view = "analytics"
        st.rerun()
    
    # Check if we have any results
    if not filtered_models:
        st.info("No models match your filters.")
        return
    
    # Display the filtered models in a grid layout
    num_cols = 3  # Number of columns in the grid
    rows = [filtered_models[i:i + num_cols] for i in range(0, len(filtered_models), num_cols)]
    
    for row in rows:
        cols = st.columns(num_cols)
        
        for i, model in enumerate(row):
            if i < len(cols):  # Ensure we have enough columns
                with cols[i]:
                    # Create a card for each model
                    card_container = st.container()
                    
                    with card_container:
                        # Apply card styling
                        st.markdown("""
                        <style>
                            .model-card {
                                border: 1px solid #e0e0e0;
                                border-radius: 5px;
                                padding: 10px;
                                height: 100%;
                                transition: transform 0.2s;
                            }
                            .model-card:hover {
                                transform: translateY(-5px);
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }
                            .model-thumbnail {
                                width: 100%;
                                border-radius: 5px;
                                margin-bottom: 10px;
                            }
                            .model-title {
                                font-weight: bold;
                                margin-bottom: 5px;
                            }
                            .model-info {
                                color: #666;
                                font-size: 0.85em;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Start card container
                        st.markdown('<div class="model-card">', unsafe_allow_html=True)
                        
                        # Model thumbnail
                        st.image(model["thumbnail"], caption=None, use_column_width=True, clamp=True, channels="RGB")
                        
                        # Model title and type
                        st.markdown(f'<div class="model-title">{model["name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="model-info">Type: {model["type"]} | Format: {model["format"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="model-info">Version: {model["version"]} | Size: {model["size"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="model-info">Modified: {model["last_modified"]}</div>', unsafe_allow_html=True)
                        
                        # Action buttons
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("👁️ View", key=f"view_{model['id']}", use_container_width=True):
                                # Store model details in session state
                                st.session_state.selected_model_id = model['id'] 
                                st.session_state.selected_model_data = model
                                # Set view mode
                                st.session_state["bim_view"] = "view"
                                # Force refresh
                                st.rerun()
                        
                        with col2:
                            if st.button("ℹ️ Details", key=f"details_{model['id']}", use_container_width=True):
                                # Store model details in session state
                                st.session_state.selected_model_id = model['id'] 
                                st.session_state.selected_model_data = model
                                # Set details mode
                                st.session_state["bim_view"] = "details"
                                # Force refresh
                                st.rerun()
                        
                        # End card container
                        st.markdown('</div>', unsafe_allow_html=True)

def render_model_viewer():
    """Render the BIM model viewer with interactive 3D model"""
    # Ensure we have a selected model
    if not st.session_state.get("selected_model_id"):
        st.error("No model selected. Please select a model from the list.")
        # Return to list view
        st.session_state.bim_view = "list"
        st.rerun()
        return
    
    # Get the selected model data
    model = st.session_state.get("selected_model_data", None)
    
    if not model:
        # If somehow we have an ID but no data, try to find it
        models = generate_sample_models()
        model = next((m for m in models if m["id"] == st.session_state.selected_model_id), None)
        
        if not model:
            st.error(f"Model with ID {st.session_state.selected_model_id} not found.")
            # Return to list view
            st.session_state.bim_view = "list"
            st.rerun()
            return
    
    # Display model title and info
    st.subheader(f"{model['name']} - 3D Viewer")
    
    # Create tabs for different viewing modes
    tab1, tab2, tab3 = st.tabs(["3D Model", "Clash Detection", "Element Properties"])
    
    # Tab 1: 3D Model View
    with tab1:
        # Options for model display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            view_mode = st.selectbox(
                "View Mode",
                ["Shaded", "Wireframe", "Hidden Line"],
                index=0,
                key="view_mode"
            )
        
        with col2:
            show_grid = st.checkbox("Show Grid", value=True, key="show_grid")
        
        with col3:
            clip_plane = st.checkbox("Section Plane", value=False, key="clip_plane")
            
            if clip_plane:
                section_height = st.slider("Section Height", 0.0, 1.0, 0.5, step=0.01, key="section_height")
        
        with col4:
            # Add a measurement tool toggle
            measure_tool = st.checkbox("Measurement Tool", value=False, key="measure_tool")
        
        # Set up the 3D model viewer with Streamlit Elements
        with elements("bim_viewer"):
            # Create a container for the viewer
            mui.Box(
                sx={
                    "height": "500px", 
                    "width": "100%", 
                    "bgcolor": "#f5f5f5",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "20px",
                    "borderRadius": "10px"
                },
                children=[
                    mui.Typography("Interactive 3D BIM Viewer", variant="h6"),
                    mui.Typography("The 3D model would be displayed here in a production environment.", variant="body1"),
                    mui.Typography("This is a placeholder for the Three.js viewer component.", variant="body2"),
                    mui.Box(
                        sx={
                            "height": "70%", 
                            "width": "100%", 
                            "display": "flex", 
                            "justifyContent": "center", 
                            "alignItems": "center",
                            "marginTop": "20px"
                        },
                        children=[
                            html.img({"src": "gcpanel.png", "style": {"maxHeight": "350px", "maxWidth": "100%"}})
                        ]
                    )
                ]
            )
        
        # Display instructions for using the viewer
        st.markdown("### Viewer Instructions")
        st.markdown("- **Left-click + drag**: Rotate the model")
        st.markdown("- **Right-click + drag**: Pan the model")
        st.markdown("- **Scroll wheel**: Zoom in/out")
        if measure_tool:
            st.markdown("- **Click on two points**: Measure distance between points")
        if clip_plane:
            st.markdown("- **Adjust section slider**: Change section cut height")
    
    # Tab 2: Clash Detection
    with tab2:
        st.subheader("Clash Detection")
        
        # Controls for clash detection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tolerance = st.number_input("Clash Tolerance (mm)", min_value=1, max_value=100, value=10, step=1)
        
        with col2:
            clash_types = st.multiselect(
                "Clash Types",
                ["Hard", "Clearance", "Duplicate"],
                default=["Hard", "Clearance"]
            )
        
        with col3:
            run_clash = st.button("Run Clash Detection")
        
        # Display clash results (sample data)
        if run_clash or True:  # Always show for demo
            # Generate sample clash data
            clash_count = random.randint(5, 20)
            clashes = []
            
            for i in range(clash_count):
                clash_type = random.choice(["Hard", "Clearance", "Duplicate"])
                if clash_type not in clash_types:
                    continue
                    
                clashes.append({
                    "id": f"CLH-{i+1:03d}",
                    "type": clash_type,
                    "element1": f"Element ID: {random.randint(10000, 99999)}",
                    "element2": f"Element ID: {random.randint(10000, 99999)}",
                    "location": f"Level {random.randint(1, 15)}",
                    "distance": f"{random.randint(1, 100)} mm",
                    "status": random.choice(["New", "Active", "Resolved", "Approved"])
                })
            
            # Display clash summary
            st.subheader("Clash Summary")
            
            # Count clashes by type
            clash_by_type = {}
            for clash in clashes:
                clash_type = clash["type"]
                if clash_type in clash_by_type:
                    clash_by_type[clash_type] += 1
                else:
                    clash_by_type[clash_type] = 1
            
            # Count clashes by status
            clash_by_status = {}
            for clash in clashes:
                status = clash["status"]
                if status in clash_by_status:
                    clash_by_status[status] += 1
                else:
                    clash_by_status[status] = 1
            
            # Display summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Clashes", len(clashes))
            
            with col2:
                # Create a breakdown by type
                st.write("Clashes by Type")
                for clash_type, count in clash_by_type.items():
                    st.caption(f"{clash_type}: {count}")
            
            with col3:
                # Create a breakdown by status
                st.write("Clashes by Status")
                for status, count in clash_by_status.items():
                    st.caption(f"{status}: {count}")
            
            # Display clash list
            st.subheader("Clash List")
            
            # Check if we have any clashes
            if not clashes:
                st.info("No clashes detected with current settings.")
            else:
                # Convert to DataFrame for display
                clash_df = pd.DataFrame(clashes)
                st.dataframe(clash_df, use_container_width=True)
    
    # Tab 3: Element Properties
    with tab3:
        st.subheader("Element Properties")
        
        st.markdown("Click on an element in the 3D view to see its properties.")
        
        # Element selection (simulated)
        element_types = ["Wall", "Floor", "Column", "Beam", "Door", "Window", "MEP Equipment", "Furniture"]
        selected_element_type = st.selectbox(
            "Select Element Type",
            element_types,
            index=0,
            key="element_type"
        )
        
        # Generate element properties based on selected type
        if selected_element_type == "Wall":
            properties = {
                "ID": f"W-{random.randint(1000, 9999)}",
                "Category": "Walls",
                "Family": "Basic Wall",
                "Type": "Interior - 5\" Partition",
                "Base Constraint": "Level 1",
                "Top Constraint": "Level 2",
                "Base Offset": "0'-0\"",
                "Top Offset": "0'-0\"",
                "Length": f"{random.uniform(10, 100):.2f}'",
                "Area": f"{random.uniform(100, 1000):.2f} SF",
                "Volume": f"{random.uniform(50, 500):.2f} CF",
                "Fire Rating": "1 Hour",
                "Structural": "No"
            }
        elif selected_element_type == "Floor":
            properties = {
                "ID": f"F-{random.randint(1000, 9999)}",
                "Category": "Floors",
                "Family": "Floor",
                "Type": "Concrete Slab - 6\"",
                "Level": f"Level {random.randint(1, 15)}",
                "Offset": "0'-0\"",
                "Thickness": "0'-6\"",
                "Area": f"{random.uniform(1000, 10000):.2f} SF",
                "Volume": f"{random.uniform(500, 5000):.2f} CF",
                "Structural": "Yes"
            }
        elif selected_element_type == "Column":
            properties = {
                "ID": f"C-{random.randint(1000, 9999)}",
                "Category": "Columns",
                "Family": "Structural Column",
                "Type": f"W{random.choice(['12', '14', '18', '24'])}{random.randint(50, 120)}",
                "Base Level": f"Level {random.randint(1, 14)}",
                "Top Level": f"Level {random.randint(2, 15)}",
                "Length": f"{random.uniform(10, 15):.2f}'",
                "Volume": f"{random.uniform(20, 100):.2f} CF",
                "Structural": "Yes"
            }
        elif selected_element_type == "Beam":
            properties = {
                "ID": f"B-{random.randint(1000, 9999)}",
                "Category": "Structural Framing",
                "Family": "Structural Beam",
                "Type": f"W{random.choice(['12', '14', '16', '18', '21', '24'])}{random.randint(50, 100)}",
                "Level": f"Level {random.randint(1, 15)}",
                "Start": f"Grid {random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(1, 5)}",
                "End": f"Grid {random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(1, 5)}",
                "Length": f"{random.uniform(10, 50):.2f}'",
                "Volume": f"{random.uniform(20, 80):.2f} CF"
            }
        elif selected_element_type == "Door":
            properties = {
                "ID": f"D-{random.randint(1000, 9999)}",
                "Category": "Doors",
                "Family": "Single-Flush",
                "Type": f"{random.choice(['36', '32', '30'])}\" x {random.choice(['80', '84', '90'])}\"",
                "Level": f"Level {random.randint(1, 15)}",
                "Host": f"W-{random.randint(1000, 9999)}",
                "Fire Rating": random.choice(["None", "20 min", "45 min", "60 min", "90 min"]),
                "Operation": random.choice(["Single swing", "Double swing", "Sliding", "Pocket"])
            }
        elif selected_element_type == "Window":
            properties = {
                "ID": f"WD-{random.randint(1000, 9999)}",
                "Category": "Windows",
                "Family": "Fixed",
                "Type": f"{random.choice(['36', '48', '60'])}\" x {random.choice(['36', '48', '60'])}\"",
                "Level": f"Level {random.randint(1, 15)}",
                "Host": f"W-{random.randint(1000, 9999)}",
                "Sill Height": f"{random.choice(['2', '3', '3.5', '4'])}'-0\"",
                "Operation": random.choice(["Fixed", "Casement", "Double Hung", "Sliding"])
            }
        elif selected_element_type == "MEP Equipment":
            properties = {
                "ID": f"MEP-{random.randint(1000, 9999)}",
                "Category": "Mechanical Equipment",
                "Family": random.choice(["Air Handler", "Chiller", "Fan Coil", "VAV Box"]),
                "Type": f"Size {random.randint(1, 5)}",
                "Level": f"Level {random.randint(1, 15)}",
                "Airflow": f"{random.randint(500, 5000)} CFM",
                "Electrical Load": f"{random.uniform(1, 50):.1f} kW",
                "Weight": f"{random.uniform(100, 2000):.0f} lb"
            }
        else:  # Furniture
            properties = {
                "ID": f"FN-{random.randint(1000, 9999)}",
                "Category": "Furniture",
                "Family": random.choice(["Desk", "Chair", "Table", "Sofa", "Storage"]),
                "Type": f"{random.choice(['Basic', 'Executive', 'Conference', 'Open Plan'])}",
                "Level": f"Level {random.randint(1, 15)}",
                "Width": f"{random.uniform(2, 6):.2f}'",
                "Depth": f"{random.uniform(2, 4):.2f}'",
                "Height": f"{random.uniform(2, 3):.2f}'",
                "Material": random.choice(["Laminate", "Wood", "Metal", "Plastic", "Fabric"])
            }
        
        # Display properties as a table
        property_df = pd.DataFrame({
            "Property": list(properties.keys()),
            "Value": list(properties.values())
        })
        
        st.dataframe(property_df, use_container_width=True)
        
        # Additional information
        st.markdown("### Element Information")
        
        # Create tabs for additional details
        detail_tab1, detail_tab2 = st.tabs(["Parameters", "Relationships"])
        
        with detail_tab1:
            # Generate some random parameters
            parameters = {
                "Comments": "",
                "Mark": f"{selected_element_type[0]}{random.randint(100, 999)}",
                "Phase Created": "New Construction",
                "Phase Demolished": "None",
                "Room Bounding": "Yes" if selected_element_type in ["Wall", "Floor"] else "No",
                "Workset": random.choice(["Shared Levels and Grids", "Architecture", "Structure", "MEP"]),
                "Design Option": "Main Model"
            }
            
            # Add discipline-specific parameters
            if selected_element_type in ["Wall", "Floor"]:
                parameters["Assembly Code"] = f"{random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(1000, 9999)}"
                parameters["Assembly Description"] = f"{selected_element_type}s"
                parameters["OmniClass Number"] = f"{random.randint(21, 23)}-{random.randint(10, 90)}{random.randint(10, 90)} {random.randint(10, 90)}"
            elif selected_element_type in ["Column", "Beam"]:
                parameters["Assembly Code"] = f"{random.choice(['B', 'C'])}{random.randint(1000, 9999)}"
                parameters["Assembly Description"] = f"Structural {selected_element_type}s"
                parameters["Load Bearing"] = "Yes"
            
            # Display parameters
            param_df = pd.DataFrame({
                "Parameter": list(parameters.keys()),
                "Value": list(parameters.values())
            })
            
            st.dataframe(param_df, use_container_width=True)
        
        with detail_tab2:
            # Generate relationships with other elements
            relationships = []
            
            # Number of relationships depends on element type
            relationship_count = {
                "Wall": random.randint(3, 8),
                "Floor": random.randint(5, 12),
                "Column": random.randint(2, 5),
                "Beam": random.randint(3, 7),
                "Door": 1,
                "Window": 1,
                "MEP Equipment": random.randint(3, 6),
                "Furniture": random.randint(0, 2)
            }
            
            count = relationship_count.get(selected_element_type, 2)
            
            for i in range(count):
                # Determine relationship type based on element type
                if selected_element_type == "Wall":
                    if i < 2:
                        rel_type = "Hosted by"
                        related_element = f"Floor ({random.choice(['F-1001', 'F-1002', 'F-1003'])})"
                    elif i < 4:
                        rel_type = "Connected to"
                        related_element = f"Wall ({random.choice(['W-1001', 'W-1002', 'W-1003'])})"
                    else:
                        rel_type = "Hosts"
                        related_element = f"{random.choice(['Door', 'Window'])} ({random.choice(['D-1001', 'WD-1001'])})"
                elif selected_element_type == "Floor":
                    if i < 3:
                        rel_type = "Supported by"
                        related_element = f"{random.choice(['Wall', 'Column'])} ({random.choice(['W-1001', 'C-1001'])})"
                    elif i < 6:
                        rel_type = "Hosts"
                        related_element = f"{random.choice(['Furniture', 'MEP Equipment'])} ({random.choice(['FN-1001', 'MEP-1001'])})"
                    else:
                        rel_type = "Connected to"
                        related_element = f"Floor ({random.choice(['F-1002', 'F-1003'])})"
                else:
                    rel_type = random.choice(["Connected to", "Hosted by", "Hosts", "Intersects"])
                    related_element = f"{random.choice(['Wall', 'Floor', 'Column', 'Beam'])} ({random.choice(['W-1001', 'F-1001', 'C-1001', 'B-1001'])})"
                
                relationships.append({
                    "Type": rel_type,
                    "Related Element": related_element,
                    "ID": f"REL-{random.randint(10000, 99999)}"
                })
            
            # Display relationships
            if relationships:
                rel_df = pd.DataFrame(relationships)
                st.dataframe(rel_df, use_container_width=True)
            else:
                st.info("No relationships found for this element.")

def render_model_details():
    """Render the BIM model details view with metadata and statistics"""
    # Ensure we have a selected model
    if not st.session_state.get("selected_model_id"):
        st.error("No model selected. Please select a model from the list.")
        # Return to list view
        st.session_state.bim_view = "list"
        st.rerun()
        return
    
    # Get the selected model data
    model = st.session_state.get("selected_model_data", None)
    
    if not model:
        # If somehow we have an ID but no data, try to find it
        models = generate_sample_models()
        model = next((m for m in models if m["id"] == st.session_state.selected_model_id), None)
        
        if not model:
            st.error(f"Model with ID {st.session_state.selected_model_id} not found.")
            # Return to list view
            st.session_state.bim_view = "list"
            st.rerun()
            return
    
    # Display model details
    st.subheader(f"Model Details: {model['name']}")
    
    # Create tabs for different details views
    tab1, tab2, tab3, tab4 = st.tabs(["General Info", "Element Count", "Issues", "Revisions"])
    
    # Tab 1: General Information
    with tab1:
        # Create columns for basic info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Basic Information")
            st.markdown(f"**ID:** {model['id']}")
            st.markdown(f"**Name:** {model['name']}")
            st.markdown(f"**Type:** {model['type']}")
            st.markdown(f"**Format:** {model['format']} v{model['version']}")
            st.markdown(f"**File Size:** {model['size']}")
        
        with col2:
            st.markdown("### Timeline")
            st.markdown(f"**Upload Date:** {model['upload_date']}")
            st.markdown(f"**Last Modified:** {model['last_modified']}")
            st.markdown(f"**Author:** {model['author']}")
            
            # Calculate days since last update
            last_modified = datetime.strptime(model['last_modified'], "%Y-%m-%d")
            days_since = (datetime.now() - last_modified).days
            st.markdown(f"**Days Since Update:** {days_since} days")
        
        st.markdown("### Description")
        st.markdown(model['description'])
        
        # Display model thumbnail
        st.image(model['thumbnail'], caption="Model Preview", width=400)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ View Model", use_container_width=True):
                st.session_state.bim_view = "view"
                st.rerun()
        
        with col2:
            if st.button("⬇️ Download Model", use_container_width=True):
                st.toast(f"Downloading {model['name']} ({model['format']})")
        
        with col3:
            if st.button("⬆️ Upload New Version", use_container_width=True):
                st.session_state.bim_view = "upload"
                st.session_state.update_model_id = model['id']
                st.rerun()
    
    # Tab 2: Element Count
    with tab2:
        st.markdown("### Model Element Breakdown")
        
        # Generate random element counts based on model type
        element_types = ["Walls", "Floors", "Ceilings", "Columns", "Beams", "Doors", "Windows", 
                        "Furniture", "Plumbing Fixtures", "Mechanical Equipment", "Electrical Fixtures"]
        
        element_counts = []
        total_elements = 0
        
        for element_type in element_types:
            # Different types of models have different element distributions
            if model['type'] == "Architectural" and element_type in ["Walls", "Doors", "Windows", "Furniture"]:
                count = random.randint(500, 2000)
            elif model['type'] == "Structural" and element_type in ["Columns", "Beams", "Floors"]:
                count = random.randint(500, 2000)
            elif model['type'] == "MEP" and element_type in ["Plumbing Fixtures", "Mechanical Equipment", "Electrical Fixtures"]:
                count = random.randint(500, 2000)
            elif model['type'] == "Civil" and element_type in ["Floors"]:
                count = random.randint(200, 500)
            else:
                count = random.randint(50, 500)
            
            element_counts.append({
                "Element Type": element_type,
                "Count": count
            })
            
            total_elements += count
        
        # Convert to DataFrame
        element_df = pd.DataFrame(element_counts)
        
        # Sort by count
        element_df = element_df.sort_values("Count", ascending=False)
        
        # Display summary
        st.metric("Total Elements", f"{total_elements:,}")
        
        # Create a bar chart
        fig = px.bar(
            element_df, 
            x="Element Type", 
            y="Count",
            title="Element Count by Type",
            color="Count",
            color_continuous_scale="Viridis",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display as a table
        st.dataframe(element_df, use_container_width=True)
    
    # Tab 3: Issues
    with tab3:
        st.markdown("### Model Issues")
        
        # Get all issues related to this model
        all_issues = generate_sample_issues()
        model_issues = [issue for issue in all_issues if issue['model_id'] == model['id']]
        
        # Count issues by status
        status_counts = {}
        for issue in model_issues:
            status = issue['status']
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        # Count issues by priority
        priority_counts = {}
        for issue in model_issues:
            priority = issue['priority']
            if priority in priority_counts:
                priority_counts[priority] += 1
            else:
                priority_counts[priority] = 1
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Issues", len(model_issues))
        
        with col2:
            open_issues = sum(1 for issue in model_issues if issue['status'] in ['Open', 'In Progress'])
            st.metric("Open Issues", open_issues)
        
        with col3:
            high_priority = sum(1 for issue in model_issues if issue['priority'] in ['High', 'Critical'])
            st.metric("High Priority Issues", high_priority)
        
        # Create tabs for different issue views
        issue_tab1, issue_tab2 = st.tabs(["Issue List", "Issue Analytics"])
        
        # Tab 1: Issue List
        with issue_tab1:
            # Filter controls
            col1, col2 = st.columns(2)
            
            with col1:
                # Status filter
                statuses = ["All Statuses"] + sorted(list(set(issue["status"] for issue in model_issues)))
                selected_status = st.selectbox("Status", statuses, key="issue_status_filter")
            
            with col2:
                # Priority filter
                priorities = ["All Priorities"] + sorted(list(set(issue["priority"] for issue in model_issues)))
                selected_priority = st.selectbox("Priority", priorities, key="issue_priority_filter")
            
            # Filter the issues based on selections
            filtered_issues = model_issues
            
            if selected_status != "All Statuses":
                filtered_issues = [issue for issue in filtered_issues if issue["status"] == selected_status]
            
            if selected_priority != "All Priorities":
                filtered_issues = [issue for issue in filtered_issues if issue["priority"] == selected_priority]
            
            # Display the filtered issues
            if filtered_issues:
                # Convert to DataFrame for display
                issues_df = pd.DataFrame(filtered_issues)
                # Select and reorder columns for display
                display_cols = ["id", "title", "status", "priority", "discipline", "location", "assigned_to"]
                st.dataframe(issues_df[display_cols], use_container_width=True)
            else:
                st.info("No issues match the selected filters.")
        
        # Tab 2: Issue Analytics
        with issue_tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Status distribution
                status_df = pd.DataFrame({
                    'Status': list(status_counts.keys()),
                    'Count': list(status_counts.values())
                })
                
                # Create pie chart
                fig = px.pie(
                    status_df, 
                    values='Count', 
                    names='Status',
                    title='Issue Status Distribution',
                    color='Status',
                    color_discrete_map={
                        'Open': '#EF4444',      # Red
                        'In Progress': '#F59E0B',  # Amber
                        'Resolved': '#10B981',    # Green
                        'Verified': '#0EA5E9'    # Blue
                    }
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Priority distribution
                priority_df = pd.DataFrame({
                    'Priority': list(priority_counts.keys()),
                    'Count': list(priority_counts.values())
                })
                
                # Create bar chart
                fig = px.bar(
                    priority_df, 
                    x='Priority', 
                    y='Count',
                    title='Issue Priority Distribution',
                    color='Priority',
                    color_discrete_map={
                        'Low': '#3B82F6',      # Blue
                        'Medium': '#FBBF24',   # Yellow
                        'High': '#F59E0B',     # Amber
                        'Critical': '#EF4444'  # Red
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Display issues by location
            st.subheader("Issues by Location")
            
            # Count issues by location
            location_counts = {}
            for issue in model_issues:
                location = issue['location']
                if location in location_counts:
                    location_counts[location] += 1
                else:
                    location_counts[location] = 1
            
            # Convert to DataFrame
            location_df = pd.DataFrame({
                'Location': list(location_counts.keys()),
                'Count': list(location_counts.values())
            })
            
            # Sort by location (level)
            location_df['Level'] = location_df['Location'].str.extract(r'Level (\d+)').astype(int)
            location_df = location_df.sort_values('Level')
            
            # Create bar chart
            fig = px.bar(
                location_df, 
                x='Location', 
                y='Count',
                title='Issues by Location',
                color='Count',
                color_continuous_scale='Viridis'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Revisions
    with tab4:
        st.markdown("### Model Revision History")
        
        # Generate random revision history
        current_version = float(model['version'])
        revisions = []
        
        # Generate between 1-5 prior versions
        revision_count = int(current_version * 10) - 9  # e.g., version 2.0 would have 11 revisions
        revision_count = max(1, min(revision_count, 10))  # Cap between 1-10 revisions
        
        for i in range(revision_count):
            version = float(f"{1}.{i}")
            
            # Earlier dates for earlier versions
            days_back = (revision_count - i) * random.randint(15, 30)
            date = datetime.strptime(model['last_modified'], "%Y-%m-%d") - timedelta(days=days_back)
            
            if version == current_version:
                date = datetime.strptime(model['last_modified'], "%Y-%m-%d")
            
            revisions.append({
                "Version": f"{version:.1f}",
                "Date": date.strftime("%Y-%m-%d"),
                "Author": random.choice(["J. Smith", "L. Johnson", "A. Martinez", "K. Wong", "S. Davis"]),
                "Changes": generate_revision_notes(model['type'], i, revision_count)
            })
        
        # Add current version
        revisions.append({
            "Version": model['version'],
            "Date": model['last_modified'],
            "Author": model['author'],
            "Changes": "Current version"
        })
        
        # Sort by version in descending order (newest first)
        revisions.sort(key=lambda x: float(x["Version"]), reverse=True)
        
        # Create a dataframe for display
        revision_df = pd.DataFrame(revisions)
        
        # Display the revision history
        st.dataframe(revision_df, use_container_width=True)
        
        # Create a version timeline chart
        version_timeline = []
        for rev in revisions:
            version_timeline.append({
                'Version': rev['Version'],
                'Date': datetime.strptime(rev['Date'], "%Y-%m-%d"),
                'x': datetime.strptime(rev['Date'], "%Y-%m-%d"),
                'y': float(rev['Version'])
            })
        
        # Convert to DataFrame
        timeline_df = pd.DataFrame(version_timeline)
        
        # Create a line chart
        fig = px.line(
            timeline_df, 
            x='Date', 
            y='Version',
            title='Model Version Timeline',
            markers=True,
            labels={'Version': 'Model Version', 'Date': 'Release Date'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

def generate_revision_notes(model_type, revision_index, total_revisions):
    """Generate realistic revision notes based on model type and revision progress"""
    early_revisions = [
        "Initial model setup",
        "Basic geometry and layout",
        "Core structural elements",
        "Building envelope",
        "Preliminary floor layouts"
    ]
    
    mid_revisions = {
        "Architectural": [
            "Updated interior wall layouts",
            "Added door and window details",
            "Refined facade elements",
            "Added interior finishes",
            "Updated ceiling plans"
        ],
        "Structural": [
            "Updated column layout",
            "Refined structural connections",
            "Added reinforcement details",
            "Updated foundation elements",
            "Improved structural framing"
        ],
        "MEP": [
            "Added primary duct routing",
            "Updated equipment locations",
            "Added electrical fixtures",
            "Refined piping layouts",
            "Updated mechanical room layouts"
        ],
        "Civil": [
            "Updated site grading",
            "Added utility connections",
            "Refined parking layout",
            "Updated drainage details",
            "Added landscaping elements"
        ]
    }
    
    late_revisions = [
        "Coordination updates with other disciplines",
        "Resolved clash issues",
        "Model cleanup and optimization",
        "Added metadata and parameters",
        "Final adjustments for construction documents"
    ]
    
    # Choose appropriate notes based on revision progress
    progress = revision_index / total_revisions
    
    if progress < 0.3:
        # Early development
        return early_revisions[revision_index % len(early_revisions)]
    elif progress < 0.7:
        # Middle development - use discipline-specific notes
        discipline_notes = mid_revisions.get(model_type, mid_revisions["Architectural"])
        return discipline_notes[revision_index % len(discipline_notes)]
    else:
        # Late development
        return late_revisions[revision_index % len(late_revisions)]

def render_model_upload():
    """Render the BIM model upload/edit form"""
    # Check if we're updating an existing model
    is_update = st.session_state.get("update_model_id") is not None
    
    if is_update:
        st.subheader("Update BIM Model")
        # Get the model data for updating
        model_id = st.session_state.get("update_model_id")
        models = generate_sample_models()
        model = next((m for m in models if m["id"] == model_id), None)
        
        if not model:
            st.error(f"Model with ID {model_id} not found.")
            # Return to list view
            st.session_state.bim_view = "list"
            st.session_state.update_model_id = None
            st.rerun()
            return
    else:
        st.subheader("Upload New BIM Model")
        # Initialize with default values
        model = {
            "id": f"model-{random.randint(100, 999)}",
            "name": "",
            "description": "",
            "type": "",
            "format": "",
            "version": "1.0",
            "upload_date": datetime.now().strftime("%Y-%m-%d"),
            "last_modified": datetime.now().strftime("%Y-%m-%d"),
            "size": "",
            "author": "",
            "path": "",
            "thumbnail": ""
        }
    
    # Create the form
    with st.form(key="model_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            # Model name
            name = st.text_input("Model Name *", value=model.get("name", ""))
            
            # Model type
            model_types = ["Architectural", "Structural", "MEP", "Civil", "Coordination", "Other"]
            
            # Find index of selected type if updating
            type_index = 0
            if is_update and model.get("type") in model_types:
                type_index = model_types.index(model.get("type"))
            
            selected_type = st.selectbox(
                "Model Type *",
                model_types,
                index=type_index
            )
        
        with col2:
            # Model format
            formats = ["IFC", "RVT", "NWD", "DGN", "Other"]
            
            # Find index of selected format if updating
            format_index = 0
            if is_update and model.get("format") in formats:
                format_index = formats.index(model.get("format"))
            
            selected_format = st.selectbox(
                "File Format *",
                formats,
                index=format_index
            )
            
            # Version
            version = st.text_input("Version *", value=model.get("version", "1.0"))
            
            # Author
            author = st.text_input("Author *", value=model.get("author", ""))
        
        # Description
        description = st.text_area(
            "Description *",
            value=model.get("description", ""),
            height=100,
            placeholder="Provide a description of the model..."
        )
        
        # File upload (only for new models or updates)
        uploaded_file = st.file_uploader(
            "Upload Model File *" if not is_update else "Upload New Version",
            type=["ifc", "rvt", "nwd", "dgn", "zip"],
            help="Upload a BIM model file. For large files, consider using a compressed (ZIP) format."
        )
        
        # Upload thumbnail
        uploaded_thumbnail = st.file_uploader(
            "Upload Thumbnail Image",
            type=["png", "jpg", "jpeg"],
            help="Upload a thumbnail image for the model."
        )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Update Model" if is_update else "Upload Model",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not name:
            st.error("Please enter a model name.")
            return
        
        if not description:
            st.error("Please enter a description.")
            return
        
        if not version:
            st.error("Please enter a version number.")
            return
        
        if not author:
            st.error("Please enter an author.")
            return
        
        # Validate file upload for new models
        if not is_update and not uploaded_file:
            st.error("Please upload a model file.")
            return
        
        # In a real app, this would save to database and file storage
        if is_update:
            st.success(f"Model {model['name']} updated to version {version}!")
            # Clear update flag
            st.session_state.update_model_id = None
        else:
            st.success(f"Model {name} uploaded successfully!")
        
        # Return to list view
        st.session_state.bim_view = "list"
        st.rerun()
    
    if cancel_button:
        # Clear update flag if set
        if st.session_state.get("update_model_id"):
            st.session_state.update_model_id = None
        
        # Return to list view
        st.session_state.bim_view = "list"
        st.rerun()

def render_model_analytics():
    """Render BIM analytics with charts and metrics"""
    st.subheader("BIM Analytics Dashboard")
    
    # Get sample data
    models = generate_sample_models()
    issues = generate_sample_issues()
    
    # Calculate summary metrics
    total_models = len(models)
    total_issues = len(issues)
    open_issues = sum(1 for issue in issues if issue["status"] in ["Open", "In Progress"])
    resolved_issues = sum(1 for issue in issues if issue["status"] in ["Resolved", "Verified"])
    
    # Summary metrics in a nice grid
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Models", f"{total_models}")
    
    with col2:
        st.metric("Total Issues", f"{total_issues}")
    
    with col3:
        st.metric("Open Issues", f"{open_issues}", delta=f"{-open_issues} to resolve")
    
    with col4:
        resolution_rate = resolved_issues / total_issues if total_issues > 0 else 0
        st.metric("Resolution Rate", f"{resolution_rate:.0%}")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Model Statistics", "Issue Analysis", "Model Activity"])
    
    # Tab 1: Model Statistics
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Model type distribution
            type_counts = {}
            for model in models:
                model_type = model["type"]
                if model_type in type_counts:
                    type_counts[model_type] += 1
                else:
                    type_counts[model_type] = 1
            
            # Create DataFrame
            type_df = pd.DataFrame({
                'Model Type': list(type_counts.keys()),
                'Count': list(type_counts.values())
            })
            
            # Create pie chart
            fig = px.pie(
                type_df, 
                values='Count', 
                names='Model Type',
                title='Model Type Distribution',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Model format distribution
            format_counts = {}
            for model in models:
                model_format = model["format"]
                if model_format in format_counts:
                    format_counts[model_format] += 1
                else:
                    format_counts[model_format] = 1
            
            # Create DataFrame
            format_df = pd.DataFrame({
                'Format': list(format_counts.keys()),
                'Count': list(format_counts.values())
            })
            
            # Create pie chart
            fig = px.pie(
                format_df, 
                values='Count', 
                names='Format',
                title='Model Format Distribution',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Model size analysis
        st.subheader("Model Size Analysis")
        
        # Parse size strings to numeric values (MB)
        model_sizes = []
        for model in models:
            size_str = model["size"]
            if "MB" in size_str:
                size_mb = float(size_str.split()[0])
                model_sizes.append({
                    "Model": model["name"],
                    "Size (MB)": size_mb,
                    "Type": model["type"]
                })
        
        # Convert to DataFrame
        size_df = pd.DataFrame(model_sizes)
        
        # Create bar chart
        fig = px.bar(
            size_df, 
            x='Model', 
            y='Size (MB)',
            color='Type',
            title='Model Size Comparison',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Issue Analysis
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Issue status distribution
            status_counts = {}
            for issue in issues:
                status = issue["status"]
                if status in status_counts:
                    status_counts[status] += 1
                else:
                    status_counts[status] = 1
            
            # Create DataFrame
            status_df = pd.DataFrame({
                'Status': list(status_counts.keys()),
                'Count': list(status_counts.values())
            })
            
            # Create pie chart
            fig = px.pie(
                status_df, 
                values='Count', 
                names='Status',
                title='Issue Status Distribution',
                color='Status',
                color_discrete_map={
                    'Open': '#EF4444',      # Red
                    'In Progress': '#F59E0B',  # Amber
                    'Resolved': '#10B981',    # Green
                    'Verified': '#0EA5E9'    # Blue
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Issue priority distribution
            priority_counts = {}
            for issue in issues:
                priority = issue["priority"]
                if priority in priority_counts:
                    priority_counts[priority] += 1
                else:
                    priority_counts[priority] = 1
            
            # Create DataFrame
            priority_df = pd.DataFrame({
                'Priority': list(priority_counts.keys()),
                'Count': list(priority_counts.values())
            })
            
            # Sort by priority level
            priority_order = ['Critical', 'High', 'Medium', 'Low']
            priority_df['Priority'] = pd.Categorical(priority_df['Priority'], categories=priority_order, ordered=True)
            priority_df = priority_df.sort_values('Priority')
            
            # Create bar chart
            fig = px.bar(
                priority_df, 
                x='Priority', 
                y='Count',
                title='Issue Priority Distribution',
                color='Priority',
                color_discrete_map={
                    'Critical': '#EF4444',  # Red
                    'High': '#F59E0B',      # Amber
                    'Medium': '#FBBF24',    # Yellow
                    'Low': '#3B82F6'        # Blue
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Issues by discipline
        st.subheader("Issues by Discipline")
        
        # Count issues by discipline
        discipline_counts = {}
        for issue in issues:
            discipline = issue["discipline"]
            if discipline in discipline_counts:
                discipline_counts[discipline] += 1
            else:
                discipline_counts[discipline] = 1
        
        # Create DataFrame
        discipline_df = pd.DataFrame({
            'Discipline': list(discipline_counts.keys()),
            'Count': list(discipline_counts.values())
        })
        
        # Sort by count
        discipline_df = discipline_df.sort_values('Count', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            discipline_df, 
            x='Discipline', 
            y='Count',
            title='Issues by Discipline',
            color='Count',
            color_continuous_scale='Viridis',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Issues by location (level)
        st.subheader("Issues by Location")
        
        # Count issues by location
        location_counts = {}
        for issue in issues:
            location = issue["location"]
            if location in location_counts:
                location_counts[location] += 1
            else:
                location_counts[location] = 1
        
        # Create DataFrame
        location_df = pd.DataFrame({
            'Location': list(location_counts.keys()),
            'Count': list(location_counts.values())
        })
        
        # Extract level numbers for sorting
        location_df['Level'] = location_df['Location'].str.extract(r'Level (\d+)').astype(int)
        location_df = location_df.sort_values('Level')
        
        # Create bar chart
        fig = px.bar(
            location_df, 
            x='Location', 
            y='Count',
            title='Issues by Location',
            color='Count',
            color_continuous_scale='Viridis',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Model Activity
    with tab3:
        st.subheader("Model Activity Timeline")
        
        # Create a timeline of model uploads and modifications
        activity_data = []
        
        for model in models:
            # Add upload event
            upload_date = datetime.strptime(model["upload_date"], "%Y-%m-%d")
            activity_data.append({
                'Date': upload_date,
                'Activity': 'Upload',
                'Model': model["name"],
                'Type': model["type"]
            })
            
            # Add modification event if different from upload date
            last_modified = datetime.strptime(model["last_modified"], "%Y-%m-%d")
            if last_modified > upload_date:
                activity_data.append({
                    'Date': last_modified,
                    'Activity': 'Modification',
                    'Model': model["name"],
                    'Type': model["type"]
                })
        
        # Add issue creation events
        for issue in issues:
            created_date = datetime.strptime(issue["created_date"], "%Y-%m-%d")
            activity_data.append({
                'Date': created_date,
                'Activity': 'Issue Created',
                'Model': next((m["name"] for m in models if m["id"] == issue["model_id"]), "Unknown"),
                'Type': 'Issue'
            })
            
            # Add issue resolution events
            if issue["resolution_date"]:
                resolution_date = datetime.strptime(issue["resolution_date"], "%Y-%m-%d")
                activity_data.append({
                    'Date': resolution_date,
                    'Activity': 'Issue Resolved',
                    'Model': next((m["name"] for m in models if m["id"] == issue["model_id"]), "Unknown"),
                    'Type': 'Issue'
                })
        
        # Convert to DataFrame
        activity_df = pd.DataFrame(activity_data)
        
        # Sort by date
        activity_df = activity_df.sort_values('Date')
        
        # Group by week and activity
        activity_df['Week'] = activity_df['Date'].dt.strftime('%Y-%W')
        activity_by_week = activity_df.groupby(['Week', 'Activity']).size().reset_index(name='Count')
        
        # Create the figure
        fig = px.line(
            activity_by_week,
            x='Week',
            y='Count',
            color='Activity',
            title='Model Activity Over Time',
            markers=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show recent activity
        st.subheader("Recent Activity")
        
        # Sort by date in descending order (newest first)
        recent_activity = activity_df.sort_values('Date', ascending=False).head(10)
        
        # Format date for display
        recent_activity['Date'] = recent_activity['Date'].dt.strftime('%Y-%m-%d')
        
        # Display recent activity
        st.dataframe(recent_activity[['Date', 'Activity', 'Model']], use_container_width=True)