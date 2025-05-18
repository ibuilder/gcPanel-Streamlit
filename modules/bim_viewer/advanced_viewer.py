"""
Advanced BIM Viewer Module with 3D IFC Visualization

This module provides a 3D interactive viewer for IFC files using web-ifc library.
"""
import os
import json
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Get the list of available IFC files
def get_available_ifc_files():
    """Get a list of IFC files in the static/models directory"""
    models_dir = 'static/models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    return [f for f in os.listdir(models_dir) if f.lower().endswith('.ifc')]

def create_sample_properties():
    """Create sample properties for demo purposes"""
    return {
        "General": {
            "Name": "Highland Tower",
            "Description": "15-story mixed-use high-rise building",
            "Building Type": "Mixed-use Residential",
            "Construction Year": "2025"
        },
        "Dimensions": {
            "Height": "168.5 ft (51.4 m)",
            "Width": "80.2 ft (24.4 m)",
            "Length": "120.7 ft (36.8 m)",
            "Total Area": "168,500 sq ft (15,650 sq m)"
        },
        "Performance": {
            "Energy Rating": "LEED Gold",
            "Structural Type": "Reinforced concrete core with steel frame",
            "Fire Rating": "Type 1A - 3 hour rating"
        }
    }

def render_advanced_bim_viewer():
    """Render the advanced 3D BIM Viewer interface"""
    st.title("BIM Viewer (3D)")
    
    # Initialize session state for BIM viewer
    if "bim_properties" not in st.session_state:
        st.session_state.bim_properties = create_sample_properties()
        
    if "selected_element" not in st.session_state:
        st.session_state.selected_element = None
        
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "3D"
    
    # Main content
    with st.container():
        # Tabs for different view modes
        view_modes = ["3D View", "Properties", "Analysis"]
        tab1, tab2, tab3 = st.tabs(view_modes)
        
        with tab1:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Main viewer container with enhanced styling
                viewer_container = st.container()
                
                with viewer_container:
                    # Status indicator above the viewer
                    st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center;">
                            <div class="status-badge success">
                                <span style="display: flex; align-items: center;">
                                    <span class="material-icons" style="font-size: 14px; margin-right: 4px;">check_circle</span>
                                    Model Ready
                                </span>
                            </div>
                        </div>
                        <div>
                            <div class="status-badge info">
                                <span style="display: flex; align-items: center;">
                                    <span class="material-icons" style="font-size: 14px; margin-right: 4px;">info</span>
                                    Highland Tower Development
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # HTML for the 3D viewer with enhanced styling
                    html_content = """
                    <div class="viewer-container" style="width: 100%; height: 600px; position: relative; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <div id="ifc-viewer-container" style="width: 100%; height: 100%;"></div>
                        
                        <!-- Loading overlay -->
                        <div id="loading-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                             background-color: rgba(255,255,255,0.8); display: flex; justify-content: center; 
                             align-items: center; z-index: 1000; display: none;">
                            <div style="text-align: center;">
                                <div class="material-icons" style="font-size: 48px; color: #3367D6; animation: spin 2s linear infinite;">
                                    sync
                                </div>
                                <p style="margin-top: 10px; font-weight: 500; color: #3367D6;">Loading model...</p>
                            </div>
                        </div>
                        
                        <!-- Tools overlay -->
                        <div style="position: absolute; bottom: 10px; left: 10px; display: flex; gap: 5px;">
                            <button id="section-tool" class="viewer-tool-button" title="Section Tool" style="width: 40px; height: 40px; border-radius: 50%; background: white; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <span class="material-icons" style="font-size: 20px; color: #3367D6;">content_cut</span>
                            </button>
                            <button id="measure-tool" class="viewer-tool-button" title="Measure Tool" style="width: 40px; height: 40px; border-radius: 50%; background: white; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <span class="material-icons" style="font-size: 20px; color: #3367D6;">straighten</span>
                            </button>
                        </div>
                    </div>
                    
                    <style>
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    .viewer-tool-button:hover {
                        background-color: #f0f0f0 !important;
                        transform: translateY(-2px);
                        transition: all 0.2s;
                    }
                    </style>
                    
                    <script src="https://unpkg.com/three@0.130.1/build/three.min.js"></script>
                    <script src="https://unpkg.com/web-ifc@0.0.36/web-ifc-api.js"></script>
                    <script src="https://unpkg.com/web-ifc-viewer@0.0.32/dist/web-ifc-viewer.js"></script>
                    <script type="module" src="static/js/ifc-viewer.js"></script>
                    
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    """
                    
                    st.markdown(html_content, unsafe_allow_html=True)
                
                # Information panel below the viewer
                with st.expander("Model Information", expanded=False):
                    st.markdown("""
                    <style>
                    .info-grid {
                        display: grid;
                        grid-template-columns: 1fr 1fr 1fr;
                        gap: 10px;
                        margin-top: 10px;
                    }
                    .info-item {
                        background-color: #F8F9FA;
                        border-radius: 8px;
                        padding: 10px;
                    }
                    .info-item h4 {
                        margin: 0 0 5px 0;
                        font-size: 14px;
                        color: #5F6368;
                    }
                    .info-item p {
                        margin: 0;
                        font-size: 16px;
                        font-weight: 500;
                    }
                    </style>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <h4>Project</h4>
                            <p>Highland Tower</p>
                        </div>
                        <div class="info-item">
                            <h4>Last Modified</h4>
                            <p>{}</p>
                        </div>
                        <div class="info-item">
                            <h4>Version</h4>
                            <p>2.3.1</p>
                        </div>
                        <div class="info-item">
                            <h4>Created By</h4>
                            <p>Smith Architects</p>
                        </div>
                        <div class="info-item">
                            <h4>File Size</h4>
                            <p>24.7 MB</p>
                        </div>
                        <div class="info-item">
                            <h4>Elements</h4>
                            <p>4,283</p>
                        </div>
                    </div>
                    """.format(datetime.now().strftime("%b %d, %Y")), unsafe_allow_html=True)
            
            with col2:
                with st.container():
                    st.subheader("Model Controls")
                    
                    # Model selection with improved UI
                    available_models = get_available_ifc_files()
                    
                    # Add default TallBuilding.ifc if it doesn't exist
                    models_dir = 'static/models'
                    if not os.path.exists(models_dir):
                        os.makedirs(models_dir)
                        
                    default_model = 'TallBuilding.ifc'
                    default_model_path = os.path.join(models_dir, default_model)
                    if not os.path.exists(default_model_path) and os.path.exists('attached_assets/TallBuilding.ifc'):
                        with open('attached_assets/TallBuilding.ifc', 'rb') as src, open(default_model_path, 'wb') as dst:
                            dst.write(src.read())
                            available_models = get_available_ifc_files()
                    
                    if available_models:
                        selected_model = st.selectbox(
                            "Select Model",
                            available_models,
                            index=0 if default_model in available_models else 0
                        )
                        
                        # Style the button as a primary action
                        st.markdown("""
                        <style>
                        div[data-testid="stButton"] > button {
                            background-color: #3367D6;
                            color: white;
                            font-weight: 500;
                            border-radius: 4px;
                            border: none;
                            padding: 0.5rem 1rem;
                            width: 100%;
                        }
                        div[data-testid="stButton"] > button:hover {
                            background-color: #4285F4;
                            border: none;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📥 Load Model", key="load_model"):
                            # We would trigger loading the model with JavaScript
                            st.markdown(f"""
                            <div class="status-badge success">
                                <span style="display: flex; align-items: center;">
                                    <span class="material-icons" style="font-size: 14px; margin-right: 4px;">check_circle</span>
                                    Loading model: {selected_model}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("No IFC models found. Please upload a model file.")
                    
                    # Divider
                    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #DADCE0;'>", unsafe_allow_html=True)
                    
                    # File upload with improved styling
                    st.subheader("Import Model")
                    uploaded_file = st.file_uploader("Upload IFC File", type=['ifc'])
                    if uploaded_file is not None:
                        # Save uploaded file
                        model_path = os.path.join('static/models', uploaded_file.name)
                        with open(model_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        st.markdown(f"""
                        <div class="status-badge success">
                            <span style="display: flex; align-items: center;">
                                <span class="material-icons" style="font-size: 14px; margin-right: 4px;">check_circle</span>
                                File uploaded: {uploaded_file.name}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📥 Load Uploaded Model", key="load_uploaded"):
                            st.markdown(f"""
                            <div class="status-badge info">
                                <span style="display: flex; align-items: center;">
                                    <span class="material-icons" style="font-size: 14px; margin-right: 4px;">info</span>
                                    Loading uploaded model: {uploaded_file.name}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Divider
                    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #DADCE0;'>", unsafe_allow_html=True)
                    
                    # Viewer controls with improved UI
                    st.subheader("View Options")
                    
                    # Create two columns for controls
                    ctrl_col1, ctrl_col2 = st.columns(2)
                    
                    with ctrl_col1:
                        st.button("🔄 Reset View", key="reset_view")
                        st.checkbox("🛣️ Show Grid", value=True, key="show_grid")
                    
                    with ctrl_col2:
                        st.button("📷 Screenshot", key="screenshot")
                        st.checkbox("📏 Show Axes", value=True, key="show_axes")
                    
                    # Divider
                    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #DADCE0;'>", unsafe_allow_html=True)
                    
                    # Display options
                    st.subheader("Display Options")
                    
                    display_mode = st.radio(
                        "Display Mode",
                        ["Solid", "Wireframe", "Hidden Lines"],
                        horizontal=True
                    )
                    
                    # Color theme selection
                    color_scheme = st.select_slider(
                        "Color Scheme",
                        options=["By Type", "By Material", "By Level", "By System"]
                    )
                    
                    # Transparency slider
                    transparency = st.slider("Transparency", 0, 100, 0, format="%d%%")
                    
        # Properties tab content
        with tab2:
            properties_col1, properties_col2 = st.columns([2, 1])
            
            with properties_col1:
                st.subheader("Model Properties")
                
                for category, props in st.session_state.bim_properties.items():
                    with st.expander(category, expanded=(category == "General")):
                        for key, value in props.items():
                            cols = st.columns([1, 2])
                            cols[0].markdown(f"**{key}:**")
                            cols[1].markdown(value)
            
            with properties_col2:
                st.subheader("Selected Element")
                if st.session_state.selected_element:
                    st.json(st.session_state.selected_element)
                else:
                    st.info("No element selected. Click on an element in the 3D view to see its properties.")
                    
                    # Sample element button for demo
                    if st.button("Select Sample Element"):
                        st.session_state.selected_element = {
                            "id": "2zFvHYuG98QBPyc3i3yBmA",
                            "type": "IfcWall",
                            "name": "Basic Wall:Interior - 4 7/8\" Partition (1-hr):184384",
                            "level": "Level 5",
                            "material": "Gypsum Wall Board",
                            "dimensions": {
                                "length": 3.45,
                                "width": 0.12,
                                "height": 2.9,
                                "area": 10.01
                            }
                        }
                        st.rerun()
        
        # Analysis tab content
        with tab3:
            st.subheader("Model Analysis")
            
            analysis_tabs = st.tabs(["Element Breakdown", "Space Usage", "Materials", "Issues"])
            
            with analysis_tabs[0]:
                st.subheader("Element Types")
                
                # Create sample data for the element breakdown chart
                element_types = ['Walls', 'Floors', 'Ceilings', 'Doors', 'Windows', 'Furniture', 'MEP', 'Structure']
                element_counts = [145, 78, 72, 64, 92, 38, 128, 56]
                
                # Create a bar chart
                st.bar_chart({
                    'Elements': element_counts
                }, use_container_width=True)
                
                # Element table
                st.markdown("#### Element Details")
                element_data = {
                    'Type': element_types,
                    'Count': element_counts,
                    'Modeled': ['Yes'] * len(element_types),
                    'Issues': [0, 2, 0, 1, 0, 0, 4, 0]
                }
                st.dataframe(element_data)
            
            with analysis_tabs[1]:
                st.subheader("Space Usage Analysis")
                st.info("Space usage analysis shows how building area is utilized across different functions.")
                
                # Create sample data for space usage chart
                space_types = ['Residential', 'Retail', 'Common Areas', 'Mechanical', 'Circulation', 'Amenities']
                space_areas = [102500, 12000, 18000, 14000, 16000, 6000]
                
                # Create a pie chart
                st.write("Space Distribution (sq ft)")
                st.write("Total Area: 168,500 sq ft")
                # We can't directly create a pie chart in Streamlit, so we'll use a placeholder
                st.markdown("""
                <div style="width: 100%; height: 300px; display: flex; justify-content: center; align-items: center; background-color: #f8f9fa; border-radius: 8px;">
                    <img src="https://mec-s1-p.mlstatic.com/977210-MEC49308273448_032022-O.jpg" style="max-width: 100%; max-height: 100%;">
                    <div style="position: absolute; text-align: center;">
                        <p style="font-weight: bold;">Space Usage Chart</p>
                        <p>Interactive pie chart would display here</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with analysis_tabs[2]:
                st.subheader("Materials Analysis")
                st.info("Material analysis shows the types and quantities of materials used in the model.")
                
                # Create material quantity table
                st.markdown("#### Material Quantities")
                material_data = {
                    'Material': ['Concrete', 'Steel', 'Glass', 'Gypsum Board', 'Wood', 'Insulation', 'Brick'],
                    'Volume (cu ft)': [24500, 4200, 3600, 12000, 1800, 8500, 3200],
                    'Weight (tons)': [2940, 1050, 360, 324, 45, 85, 256],
                    'Cost ($)': [980000, 840000, 432000, 144000, 126000, 76500, 128000]
                }
                st.dataframe(material_data)
                
                # Add a material cost chart
                st.markdown("#### Material Cost Breakdown")
                st.bar_chart({
                    'Cost ($)': material_data['Cost ($)']
                }, use_container_width=True)
            
            with analysis_tabs[3]:
                st.subheader("Issues Report")
                
                # Create an issues status indicator
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div style="background-color: #fef0f0; border-left: 4px solid #DB4437; padding: 15px; border-radius: 4px;">
                        <h3 style="margin: 0; color: #DB4437; font-size: 16px;">Critical Issues</h3>
                        <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">2</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color: #fef6e7; border-left: 4px solid #F4B400; padding: 15px; border-radius: 4px;">
                        <h3 style="margin: 0; color: #F4B400; font-size: 16px;">Warnings</h3>
                        <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">5</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div style="background-color: #e8f4eb; border-left: 4px solid #0F9D58; padding: 15px; border-radius: 4px;">
                        <h3 style="margin: 0; color: #0F9D58; font-size: 16px;">Resolved</h3>
                        <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">12</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Issues list
                st.markdown("#### Recent Issues")
                issues_data = {
                    'ID': ['IFC-01', 'IFC-02', 'IFC-03', 'IFC-04', 'IFC-05'],
                    'Type': ['Clash', 'Missing Element', 'Geometry Error', 'Clash', 'Parameter Error'],
                    'Description': [
                        'MEP duct intersects with structural beam',
                        'Door missing from level 8 apartment unit',
                        'Wall geometry error on north facade',
                        'Plumbing pipe intersects with electrical conduit',
                        'Fire rating parameter missing from walls'
                    ],
                    'Status': ['Critical', 'Warning', 'Warning', 'Critical', 'Warning'],
                    'Location': ['Level 3', 'Level 8', 'Level 12', 'Level 2', 'Multiple']
                }
                st.dataframe(issues_data)
                
    # Additional information about the model in an expander
    with st.expander("About BIM Models"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ## Building Information Modeling (BIM)
            
            BIM is a digital representation of the physical and functional characteristics of a facility.
            A BIM model contains rich information about the building elements, their properties, and relationships.
            
            The IFC (Industry Foundation Classes) format is an open standard for BIM data exchange.
            """)
        
        with col2:
            st.markdown("""
            ### Tips for using this viewer:
            
            - 🖱️ Left-click and drag to rotate the model
            - 🖱️ Right-click and drag to pan
            - 🖱️ Scroll to zoom in and out
            - ✂️ Use section tool to create cross-sections
            - 📏 Use measure tool to calculate distances
            """)
            
            # Add a download button for user guide
            st.download_button(
                label="📥 Download User Guide",
                data="This would be the content of a PDF user guide",
                file_name="bim_viewer_guide.pdf",
                mime="application/pdf"
            )