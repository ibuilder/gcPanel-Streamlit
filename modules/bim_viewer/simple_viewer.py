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
    
    # Display static visualization
    st.markdown("""
    <div style="background-color: #f5f5f5; border-radius: 8px; padding: 20px; text-align: center; height: 400px;">
        <h3 style="margin-bottom: 20px;">Highland Tower 3D Model</h3>
        <div style="display: flex; justify-content: center;">
            <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                <!-- Base building shape -->
                <rect x="100" y="200" width="200" height="80" fill="#ddd" stroke="#999" />
                
                <!-- Tower -->
                <rect x="150" y="50" width="100" height="150" fill="#ccc" stroke="#999" />
                
                <!-- Windows -->
                <rect x="160" y="70" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="190" y="70" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="220" y="70" width="20" height="20" fill="#aaddff" stroke="#999" />
                
                <rect x="160" y="100" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="190" y="100" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="220" y="100" width="20" height="20" fill="#aaddff" stroke="#999" />
                
                <rect x="160" y="130" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="190" y="130" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="220" y="130" width="20" height="20" fill="#aaddff" stroke="#999" />
                
                <rect x="160" y="160" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="190" y="160" width="20" height="20" fill="#aaddff" stroke="#999" />
                <rect x="220" y="160" width="20" height="20" fill="#aaddff" stroke="#999" />
                
                <!-- Entrance -->
                <rect x="190" y="230" width="20" height="30" fill="#333" />
                
                <!-- Roof elements -->
                <rect x="150" y="30" width="100" height="20" fill="#aaa" stroke="#999" />
                
                <!-- Text label -->
                <text x="200" y="245" text-anchor="middle" font-family="Arial" font-size="10" fill="white">ENTRANCE</text>
                
                <!-- Building name -->
                <text x="200" y="20" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Highland Tower</text>
            </svg>
        </div>
        <div style="margin-top: 20px; color: #666;">
            Selected model: {0}
        </div>
    </div>
    """.format(selected_ifc), unsafe_allow_html=True)
    
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