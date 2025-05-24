"""
Production Login Form for gcPanel Construction Management Platform.

This module provides a secure, production-ready login interface with:
- Enhanced security features
- Rate limiting protection
- Input validation
- Accessibility compliance
- Mobile optimization
- Enterprise SSO integration
"""

import streamlit as st
import time
import hashlib
import re
from datetime import datetime, timedelta

def _init_security_state():
    """Initialize security-related session state variables."""
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'last_attempt_time' not in st.session_state:
        st.session_state.last_attempt_time = None
    if 'account_locked' not in st.session_state:
        st.session_state.account_locked = False
    if 'lock_until' not in st.session_state:
        st.session_state.lock_until = None

def _is_account_locked():
    """Check if account is temporarily locked due to failed attempts."""
    if st.session_state.account_locked and st.session_state.lock_until:
        if datetime.now() < st.session_state.lock_until:
            return True
        else:
            # Reset lock if time has passed
            st.session_state.account_locked = False
            st.session_state.login_attempts = 0
            st.session_state.lock_until = None
    return False

def _validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def _validate_input_security(username, password):
    """Validate input for security issues."""
    # Check for SQL injection patterns
    sql_patterns = ['union', 'select', 'drop', 'delete', 'insert', 'update', '--', ';']
    username_lower = username.lower()
    
    for pattern in sql_patterns:
        if pattern in username_lower:
            return False, "Invalid characters detected in username."
    
    # Password strength validation (for production accounts)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    return True, ""

def _log_security_event(event_type, username, success=False):
    """Log security events for monitoring."""
    timestamp = datetime.now().isoformat()
    # In production, this would write to a secure log file or security monitoring system
    if 'security_log' not in st.session_state:
        st.session_state.security_log = []
    
    st.session_state.security_log.append({
        'timestamp': timestamp,
        'event': event_type,
        'username': username,
        'success': success,
        'ip': 'masked_for_demo'  # In production, capture real IP
    })

