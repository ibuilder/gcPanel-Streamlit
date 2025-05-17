import streamlit as st
import streamlit.components.v1 as components

def render_navigation():
    """Render the navigation bar"""
    with st.container():
        # Get the current section and module
        current_section = st.session_state.get('current_section')
        current_module = st.session_state.get('current_module')
        
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
            
            # Navigation breadcrumbs
            cols = st.columns([1, 3, 6])
            with cols[0]:
                if st.button("< Back to Sections"):
                    st.session_state.current_section = None
                    st.session_state.current_module = None
                    st.rerun()
            
            with cols[1]:
                st.markdown(f"**Section:** {section_display_name}")
            
            with cols[2]:
                st.markdown(f"**Module:** {module_display_name}")
            
            # Module navigation tabs
            tab1, tab2, tab3 = st.tabs(["List", "View", "Form"])
            
            with tab1:
                if st.button("List View", key="list_view_btn"):
                    st.session_state.current_view = "list"
                    st.rerun()
            
            with tab2:
                if st.button("Detail View", key="detail_view_btn"):
                    st.session_state.current_view = "view"
                    st.rerun()
            
            with tab3:
                if st.button("Form", key="form_view_btn"):
                    st.session_state.current_view = "form"
                    st.rerun()
            
            st.markdown("<hr>", unsafe_allow_html=True)
