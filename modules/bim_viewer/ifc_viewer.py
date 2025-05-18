"""
BIM Viewer module for viewing IFC files.

This module provides functionality for viewing IFC files using Three.js and IFC.js in Streamlit.
"""

import streamlit as st
import os

def render_bim_viewer():
    """Render the BIM Viewer component."""
    
    st.title("BIM Viewer")
    
    # Sample IFC file selection
    st.subheader("IFC Model Viewer")
    
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
        "Select IFC file", 
        ifc_files,
        index=default_index
    )
    
    # Load the IFC.js viewer
    st.markdown("""
    <div style="width: 100%; height: 600px; position: relative; background-color: #f5f5f5; border-radius: 8px; overflow: hidden;">
        <canvas id="three-canvas" style="width: 100%; height: 100%;"></canvas>
    </div>
    
    <script type="importmap">
    {
        "imports": {
            "three": "https://unpkg.com/three@0.154.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.154.0/examples/jsm/",
            "web-ifc-three": "https://unpkg.com/web-ifc-three@0.0.126/dist/web-ifc-three.esm.js",
            "web-ifc": "https://unpkg.com/web-ifc@0.0.46/dist/web-ifc-api.js"
        }
    }
    </script>
    
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { IFCLoader } from 'web-ifc-three/IFCLoader';
        
        // Set up scene
        const canvas = document.getElementById('three-canvas');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf5f5f5);
        
        // Set up camera
        const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
        camera.position.z = 10;
        camera.position.y = 10;
        camera.position.x = 10;
        
        // Set up renderer
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        
        // Set up controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 10, 7.5);
        scene.add(directionalLight);
        
        // Set up IFC loader
        const ifcLoader = new IFCLoader();
        ifcLoader.ifcManager.setWasmPath('https://unpkg.com/web-ifc@0.0.46/');
        
        // Load IFC file
        const url = '/static/models/{0}';
        ifcLoader.load(url, (ifcModel) => {
            scene.add(ifcModel);
            
            // Fit camera to model
            const box = new THREE.Box3().setFromObject(ifcModel);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            const cameraDistance = maxDim / (2 * Math.tan(fov / 2));
            
            camera.position.set(center.x + cameraDistance, center.y + cameraDistance, center.z + cameraDistance);
            camera.lookAt(center);
            
            controls.target.set(center.x, center.y, center.z);
            controls.update();
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = canvas.clientWidth / canvas.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        });
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        
        animate();
    </script>
    """.format(selected_ifc), unsafe_allow_html=True)
    
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
        - **Units**: 120 residential, 8 retail
        - **Height**: 15 stories above ground, 2 below
        """)
    
    with tabs[1]:
        st.markdown("""
        | Level | Height (m) | Function |
        | ----- | ---------- | -------- |
        | Level 1 | 0.0 | Retail/Lobby |
        | Level 2 | 4.0 | Residential |
        | Level 3 | 8.0 | Residential |
        | Level 4 | 12.0 | Residential |
        | Level 5 | 16.0 | Residential |
        """)
    
    with tabs[2]:
        st.markdown("""
        ### Element Statistics
        - Structural Elements: 520
        - Doors: 145
        - Windows: 280
        - MEP Elements: 1,245
        - Walls: 380
        - Floors: 35
        """)
    
    # Controls section
    st.subheader("Viewer Controls")
    
    # Create a two-column layout for controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Rotate**: Left mouse button + drag
        - **Pan**: Middle mouse button + drag
        - **Zoom**: Mouse wheel or right button + drag
        """)
    
    with col2:
        # Theme toggle for the BIM viewer
        st.checkbox("Dark Mode", key="bim_dark_mode", 
                   help="Toggle between light and dark mode for the BIM viewer")
        
        # Display options
        st.multiselect("Display Options", 
                     ["Structural Elements", "Architectural Elements", "MEP", "Furniture"],
                     default=["Structural Elements", "Architectural Elements"],
                     help="Select elements to display in the model")
    
    # Add custom JavaScript to handle the model viewer dark mode toggle
    if st.session_state.get("bim_dark_mode", False):
        st.markdown("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Apply dark mode to the canvas background
                const scene = document.querySelector('scene');
                if (scene) {
                    scene.background = new THREE.Color(0x222222);
                }
            });
        </script>
        """, unsafe_allow_html=True)