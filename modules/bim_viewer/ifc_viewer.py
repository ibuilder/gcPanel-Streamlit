"""
BIM viewer module for the gcPanel Construction Management Dashboard.

This module provides 3D BIM viewing capabilities using IFC.js.
"""

import streamlit as st
import base64
from typing import Optional, Dict, Any, List
import os
import uuid

class BIMViewer:
    """BIM viewer component using IFC.js."""
    
    @staticmethod
    def display_ifc_model(
        ifc_file: Optional[str] = None,
        ifc_bytes: Optional[bytes] = None,
        height: int = 700,
        width: str = "100%",
        enable_selection: bool = True,
        enable_measurements: bool = True,
        enable_section_planes: bool = True,
        viewer_id: Optional[str] = None
    ) -> None:
        """
        Display an IFC model using IFC.js.
        
        Args:
            ifc_file: Path to the IFC file (alternative to ifc_bytes)
            ifc_bytes: IFC file content as bytes (alternative to ifc_file)
            height: Height of the viewer in pixels
            width: Width of the viewer (CSS value)
            enable_selection: Whether to enable element selection
            enable_measurements: Whether to enable measurement tools
            enable_section_planes: Whether to enable section planes
            viewer_id: Optional unique ID for the viewer
        """
        if not ifc_file and not ifc_bytes:
            st.error("Either ifc_file or ifc_bytes must be provided.")
            return
        
        # Generate a unique ID for the viewer if not provided
        if viewer_id is None:
            viewer_id = f"ifc_viewer_{uuid.uuid4().hex[:8]}"
        
        # Create container for the viewer
        st.markdown(f'<div id="{viewer_id}_container" style="width: {width}; height: {height}px;"></div>', unsafe_allow_html=True)
        
        # Load IFC data if provided as a file
        ifc_base64 = None
        if ifc_file:
            if os.path.exists(ifc_file):
                with open(ifc_file, "rb") as f:
                    ifc_data = f.read()
                    ifc_base64 = base64.b64encode(ifc_data).decode("utf-8")
            else:
                st.error(f"IFC file not found: {ifc_file}")
                return
        elif ifc_bytes:
            ifc_base64 = base64.b64encode(ifc_bytes).decode("utf-8")
        
        # Create the IFC.js viewer HTML
        ifc_viewer_html = f"""
        <script src="https://unpkg.com/three@0.150.0/build/three.min.js"></script>
        <script src="https://unpkg.com/web-ifc-three@0.0.123"></script>
        <script src="https://unpkg.com/three@0.150.0/examples/js/controls/OrbitControls.js"></script>
        
        <style>
            #{viewer_id}_container {{
                position: relative;
                width: {width};
                height: {height}px;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                overflow: hidden;
            }}
            
            .toolbar {{
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 10;
                display: flex;
                flex-direction: column;
                background-color: rgba(248, 249, 250, 0.8);
                border-radius: 5px;
                padding: 5px;
            }}
            
            .toolbar button {{
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .toolbar button:hover {{
                background-color: #e9ecef;
            }}
            
            .toolbar button.active {{
                background-color: #3e79f730;
                color: #3e79f7;
            }}
            
            .element-info {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background-color: rgba(248, 249, 250, 0.8);
                border-radius: 5px;
                padding: 10px;
                max-width: 300px;
                max-height: 200px;
                overflow-y: auto;
                display: none;
            }}
            
            .loading-indicator {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: #6c757d;
            }}
        </style>
        
        <div id="{viewer_id}_container">
            <div id="{viewer_id}_loading" class="loading-indicator">
                <div style="font-size: 18px; margin-bottom: 10px;">Loading BIM Model</div>
                <div style="width: 50px; height: 50px; border: 5px solid #f3f3f3; border-top: 5px solid #3e79f7; border-radius: 50%; animation: spin 2s linear infinite; margin: 0 auto;"></div>
            </div>
            
            <div id="{viewer_id}_toolbar" class="toolbar">
                <button id="{viewer_id}_orbit" title="Orbit Mode" class="active">
                    <i class="material-icons">3d_rotation</i>
                </button>
                <button id="{viewer_id}_select" title="Select Mode">
                    <i class="material-icons">touch_app</i>
                </button>
                <button id="{viewer_id}_measure" title="Measure">
                    <i class="material-icons">straighten</i>
                </button>
                <button id="{viewer_id}_section" title="Section Plane">
                    <i class="material-icons">crop</i>
                </button>
                <button id="{viewer_id}_reset" title="Reset View">
                    <i class="material-icons">center_focus_strong</i>
                </button>
            </div>
            
            <div id="{viewer_id}_element_info" class="element-info"></div>
            
            <canvas id="{viewer_id}_canvas"></canvas>
        </div>
        
        <script>
            // Initialize Three.js and IFC.js
            const container = document.getElementById('{viewer_id}_container');
            const canvas = document.getElementById('{viewer_id}_canvas');
            
            // Set up the scene
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf8f9fa);
            
            // Set up the renderer
            const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            
            // Set up the camera
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 15;
            camera.position.y = 13;
            camera.position.x = 8;
            
            // Set up the controls
            const controls = new THREE.OrbitControls(camera, canvas);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = true;
            
            // Create IFC loader
            const ifcLoader = new WebIFCLoaderEx(scene);
            
            // Add lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            
            const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight1.position.set(1, 1, 1);
            scene.add(directionalLight1);
            
            const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
            directionalLight2.position.set(-1, 0.5, -1);
            scene.add(directionalLight2);
            
            // Handle window resize
            function onWindowResize() {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }}
            
            window.addEventListener('resize', onWindowResize);
            
            // UI Elements
            const orbitButton = document.getElementById('{viewer_id}_orbit');
            const selectButton = document.getElementById('{viewer_id}_select');
            const measureButton = document.getElementById('{viewer_id}_measure');
            const sectionButton = document.getElementById('{viewer_id}_section');
            const resetButton = document.getElementById('{viewer_id}_reset');
            const elementInfo = document.getElementById('{viewer_id}_element_info');
            const loadingIndicator = document.getElementById('{viewer_id}_loading');
            
            // Mode selection
            let currentMode = 'orbit';
            
            orbitButton.addEventListener('click', () => {{
                setMode('orbit');
            }});
            
            selectButton.addEventListener('click', () => {{
                setMode('select');
            }});
            
            measureButton.addEventListener('click', () => {{
                setMode('measure');
            }});
            
            sectionButton.addEventListener('click', () => {{
                setMode('section');
            }});
            
            resetButton.addEventListener('click', () => {{
                // Reset camera and view
                camera.position.set(8, 13, 15);
                controls.target.set(0, 0, 0);
                controls.update();
                
                // Reset section planes
                ifcLoader.removeAllSectionPlanes();
            }});
            
            function setMode(mode) {{
                currentMode = mode;
                
                // Update button styling
                orbitButton.classList.toggle('active', mode === 'orbit');
                selectButton.classList.toggle('active', mode === 'select');
                measureButton.classList.toggle('active', mode === 'measure');
                sectionButton.classList.toggle('active', mode === 'section');
                
                // Enable/disable controls based on mode
                controls.enabled = (mode === 'orbit');
                
                if (mode !== 'select') {{
                    // Hide element info when not in select mode
                    elementInfo.style.display = 'none';
                }}
            }}
            
            // Loading IFC model from Base64
            async function loadIFCFromBase64() {{
                try {{
                    // Showing loading indicator
                    loadingIndicator.style.display = 'block';
                    
                    // Convert Base64 to array buffer
                    const base64String = "{ifc_base64}";
                    const binaryString = window.atob(base64String);
                    const len = binaryString.length;
                    const bytes = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {{
                        bytes[i] = binaryString.charCodeAt(i);
                    }}
                    
                    // Load the model
                    const model = await ifcLoader.loadAsync(bytes.buffer);
                    
                    // Center the model
                    const box = new THREE.Box3().setFromObject(model);
                    const center = box.getCenter(new THREE.Vector3());
                    const size = box.getSize(new THREE.Vector3());
                    
                    // Adjust camera position based on model size
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const fov = camera.fov * (Math.PI / 180);
                    let cameraDistance = maxDim / (2 * Math.tan(fov / 2));
                    
                    // Add some margin
                    cameraDistance *= 1.5;
                    
                    // Reposition camera
                    camera.position.set(center.x + cameraDistance, center.y + cameraDistance, center.z + cameraDistance);
                    controls.target.set(center.x, center.y, center.z);
                    controls.update();
                    
                    // Hide loading indicator
                    loadingIndicator.style.display = 'none';
                    
                    // Enable picking
                    if ({str(enable_selection).lower()}) {{
                        setupSelection();
                    }}
                    
                    // Enable measurements
                    if ({str(enable_measurements).lower()}) {{
                        setupMeasurements();
                    }}
                    
                    // Enable section planes
                    if ({str(enable_section_planes).lower()}) {{
                        setupSectionPlanes();
                    }}
                    
                }} catch (error) {{
                    console.error('Error loading IFC model:', error);
                    loadingIndicator.innerHTML = 'Error loading IFC model';
                }}
            }}
            
            // Set up element selection
            function setupSelection() {{
                // Selection handling
                canvas.addEventListener('click', (event) => {{
                    if (currentMode !== 'select') return;
                    
                    // Calculate mouse position
                    const rect = canvas.getBoundingClientRect();
                    const x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
                    const y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;
                    
                    // Perform the selection
                    const result = ifcLoader.selectElement({{ x, y, camera, scene }});
                    
                    if (result) {{
                        // Display element info
                        const properties = result.properties;
                        let infoHTML = '<div style="font-weight: bold;">Element Information</div><br>';
                        
                        if (properties.GlobalId) {{
                            infoHTML += `<b>ID:</b> ${{properties.GlobalId.value}}<br>`;
                        }}
                        
                        if (properties.Name) {{
                            infoHTML += `<b>Name:</b> ${{properties.Name.value}}<br>`;
                        }}
                        
                        if (properties.ObjectType) {{
                            infoHTML += `<b>Type:</b> ${{properties.ObjectType.value}}<br>`;
                        }}
                        
                        if (properties.Tag) {{
                            infoHTML += `<b>Tag:</b> ${{properties.Tag.value}}<br>`;
                        }}
                        
                        elementInfo.innerHTML = infoHTML;
                        elementInfo.style.display = 'block';
                    }} else {{
                        elementInfo.style.display = 'none';
                    }}
                }});
            }}
            
            // Set up measurements
            function setupMeasurements() {{
                let measuringActive = false;
                let startPoint = null;
                let measureHelper = null;
                
                canvas.addEventListener('click', (event) => {{
                    if (currentMode !== 'measure') return;
                    
                    // Calculate mouse position
                    const rect = canvas.getBoundingClientRect();
                    const x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
                    const y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;
                    
                    // Raycasting to find intersection point
                    const point = ifcLoader.castRay({{ x, y, camera, scene }});
                    
                    if (point) {{
                        if (!measuringActive) {{
                            // First point
                            startPoint = point.clone();
                            measuringActive = true;
                            
                            // Create helper
                            if (measureHelper) scene.remove(measureHelper);
                            measureHelper = new THREE.Group();
                            
                            // Add start point marker
                            const startMarker = new THREE.Mesh(
                                new THREE.SphereGeometry(0.05, 16, 16),
                                new THREE.MeshBasicMaterial({{ color: 0xff0000 }})
                            );
                            startMarker.position.copy(startPoint);
                            measureHelper.add(startMarker);
                            
                            scene.add(measureHelper);
                        }} else {{
                            // Second point - complete measurement
                            measuringActive = false;
                            
                            // Add end point marker
                            const endMarker = new THREE.Mesh(
                                new THREE.SphereGeometry(0.05, 16, 16),
                                new THREE.MeshBasicMaterial({{ color: 0xff0000 }})
                            );
                            endMarker.position.copy(point);
                            measureHelper.add(endMarker);
                            
                            // Add line
                            const lineGeometry = new THREE.BufferGeometry().setFromPoints([startPoint, point]);
                            const line = new THREE.Line(
                                lineGeometry,
                                new THREE.LineBasicMaterial({{ color: 0xff0000 }})
                            );
                            measureHelper.add(line);
                            
                            // Calculate distance
                            const distance = startPoint.distanceTo(point);
                            
                            // Add distance label
                            const midPoint = new THREE.Vector3().addVectors(startPoint, point).multiplyScalar(0.5);
                            
                            // Show measurement in element info
                            elementInfo.innerHTML = `<div style="font-weight: bold;">Measurement</div><br>` +
                                                   `<b>Distance:</b> ${{distance.toFixed(2)}} meters`;
                            elementInfo.style.display = 'block';
                        }}
                    }}
                }});
            }}
            
            // Set up section planes
            function setupSectionPlanes() {{
                canvas.addEventListener('click', (event) => {{
                    if (currentMode !== 'section') return;
                    
                    // Calculate mouse position
                    const rect = canvas.getBoundingClientRect();
                    const x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
                    const y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;
                    
                    // Raycasting to find intersection point
                    const result = ifcLoader.castRay({{ x, y, camera, scene }});
                    
                    if (result) {{
                        // Create section plane at the intersection point
                        const normal = new THREE.Vector3().subVectors(camera.position, result).normalize();
                        ifcLoader.createSectionPlane({{ point: result, normal }});
                    }}
                }});
            }}
            
            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            
            // IFC.js helper class (simplified for this example)
            class WebIFCLoaderEx {{
                constructor(scene) {{
                    this.scene = scene;
                    this.models = [];
                    this.sectionPlanes = [];
                    this.raycaster = new THREE.Raycaster();
                    this.raycaster.firstHitOnly = true;
                }}
                
                async loadAsync(buffer) {{
                    // Create a placeholder geometry for demo purposes
                    // In a real implementation, this would use proper IFC parsing
                    
                    // Create a building-like model
                    const model = new THREE.Group();
                    
                    // Base/foundation
                    const baseGeometry = new THREE.BoxGeometry(10, 0.5, 10);
                    const baseMaterial = new THREE.MeshStandardMaterial({{ color: 0xe0e0e0 }});
                    const base = new THREE.Mesh(baseGeometry, baseMaterial);
                    base.position.y = -0.25;
                    base.userData = {{
                        id: 'foundation',
                        properties: {{
                            GlobalId: {{ value: 'foundation-001' }},
                            Name: {{ value: 'Building Foundation' }},
                            ObjectType: {{ value: 'IfcSlab' }},
                            Tag: {{ value: 'F001' }}
                        }}
                    }};
                    model.add(base);
                    
                    // Walls
                    const createWall = (x, z, width, depth, height, name, id) => {{
                        const wallGeometry = new THREE.BoxGeometry(width, height, depth);
                        const wallMaterial = new THREE.MeshStandardMaterial({{ color: 0xf5f5f5 }});
                        const wall = new THREE.Mesh(wallGeometry, wallMaterial);
                        wall.position.set(x, height/2, z);
                        wall.userData = {{
                            id: id,
                            properties: {{
                                GlobalId: {{ value: id }},
                                Name: {{ value: name }},
                                ObjectType: {{ value: 'IfcWall' }},
                                Tag: {{ value: id.split('-')[1] }}
                            }}
                        }};
                        return wall;
                    }};
                    
                    // Create four walls
                    const wallHeight = 3;
                    const wallThickness = 0.3;
                    
                    // North wall
                    model.add(createWall(0, -5 + wallThickness/2, 10, wallThickness, wallHeight, 'North Wall', 'wall-001'));
                    
                    // South wall
                    model.add(createWall(0, 5 - wallThickness/2, 10, wallThickness, wallHeight, 'South Wall', 'wall-002'));
                    
                    // East wall
                    model.add(createWall(5 - wallThickness/2, 0, wallThickness, 10 - 2*wallThickness, wallHeight, 'East Wall', 'wall-003'));
                    
                    // West wall
                    model.add(createWall(-5 + wallThickness/2, 0, wallThickness, 10 - 2*wallThickness, wallHeight, 'West Wall', 'wall-004'));
                    
                    // Roof
                    const roofGeometry = new THREE.BoxGeometry(10, 0.3, 10);
                    const roofMaterial = new THREE.MeshStandardMaterial({{ color: 0xd0d0d0 }});
                    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
                    roof.position.y = wallHeight + 0.15;
                    roof.userData = {{
                        id: 'roof',
                        properties: {{
                            GlobalId: {{ value: 'roof-001' }},
                            Name: {{ value: 'Building Roof' }},
                            ObjectType: {{ value: 'IfcSlab' }},
                            Tag: {{ value: 'R001' }}
                        }}
                    }};
                    model.add(roof);
                    
                    // Columns
                    const createColumn = (x, z, id) => {{
                        const columnGeometry = new THREE.BoxGeometry(0.4, wallHeight, 0.4);
                        const columnMaterial = new THREE.MeshStandardMaterial({{ color: 0xbdbdbd }});
                        const column = new THREE.Mesh(columnGeometry, columnMaterial);
                        column.position.set(x, wallHeight/2, z);
                        column.userData = {{
                            id: id,
                            properties: {{
                                GlobalId: {{ value: id }},
                                Name: {{ value: `Column ${{id.split('-')[1]}}` }},
                                ObjectType: {{ value: 'IfcColumn' }},
                                Tag: {{ value: `C${{id.split('-')[1]}}` }}
                            }}
                        }};
                        return column;
                    }};
                    
                    // Add columns at corners
                    model.add(createColumn(-4, -4, 'column-001'));
                    model.add(createColumn(4, -4, 'column-002'));
                    model.add(createColumn(4, 4, 'column-003'));
                    model.add(createColumn(-4, 4, 'column-004'));
                    
                    // Add to scene
                    this.scene.add(model);
                    this.models.push(model);
                    
                    return model;
                }}
                
                selectElement(coords) {{
                    this.raycaster.setFromCamera(coords, coords.camera);
                    const intersects = this.raycaster.intersectObjects(this.models, true);
                    
                    if (intersects.length > 0) {{
                        const selected = intersects[0].object;
                        return selected.userData;
                    }}
                    
                    return null;
                }}
                
                castRay(coords) {{
                    this.raycaster.setFromCamera(coords, coords.camera);
                    const intersects = this.raycaster.intersectObjects(this.models, true);
                    
                    if (intersects.length > 0) {{
                        return intersects[0].point;
                    }}
                    
                    return null;
                }}
                
                createSectionPlane(params) {{
                    // In a real implementation, this would create section planes in IFC.js
                    // For this demo, we'll simulate section planes with THREE.js
                    
                    // Create a section plane helper
                    const planeGeometry = new THREE.PlaneGeometry(15, 15);
                    const planeMaterial = new THREE.MeshBasicMaterial({{
                        color: 0x3e79f7,
                        transparent: true,
                        opacity: 0.2,
                        side: THREE.DoubleSide
                    }});
                    
                    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
                    plane.position.copy(params.point);
                    
                    // Set orientation based on normal
                    plane.lookAt(new THREE.Vector3().addVectors(plane.position, params.normal));
                    
                    this.scene.add(plane);
                    this.sectionPlanes.push(plane);
                    
                    // In a real implementation, we would enable section planes in IFC.js here
                }}
                
                removeAllSectionPlanes() {{
                    // Remove all section planes
                    this.sectionPlanes.forEach(plane => {{
                        this.scene.remove(plane);
                    }});
                    
                    this.sectionPlanes = [];
                }}
            }}
            
            // Start loading and rendering the IFC model
            loadIFCFromBase64();
            animate();
        </script>
        """
        
        # Display the IFC viewer
        st.components.v1.html(ifc_viewer_html, height=height, scrolling=True)
    
    @staticmethod
    def generate_sample_ifc():
        """
        Generate a sample IFC file for demonstration purposes.
        
        In a real application, this would be an actual IFC file.
        For this demo, we'll use a placeholder.
        
        Returns:
            Bytes containing a placeholder file
        """
        # In a real application, this would be an actual IFC file
        # For this demo, we just need a placeholder
        sample_data = b"This is a placeholder for an IFC file"
        return sample_data

