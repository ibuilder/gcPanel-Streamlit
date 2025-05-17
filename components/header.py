import streamlit as st
from utils.auth import logout_user
from components.custom_elements import toggle_button, icon_button

def render_header():
    """Render the application header"""
    # Initialize theme in session state if not already present
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
        
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 2])
        
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
                # Theme toggle and user info in columns
                theme_col, user_col = st.columns([1, 2])
                
                with theme_col:
                    # Dark/Light theme toggle with improved styling
                    st.markdown('<div style="text-align: center; font-size: 10px; color: #666; margin-bottom: 2px;">Theme</div>', unsafe_allow_html=True)
                    if toggle_button(
                        label="Dark" if st.session_state.theme == 'dark' else "Light", 
                        value=st.session_state.theme == 'dark',
                        key="theme_toggle_element"
                    ):
                        # Can't use callback directly due to Streamlit's execution model, so use a standard button
                        pass
                        
                    # Hidden button for the toggle functionality
                    if st.button("Toggle Theme", key="theme_toggle_btn", help="Switch between dark and light theme"):
                        # Toggle theme
                        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                        st.rerun()
                
                with user_col:
                    # User info with improved styling
                    st.markdown(f"""
                    <div style="display: flex; flex-direction: column; padding-top: 5px;">
                        <div style="font-size: 14px; font-weight: 600;">{st.session_state.username}</div>
                        <div style="font-size: 12px; color: #666;">{st.session_state.user_role}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Logout button with visual improvement
                    st.markdown("""
                    <style>
                    div[data-testid="stButton"] button {
                        background-color: rgba(244, 67, 54, 0.1);
                        color: #f44336;
                        border: 1px solid rgba(244, 67, 54, 0.2);
                        padding: 2px 10px;
                        font-size: 12px;
                        transition: all 0.3s;
                    }
                    div[data-testid="stButton"] button:hover {
                        background-color: rgba(244, 67, 54, 0.2);
                        border: 1px solid rgba(244, 67, 54, 0.3);
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    if st.button("Logout", key="logout_btn", help="Log out from your account"):
                        logout_user()
    
    # Apply theme based on selection
    if st.session_state.theme == 'light':
        # Apply light theme CSS variables
        st.markdown("""
        <style>
            :root {
                --primary-color: #1976d2;
                --secondary-color: #2e7d32;
                --accent-color: #ff8f00;
                --background-color: #ffffff;
                --sidebar-bg: #f5f5f5;
                --sidebar-text: #333333;
                --card-bg: white;
                --text-color: #333333;
                --border-color: #e0e0e0;
                --success-color: #4caf50;
                --warning-color: #ff9800;
                --danger-color: #f44336;
                --info-color: #2196f3;
            }
            
            /* Light theme sidebar */
            section[data-testid="stSidebar"] {
                background-color: var(--sidebar-bg);
            }
            
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] .stSubheader,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] button {
                color: var(--sidebar-text) !important;
            }
            
            section[data-testid="stSidebar"] hr {
                border-color: #d0d0d0;
            }
            
            .main {
                background-color: #fafafa;
            }
            
            /* Additional light theme customizations */
            .stButton button {
                background-color: var(--primary-color);
                color: white;
                border: none;
                font-weight: 500;
            }
            
            .stButton button:hover {
                background-color: var(--primary-color);
                opacity: 0.9;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Horizontal line
    st.markdown("<hr>", unsafe_allow_html=True)
