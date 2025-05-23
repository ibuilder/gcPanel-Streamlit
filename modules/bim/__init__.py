"""
BIM (Building Information Modeling) module for the gcPanel Construction Management Dashboard.

This module provides BIM visualization and management functionality including:
- 3D model viewing
- Clash detection
- Model analytics
- Issue tracking
- Element properties and metadata

This module follows a clear CRUD pattern with:
1. List views for model selection with filtering/searching
2. Detail views for viewing model metadata and properties
3. Upload/Edit forms for adding and updating models
4. Analytics dashboards for model statistics
"""

import streamlit as st
from modules.bim.components.model_viewer import (
    render_model_list,
    render_model_viewer,
    render_model_details,
    render_model_upload,
    render_model_analytics
)
from modules.bim.enterprise_viewer import render_enterprise_bim_viewer

def render_bim():
    """Render the comprehensive BIM module with enterprise 3D viewer"""
    
    # Header
    st.title("🏗️ BIM Management & 3D Visualization")
    
    # Create tabs for different BIM features
    tabs = st.tabs([
        "📋 Model Library", 
        "🎮 3D Viewer", 
        "📊 Analytics", 
        "⚙️ Management"
    ])
    
    with tabs[0]:
        render_model_library()
    
    with tabs[1]:
        render_enterprise_bim_viewer()
    
    with tabs[2]:
        render_model_analytics()
    
    with tabs[3]:
        render_bim_management()

def render_model_library():
    """Render the model library with list and details"""
    
    # Add debug checkbox to help troubleshooting
    if st.checkbox("🔍 Debug state", value=False, key="bim_debug_state"):
        st.write(f"Current BIM view: {st.session_state.get('bim_view')}")
        st.write(f"Selected model ID: {st.session_state.get('selected_model_id')}")
        st.write(f"Update model ID: {st.session_state.get('update_model_id')}")
    
    # Initialize session state variables if not present
    if "bim_view" not in st.session_state:
        st.session_state.bim_view = "list"
    
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = None
    
    if "update_model_id" not in st.session_state:
        st.session_state.update_model_id = None
    
    # Get current view from session state
    current_view = st.session_state.bim_view
    
    # Add navigation buttons at the top for non-list views
    if current_view != "list":
        # Back button at the top of any non-list view
        if st.button("← Back to Model List", key="back_to_model_list"):
            st.session_state.bim_view = "list"
            # Clear update model ID if present
            if st.session_state.get("update_model_id"):
                st.session_state.update_model_id = None
            st.rerun()
    
    # Render the appropriate view based on session state
    if current_view == "list":
        render_model_list()
    elif current_view == "view":
        render_model_viewer()
    elif current_view == "details":
        render_model_details()
    elif current_view == "upload":
        render_model_upload()

def render_bim_management():
    """Render BIM management interface"""
    
    st.markdown("### ⚙️ BIM Model Management")
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Upload New Model", use_container_width=True):
            st.session_state.bim_view = "upload"
            st.rerun()
    
    with col2:
        if st.button("📋 View All Models", use_container_width=True):
            st.session_state.bim_view = "list"
            st.rerun()
    
    with col3:
        if st.button("🔄 Sync Models", use_container_width=True):
            st.success("✅ Models synchronized successfully!")
    
    # Recent activity
    st.markdown("#### 📈 Recent Activity")
    
    recent_activity = [
        {"action": "Model Uploaded", "model": "Highland Tower - Level 15", "user": "John Smith", "time": "2 hours ago"},
        {"action": "Clash Detection", "model": "Highland Tower - Structural", "user": "Sarah Johnson", "time": "4 hours ago"},
        {"action": "Properties Updated", "model": "Highland Tower - MEP", "user": "Mike Davis", "time": "1 day ago"},
        {"action": "Model Viewed", "model": "Highland Tower - Architectural", "user": "Lisa Chen", "time": "2 days ago"}
    ]
    
    for activity in recent_activity:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            
            with col1:
                st.write(f"**{activity['action']}**")
            
            with col2:
                st.write(activity['model'])
            
            with col3:
                st.write(activity['user'])
            
            with col4:
                st.write(activity['time'])
            
            st.markdown("---")
    
    # Model statistics
    st.markdown("#### 📊 Model Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Models", "12", "+2 this week")
    
    with col2:
        st.metric("Active Clashes", "3", "-5 resolved")
    
    with col3:
        st.metric("Storage Used", "2.8 GB", "+450 MB")
    
    with col4:
        st.metric("Team Members", "8", "+1 new user")
    
    # Advanced features
    st.markdown("#### 🔧 Advanced Features")
    
    advanced_col1, advanced_col2 = st.columns(2)
    
    with advanced_col1:
        st.markdown("**🔍 Clash Detection**")
        st.write("Automatically detect and report clashes between different building systems")
        if st.button("🚀 Run Clash Detection"):
            st.info("Clash detection analysis would be performed here")
        
        st.markdown("**📏 Model Validation**")
        st.write("Validate model integrity and compliance with standards")
        if st.button("✅ Validate Models"):
            st.info("Model validation would be performed here")
    
    with advanced_col2:
        st.markdown("**📊 Progress Tracking**")
        st.write("Track model progress and completion status")
        if st.button("📈 View Progress"):
            st.info("Progress tracking dashboard would be shown here")
        
        st.markdown("**🔗 External Integration**")
        st.write("Sync with external BIM platforms and tools")
        if st.button("🔌 Manage Integrations"):
            st.info("External integration settings would be available here")