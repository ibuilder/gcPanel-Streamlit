import streamlit as st
from utils.auth import logout_user
from components.custom_elements import toggle_button, icon_button

def render_header():
    """Render the application header"""
    # Initialize theme in session state if not already present
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
        
    # Material Icons link
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Modern header with improved layout and styling
    with st.container():
        # Add elevated header style
        st.markdown("""
        <style>
        /* Header container styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 5px;
            margin-bottom: 5px;
            border-radius: 8px;
        }
        
        /* Logo and title styling */
        .header-logo {
            display: flex;
            align-items: center;
        }
        
        .header-logo h2 {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
            color: var(--text-color, #ffffff);
        }
        
        /* User controls area */
        .header-controls {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        /* Theme toggle button */
        .theme-toggle {
            cursor: pointer;
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 4px 10px;
            font-size: 13px;
            transition: all 0.2s ease;
        }
        
        .theme-toggle:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* User info */
        .user-info {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
        }
        
        /* Logout button */
        .logout-btn {
            cursor: pointer;
            color: #f44336;
            padding: 3px;
            font-size: 20px;
            border-radius: 50%;
            transition: background-color 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .logout-btn:hover {
            background-color: rgba(244, 67, 54, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Define variables for template
        theme_icon = "dark_mode" if st.session_state.theme == 'light' else "light_mode"
        theme_text = "Light" if st.session_state.theme == 'dark' else "Dark"
        project_name = st.session_state.get('current_project', 'gcPanel Dashboard')
        project_icon = "domain" if 'current_project' in st.session_state else "dashboard"
        username = st.session_state.get('username', '')
        
        # Render the header
        if st.session_state.authenticated:
            # Create clean columns layout for header
            left_col, middle_col, right_col = st.columns([1, 3, 1])
            
            # Logo and project name
            with left_col:
                st.write(f"""
                <div style="display: flex; align-items: center; height: 60px;">
                    <div style="background-color: var(--primary-color); width: 40px; height: 40px; border-radius: 8px;
                             display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                        <span class="material-icons" style="color: white; font-size: 24px;">{project_icon}</span>
                    </div>
                    <div>
                        <h2 style="font-size: 18px; font-weight: 600; margin: 0; line-height: 1.2;">{project_name}</h2>
                        <div style="font-size: 12px; color: var(--text-secondary);">Construction Management</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # User controls in right column
            with right_col:
                # Create a single row for theme toggle, user info, and logout
                theme_toggle_col, user_col, logout_col = st.columns([5, 10, 2])
                
                # Theme toggle button
                with theme_toggle_col:
                    if st.button(f"{theme_icon}", key="theme_toggle_btn", help=f"Switch to {theme_text} theme"):
                        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                        st.rerun()
                
                # User info display
                with user_col:
                    st.write(f"""
                    <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 6px 12px; 
                             display: flex; align-items: center; gap: 8px; width: fit-content; margin-left: auto;">
                        <span class="material-icons" style="font-size: 18px;">account_circle</span>
                        <span style="font-size: 14px;">{username}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Logout button
                with logout_col:
                    if st.button("", key="logout_btn", help="Log out from your account"):
                        logout_user()
                        
                    # Add styled logout icon
                    st.markdown("""
                    <style>
                    /* Style for logout button */
                    [data-testid="baseButton-secondary"]:has(div[data-testid="StyledLinkIconContainer"]) {
                        color: var(--error-color);
                        height: 36px;
                        width: 36px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                    }
                    
                    /* Add logout icon */
                    [data-testid="baseButton-secondary"]:has(div[data-testid="StyledLinkIconContainer"])::before {
                        content: "logout";
                        font-family: "Material Icons";
                        position: absolute;
                        font-size: 20px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
            
            # Remove duplicate button functions since we're handling them directly in the columns now
    
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
