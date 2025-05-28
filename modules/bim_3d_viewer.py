"""
Highland Tower Development - BIM 3D Viewer
Pure Python implementation with Three.js integration for visual project coordination.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

def render_bim_3d_viewer():
    """Highland Tower Development - Advanced BIM 3D Viewer"""
    
    st.markdown("""
    <div class="module-header">
        <h1>🏢 Highland Tower Development - BIM 3D Viewer</h1>
        <p>$45.5M Project - Visual Project Coordination & Model Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize BIM data
    initialize_highland_bim_data()
    
    # BIM overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Models", "3", "Architectural, Structural, HVAC")
    with col2:
        st.metric("Total Clashes", "47", "12 resolved, 35 active")
    with col3:
        st.metric("Model Coordination", "94.2%", "Excellent integration")
    with col4:
        st.metric("Last Update", "2 hours ago", "Real-time sync")
    
    # Main BIM tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ 3D Model Viewer",
        "⚠️ Clash Detection", 
        "📏 Model Coordination",
        "📊 Progress Tracking",
        "🔧 Model Management"
    ])
    
    with tab1:
        render_3d_model_viewer()
    
    with tab2:
        render_clash_detection()
    
    with tab3:
        render_model_coordination()
    
    with tab4:
        render_progress_tracking()
    
    with tab5:
        render_model_management()

def initialize_highland_bim_data():
    """Initialize Highland Tower Development BIM data"""
    
    if "highland_bim_models" not in st.session_state:
        st.session_state.highland_bim_models = [
            {
                "model_id": "HTD-ARCH-001",
                "name": "Highland Tower - Architectural",
                "discipline": "Architecture",
                "version": "Rev 23",
                "last_updated": "2024-05-28 14:30:00",
                "file_size": "245 MB",
                "elements": 24789,
                "status": "Current",
                "author": "Highland Design Associates",
                "coordination_status": "Coordinated",
                "clash_count": 12
            },
            {
                "model_id": "HTD-STRUC-001", 
                "name": "Highland Tower - Structural",
                "discipline": "Structural",
                "version": "Rev 18",
                "last_updated": "2024-05-28 09:45:00",
                "file_size": "156 MB",
                "elements": 18653,
                "status": "Current",
                "author": "Structural Engineering LLC",
                "coordination_status": "Coordinated",
                "clash_count": 8
            },
            {
                "model_id": "HTD-HVAC-001",
                "name": "Highland Tower - HVAC Systems",
                "discipline": "HVAC",
                "version": "Rev 15",
                "last_updated": "2024-05-27 16:20:00",
                "file_size": "98 MB", 
                "elements": 12456,
                "status": "Under Review",
                "author": "MEP Engineering Group",
                "coordination_status": "Needs Review",
                "clash_count": 27
            }
        ]
    
    if "highland_bim_clashes" not in st.session_state:
        st.session_state.highland_bim_clashes = [
            {
                "clash_id": "CL-001",
                "type": "Hard Clash",
                "severity": "High",
                "discipline_a": "Structural",
                "discipline_b": "HVAC",
                "description": "Steel beam conflicts with main supply duct",
                "location": "Level 8, Grid C-4",
                "assigned_to": "MEP Coordinator",
                "status": "Active",
                "created_date": "2024-05-25",
                "due_date": "2024-05-30",
                "resolution_notes": ""
            },
            {
                "clash_id": "CL-002",
                "type": "Clearance",
                "severity": "Medium", 
                "discipline_a": "Architecture",
                "discipline_b": "HVAC",
                "description": "Insufficient clearance for ductwork maintenance",
                "location": "Level 12, Mechanical Room",
                "assigned_to": "Design Team",
                "status": "Resolved",
                "created_date": "2024-05-20",
                "due_date": "2024-05-28",
                "resolution_notes": "Ductwork rerouted per RFI-045"
            },
            {
                "clash_id": "CL-003",
                "type": "Hard Clash",
                "severity": "Critical",
                "discipline_a": "Structural", 
                "discipline_b": "Architecture",
                "description": "Column placement conflicts with window opening",
                "location": "Level 5, West Facade",
                "assigned_to": "Structural Engineer",
                "status": "Active",
                "created_date": "2024-05-28",
                "due_date": "2024-06-02",
                "resolution_notes": ""
            }
        ]

