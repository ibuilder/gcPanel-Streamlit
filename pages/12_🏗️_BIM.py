"""
BIM Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="BIM - gcPanel", page_icon="🏗️", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🏗️ BIM Management")
st.markdown("Highland Tower Development - Building Information Modeling")
st.markdown("---")

if 'bim_models' not in st.session_state:
    st.session_state.bim_models = [
        {
            "id": "BIM-001",
            "model_name": "Highland Tower Structural Model",
            "discipline": "Structural",
            "version": "v2.3",
            "last_updated": "2024-12-15",
            "file_size": "145.2 MB",
            "status": "Current"
        }
    ]

tab1, tab2, tab3 = st.tabs(["📁 Model Management", "🔍 Model Viewer", "📊 Coordination"])

with tab1:
    st.subheader("📁 BIM Model Management")
    
    with st.form("bim_model_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.text_input("Model Name", placeholder="Descriptive model name")
            discipline = st.selectbox("Discipline", 
                ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"])
            version = st.text_input("Version", placeholder="e.g., v1.0, v2.1")
            author = st.text_input("Author", placeholder="Model creator")
        
        with col2:
            update_date = st.date_input("Last Updated", value=date.today())
            file_format = st.selectbox("File Format", [".rvt", ".ifc", ".dwg", ".nwd", ".bcf"])
            file_size = st.text_input("File Size", placeholder="e.g., 125.5 MB")
            status = st.selectbox("Status", ["Draft", "Current", "Superseded", "Archived"])
        
        description = st.text_area("Model Description", placeholder="Purpose and contents of the model...")
        
        submitted = st.form_submit_button("📋 Register Model", type="primary", use_container_width=True)
        
        if submitted and model_name:
            new_model = {
                "id": f"BIM-{len(st.session_state.bim_models) + 1:03d}",
                "model_name": model_name,
                "discipline": discipline,
                "version": version,
                "author": author,
                "last_updated": str(update_date),
                "file_format": file_format,
                "file_size": file_size,
                "status": status,
                "description": description
            }
            st.session_state.bim_models.insert(0, new_model)
            st.success(f"BIM model {new_model['id']} registered successfully!")
            st.rerun()

with tab2:
    st.subheader("🔍 3D Model Viewer")
    
    st.info("BIM model viewer integration would connect to Autodesk Forge or similar platform for 3D visualization")
    
    selected_model = st.selectbox("Select Model to View", 
        [model['model_name'] for model in st.session_state.bim_models] if st.session_state.bim_models else ["No models available"])
    
    if selected_model and selected_model != "No models available":
        st.markdown(f"**Viewing:** {selected_model}")
        
        # Placeholder for 3D viewer
        st.markdown("""
        <div style="height: 400px; background-color: #f0f0f0; border: 2px dashed #ccc; 
                    display: flex; align-items: center; justify-content: center; border-radius: 10px;">
            <div style="text-align: center; color: #666;">
                <h3>3D BIM Viewer</h3>
                <p>Interactive 3D model viewer would be embedded here</p>
                <p>Model: {}</p>
            </div>
        </div>
        """.format(selected_model), unsafe_allow_html=True)

with tab3:
    st.subheader("📊 Model Coordination")
    
    if st.session_state.bim_models:
        df = pd.DataFrame(st.session_state.bim_models)
        
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Search models...")
        with col2:
            discipline_filter = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df['discipline'] == discipline_filter]
        
        st.write(f"**Total Models:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No BIM models registered. Register your first model above!")
    
    # Coordination metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Models", "8", "1")
    
    with col2:
        st.metric("Current Models", "6", "0")
    
    with col3:
        st.metric("Clash Issues", "12", "-3")
    
    with col4:
        st.metric("Last Coordination", "2 days ago")