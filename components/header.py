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
    
    # Clean, modern header with proper alignment
    with st.container():
        # Use 3 columns for better layout
        col1, col2, col3 = st.columns([3, 5, 2])
        
        with col1:
            # Clean title with project name if selected
            if 'current_project' in st.session_state:
                st.markdown(f"""
                <div style="margin-top: 10px;">
                    <h2 style="font-size: 18px; font-weight: 500; margin: 0;">
                        <span class="material-icons" style="font-size: 18px; vertical-align: bottom; margin-right: 5px;">domain</span>
                        {st.session_state.current_project}
                    </h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="margin-top: 10px;">
                    <h2 style="font-size: 18px; font-weight: 500; margin: 0;">
                        <span class="material-icons" style="font-size: 18px; vertical-align: bottom; margin-right: 5px;">dashboard</span>
                        gcPanel Dashboard
                    </h2>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Optional space for search or notifications in the future
            pass
            
        with col3:
            # User info and logout - compact design
            if st.session_state.authenticated:
                # Style for the header area
                st.markdown("""
                <style>
                /* Compact user area */
                .user-area {
                    display: flex;
                    justify-content: flex-end;
                    align-items: center;
                    gap: 15px;
                    padding: 5px 0;
                }
                
                /* Theme toggle button */
                .theme-toggle {
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    background: rgba(0,0,0,0.1);
                    border-radius: 20px;
                    padding: 2px 8px;
                    font-size: 12px;
                }
                
                /* User info */
                .user-info {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }
                
                /* Logout button */
                #logout-btn {
                    cursor: pointer;
                    color: #f44336;
                    padding: 2px 5px;
                    font-size: 18px;
                    border-radius: 50%;
                    transition: background-color 0.3s;
                }
                
                #logout-btn:hover {
                    background-color: rgba(244, 67, 54, 0.1);
                }
                </style>
                
                <div class="user-area">
                    <div class="theme-toggle" id="theme-toggle" title="Toggle light/dark theme">
                        <span class="material-icons" style="font-size: 14px; margin-right: 3px;">
                            {("dark_mode" if st.session_state.theme == 'light' else "light_mode")}
                        </span>
                        {("Light" if st.session_state.theme == 'dark' else "Dark")}
                    </div>
                    
                    <div class="user-info">
                        <span class="material-icons" style="font-size: 18px;">account_circle</span>
                        <span style="font-size: 14px; font-weight: 500;">{st.session_state.username}</span>
                    </div>
                    
                    <span class="material-icons" id="logout-btn" title="Logout">logout</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden buttons for actions
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    if st.button("", key="theme_toggle_btn", help="Switch between dark and light theme"):
                        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                        st.rerun()
                with col_b:
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
