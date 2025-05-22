"""
Login form component for gcPanel.

This module provides a comprehensive login form that supports multiple user roles
with different permission levels for testing the application.
"""

import streamlit as st
import time

def render_login_form():
    """Render a modern, professional login form with enhanced UI."""
    
    # Apply custom CSS for better login page styling
    st.markdown("""
    <style>
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        color: white;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
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
    
    # Main login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
    <div class="login-header">
        <div class="login-title">gcPanel</div>
        <div class="login-subtitle">Construction Management Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Project information
    st.markdown("""
    <div class="project-info">
        <div class="project-name">Highland Tower Development</div>
        <div class="project-details">$45.5M Mixed-Use Project • 120 Residential + 8 Retail Units</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Multi-tab interface with demo accounts first
    demo_tab, login_tab = st.tabs(["🎯 Demo Accounts", "🔐 User Login"])
    
    with login_tab:
        st.markdown("### Sign In to Your Account")
        
        # Standard login form
        username = st.text_input("📧 Email or Username", key="username_input", placeholder="Enter your email or username")
        password = st.text_input("🔒 Password", type="password", key="password_input", placeholder="Enter your password")
        
        # Remember me checkbox
        col1, col2 = st.columns([1, 1])
        with col1:
            remember = st.checkbox("Remember me", value=False)
        
        # Login button
        if st.button("🚀 Sign In", use_container_width=True, type="primary", key="signin_btn"):
            if not username or not password:
                st.error("⚠️ Please enter both username/email and password")
            else:
                # Store the form submission in session state for processing in the main app
                st.session_state.login_username = username
                st.session_state.login_password = password
                st.session_state.login_form_submitted = True
                
                # Show a loading message
                with st.spinner("🔄 Authenticating..."):
                    time.sleep(1)
                st.success("✅ Authentication successful! Redirecting...")
                time.sleep(0.5)
                st.rerun()
        
        # Display "forgot password" link
        st.markdown('<div class="forgot-password"><a href="#">Forgot your password?</a></div>', 
                    unsafe_allow_html=True)
    
    with demo_tab:
        st.markdown("### 🎭 Demo Account Options")
        st.markdown("Choose a role to explore different permission levels and features:")
        
        # Create enhanced demo accounts with better organization
        demo_accounts = [
            {"Role": "👑 Admin", "Username": "admin", "Password": "admin123", "Access": "Complete system control", "Icon": "👑", "Color": "#e74c3c"},
            {"Role": "🏗️ Project Manager", "Username": "pm", "Password": "pm123", "Access": "Full project oversight", "Icon": "🏗️", "Color": "#3498db"},
            {"Role": "🦺 Superintendent", "Username": "super", "Password": "super123", "Access": "Field operations control", "Icon": "🦺", "Color": "#f39c12"},
            {"Role": "📊 Estimator", "Username": "estimator", "Password": "est123", "Access": "Cost management focus", "Icon": "📊", "Color": "#27ae60"},
            {"Role": "📐 Architect", "Username": "architect", "Password": "arch123", "Access": "Design and documentation", "Icon": "📐", "Color": "#9b59b6"},
            {"Role": "⚙️ Engineer", "Username": "engineer", "Password": "eng123", "Access": "Technical specifications", "Icon": "⚙️", "Color": "#34495e"},
            {"Role": "🔨 Subcontractor", "Username": "sub", "Password": "sub123", "Access": "Trade-specific access", "Icon": "🔨", "Color": "#e67e22"},
            {"Role": "🏢 Owner", "Username": "owner", "Password": "owner123", "Access": "Executive dashboard", "Icon": "🏢", "Color": "#2c3e50"},
            {"Role": "👁️ Viewer", "Username": "demo", "Password": "demo123", "Access": "Read-only access", "Icon": "👁️", "Color": "#7f8c8d"}
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
        <span>OR CONTINUE WITH</span>
    </div>
    """, unsafe_allow_html=True)
                
    # OAuth buttons with enhanced styling
    st.markdown('<div class="oauth-buttons">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Google SSO", use_container_width=True, key="google_sso"):
            st.info("🚧 Google SSO integration coming soon")
            
    with col2:
        if st.button("💼 Microsoft 365", use_container_width=True, key="microsoft_sso"):
            st.info("🚧 Microsoft 365 integration coming soon")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer information
    st.markdown("""
    <div style="margin-top: 30px; text-align: center; font-size: 0.8rem; opacity: 0.7;">
        <div style="margin-bottom: 10px;">
            🔒 Secure • 🌍 Enterprise-Grade • 📱 Mobile-Ready
        </div>
        <div>
            Need help? Contact <a href="mailto:support@gcpanel.com" style="color: rgba(255,255,255,0.8);">support@gcpanel.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)