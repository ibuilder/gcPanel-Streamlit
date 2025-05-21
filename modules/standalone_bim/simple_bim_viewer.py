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
            # Use a placeholder image instead since IFC files cannot be displayed directly as images
            try:
                st.image("gcpanel.png", caption="BIM Model Preview (Sample Visualization)")
            except:
                st.warning("Model visualization could not be loaded. Please upload a model image.")
                st.file_uploader("Upload a model preview image", type=["png", "jpg", "jpeg"])
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
            
            # Display clashes using Streamlit's native table component instead of HTML
            st.table(clash_df)
            
            # Removed closing table tag as we're using st.table instead of custom HTML
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    # End of the standalone BIM module