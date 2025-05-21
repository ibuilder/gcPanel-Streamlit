"""
Simple BIM Viewer - A standalone module for BIM visualization.

This module provides a simple, self-contained BIM viewer that doesn't depend on other
components in the gcPanel application. It can be used independently without
interfering with other modules.
"""

import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
from utils.style_manager import load_css

def render_standalone_bim():
    """Render a simplified BIM viewer that works independently"""
    # Load dedicated CSS for standalone BIM module
    load_css("standalone_bim.css")
    
    st.markdown("<h1 style='text-align: center;'>BIM Model Viewer</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='bim-standalone-container'>", unsafe_allow_html=True)
        
        # Project model selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Available Models")
            
            # Demo models data
            models = [
                {"name": "Highland Tower - Architectural", "type": "IFC", "size": "42.5 MB", "updated": "2023-05-15", "status": "Current"},
                {"name": "Highland Tower - Structural", "type": "IFC", "size": "38.2 MB", "updated": "2023-05-10", "status": "Current"},
                {"name": "Highland Tower - MEP", "type": "IFC", "size": "56.3 MB", "updated": "2023-05-12", "status": "Current"},
                {"name": "Sample Building", "type": "IFC", "size": "22.1 MB", "updated": "2023-04-20", "status": "Reference"}
            ]
            
            # Create cards for each model
            for model in models:
                with st.container():
                    st.markdown(f"""
                    <div class='model-card'>
                        <h3>{model['name']}</h3>
                        <p><strong>Type:</strong> {model['type']} | <strong>Size:</strong> {model['size']} | <strong>Updated:</strong> {model['updated']}</p>
                        <p><strong>Status:</strong> {model['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Model Controls")
            st.markdown("<div class='bim-controls'>", unsafe_allow_html=True)
            
            # Simple mock controls
            st.selectbox("Select Model", ["Highland Tower - Architectural", "Highland Tower - Structural", "Highland Tower - MEP", "Sample Building"])
            st.selectbox("View Mode", ["3D", "Floor Plan", "Section"])
            
            # Simple toggles for visibility
            st.checkbox("Show Dimensions", value=True)
            st.checkbox("Show Properties", value=True)
            st.checkbox("Enable Clash Detection", value=False)
            
            st.button("Load Model")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Model viewer placeholder
        st.subheader("3D Viewer")
        with st.container():
            st.markdown("<div class='bim-viewer-container'>", unsafe_allow_html=True)
            st.image("attached_assets/TallBuilding.ifc", caption="BIM Model Preview")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Properties and clash detection in tabs
        tab1, tab2 = st.tabs(["Properties", "Clash Detection"])
        
        with tab1:
            st.markdown("<div class='properties-panel'>", unsafe_allow_html=True)
            st.subheader("Element Properties")
            st.write("Select an element in the model to view its properties")
            
            # Example properties table
            properties = {
                "ID": "WALL-001",
                "Type": "Wall",
                "Material": "Concrete",
                "Dimensions": "4.5m x 0.3m x 3.2m",
                "Level": "Floor 3",
                "Fire Rating": "2 hours"
            }
            
            for key, value in properties.items():
                st.markdown(f"**{key}:** {value}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='properties-panel'>", unsafe_allow_html=True)
            st.subheader("Clash Detection Results")
            
            # Example clash detection results
            clash_data = {
                "ID": ["CL-001", "CL-002", "CL-003", "CL-004", "CL-005"],
                "Type": ["Hard Clash", "Clearance Clash", "Hard Clash", "Duplicate", "Hard Clash"],
                "Elements": ["Beam B45 / Duct D12", "Pipe P78 / Wall W34", "Column C22 / Conduit E15", "Door D56 / Door D57", "Beam B22 / Pipe P45"],
                "Location": ["Floor 4, Grid C-5", "Floor 2, Grid D-8", "Floor 3, Grid A-2", "Floor 1, Grid E-3", "Floor 5, Grid B-6"],
                "Status": ["New", "Resolved", "In Review", "New", "Resolved"],
                "Severity": ["High", "Medium", "High", "Low", "Medium"]
            }
            
            clash_df = pd.DataFrame(clash_data)
            
            # Display clashes in a table
            st.markdown("<table class='clash-results'>", unsafe_allow_html=True)
            st.markdown("<tr><th>ID</th><th>Type</th><th>Elements</th><th>Location</th><th>Status</th><th>Severity</th></tr>", unsafe_allow_html=True)
            
            for i, row in clash_df.iterrows():
                status_class = f"clash-status-{row['Status'].lower().replace(' ', '-')}"
                st.markdown(f"""
                <tr>
                    <td>{row['ID']}</td>
                    <td>{row['Type']}</td>
                    <td>{row['Elements']}</td>
                    <td>{row['Location']}</td>
                    <td class='{status_class}'>{row['Status']}</td>
                    <td>{row['Severity']}</td>
                </tr>
                """, unsafe_allow_html=True)
            
            st.markdown("</table>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.title("BIM Model Viewer")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Model Gallery", "3D Viewer", "Clash Detection"])
    
    # Tab 1: Model Gallery
    with tab1:
        st.header("Model Gallery")
        
        # Simple filter options 
        col1, col2 = st.columns(2)
        with col1:
            model_type = st.selectbox("Model Type", 
                                     ["All Types", "Architectural", "Structural", "MEP", "Civil"])
        with col2:
            search_term = st.text_input("Search Models", placeholder="Search by name or ID...")
        
        # Sample model data
        models = [
            {
                "name": "Highland Tower - Full Model",
                "type": "Architectural",
                "revision": "2.0",
                "date": "2025-04-15",
                "thumbnail": "gcpanel.png"
            },
            {
                "name": "Highland Tower - Structural",
                "type": "Structural",
                "revision": "1.5",
                "date": "2025-04-02",
                "thumbnail": "gcpanel.png"
            },
            {
                "name": "Highland Tower - MEP",
                "type": "MEP",
                "revision": "1.3",
                "date": "2025-03-20",
                "thumbnail": "gcpanel.png"
            },
            {
                "name": "Highland Tower - Site",
                "type": "Civil",
                "revision": "1.2",
                "date": "2025-02-28",
                "thumbnail": "gcpanel.png"
            }
        ]
        
        # Filter models
        if model_type != "All Types":
            models = [m for m in models if m["type"] == model_type]
            
        if search_term:
            models = [m for m in models if search_term.lower() in m["name"].lower()]
        
        # Display models in a grid
        if not models:
            st.info("No models match your search criteria.")
        else:
            # Use columns to create a grid
            col1, col2 = st.columns(2)
            
            for i, model in enumerate(models):
                # Alternate between columns
                with col1 if i % 2 == 0 else col2:
                    # Create a card for the model using st.container()
                    with st.container():
                        # Create a bordered container with CSS
                        st.markdown("""
                        <style>
                        .model-card {
                            border: 1px solid #e0e0e0;
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 20px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"<div class='model-card'>", unsafe_allow_html=True)
                        
                        # Display model thumbnail
                        st.image(model["thumbnail"], use_column_width=True)
                        
                        # Model info
                        st.subheader(model["name"])
                        st.write(f"Type: {model['type']} | Rev: {model['revision']} | Updated: {model['date']}")
                        
                        # Action buttons
                        col1a, col2a = st.columns(2)
                        with col1a:
                            st.button("View", key=f"view_{i}")
                        with col2a:
                            st.button("Details", key=f"details_{i}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 2: 3D Viewer
    with tab2:
        st.header("3D Model Viewer")
        
        # Model selection
        selected_model = st.selectbox(
            "Select Model",
            ["Highland Tower - Full Model", "Highland Tower - Structural", 
             "Highland Tower - MEP", "Highland Tower - Site"]
        )
        
        # View options
        col1, col2, col3 = st.columns(3)
        with col1:
            view_mode = st.radio("View Mode", ["Shaded", "Wireframe", "Hidden Line"])
        with col2:
            st.checkbox("Show Grid", value=True)
        with col3:
            measure_on = st.checkbox("Measurement Tool", value=False)
        
        # Display the 3D viewer (placeholder)
        st.image("gcpanel.png", caption="3D Model View", use_column_width=True)
        
        # Add some controls below the viewer
        st.subheader("Model Navigation")
        st.markdown("""
        - **Left-click + drag**: Rotate the model
        - **Right-click + drag**: Pan the model
        - **Scroll wheel**: Zoom in/out
        - **Double-click**: Focus on element
        """)
        
        if measure_on:
            st.info("Measurement tool active. Click two points to measure distance.")
        
        # Element properties (sample)
        st.subheader("Selected Element Properties")
        
        # Sample element data
        element_props = {
            "ID": "W-1234",
            "Category": "Walls",
            "Type": "Interior - 5\" Partition",
            "Material": "Gypsum Board",
            "Length": "12.5 ft",
            "Height": "10.0 ft",
            "Fire Rating": "1 Hr",
            "Level": "Level 3"
        }
        
        # Convert to DataFrame for display
        props_df = pd.DataFrame({"Property": element_props.keys(), "Value": element_props.values()})
        st.table(props_df)
    
    # Tab 3: Clash Detection
    with tab3:
        st.header("Clash Detection")
        
        col1, col2 = st.columns(2)
        with col1:
            clash_tolerance = st.slider("Clash Tolerance (mm)", 0, 50, 10)
        with col2:
            run_clash = st.button("Run Clash Detection", key="run_clash")
        
        # Select disciplines to check
        st.multiselect(
            "Select Disciplines to Check",
            ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing"],
            default=["Structural", "Mechanical", "Electrical"]
        )
        
        # Display sample clash results
        st.subheader("Clash Results")
        
        # Sample clash data
        clash_data = [
            {"id": "CLH-001", "type": "Hard", "discipline1": "Structural", "discipline2": "Mechanical", 
             "element1": "Beam B-1023", "element2": "Duct D-4501", "status": "New"},
            {"id": "CLH-002", "type": "Hard", "discipline1": "Mechanical", "discipline2": "Electrical", 
             "element1": "Duct D-4505", "element2": "Conduit E-3342", "status": "Resolved"},
            {"id": "CLH-003", "type": "Clearance", "discipline1": "Structural", "discipline2": "Plumbing", 
             "element1": "Column C-2241", "element2": "Pipe P-5567", "status": "New"},
            {"id": "CLH-004", "type": "Hard", "discipline1": "Mechanical", "discipline2": "Plumbing", 
             "element1": "Air Handler AHU-01", "element2": "Pipe P-5570", "status": "In Review"}
        ]
        
        # Create DataFrame for display
        clash_df = pd.DataFrame(clash_data)
        
        # Display the clash list
        st.table(clash_df)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Clashes", "4")
        with col2:
            st.metric("Open Clashes", "3")
        with col3:
            st.metric("Resolved", "1")