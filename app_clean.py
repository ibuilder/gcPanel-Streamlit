"""
Highland Tower Development - Clean Sidebar Layout

Stable version using Streamlit's default sidebar components.
Eliminates customization conflicts for better reliability.
"""

import streamlit as st
from login_form import render_login_form
import modules

def initialize_session_state():
    """Initialize session state with default values."""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "guest",
        "current_menu": "Dashboard",
        "current_project": "Highland Tower Development",
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_sidebar():
    """Render clean sidebar with project info and navigation."""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏗️</div>
            <h2 style='color: #3498db; margin: 0; font-weight: bold;'>gcPanel</h2>
            <p style='color: #95a5a6; font-size: 0.9em; margin: 5px 0;'>Construction Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Project Information
        st.markdown("### Highland Tower Development")
        st.markdown("""
        **Project Value:** $45.5M  
        **Type:** Mixed-Use Development  
        **Units:** 120 Residential + 8 Retail  
        **Size:** 168,500 sq ft  
        **Floors:** 15 Above + 2 Below Ground
        """)
        
        st.divider()
        
        # User Information
        current_user = st.session_state.get("username", "Project Manager")
        user_role = st.session_state.get("user_role", "admin")
        
        st.markdown(f"""
        **User:** {current_user}  
        **Role:** {user_role.title()}
        """)
        
        st.divider()
        
        # Navigation Menu
        st.markdown("### Navigation")
        
        navigation_options = [
            "Dashboard", "Preconstruction", "Engineering", "Field Operations", 
            "Safety", "Contracts", "Cost Management", "BIM", "Closeout", 
            "Analytics", "Documents"
        ]
        
        current_menu = st.selectbox(
            "Select Module:",
            navigation_options,
            index=navigation_options.index(st.session_state.get("current_menu", "Dashboard")),
            key="navigation_select"
        )
        
        # Update session state with selected menu
        st.session_state["current_menu"] = current_menu
        
        st.divider()
        
        # Quick Actions
        st.markdown("### Quick Actions")
        if st.button("📊 Analytics", use_container_width=True, key="quick_analytics"):
            st.session_state["current_menu"] = "Analytics"
            st.rerun()
        
        if st.button("📋 Safety", use_container_width=True, key="quick_safety"):
            st.session_state["current_menu"] = "Safety"
            st.rerun()
        
        if st.button("💰 Budget", use_container_width=True, key="quick_budget"):
            st.session_state["current_menu"] = "Cost Management"
            st.rerun()

def render_main_content():
    """Render the main content area based on selected module."""
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Module mapping with error handling
    try:
        if current_menu == "Dashboard":
            modules.dashboard.render_dashboard()
        elif current_menu == "Analytics":
            modules.analytics.render_analytics_dashboard()
        elif current_menu == "Preconstruction":
            modules.preconstruction.render()
        elif current_menu == "Engineering":
            modules.engineering.render_engineering()
        elif current_menu == "Field Operations":
            modules.field_operations.render()
        elif current_menu == "Safety":
            modules.safety.render()
        elif current_menu == "Contracts":
            modules.contracts.render()
        elif current_menu == "Cost Management":
            modules.cost_management.render()
        elif current_menu == "BIM":
            modules.bim.render()
        elif current_menu == "Closeout":
            modules.closeout.render()
        elif current_menu == "Documents":
            modules.documents.render()
        else:
            st.info(f"Loading {current_menu} module...")
            st.write("Module content will be displayed here.")
            
    except Exception as e:
        st.error(f"Error loading {current_menu} module")
        st.info("Please try selecting a different module or refresh the page.")
        st.write(f"Technical details: {str(e)}")

def main():
    """Main application entry point with clean sidebar layout."""
    # Set page configuration
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply clean dark theme
    st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        
        /* Clean sidebar styling */
        .css-1d391kg {
            background-color: #2d3e50;
        }
        
        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #2980b9;
        }
        
        /* Metrics styling */
        [data-testid="metric-container"] {
            background-color: #2d3e50;
            border: 1px solid #34495e;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Form elements */
        .stSelectbox > div > div {
            background-color: #34495e;
            color: white;
            border: 1px solid #3498db;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Check authentication
    if not st.session_state.get("authenticated", False):
        render_login_form()
        return
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render main content
    render_main_content()

if __name__ == "__main__":
    main()