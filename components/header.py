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
            # Set up three columns for the header
            logo_col, spacer_col, controls_col = st.columns([3, 5, 2])
            
            with logo_col:
                # Display project logo and name
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 10px 0;">
                    <span class="material-icons" style="margin-right: 10px; font-size: 24px;">{project_icon}</span>
                    <h2 style="font-size: 20px; font-weight: 600; margin: 0;">{project_name}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            with controls_col:
                # User controls (theme toggle and user info)
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 16px; padding: 10px 0;">
                    <div style="cursor: pointer; display: flex; align-items: center; background: rgba(255, 255, 255, 0.1); 
                              border-radius: 20px; padding: 4px 10px; font-size: 13px;" id="theme-toggle">
                        <span class="material-icons" style="font-size: 16px; margin-right: 5px;">{theme_icon}</span>
                        {theme_text}
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 8px; padding: 4px 10px; 
                              background: rgba(0, 0, 0, 0.2); border-radius: 20px;">
                        <span class="material-icons" style="font-size: 18px;">account_circle</span>
                        <span style="font-size: 14px; font-weight: 500;">{username}</span>
                    </div>
                    
                    <div style="cursor: pointer; color: #f44336; padding: 3px; font-size: 20px; border-radius: 50%; 
                              display: flex; align-items: center; justify-content: center;" id="logout-btn">
                        <span class="material-icons">logout</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Hidden buttons for actual functionality
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("", key="theme_toggle_btn", help="Switch between dark and light theme"):
                    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                    st.rerun()
            with col2:
                if st.button("", key="logout_btn", help="Log out from your account"):
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