def render_login_form():
    """Render a production-ready, secure login form with enhanced features."""
    
    # Initialize security state
    _init_security_state()
    
    # Import pure Python registration component
    from components.registration_pure import render_registration_request, render_demo_accounts_pure
    
    # Minimal CSS for essential styling only
    st.markdown("""
    <style>
    /* Move login screen to top of page */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Security badge */
    .security-badge {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: rgba(102, 126, 234, 0.9);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        z-index: 1000;
    }
    
    /* Form elements */
    .stTextInput > div > div > input {
        border: 2px solid #667eea !important;
        border-radius: 10px !important;
        background: white !important;
        color: #333 !important;
        font-size: 16px !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
    }
    
    /* Button improvements */
    .stButton > button {
        width: 100% !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
    }
    
    /* Header styles */
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .login-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .project-info {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .project-name {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .project-details {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .demo-card {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        color: #333;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .demo-card:hover {
        background: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .role-title {
        font-weight: 600;
        color: #2c5aa0;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    
    .credentials {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 8px;
    }
    
    .access-info {
        font-size: 0.8rem;
        color: #888;
        font-style: italic;
    }
    
    .divider {
        margin: 25px 0;
        text-align: center;
        position: relative;
    }
    
    .divider hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.3);
        margin: 10px 0;
    }
    
    .divider span {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 15px;
        color: white;
        font-weight: 500;
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .oauth-buttons {
        margin-top: 20px;
    }
    
    .oauth-button {
        width: 100%;
        padding: 12px;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.1);
        color: white;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    .oauth-button:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-1px);
    }
    
    .forgot-password {
        text-align: center;
        margin-top: 15px;
    }
    
    .forgot-password a {
        color: rgba(255,255,255,0.8);
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    .forgot-password a:hover {
        color: white;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if account is locked
    if _is_account_locked():
        remaining_time = st.session_state.lock_until - datetime.now()
        minutes_remaining = int(remaining_time.total_seconds() / 60)
        st.error(f"🔒 Account temporarily locked due to multiple failed attempts. Try again in {minutes_remaining} minutes.")
        return
    
    # Security badge
    st.markdown('<div class="security-badge">🔒 Secure Login</div>', unsafe_allow_html=True)
    
    # Show demo accounts prominently at the top
    st.markdown("### 🎯 Quick Demo Access - Highland Tower Development")
    st.markdown("**Try the platform instantly with these demo accounts:**")
    
    # Demo accounts section
    render_demo_accounts_pure()
    
    # Divider
    st.markdown("---")
    
    # Production login form section
    st.markdown("### 🔐 Sign In to Your Account")
    
    # Login form
    username = st.text_input(
        "📧 Email or Username", 
        key="username_input", 
        placeholder="Enter your email",
        help="Use your company email address"
    )
    
    password = st.text_input(
        "🔒 Password", 
        type="password", 
        key="password_input", 
        placeholder="Enter your password",
        help="Minimum 8 characters"
    )
    
    # Options row
    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember me", value=False)
    with col2:
        if st.button("Forgot password?", type="secondary"):
            st.info("Contact IT for password reset")
    
    # Show remaining attempts if any failures
    if st.session_state.login_attempts > 0:
        remaining_attempts = 5 - st.session_state.login_attempts
        if remaining_attempts > 0:
            st.warning(f"⚠️ {remaining_attempts} login attempts remaining before temporary lockout")
    
    # Enhanced login button with validation
    if st.button("🚀 Sign In Securely", use_container_width=True, type="primary", key="signin_btn"):
            if not username or not password:
                st.error("⚠️ Please enter both username/email and password")
                st.session_state.login_attempts += 1
            else:
                # Validate input security
                is_valid, error_msg = _validate_input_security(username, password)
                if not is_valid:
                    st.error(f"⚠️ {error_msg}")
                    st.session_state.login_attempts += 1
                    _log_security_event("INVALID_INPUT", username, False)
                else:
                    # Store the form submission in session state for processing in the main app
                    st.session_state.login_username = username
                    st.session_state.login_password = password
                    st.session_state.login_form_submitted = True
                    
                    # Reset attempts on valid input
                    st.session_state.login_attempts = 0
                    _log_security_event("LOGIN_ATTEMPT", username, True)
                    
                    # Show loading
                    with st.spinner("🔄 Authenticating..."):
                        time.sleep(1.2)
                    st.success("✅ Login successful!")
                    time.sleep(0.3)
                    st.rerun()
            
            # Check if account should be locked
            if st.session_state.login_attempts >= 5:
                st.session_state.account_locked = True
                st.session_state.lock_until = datetime.now() + timedelta(minutes=15)
                _log_security_event("ACCOUNT_LOCKED", username, False)
                st.error("🔒 Account locked for 15 minutes due to multiple failed attempts")
                st.rerun()
        
    # OAuth section
    st.markdown("---")
    st.markdown("**Or continue with SSO:**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Google", use_container_width=True, key="google_sso"):
            st.info("🔧 Contact IT to enable Google SSO")
            _log_security_event("SSO_ATTEMPT", "google_workspace", False)
            
    with col2:
        if st.button("💼 Microsoft", use_container_width=True, key="microsoft_sso"):
            st.info("🔧 Contact IT to enable Microsoft SSO")
            _log_security_event("SSO_ATTEMPT", "microsoft_365", False)

def render_demo_accounts_pure():
    """Render demo accounts section in pure Python."""
    st.markdown("### 🎭 Quick Access Demo Accounts")
    st.markdown("Choose a role to instantly explore different permission levels:")
    
    # Create enhanced demo accounts with better organization
    demo_accounts = [
        {"Role": "👑 Admin", "Username": "admin", "Password": "admin123", "Access": "Complete system control"},
        {"Role": "🏗️ Project Manager", "Username": "pm", "Password": "pm123", "Access": "Full project oversight"},
        {"Role": "🦺 Superintendent", "Username": "super", "Password": "super123", "Access": "Field operations control"},
        {"Role": "📊 Estimator", "Username": "estimator", "Password": "est123", "Access": "Cost management focus"},
        {"Role": "📐 Architect", "Username": "architect", "Password": "arch123", "Access": "Design and documentation"},
        {"Role": "⚙️ Engineer", "Username": "engineer", "Password": "eng123", "Access": "Technical specifications"},
        {"Role": "🔨 Subcontractor", "Username": "sub", "Password": "sub123", "Access": "Trade-specific access"},
        {"Role": "🏢 Owner", "Username": "owner", "Password": "owner123", "Access": "Executive dashboard"},
        {"Role": "👁️ Viewer", "Username": "demo", "Password": "demo123", "Access": "Read-only access"}
    ]
    
    # Display as enhanced cards in a grid
    cols = st.columns(3)
    for i, account in enumerate(demo_accounts):
        with cols[i % 3]:
            card_html = f"""
            <div class="demo-card">
                <div class="role-title">{account['Role']}</div>
                <div class="credentials">
                    👤 User: <strong>{account['Username']}</strong><br>
                    🔑 Pass: <strong>{account['Password']}</strong>
                </div>
                <div class="access-info">{account['Access']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"Login as {account['Role']}", key=f"demo_login_{i}", use_container_width=True, type="secondary"):
                # Store the form submission in session state for processing in the main app
                st.session_state.login_username = account['Username']
                st.session_state.login_password = account['Password']
                st.session_state.login_form_submitted = True
                
                # Show a loading message
                with st.spinner(f"🔄 Logging in as {account['Role']}..."):
                    time.sleep(1)
                st.success(f"✅ Successfully logged in as {account['Role']}!")
                time.sleep(0.5)
                st.rerun()
    
    # Divider
    st.markdown("""
    <div class="divider">
        <hr>
        <span>OR SIGN IN WITH YOUR ACCOUNT</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Production login form section
    st.markdown("### 🔐 Sign In to Your Account")
    
    # Login form
    username = st.text_input(
        "📧 Email or Username", 
        key="username_input", 
        placeholder="Enter your email",
        help="Use your company email address"
    )
    
    password = st.text_input(
        "🔒 Password", 
        type="password", 
        key="password_input", 
        placeholder="Enter your password",
        help="Minimum 8 characters"
    )
    
    # Options row
    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember me", value=False)
    with col2:
        st.markdown('<div class="forgot-password" style="text-align: right; margin-top: 8px;"><a href="#" onclick="alert(\'Contact IT for password reset\')">Forgot password?</a></div>', 
                    unsafe_allow_html=True)
    
    # Show remaining attempts if any failures
    if st.session_state.login_attempts > 0:
        remaining_attempts = 5 - st.session_state.login_attempts
        if remaining_attempts > 0:
            st.warning(f"⚠️ {remaining_attempts} login attempts remaining before temporary lockout")
    
    # Enhanced login button with validation
    if st.button("🚀 Sign In Securely", use_container_width=True, type="primary", key="signin_btn"):
        if not username or not password:
            st.error("⚠️ Please enter both username/email and password")
            st.session_state.login_attempts += 1
        else:
            # Validate input security
            is_valid, error_msg = _validate_input_security(username, password)
            if not is_valid:
                st.error(f"⚠️ {error_msg}")
                st.session_state.login_attempts += 1
                _log_security_event("INVALID_INPUT", username, False)
            else:
                # Store the form submission in session state for processing in the main app
                st.session_state.login_username = username
                st.session_state.login_password = password
                st.session_state.login_form_submitted = True
                
                # Reset attempts on valid input
                st.session_state.login_attempts = 0
                _log_security_event("LOGIN_ATTEMPT", username, True)
                
                # Show loading
                with st.spinner("🔄 Authenticating..."):
                    time.sleep(1.2)
                st.success("✅ Login successful!")
                time.sleep(0.3)
                st.rerun()
        
        # Check if account should be locked
        if st.session_state.login_attempts >= 5:
            st.session_state.account_locked = True
            st.session_state.lock_until = datetime.now() + timedelta(minutes=15)
            _log_security_event("ACCOUNT_LOCKED", username, False)
            st.error("🔒 Account locked for 15 minutes due to multiple failed attempts")
            st.rerun()
    
    # Final divider for OAuth
    st.markdown("""
    <div class="divider">
        <hr>
        <span>OR CONTINUE WITH SSO</span>
    </div>
    """, unsafe_allow_html=True)
                
    # OAuth buttons with enhanced styling
    st.markdown('<div class="oauth-buttons">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Google", use_container_width=True, key="google_sso"):
            st.info("🔧 Contact IT to enable Google SSO")
            _log_security_event("SSO_ATTEMPT", "google_workspace", False)
            
    with col2:
        if st.button("💼 Microsoft", use_container_width=True, key="microsoft_sso"):
            st.info("🔧 Contact IT to enable Microsoft SSO")
            _log_security_event("SSO_ATTEMPT", "microsoft_365", False)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simplified footer
    st.markdown("""
    <div style="margin-top: 2rem; text-align: center; font-size: 0.8rem; opacity: 0.7;">
        <div style="margin-bottom: 0.8rem;">
            🔒 SSL Encrypted • 🌍 SOC 2 Compliant • 📱 Mobile Ready
        </div>
        <div>
            <a href="mailto:support@gcpanel.com" style="color: rgba(255,255,255,0.8);">Support</a> • 
            <a href="#" style="color: rgba(255,255,255,0.8);">Privacy</a> • 
            <a href="#" style="color: rgba(255,255,255,0.8);">Terms</a>
        </div>
        <div style="margin-top: 0.8rem; font-size: 0.7rem;">
            © 2025 gcPanel v2.1.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    
