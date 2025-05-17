import streamlit as st
import streamlit.components.v1 as components

def render_navigation():
    """Render the navigation bar with improved UI"""
    # Get the current section and module
    current_section = st.session_state.get('current_section')
    current_module = st.session_state.get('current_module')
    current_view = st.session_state.get('current_view', 'list')
    
    # Add navigation styles
    st.markdown("""
    <style>
    /* Navigation container */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 5px;
        margin-bottom: 15px;
        background: rgba(0,0,0,0.05);
        border-radius: 8px;
    }
    
    /* Breadcrumbs */
    .breadcrumbs {
        display: flex;
        align-items: center;
        font-size: 14px;
    }
    
    .breadcrumbs span {
        margin: 0 5px;
        color: #999;
    }
    
    .breadcrumbs a {
        color: var(--text-color);
        text-decoration: none;
    }
    
    /* View tabs */
    .view-tabs {
        display: flex;
        gap: 5px;
    }
    
    .view-tab {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .view-tab.active {
        background: var(--primary-color, #1e88e5);
        color: white;
    }
    
    .view-tab:not(.active) {
        background: rgba(100,100,100,0.1);
    }
    
    .view-tab:not(.active):hover {
        background: rgba(100,100,100,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # If a section and module are selected, render the navigation for that module
    if current_section and current_module:
        modules = st.session_state.get('modules', {})
        
        # Get section and module info
        section_info = modules.get(current_section, {})
        section_display_name = section_info.get('display_name', current_section.title())
        
        # Find the current module
        module_info = None
        for module in section_info.get('modules', []):
            if module['name'] == current_module:
                module_info = module
                break
        
        module_display_name = module_info['display_name'] if module_info else current_module.replace('_', ' ').title()
        module_icon = module_info.get('icon', 'folder') if module_info else 'folder'
        
        # Render the modern navigation UI with better styling
        st.markdown(f"""
        <div class="card" style="margin-bottom: 20px; padding: 16px; background: linear-gradient(to right, rgba(25, 118, 210, 0.05), rgba(25, 118, 210, 0.02));">
            <div class="breadcrumb">
                <div class="breadcrumb-item">
                    <a href="#" id="back-to-home" style="display: flex; align-items: center; gap: 6px;">
                        <span class="material-icons" style="font-size: 16px;">home</span> 
                        <span>Dashboard</span>
                    </a>
                </div>
                <div class="breadcrumb-item">
                    <a href="#" id="back-to-section" style="display: flex; align-items: center; gap: 6px;">
                        <span class="material-icons" style="font-size: 16px;">folder</span>
                        <span>{section_display_name}</span>
                    </a>
                </div>
                <div class="breadcrumb-item" style="display: flex; align-items: center; gap: 6px;">
                    <span class="material-icons" style="font-size: 16px;">{module_icon}</span>
                    <span>{module_display_name}</span>
                </div>
            </div>
            
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: 15px;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="background-color: var(--primary-color); width: 36px; height: 36px; border-radius: 8px;
                             display: flex; align-items: center; justify-content: center; margin-right: 16px;">
                        <span class="material-icons" style="color: white; font-size: 20px;">{module_icon}</span>
                    </div>
                    <h2 style="font-size: 22px; margin: 0; font-weight: 500; color: var(--text-primary);">{module_display_name}</h2>
                </div>
                
                <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                    <div class="status-pill" 
                        style="background-color: {('var(--primary-color)' if current_view == 'list' else 'rgba(255, 255, 255, 0.05)')};
                               color: {('white' if current_view == 'list' else 'var(--text-secondary)')};
                               cursor: pointer; box-shadow: {('0 2px 8px rgba(25, 118, 210, 0.4)' if current_view == 'list' else 'none')};"
                        id="list-view-tab">
                        <span class="material-icons" style="font-size: 14px; margin-right: 4px;">view_list</span> 
                        List
                    </div>
                    <div class="status-pill" 
                        style="background-color: {('var(--primary-color)' if current_view == 'view' else 'rgba(255, 255, 255, 0.05)')};
                               color: {('white' if current_view == 'view' else 'var(--text-secondary)')};
                               cursor: pointer; box-shadow: {('0 2px 8px rgba(25, 118, 210, 0.4)' if current_view == 'view' else 'none')};"
                        id="detail-view-tab">
                        <span class="material-icons" style="font-size: 14px; margin-right: 4px;">visibility</span> 
                        Details
                    </div>
                    <div class="status-pill" 
                        style="background-color: {('var(--primary-color)' if current_view == 'form' else 'rgba(255, 255, 255, 0.05)')};
                               color: {('white' if current_view == 'form' else 'var(--text-secondary)')};
                               cursor: pointer; box-shadow: {('0 2px 8px rgba(25, 118, 210, 0.4)' if current_view == 'form' else 'none')};"
                        id="form-view-tab">
                        <span class="material-icons" style="font-size: 14px; margin-right: 4px;">edit</span> 
                        Form
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden action buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 7])
        
        with col1:
            if st.button("", key="back_to_home_btn", help="Return to the dashboard"):
                st.session_state.current_section = None
                st.session_state.current_module = None
                st.rerun()
                
        with col2:
            if st.button("", key="back_to_section_btn", help="Return to section"):
                st.session_state.current_section = None
                st.rerun()
                
        # Navigation tabs with proper view selection
        col_a, col_b, col_c = st.columns([1, 1, 1])
        
        with col_a:
            if st.button("", key="list_view_btn", help="List View"):
                st.session_state.current_view = "list"
                st.rerun()
        
        with col_b:
            if st.button("", key="detail_view_btn", help="Detail View"):
                st.session_state.current_view = "view"
                st.rerun()
        
        with col_c:
            if st.button("", key="form_view_btn", help="Form View"):
                st.session_state.current_view = "form"
                st.rerun()
