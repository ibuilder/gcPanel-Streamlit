import streamlit as st
from utils.module_loader import upload_module

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        st.title("gcPanel")
        
        # Project selection
        st.subheader("Project Selection")
        
        # In a real application, we would fetch projects from the database
        # For demonstration, we'll use a static list
        projects = ["Sample Project 1", "Sample Project 2", "Sample Project 3"]
        selected_project = st.selectbox(
            "Select Project",
            projects,
            index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
            key="project_selector"
        )
        
        if st.button("Load Project") or 'current_project' not in st.session_state:
            st.session_state.current_project = selected_project
            st.rerun()
        
        st.markdown("---")
        
        # Module navigation
        st.subheader("Modules")
        
        # Get sections and modules from session state
        modules = st.session_state.get('modules', {})
        
        # Display sections as expanders
        for section_name, section_info in modules.items():
            with st.expander(section_info['display_name'], expanded=st.session_state.get('current_section') == section_name):
                # Display modules as buttons
                for module in section_info['modules']:
                    if st.button(f"{module['display_name']}", key=f"module_{section_name}_{module['name']}"):
                        st.session_state.current_section = section_name
                        st.session_state.current_module = module['name']
                        st.session_state.current_view = "list"  # Default to list view
                        st.rerun()
        
        st.markdown("---")
        
        # Administrator tools
        if st.session_state.get('user_role') == 'administrator':
            st.subheader("Administrator Tools")
            
            # Module upload
            with st.expander("Upload Module"):
                uploaded_file = st.file_uploader("Select Module ZIP file", type="zip")
                
                if uploaded_file is not None and st.button("Install Module"):
                    success, message = upload_module(uploaded_file)
                    if success:
                        st.success(message)
                        # Reload modules
                        st.session_state.modules = None
                        st.rerun()
                    else:
                        st.error(message)
            
            # User management (link to module)
            if st.button("User Management"):
                st.session_state.current_section = "settings"
                st.session_state.current_module = "user_management"
                st.session_state.current_view = "list"
                st.rerun()
            
            # Database settings (link to module)
            if st.button("Database Settings"):
                st.session_state.current_section = "settings"
                st.session_state.current_module = "database_settings"
                st.session_state.current_view = "list"
                st.rerun()
        
        st.markdown("---")
        
        # Help and documentation
        with st.expander("Help & Documentation"):
            st.markdown("[User Manual](#)")
            st.markdown("[API Documentation](#)")
            st.markdown("[Report Issue](#)")
        
        # Display version info
        st.caption("gcPanel v1.0.0")
        st.caption("© 2023 gcPanel Team")
