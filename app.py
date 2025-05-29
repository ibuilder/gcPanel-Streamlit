"""
gcPanel - Construction Management Platform
Highland Tower Development - $45.5M Mixed-Use Development

Main application entry point with authentication and navigation
"""

import streamlit as st
import hashlib
from datetime import datetime
from utils.helpers import initialize_session_state, check_authentication

# Configure page
st.set_page_config(
    page_title="gcPanel - Construction Management",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import authentication modules
try:
    from database.connection import authenticate_user, update_user_login
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

def hash_password(password: str) -> str:
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user_app(username: str, password: str) -> bool:
    """Authenticate user with credentials - integrated database and fallback"""
    # Try database authentication first
    if DATABASE_AVAILABLE:
        try:
            password_hash = hash_password(password)
            user = authenticate_user(username, password_hash)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = user.get('role', 'user').title()
                st.session_state.user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
                st.session_state.login_time = datetime.now()
                st.session_state.user_id = user['id']
                update_user_login(user['id'])
                return True
        except Exception as e:
            print(f"Database authentication failed: {e}")
    
    # Fallback authentication for demo
    valid_users = {
        "admin": "highland2025",
        "manager": "manager123", 
        "engineer": "engineer123"
    }
    
    user_roles = {
        "admin": {"role": "Administrator", "name": "System Administrator"},
        "manager": {"role": "Project Manager", "name": "Project Manager"},
        "engineer": {"role": "Engineer", "name": "Site Engineer"}
    }
    
    if username in valid_users and valid_users[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = user_roles[username]["role"]
        st.session_state.user_name = user_roles[username]["name"]
        st.session_state.login_time = datetime.now()
        st.session_state.user_id = 1  # Default user ID for fallback
        return True
    return False

def logout():
    """Log out the current user"""
    for key in ['authenticated', 'username', 'user_role', 'user_name', 'login_time', 'user_id']:
        if key in st.session_state:
            del st.session_state[key]

def render_login_page():
    """Render the login page"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .login-title {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .login-subtitle {
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">🏗️ gcPanel</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Highland Tower Development<br>Construction Management Platform</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔐 Password", type="password", placeholder="Enter your password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
            with col_login2:
                demo_info = st.form_submit_button("ℹ️ Demo Info", use_container_width=True)
            
            if login_button:
                if authenticate_user_app(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            
            if demo_info:
                st.info("""
                **Demo Credentials:**
                - Username: admin, Password: highland2025
                - Username: manager, Password: manager123
                - Username: engineer, Password: engineer123
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Check authentication
    if not check_authentication():
        render_login_page()
        return
    
    # Authenticated user interface
    st.title("🏗️ gcPanel - Construction Management")
    st.markdown(f"Welcome back, **{st.session_state.get('user_name', 'User')}** ({st.session_state.get('user_role', 'User')})")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        
        if st.button("🏠 Dashboard"):
            st.switch_page("pages/01_📊_Dashboard.py")
        
        if st.button("📋 Daily Reports"):
            st.switch_page("pages/02_📋_Daily_Reports.py")
        
        if st.button("📄 RFIs"):
            st.switch_page("pages/03_📄_RFIs.py")
        
        if st.button("📨 Submittals"):
            st.switch_page("pages/04_📨_Submittals.py")
        
        if st.button("📑 Contracts"):
            st.switch_page("pages/05_📑_Contracts.py")
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
    
    # Main content area
    st.markdown("### Select a module from the sidebar to get started")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Progress", "78.5%", "2.3%")
    
    with col2:
        st.metric("Active RFIs", "12", "-3")
    
    with col3:
        st.metric("Budget Status", "$35.2M", "Under")
    
    with col4:
        st.metric("Schedule", "On Track", "1 day ahead")

if __name__ == "__main__":
    main()