def render_3d_model_viewer():
    """Render interactive 3D model viewer"""
    
    st.subheader("🏗️ Highland Tower Development - 3D Model Viewer")
    
    # Model selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**📋 Model Selection:**")
        
        # Available models
        models = st.session_state.highland_bim_models
        model_options = [f"{model['name']} ({model['version']})" for model in models]
        selected_model_idx = st.selectbox("Select Model", range(len(model_options)), format_func=lambda x: model_options[x])
        selected_model = models[selected_model_idx]
        
        # Model info
        st.markdown("**📊 Model Information:**")
        st.write(f"**Discipline:** {selected_model['discipline']}")
        st.write(f"**Version:** {selected_model['version']}")
        st.write(f"**Elements:** {selected_model['elements']:,}")
        st.write(f"**File Size:** {selected_model['file_size']}")
        st.write(f"**Status:** {selected_model['status']}")
        st.write(f"**Last Updated:** {selected_model['last_updated']}")
        
        # View controls
        st.markdown("**🎮 View Controls:**")
        view_mode = st.selectbox("View Mode", ["Perspective", "Orthographic", "Section"])
        show_grid = st.checkbox("Show Grid", value=True)
        show_levels = st.checkbox("Show Levels", value=True)
        show_dimensions = st.checkbox("Show Dimensions", value=False)
        
        # Visibility controls
        st.markdown("**👁️ Element Visibility:**")
        show_structure = st.checkbox("Structure", value=True)
        show_architecture = st.checkbox("Architecture", value=True)
        show_hvac = st.checkbox("HVAC", value=True)
        show_electrical = st.checkbox("Electrical", value=False)
        show_plumbing = st.checkbox("Plumbing", value=False)
    
    with col2:
        st.markdown("**🏗️ 3D Model Viewer:**")
        
        # Create the 3D viewer component
        viewer_html = generate_3d_viewer_html(selected_model, {
            "view_mode": view_mode,
            "show_grid": show_grid,
            "show_levels": show_levels,
            "show_dimensions": show_dimensions,
            "show_structure": show_structure,
            "show_architecture": show_architecture,
            "show_hvac": show_hvac,
            "show_electrical": show_electrical,
            "show_plumbing": show_plumbing
        })
        
        # Display the 3D viewer
        components.html(viewer_html, height=600)
        
        # Model statistics
        st.markdown("**📊 Model Statistics:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Walls", "2,847", "Architectural")
        with col2:
            st.metric("Beams", "1,653", "Structural")
        with col3:
            st.metric("Ducts", "745", "HVAC")
        with col4:
            st.metric("Equipment", "156", "MEP")

