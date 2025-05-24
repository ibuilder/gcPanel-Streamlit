"""
Highland Tower Development - gcPanel Construction Management
Clean, working navigation with all your sophisticated modules properly connected
"""

import streamlit as st
import sys
import os

# Add current directory to Python path for module imports
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

def initialize_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_menu" not in st.session_state:
        st.session_state.current_menu = "Dashboard"
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_role" not in st.session_state:
        st.session_state.user_role = ""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

def render_login():
    """Render simple login form"""
    st.markdown("# 🏗️ Highland Tower Development")
    st.markdown("### gcPanel Construction Management")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Login")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Login", use_container_width=True, type="primary"):
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = "admin"
                    st.rerun()
                else:
                    st.error("Please enter username and password")
        
        with col_btn2:
            if st.button("Demo Login", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = "demo_user"
                st.session_state.user_role = "manager"
                st.rerun()

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        # Project header
        st.markdown("# 🏗️ Highland Tower")
        st.markdown("**Development Project**")
        st.markdown("$45.5M Mixed-Use Development")
        st.markdown("---")
        
        # User info
        st.markdown(f"**User:** {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.user_role}")
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### Navigation")
        
        menu_items = [
            "Dashboard",
            "Preconstruction", 
            "Engineering",
            "Field Operations",
            "Safety",
            "Contracts",
            "Cost Management",
            "BIM",
            "Closeout",
            "Analytics",
            "Documents",
            "RFIs",
            "Daily Reports",
            "Submittals",
            "Transmittals",
            "Scheduling",
            "Settings",
            "AI Assistant",
            "Mobile Companion"
        ]
        
        for item in menu_items:
            if st.button(item, use_container_width=True, key=f"nav_{item}"):
                st.session_state.current_menu = item
                st.rerun()
        
        st.markdown("---")
        
        # Theme toggle
        if st.button("🌙 Toggle Theme", use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_menu = "Dashboard"
            st.rerun()

def load_module_safely(module_name):
    """Load module safely with error handling"""
    try:
        if module_name == "Cost Management":
            import modules.cost_management as module
            module.render()
            return True
        elif module_name == "Contracts":
            import modules.contracts as module
            module.render()
            return True
        elif module_name == "Engineering":
            import modules.engineering as module
            module.render()
            return True
        elif module_name == "Field Operations":
            import modules.field_operations as module
            module.render()
            return True
        elif module_name == "Safety":
            import modules.safety as module
            module.render()
            return True
        elif module_name == "BIM":
            try:
                import modules.bim as module
                module.render()
                return True
            except ImportError:
                import modules.bim_viewer.basic_viewer as module
                module.render()
                return True
        elif module_name == "Analytics":
            import modules.analytics as module
            module.render()
            return True
        elif module_name == "Documents":
            try:
                import modules.documents as module
                module.render()
                return True
            except ImportError:
                import modules.pdf_viewer.pdf_viewer as module
                module.render()
                return True
        elif module_name == "Closeout":
            import modules.closeout as module
            module.render()
            return True
        elif module_name == "Preconstruction":
            import modules.preconstruction as module
            module.render()
            return True
        elif module_name == "Settings":
            import modules.settings as module
            module.render()
            return True
        elif module_name == "AI Assistant":
            import modules.ai_assistant as module
            module.render()
            return True
        elif module_name == "Mobile Companion":
            import modules.mobile_companion as module
            module.render()
            return True
        elif module_name == "RFIs":
            import modules.rfis as module
            module.render()
            return True
        elif module_name == "Daily Reports":
            import modules.daily_reports as module
            module.render()
            return True
        elif module_name == "Submittals":
            import modules.submittals as module
            module.render()
            return True
        elif module_name == "Transmittals":
            import modules.transmittals as module
            module.render()
            return True
        elif module_name == "Scheduling":
            import modules.scheduling as module
            module.render()
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error loading {module_name}: {str(e)}")
        st.info("This module is being connected to your sophisticated functionality.")
        return False

def render_dashboard():
    """Render main dashboard"""
    st.title("📊 Highland Tower Development Dashboard")
    
    # Project metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Progress", "42%", "↗️ +5%")
    with col2:
        st.metric("Budget Status", "$18.2M", "↗️ +$2.1M")
    with col3:
        st.metric("Safety Score", "98%", "↗️ +2%")
    with col4:
        st.metric("Schedule", "On Track", "✅")
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Activity")
        st.write("• Foundation pour completed - Level B2")
        st.write("• Steel delivery scheduled for next week")
        st.write("• MEP rough-in started - Level 1")
        st.write("• Safety inspection passed")
        st.write("• Change order CO-003 approved")
    
    with col2:
        st.subheader("⚠️ Action Items")
        st.write("• Review RFI-001 response needed")
        st.write("• Approve structural steel submittals")
        st.write("• Schedule concrete pump for Level 1")
        st.write("• Update progress photos")
        st.write("• Weekly safety meeting - Friday")

def render_main_content():
    """Render main content based on selected menu"""
    current_menu = st.session_state.current_menu
    
    if current_menu == "Dashboard":
        render_dashboard()
    else:
        # Try to load the specific module
        if not load_module_safely(current_menu):
            # Fallback content
            st.title(f"🔧 {current_menu}")
            st.info(f"The {current_menu} module is being connected...")
            st.write("This module contains your advanced construction management features with CRUD functionality, digital signatures, and sophisticated tools.")

def apply_theme():
    """Apply consistent Highland Tower branding for both light and dark themes"""
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stSidebar {
            background-color: #262730;
            border-right: 2px solid #FF6B35;
        }
        .stButton > button {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #E55A2B;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        }
        .stMetric {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #FF6B35;
        }
        h1, h2, h3 {
            color: #FF6B35;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #1E1E1E;
        }
        .stSidebar {
            background-color: #F8F9FA;
            border-right: 2px solid #FF6B35;
        }
        .stButton > button {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #E55A2B;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        }
        .stMetric {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #FF6B35;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #FF6B35;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stSidebar .stMarkdown {
            color: #1E1E1E;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    apply_theme()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        render_sidebar()
        render_main_content()

if __name__ == "__main__":
    main()