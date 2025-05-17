import streamlit as st
from utils.auth import logout_user

def render_header():
    """Render the application header"""
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            st.image("https://pixabay.com/get/g3cfd2af0042cda0f537173d61cbd8a7ae0d48b14297c65a68dd9efb85198a4f77f365bf104fe039586f2d602de0204930ff2a6faead82b4fddf3415e29edf73b_1280.jpg", 
                    width=100)
        
        with col2:
            st.title("gcPanel - Construction Management Dashboard")
            
            # Display current project if selected
            if 'current_project' in st.session_state:
                st.subheader(f"Project: {st.session_state.current_project}")
        
        with col3:
            # User info and logout
            if st.session_state.authenticated:
                st.write(f"Logged in as: {st.session_state.username}")
                st.write(f"Role: {st.session_state.user_role}")
                if st.button("Logout"):
                    logout_user()
    
    # Horizontal line
    st.markdown("<hr>", unsafe_allow_html=True)