def render_clash_detection():
    """Render clash detection interface"""
    
    st.subheader("⚠️ Highland Tower Development - Clash Detection")
    
    # Clash summary
    col1, col2, col3, col4 = st.columns(4)
    
    total_clashes = len(st.session_state.highland_bim_clashes)
    active_clashes = len([c for c in st.session_state.highland_bim_clashes if c['status'] == 'Active'])
    resolved_clashes = len([c for c in st.session_state.highland_bim_clashes if c['status'] == 'Resolved'])
    critical_clashes = len([c for c in st.session_state.highland_bim_clashes if c['severity'] == 'Critical'])
    
    with col1:
        st.metric("Total Clashes", total_clashes, "Across all models")
    with col2:
        st.metric("Active Clashes", active_clashes, "Require attention")
    with col3:
        st.metric("Resolved", resolved_clashes, f"{(resolved_clashes/total_clashes)*100:.1f}% complete")
    with col4:
        st.metric("Critical", critical_clashes, "High priority")
    
    # Clash management
    st.markdown("**⚠️ Active Clashes:**")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Resolved", "Under Review"])
    with col3:
        discipline_filter = st.selectbox("Filter by Discipline", ["All", "Structural", "Architecture", "HVAC", "Electrical"])
    
    # Apply filters
    filtered_clashes = st.session_state.highland_bim_clashes
    if severity_filter != "All":
        filtered_clashes = [c for c in filtered_clashes if c['severity'] == severity_filter]
    if status_filter != "All":
        filtered_clashes = [c for c in filtered_clashes if c['status'] == status_filter]
    if discipline_filter != "All":
        filtered_clashes = [c for c in filtered_clashes if discipline_filter in [c['discipline_a'], c['discipline_b']]]
    
    # Display clashes
    for clash in filtered_clashes:
        severity_color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(clash['severity'], "⚪")
        status_color = {"Active": "⚠️", "Resolved": "✅", "Under Review": "🔍"}.get(clash['status'], "⚪")
        
        with st.expander(f"{severity_color} {clash['clash_id']} - {clash['description'][:50]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Type:** {clash['type']}")
                st.write(f"**Severity:** {clash['severity']}")
                st.write(f"**Status:** {status_color} {clash['status']}")
                st.write(f"**Location:** {clash['location']}")
                st.write(f"**Disciplines:** {clash['discipline_a']} ↔ {clash['discipline_b']}")
            
            with col2:
                st.write(f"**Assigned To:** {clash['assigned_to']}")
                st.write(f"**Created:** {clash['created_date']}")
                st.write(f"**Due Date:** {clash['due_date']}")
                if clash['resolution_notes']:
                    st.write(f"**Resolution:** {clash['resolution_notes']}")
            
            # Clash actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if clash['status'] == 'Active' and st.button(f"🔍 View in 3D", key=f"view_{clash['clash_id']}"):
                    st.info("Opening 3D view for clash location...")
            
            with col2:
                if clash['status'] == 'Active' and st.button(f"✅ Mark Resolved", key=f"resolve_{clash['clash_id']}"):
                    # Update clash status
                    for i, c in enumerate(st.session_state.highland_bim_clashes):
                        if c['clash_id'] == clash['clash_id']:
                            st.session_state.highland_bim_clashes[i]['status'] = 'Resolved'
                            break
                    st.success("Clash marked as resolved!")
                    st.rerun()
            
            with col3:
                if st.button(f"📝 Add Note", key=f"note_{clash['clash_id']}"):
                    st.session_state[f"show_note_form_{clash['clash_id']}"] = True
            
            # Note form
            if st.session_state.get(f"show_note_form_{clash['clash_id']}", False):
                with st.form(f"note_form_{clash['clash_id']}"):
                    resolution_note = st.text_area("Resolution Notes", placeholder="Describe the resolution or current status...")
                    
                    if st.form_submit_button("💾 Save Note"):
                        # Update clash with note
                        for i, c in enumerate(st.session_state.highland_bim_clashes):
                            if c['clash_id'] == clash['clash_id']:
                                st.session_state.highland_bim_clashes[i]['resolution_notes'] = resolution_note
                                break
                        st.success("Note saved!")
                        st.session_state[f"show_note_form_{clash['clash_id']}"] = False
                        st.rerun()

