"""
Simple BIM Viewer module with static visualization.
"""

import streamlit as st
import os

def render_simple_bim_viewer():
    """Render a simple BIM Viewer with static visualization."""
    
    st.title("BIM Viewer")
    
    # Sample IFC file selection
    st.subheader("Building Model Viewer")
    
    # List available IFC files
    ifc_files = []
    for file in os.listdir("static/models"):
        if file.endswith(".ifc"):
            ifc_files.append(file)
    
    # Default to TallBuilding.ifc if available
    default_index = 0
    if "TallBuilding.ifc" in ifc_files:
        default_index = ifc_files.index("TallBuilding.ifc")
    
    selected_ifc = st.selectbox(
        "Select building model", 
        ifc_files,
        index=default_index
    )
    
    # Display a header for the model
    st.subheader(f"Building Model: {selected_ifc}")
    
    # Display a building image with Streamlit components instead of HTML/SVG
    st.info("3D model visualization - Highland Tower")
    
    # Create a simple building representation with native Streamlit components
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Display an image placeholder using expander and progress bars for visualization
        with st.expander("Building Structure", expanded=True):
            st.markdown("### Highland Tower")
            
            # Display floor levels with progress bars
            st.markdown("##### Floors")
            st.progress(1.0, text="Penthouse")
            st.progress(0.9, text="Floor 12-14")
            st.progress(0.7, text="Floor 7-11")
            st.progress(0.5, text="Floor 4-6")
            st.progress(0.3, text="Floor 1-3")
            st.progress(0.1, text="Lobby")
            
            # Show selected model
            st.markdown(f"**Selected Model**: {selected_ifc}")
            
            # Display dimensions
            st.markdown("##### Dimensions")
            st.code("""
            Width: 35m
            Length: 40m
            Height: 60m
            Gross Area: 168,500 sq ft
            """)
    
    # Display model controls
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Rotate View")
    with col2:
        st.button("Explode View") 
    with col3:
        st.button("Reset View")
    
    # Display model information
    st.subheader("Model Information")
    
    # Create tabs for different aspects of the model
    tabs = st.tabs(["Project Details", "Levels", "Elements"])
    
    with tabs[0]:
        st.markdown("""
        ### Highland Tower Development
        - **Type**: Mixed-use building
        - **Value**: $45.5M
        - **Area**: 168,500 sq ft
        - **Floors**: 15 stories above ground, 2 below
        - **Units**: 120 residential, 8 retail
        - **Architect**: Robertson Architects
        - **Structural Engineer**: Miller & Associates
        - **MEP Engineer**: Dawson Engineering
        """)
    
    with tabs[1]:
        st.markdown("""
        ### Building Levels
        | Level | Function | Area (sq ft) | Floor-to-Ceiling (ft) |
        |-------|----------|--------------|-------------|
        | B2 | Parking | 12,500 | 9.0 |
        | B1 | Parking/Storage | 12,500 | 9.0 |
        | G | Lobby/Retail | 11,500 | 14.0 |
        | 1 | Retail/Amenities | 11,500 | 12.0 |
        | 2-3 | Residential | 11,000 | 10.0 |
        | 4-14 | Residential | 10,000 | 10.0 |
        | 15 | Residential/Mech | 8,000 | 12.0 |
        """)
    
    with tabs[2]:
        st.markdown("""
        ### Building Elements
        | Category | Count | Status |
        |----------|-------|--------|
        | Walls | 645 | Approved |
        | Doors | 392 | Approved |
        | Windows | 258 | Approved |
        | Floors | 17 | Approved |
        | Columns | 210 | Approved |
        | Beams | 380 | Approved |
        | MEP Systems | 124 | In Review |
        | Furniture | 85 | Not Started |
        """)
        
    # Add action buttons
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Export Model")
    with col2:
        st.button("Generate Report")
    with col3:
        st.button("Share Model")