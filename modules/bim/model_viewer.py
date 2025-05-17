import streamlit as st
import streamlit.components.v1 as components
import os
import json
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "3D Model Viewer"
MODULE_ICON = "box"

def init_database():
    """Initialize the database tables for BIM models"""
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # Create BIM models table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bim_models (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                model_path VARCHAR(255),
                model_type VARCHAR(50),
                uploaded_by INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create issues table for coordination
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bim_issues (
                id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES bim_models(id),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                location_x FLOAT,
                location_y FLOAT,
                location_z FLOAT,
                status VARCHAR(50),
                assigned_to VARCHAR(100),
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error initializing BIM database tables: {str(e)}")

def render_list():
    """Render the list of available BIM models"""
    st.title("BIM Models")
    
    # Initialize database
    init_database()
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view BIM models")
        return
    
    # Fetch available models
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, description, model_type, uploaded_at
            FROM bim_models
            ORDER BY uploaded_at DESC
        ''')
        
        models = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Display models
        if models:
            st.subheader("Available Models")
            
            # Create a table to display models
            model_data = {
                "Name": [m[1] for m in models],
                "Description": [m[2] for m in models],
                "Type": [m[3] for m in models],
                "Upload Date": [m[4].strftime("%Y-%m-%d") for m in models]
            }
            
            # Show models in a dataframe
            import pandas as pd
            model_df = pd.DataFrame(model_data)
            st.dataframe(model_df)
            
            # Select model to view
            model_options = {m[1]: m[0] for m in models}
            selected_model = st.selectbox("Select Model to View", options=list(model_options.keys()))
            
            if st.button("View Model"):
                st.session_state.current_model_id = model_options[selected_model]
                st.session_state.current_view = "view"
                st.rerun()
        else:
            st.info("No BIM models available")
        
        # Upload new model
        if check_permission('create'):
            st.subheader("Upload New Model")
            with st.form("upload_model_form"):
                model_name = st.text_input("Model Name")
                model_description = st.text_area("Description")
                model_type = st.selectbox("Model Type", options=["IFC", "OBJ", "GLTF", "Other"])
                model_file = st.file_uploader("Upload Model File", type=["ifc", "obj", "gltf", "glb"])
                
                submitted = st.form_submit_button("Upload")
                
                if submitted and model_name and model_file:
                    # In a real application, we would save the file to a storage service
                    # and then store the reference in the database
                    # For this example, we'll just store metadata
                    
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        # Mock file path - in a real app this would be a proper storage path
                        model_path = f"/models/{model_name.replace(' ', '_')}_{model_file.name}"
                        
                        cursor.execute('''
                            INSERT INTO bim_models 
                            (name, description, model_path, model_type, uploaded_by) 
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                        ''', (model_name, model_description, model_path, model_type, st.session_state.get('user_id')))
                        
                        model_id = cursor.fetchone()[0]
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        st.success(f"Model '{model_name}' uploaded successfully")
                        st.session_state.current_model_id = model_id
                        st.session_state.current_view = "view"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error uploading model: {str(e)}")
        
    except Exception as e:
        st.error(f"Error loading BIM models: {str(e)}")

def render_threejs_viewer(model_path):
    """Render a Three.js based IFC viewer"""
    # Create a custom component for Three.js viewer
    threejs_viewer = """
    <div id="model-container" style="width:100%; height:500px; border:1px solid #ccc;"></div>
    <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/web-ifc-three@0.0.122/dist/web-ifc-three.js"></script>
    
    <script>
        // Initialize Three.js scene
        const container = document.getElementById('model-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f0f0);
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(1, 1, 1);
        scene.add(directionalLight);
        
        // Set up camera
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 5;
        
        // Set up renderer
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);
        
        // Add OrbitControls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.25;
        
        // Add a grid helper
        const gridHelper = new THREE.GridHelper(10, 10);
        scene.add(gridHelper);
        
        // Add axes helper
        const axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);
        
        // Create a placeholder model
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({ color: 0x2194ce });
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        
        // In a real app, we would load the actual model here
        // For example using GLTFLoader or IFCLoader
        // const loader = new THREE.GLTFLoader();
        // loader.load('model_path', function(gltf) {
        //    scene.add(gltf.scene);
        // });
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
        
        // Handle window resize
        window.addEventListener('resize', function() {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
    """
    
    # Render the custom component
    components.html(threejs_viewer, height=550)

def render_view():
    """Render the BIM model viewer"""
    st.title("BIM Model Viewer")
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view BIM models")
        return
    
    # Get the model ID from session state
    model_id = st.session_state.get('current_model_id')
    if not model_id:
        st.warning("No model selected. Please select a model from the list.")
        if st.button("Back to Model List"):
            st.session_state.current_view = "list"
            st.rerun()
        return
    
    # Fetch model details
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, description, model_path, model_type
            FROM bim_models
            WHERE id = %s
        ''', (model_id,))
        
        model = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if model:
            st.subheader(f"Model: {model[1]}")
            st.write(f"Description: {model[2]}")
            st.write(f"Type: {model[4]}")
            
            # Render the 3D viewer
            st.subheader("3D Model Viewer")
            render_threejs_viewer(model[3])
            
            # Model controls
            st.subheader("Viewer Controls")
            st.write("- Left-click and drag to rotate the model")
            st.write("- Right-click and drag to pan")
            st.write("- Scroll to zoom in/out")
            
            # Add a back button
            if st.button("Back to Model List"):
                st.session_state.current_view = "list"
                st.rerun()
            
            # Issues section
            st.subheader("Coordination Issues")
            
            # Fetch issues for this model
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, title, description, status, assigned_to
                    FROM bim_issues
                    WHERE model_id = %s
                    ORDER BY created_at DESC
                ''', (model_id,))
                
                issues = cursor.fetchall()
                cursor.close()
                conn.close()
                
                if issues:
                    # Display issues
                    for i, issue in enumerate(issues):
                        with st.expander(f"Issue #{issue[0]}: {issue[1]}"):
                            st.write(f"Description: {issue[2]}")
                            st.write(f"Status: {issue[3]}")
                            st.write(f"Assigned To: {issue[4]}")
                            
                            # Edit/Delete buttons for administrators and editors
                            if check_permission('update'):
                                if st.button(f"Edit Issue", key=f"edit_issue_{issue[0]}"):
                                    st.session_state.editing_issue_id = issue[0]
                                    st.rerun()
                            
                            if check_permission('delete'):
                                if st.button(f"Delete Issue", key=f"delete_issue_{issue[0]}"):
                                    try:
                                        conn = get_db_connection()
                                        cursor = conn.cursor()
                                        cursor.execute('''
                                            DELETE FROM bim_issues
                                            WHERE id = %s
                                        ''', (issue[0],))
                                        
                                        conn.commit()
                                        cursor.close()
                                        conn.close()
                                        
                                        st.success(f"Issue '{issue[1]}' deleted successfully")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error deleting issue: {str(e)}")
                else:
                    st.info("No coordination issues recorded for this model")
                
                # Add issue form
                if check_permission('create'):
                    with st.expander("Add New Issue"):
                        with st.form("add_issue_form"):
                            issue_title = st.text_input("Issue Title")
                            issue_description = st.text_area("Description")
                            issue_status = st.selectbox("Status", options=["Open", "In Review", "Resolved", "Closed"])
                            issue_assigned_to = st.text_input("Assigned To")
                            
                            # Simplified position input
                            st.subheader("Position (X, Y, Z)")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                loc_x = st.number_input("X", value=0.0)
                            with col2:
                                loc_y = st.number_input("Y", value=0.0)
                            with col3:
                                loc_z = st.number_input("Z", value=0.0)
                            
                            submitted = st.form_submit_button("Add Issue")
                            
                            if submitted and issue_title:
                                try:
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    
                                    cursor.execute('''
                                        INSERT INTO bim_issues 
                                        (model_id, title, description, location_x, location_y, location_z, status, assigned_to, created_by) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ''', (model_id, issue_title, issue_description, loc_x, loc_y, loc_z, 
                                          issue_status, issue_assigned_to, st.session_state.get('user_id')))
                                    
                                    conn.commit()
                                    cursor.close()
                                    conn.close()
                                    
                                    st.success(f"Issue '{issue_title}' added successfully")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error adding issue: {str(e)}")
                    
            except Exception as e:
                st.error(f"Error loading coordination issues: {str(e)}")
            
        else:
            st.error("Model not found")
            if st.button("Back to Model List"):
                st.session_state.current_view = "list"
                st.rerun()
        
    except Exception as e:
        st.error(f"Error loading model details: {str(e)}")

def render_form():
    """Render the form for uploading a new BIM model"""
    st.title("Upload BIM Model")
    
    # Check permission
    if not check_permission('create'):
        st.error("You don't have permission to upload BIM models")
        return
    
    # For simplicity, redirect to list view with upload form
    st.session_state.current_view = "list"
    st.rerun()