def render_model_coordination():
    """Render model coordination interface"""
    
    st.subheader("📏 Highland Tower Development - Model Coordination")
    
    st.info("**📏 Model Coordination:** Manage discipline coordination and federated model assembly for Highland Tower Development.")
    
    # Coordination matrix
    st.markdown("**🔄 Discipline Coordination Matrix:**")
    
    coordination_data = {
        "Discipline": ["Architecture", "Structural", "HVAC", "Electrical", "Plumbing"],
        "Architecture": ["—", "✅ Coordinated", "⚠️ Issues", "✅ Coordinated", "✅ Coordinated"],
        "Structural": ["✅ Coordinated", "—", "⚠️ Issues", "✅ Coordinated", "🔍 Reviewing"],
        "HVAC": ["⚠️ Issues", "⚠️ Issues", "—", "✅ Coordinated", "✅ Coordinated"],
        "Electrical": ["✅ Coordinated", "✅ Coordinated", "✅ Coordinated", "—", "✅ Coordinated"],
        "Plumbing": ["✅ Coordinated", "🔍 Reviewing", "✅ Coordinated", "✅ Coordinated", "—"]
    }
    
    coordination_df = pd.DataFrame(coordination_data)
    st.dataframe(coordination_df, use_container_width=True, hide_index=True)
    
    # Model assembly status
    st.markdown("**🏗️ Federated Model Assembly:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Assembly Progress:**")
        assembly_progress = [
            {"Component": "Architectural Model", "Status": "✅ Integrated", "Progress": "100%"},
            {"Component": "Structural Model", "Status": "✅ Integrated", "Progress": "100%"},
            {"Component": "HVAC Model", "Status": "🔍 Reviewing", "Progress": "85%"},
            {"Component": "Electrical Model", "Status": "⚠️ Pending", "Progress": "45%"},
            {"Component": "Plumbing Model", "Status": "⚠️ Pending", "Progress": "35%"}
        ]
        
        for component in assembly_progress:
            st.write(f"**{component['Component']}:** {component['Status']} ({component['Progress']})")
    
    with col2:
        st.markdown("**📅 Coordination Schedule:**")
        
        # Next coordination meetings
        meetings = [
            {"Date": "2024-05-30", "Time": "10:00 AM", "Disciplines": "All", "Topic": "Level 8-12 Review"},
            {"Date": "2024-06-03", "Time": "2:00 PM", "Disciplines": "MEP", "Topic": "HVAC Routing"},
            {"Date": "2024-06-05", "Time": "9:00 AM", "Disciplines": "All", "Topic": "Facade Coordination"}
        ]
        
        for meeting in meetings:
            st.write(f"**{meeting['Date']} {meeting['Time']}**")
            st.write(f"• {meeting['Disciplines']}: {meeting['Topic']}")