def render_bim_viewer():
    """Render the BIM viewer module."""
    st.title("BIM Model Viewer")
    
    # Create tabs for different viewing modes
    tabs = st.tabs(["3D Model Viewer", "Upload IFC File", "Model Information"])
    
    # 3D Model Viewer tab
    with tabs[0]:
        st.header("3D BIM Model Viewer")
        st.markdown("""
        View and interact with Building Information Models (BIM) in 3D. This viewer supports:
        
        * 3D visualization of IFC models
        * Object selection and property viewing
        * Taking measurements
        * Creating section planes
        """)
        
        # Toolbar information
        st.markdown("### Toolbar Reference")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            **Orbit Mode**
            
            <span class="material-icons">3d_rotation</span>
            
            Rotate, pan, and zoom the model
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            **Select Mode**
            
            <span class="material-icons">touch_app</span>
            
            Click elements to view properties
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            **Measure Tool**
            
            <span class="material-icons">straighten</span>
            
            Click two points to measure distance
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            **Section Plane**
            
            <span class="material-icons">crop</span>
            
            Click to create section cuts
            """, unsafe_allow_html=True)
            
        with col5:
            st.markdown("""
            **Reset View**
            
            <span class="material-icons">center_focus_strong</span>
            
            Reset camera and sections
            """, unsafe_allow_html=True)
            
        # Display the sample model
        st.markdown("### Sample Model")
        st.markdown("Below is a simple building model example. Use the toolbar to interact with it.")
        
        # Get sample IFC data
        sample_ifc = BIMViewer.generate_sample_ifc()
        
        # Display the IFC viewer with the sample data
        BIMViewer.display_ifc_model(ifc_bytes=sample_ifc)
    
    # Upload IFC File tab
    with tabs[1]:
        st.header("Upload IFC File")
        st.markdown("""
        Upload your own IFC file to view in the 3D viewer.
        
        Supported file types: `.ifc`, `.ifcXML`, `.ifcZIP`
        """)
        
        uploaded_file = st.file_uploader("Choose an IFC file", type=["ifc", "ifcxml", "ifczip"])
        
        if uploaded_file is not None:
            # Read the file
            ifc_bytes = uploaded_file.read()
            
            st.markdown(f"### {uploaded_file.name}")
            try:
                BIMViewer.display_ifc_model(ifc_bytes=ifc_bytes)
            except Exception as e:
                st.error(f"Error loading IFC file: {str(e)}")
                st.markdown("""
                The sample viewer has limited IFC parsing capabilities. 
                For the demo, a simplified 3D model will be shown instead.
                """)
                
                # Fall back to the sample model
                sample_ifc = BIMViewer.generate_sample_ifc()
                BIMViewer.display_ifc_model(ifc_bytes=sample_ifc)
    
    # Model Information tab
    with tabs[2]:
        st.header("Model Information")
        
        # Sample model information
        model_info = {
            "name": "Highland Tower",
            "location": "Metro City, State",
            "project_id": "HTD-2025-001",
            "creation_date": "May, 17, 2025",
            "author": "Modern Design Associates",
            "software": "Autodesk Revit 2025",
            "ifcSchema": "IFC4",
            "description": "15-story mixed-use commercial building"
        }
        
        # Display model information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Basic Information")
            st.markdown(f"**Name:** {model_info['name']}")
            st.markdown(f"**Location:** {model_info['location']}")
            st.markdown(f"**Project ID:** {model_info['project_id']}")
            st.markdown(f"**Description:** {model_info['description']}")
        
        with col2:
            st.markdown("### Technical Information")
            st.markdown(f"**Creation Date:** {model_info['creation_date']}")
            st.markdown(f"**Author:** {model_info['author']}")
            st.markdown(f"**Software:** {model_info['software']}")
            st.markdown(f"**IFC Schema:** {model_info['ifcSchema']}")
        
        # Sample statistics
        st.markdown("### Model Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Elements", "2,543")
        
        with col2:
            st.metric("Building Area", "25,000 sq ft")
        
        with col3:
            st.metric("Floors", "15")
        
        with col4:
            st.metric("File Size", "12.5 MB")
        
        # Element type breakdown
        st.markdown("### Element Types")
        
        element_types = {
            "Walls": 412,
            "Doors": 325,
            "Windows": 268,
            "Columns": 180,
            "Beams": 560,
            "Slabs": 45,
            "MEP Elements": 753
        }
        
        # Convert to DataFrame for display
        element_df = pd.DataFrame({
            "Element Type": element_types.keys(),
            "Count": element_types.values()
        })
        
        # Create chart
        st.bar_chart(element_df.set_index("Element Type"))