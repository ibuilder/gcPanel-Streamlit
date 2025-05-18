"""
Advanced BIM Viewer Module with 3D IFC Visualization

This module provides a 3D interactive viewer for IFC files using web-ifc library.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

# Get the list of available IFC files
def get_available_ifc_files():
    """Get a list of IFC files in the static/models directory"""
    models_dir = 'static/models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    return [f for f in os.listdir(models_dir) if f.lower().endswith('.ifc')]

def render_advanced_bim_viewer():
    """Render the advanced 3D BIM Viewer interface"""
    st.title("BIM Viewer (3D)")
    
    with st.container():
        st.write("This 3D viewer allows you to interactively explore building information models.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Main viewer container
            viewer_container = st.empty()
            
            # HTML for the 3D viewer
            html_content = """
            <div style="width: 100%; height: 600px; position: relative; overflow: hidden; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div id="ifc-viewer-container" style="width: 100%; height: 100%;"></div>
            </div>
            
            <script src="https://unpkg.com/three@0.130.1/build/three.min.js"></script>
            <script src="https://unpkg.com/web-ifc@0.0.36/web-ifc-api.js"></script>
            <script src="https://unpkg.com/web-ifc-viewer@0.0.32/dist/web-ifc-viewer.js"></script>
            <script type="module" src="static/js/ifc-viewer.js"></script>
            
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            """
            
            viewer_container.markdown(html_content, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Model Controls")
            
            # Model selection
            available_models = get_available_ifc_files()
            if available_models:
                selected_model = st.selectbox("Select Model", available_models)
                if st.button("Load Selected Model"):
                    st.write(f"Loading model: {selected_model}")
                    # Load model via JavaScript - this would be handled by the JS code
            else:
                st.warning("No IFC models found. Please upload a model file.")
            
            # File upload
            uploaded_file = st.file_uploader("Upload IFC File", type=['ifc'])
            if uploaded_file is not None:
                # Save uploaded file
                model_path = os.path.join('static/models', uploaded_file.name)
                with open(model_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Provide button to load the uploaded model
                if st.button("Load Uploaded Model"):
                    st.write(f"Loading uploaded model: {uploaded_file.name}")
                    # Load model via JavaScript - this would be handled by the JS code
            
            # Viewer controls
            st.subheader("View Options")
            if st.button("Reset View"):
                st.write("Resetting view...")
                # This would trigger a JavaScript function to reset the view
            
            show_grid = st.checkbox("Show Grid", value=True)
            show_axes = st.checkbox("Show Axes", value=True)
            
            # Element tree (simplified)
            st.subheader("Element Explorer")
            st.write("Element hierarchy would be displayed here")
            
    # Additional information about the model
    with st.expander("About BIM Models"):
        st.write("""
        ## Building Information Modeling (BIM)
        
        BIM is a digital representation of the physical and functional characteristics of a facility.
        A BIM model contains rich information about the building elements, their properties, and relationships.
        
        The IFC (Industry Foundation Classes) format is an open standard for BIM data exchange.
        
        ### Tips for using this viewer:
        
        - Left-click and drag to rotate the model
        - Right-click and drag to pan
        - Scroll to zoom in and out
        - Use the controls panel to change view options
        """)