def render_progress_tracking():
    """Render BIM progress tracking"""
    
    st.subheader("📊 Highland Tower Development - Progress Tracking")
    
    st.info("**📊 Progress Tracking:** Monitor construction progress against BIM models with real-time updates.")
    
    # Progress by level
    st.markdown("**🏗️ Progress by Building Level:**")
    
    level_progress = [
        {"Level": "Level 1 (Retail)", "Design": "100%", "Construction": "95%", "MEP": "90%", "Status": "🟢 On Track"},
        {"Level": "Level 2 (Retail)", "Design": "100%", "Construction": "95%", "MEP": "88%", "Status": "🟢 On Track"},
        {"Level": "Level 3 (Amenities)", "Design": "100%", "Construction": "92%", "MEP": "85%", "Status": "🟢 On Track"},
        {"Level": "Levels 4-8 (Residential)", "Design": "100%", "Construction": "88%", "MEP": "75%", "Status": "🟡 Minor Delays"},
        {"Level": "Levels 9-12 (Residential)", "Design": "100%", "Construction": "82%", "MEP": "65%", "Status": "🟢 On Track"},
        {"Level": "Levels 13-15 (Penthouse)", "Design": "100%", "Construction": "75%", "MEP": "45%", "Status": "🟡 MEP Behind"},
        {"Level": "Rooftop/Mechanical", "Design": "95%", "Construction": "35%", "MEP": "25%", "Status": "🔴 Critical Path"}
    ]
    
    progress_df = pd.DataFrame(level_progress)
    st.dataframe(progress_df, use_container_width=True, hide_index=True)
    
    # Progress visualization
    st.markdown("**📈 Construction Progress Visualization:**")
    
    # Create progress chart
    import plotly.graph_objects as go
    
    levels = [level["Level"] for level in level_progress]
    design_progress = [float(level["Design"].rstrip('%')) for level in level_progress]
    construction_progress = [float(level["Construction"].rstrip('%')) for level in level_progress]
    mep_progress = [float(level["MEP"].rstrip('%')) for level in level_progress]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Design', x=levels, y=design_progress, marker_color='lightblue'))
    fig.add_trace(go.Bar(name='Construction', x=levels, y=construction_progress, marker_color='orange'))
    fig.add_trace(go.Bar(name='MEP', x=levels, y=mep_progress, marker_color='green'))
    
    fig.update_layout(
        title='Highland Tower Development - Progress by Level',
        xaxis_title='Building Levels',
        yaxis_title='Progress (%)',
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_model_management():
    """Render BIM model management interface"""
    
    st.subheader("🔧 Highland Tower Development - Model Management")
    
    # Model upload and management
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Upload New Model:**")
        
        with st.form("upload_model_form"):
            model_name = st.text_input("Model Name*", placeholder="e.g., Highland Tower - Electrical")
            discipline = st.selectbox("Discipline*", ["Architecture", "Structural", "HVAC", "Electrical", "Plumbing", "Fire Protection"])
            version = st.text_input("Version*", placeholder="e.g., Rev 12")
            author = st.text_input("Author*", placeholder="Design firm or author")
            
            uploaded_file = st.file_uploader("Choose IFC file", type=['ifc'])
            notes = st.text_area("Upload Notes", placeholder="Description of changes or updates...")
            
            if st.form_submit_button("📤 Upload Model"):
                if model_name and discipline and version and author:
                    # Add new model to session state
                    new_model = {
                        "model_id": f"HTD-{discipline.upper()}-{len(st.session_state.highland_bim_models) + 1:03d}",
                        "name": model_name,
                        "discipline": discipline,
                        "version": version,
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "file_size": "Calculating...",
                        "elements": "Processing...",
                        "status": "Processing",
                        "author": author,
                        "coordination_status": "Pending Review",
                        "clash_count": 0
                    }
                    
                    st.session_state.highland_bim_models.append(new_model)
                    st.success(f"✅ Model '{model_name}' uploaded successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields!")
    
    with col2:
        st.markdown("**📋 Current Models:**")
        
        for model in st.session_state.highland_bim_models:
            status_icon = {"Current": "🟢", "Under Review": "🟡", "Processing": "🔄", "Outdated": "🔴"}.get(model['status'], "⚪")
            
            with st.expander(f"{status_icon} {model['name']} ({model['version']})"):
                st.write(f"**Discipline:** {model['discipline']}")
                st.write(f"**Author:** {model['author']}")
                st.write(f"**Last Updated:** {model['last_updated']}")
                st.write(f"**Coordination Status:** {model['coordination_status']}")
                st.write(f"**Clash Count:** {model['clash_count']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Download", key=f"download_{model['model_id']}"):
                        st.info("Download starting...")
                
                with col2:
                    if st.button("🔄 Update", key=f"update_{model['model_id']}"):
                        st.info("Update process initiated...")
                
                with col3:
                    if st.button("🗑️ Archive", key=f"archive_{model['model_id']}"):
                        st.warning("Model archived!")

def generate_3d_viewer_html(model: Dict[str, Any], settings: Dict[str, Any]) -> str:
    """Generate HTML for 3D model viewer"""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; background: #f0f0f0; }}
            #viewer {{ width: 100%; height: 600px; }}
            .info-panel {{ 
                position: absolute; 
                top: 10px; 
                left: 10px; 
                background: rgba(0,0,0,0.7); 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div id="viewer"></div>
        <div class="info-panel">
            <strong>Highland Tower Development</strong><br>
            Model: {model['name']}<br>
            Version: {model['version']}<br>
            Elements: {model['elements']:,}<br>
            <br>
            <strong>Controls:</strong><br>
            • Mouse: Rotate view<br>
            • Wheel: Zoom in/out<br>
            • Right-click: Pan<br>
        </div>
        
        <script>
            // Set up the scene
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf0f0f0);
            
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, 600);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            
            document.getElementById('viewer').appendChild(renderer.domElement);
            
            // Add controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            
            // Add lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(50, 100, 50);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            
            // Create Highland Tower building representation
            const buildingGroup = new THREE.Group();
            
            // Ground plane
            if ({str(settings['show_grid']).lower()}) {{
                const gridHelper = new THREE.GridHelper(200, 50);
                scene.add(gridHelper);
            }}
            
            // Building floors
            for (let i = 0; i < 15; i++) {{
                // Floor slab
                const floorGeometry = new THREE.BoxGeometry(40, 0.5, 30);
                const floorMaterial = new THREE.MeshLambertMaterial({{ color: 0xcccccc }});
                const floor = new THREE.Mesh(floorGeometry, floorMaterial);
                floor.position.y = i * 4;
                floor.receiveShadow = true;
                buildingGroup.add(floor);
                
                // Exterior walls
                if (i < 14) {{
                    const wallGeometry = new THREE.BoxGeometry(40, 4, 0.3);
                    const wallMaterial = new THREE.MeshLambertMaterial({{ color: 0x8fbc8f }});
                    
                    // Front and back walls
                    const frontWall = new THREE.Mesh(wallGeometry, wallMaterial);
                    frontWall.position.set(0, i * 4 + 2, 15);
                    frontWall.castShadow = true;
                    buildingGroup.add(frontWall);
                    
                    const backWall = new THREE.Mesh(wallGeometry, wallMaterial);
                    backWall.position.set(0, i * 4 + 2, -15);
                    backWall.castShadow = true;
                    buildingGroup.add(backWall);
                    
                    // Side walls
                    const sideWallGeometry = new THREE.BoxGeometry(0.3, 4, 30);
                    const leftWall = new THREE.Mesh(sideWallGeometry, wallMaterial);
                    leftWall.position.set(-20, i * 4 + 2, 0);
                    leftWall.castShadow = true;
                    buildingGroup.add(leftWall);
                    
                    const rightWall = new THREE.Mesh(sideWallGeometry, wallMaterial);
                    rightWall.position.set(20, i * 4 + 2, 0);
                    rightWall.castShadow = true;
                    buildingGroup.add(rightWall);
                }}
                
                // Windows
                if (i > 0 && i < 14) {{
                    for (let j = -15; j <= 15; j += 5) {{
                        const windowGeometry = new THREE.BoxGeometry(3, 2.5, 0.1);
                        const windowMaterial = new THREE.MeshLambertMaterial({{ color: 0x87ceeb, transparent: true, opacity: 0.7 }});
                        const window = new THREE.Mesh(windowGeometry, windowMaterial);
                        window.position.set(j, i * 4 + 2, 15.2);
                        buildingGroup.add(window);
                    }}
                }}
            }}
            
            // Add structural elements if enabled
            if ({str(settings['show_structure']).lower()}) {{
                for (let i = 0; i < 15; i++) {{
                    for (let x = -15; x <= 15; x += 10) {{
                        for (let z = -10; z <= 10; z += 10) {{
                            const columnGeometry = new THREE.BoxGeometry(0.8, 4, 0.8);
                            const columnMaterial = new THREE.MeshLambertMaterial({{ color: 0x696969 }});
                            const column = new THREE.Mesh(columnGeometry, columnMaterial);
                            column.position.set(x, i * 4 + 2, z);
                            column.castShadow = true;
                            buildingGroup.add(column);
                        }}
                    }}
                }}
            }}
            
            // Add HVAC systems if enabled
            if ({str(settings['show_hvac']).lower()}) {{
                for (let i = 1; i < 15; i += 2) {{
                    const ductGeometry = new THREE.BoxGeometry(35, 0.5, 1);
                    const ductMaterial = new THREE.MeshLambertMaterial({{ color: 0x4169e1 }});
                    const duct = new THREE.Mesh(ductGeometry, ductMaterial);
                    duct.position.set(0, i * 4 + 3.5, 0);
                    buildingGroup.add(duct);
                }}
            }}
            
            scene.add(buildingGroup);
            
            // Position camera
            camera.position.set(60, 40, 60);
            camera.lookAt(0, 30, 0);
            
            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            
            animate();
            
            // Handle window resize
            window.addEventListener('resize', () => {{
                const width = window.innerWidth;
                const height = 600;
                
                camera.aspect = width / height;
                camera.updateProjectionMatrix();
                
                renderer.setSize(width, height);
            }});
        </script>
    </body>
    </html>
    """