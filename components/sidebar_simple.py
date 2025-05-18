"""
Simplified sidebar navigation component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_sidebar():
    """Render the simplified sidebar navigation."""
    
    with st.sidebar:
        # Add logo and title
        st.image("gcpanel.png", width=50)
        st.title("gcPanel")
        
        # Project selection
        st.markdown("### Project")
        project_name = "Highland Tower Development"
        st.markdown(f"**{project_name}**")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Module selection in sidebar
        module = st.radio(
            "Select Module",
            [
                "Dashboard",
                "Project Information",
                "Schedule",
                "Safety",
                "Contracts",
                "Cost Management",
                "Engineering",
                "Field Operations",
                "Documents",
                "BIM Viewer",
                "Closeout",
                "Settings"
            ],
            label_visibility="collapsed"  # Hide the label
        )
        
        # Update session state based on selection
        if module != st.session_state.get("current_module"):
            st.session_state.current_module = module
            
            # Map selected module to the correct menu item
            if module == "Dashboard":
                st.session_state.menu = "dashboard"
            elif module == "Project Information":
                st.session_state.menu = "project_information"
            elif module == "Schedule":
                st.session_state.menu = "scheduling"
            elif module == "Safety":
                st.session_state.menu = "safety"
            elif module == "Contracts":
                st.session_state.menu = "contracts"
            elif module == "Cost Management":
                st.session_state.menu = "cost_management"
            elif module == "Engineering":
                st.session_state.menu = "engineering"
            elif module == "Field Operations":
                st.session_state.menu = "field_operations"
            elif module == "Documents":
                st.session_state.menu = "documents"
            elif module == "BIM Viewer":
                st.session_state.menu = "bim_viewer"
            elif module == "Closeout":
                st.session_state.menu = "closeout"
            elif module == "Settings":
                st.session_state.menu = "settings"
            
            # No need to rerun, radio button will handle it
        
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel")