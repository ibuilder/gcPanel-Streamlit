"""
Basic BIM Viewer module with simplified visualization.
"""

import streamlit as st
import os

def render_basic_bim_viewer():
    """Render a basic BIM Viewer with simplified visualization."""
    
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
    
    # Create a layout for the model view
    st.markdown("### 3D Building Visualization")
    
    # Info about the model viewer
    with st.expander("About the model viewer", expanded=True):
        st.info("""
        This is a simplified building model visualization. In a full implementation, 
        this would be a 3D interactive model that you could rotate, zoom, and examine in detail.
        
        The current view shows a representation of the Highland Tower Development.
        """)
    
    # Create a visual representation of the building using columns
    st.markdown("#### Building Structure")
    
    # Create a simplified building representation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Display floor levels
        st.markdown("##### Floor Stack")
        st.progress(1.0, text="Penthouse (Floor 15)")
        st.progress(0.9, text="Upper Floors (12-14)")
        st.progress(0.8, text="Mid Floors (9-11)")
        st.progress(0.7, text="Mid Floors (6-8)")
        st.progress(0.6, text="Lower Floors (4-5)")
        st.progress(0.5, text="Lower Floors (2-3)")
        st.progress(0.3, text="Retail/Amenities (Floor 1)")
        st.progress(0.2, text="Lobby (Ground Floor)")
        st.progress(0.1, text="Basement Parking (B1)")
        st.progress(0.05, text="Basement Parking (B2)")
    
    # BIM Details
    st.markdown("#### Model Details")
    
    # Create tabs for different model information
    tabs = st.tabs(["Project Details", "Floors", "Elements"])
    
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
    st.subheader("Model Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Export Model")
    with col2:
        st.button("Generate Report")
    with col3:
        st.button("Share Model")