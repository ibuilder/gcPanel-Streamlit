"""
BIM Viewer module with interactive 3D visualization using Streamlit Elements.
"""

import streamlit as st
import os
from streamlit_elements import elements, mui, html, three

def render_simple_bim_viewer():
    """Render an interactive BIM Viewer with Streamlit Elements."""
    
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
    
    # Create an interactive 3D viewer using Streamlit Elements
    st.markdown("### 3D Building Model - Interactive View")
    
    # Viewer container with fixed height
    with st.container():
        # Use streamlit_elements to create an interactive 3D viewer
        with elements("interactive_building_viewer"):
            # Create a card to contain the 3D scene
            with mui.Box(sx={"height": "500px", "border": "1px solid #ddd", "borderRadius": "8px"}):
                # Create a Three.js scene
                with three.Scene(
                    className="full-screen",
                    camera={"position": [10, 10, 10]},
                    background="#f5f5f5"
                ):
                    # Add ambient light
                    three.AmbientLight(intensity=0.6)
                    
                    # Add directional light
                    three.DirectionalLight(
                        position=[10, 20, 10],
                        intensity=0.8,
                        castShadow=True
                    )

                    # Create a basic building model
                    # Base (ground floor)
                    three.Mesh(
                        geometry=three.BoxGeometry(width=10, height=0.5, depth=10),
                        material=three.MeshStandardMaterial(color="#999"),
                        position=[0, 0, 0],
                        receiveShadow=True,
                        castShadow=True
                    )
                    
                    # Tower base
                    three.Mesh(
                        geometry=three.BoxGeometry(width=8, height=2, depth=8),
                        material=three.MeshStandardMaterial(color="#ccc"),
                        position=[0, 1.25, 0],
                        receiveShadow=True,
                        castShadow=True
                    )
                    
                    # Main tower
                    three.Mesh(
                        geometry=three.BoxGeometry(width=6, height=10, depth=6),
                        material=three.MeshStandardMaterial(color="#ddd"),
                        position=[0, 7.25, 0],
                        receiveShadow=True,
                        castShadow=True
                    )
                    
                    # Roof structure
                    three.Mesh(
                        geometry=three.BoxGeometry(width=5, height=1, depth=5),
                        material=three.MeshStandardMaterial(color="#bbb"),
                        position=[0, 12.75, 0],
                        receiveShadow=True,
                        castShadow=True
                    )
                    
                    # Add orbital controls to allow rotation
                    three.OrbitControls(enableDamping=True, dampingFactor=0.08)
    
    # Add rotation instructions
    st.caption("👆 Click and drag to rotate the model. Use mouse wheel to zoom in/out.")
    
    # Add a separator
    st.markdown("---")
    
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