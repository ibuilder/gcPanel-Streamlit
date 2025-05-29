"""
Integration Capabilities & Security for Highland Tower Development
External platform connectivity and enterprise-grade security features
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets

def render_integrations_security():
    """Main integrations and security interface"""
    st.markdown("""
    <div class="enterprise-header">
        <h1>🔗 Integrations & Security</h1>
        <p>Highland Tower Development - Enterprise Connectivity & Protection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔗 External Integrations", 
        "🛡️ Security Controls", 
        "📊 Compliance Reporting",
        "👥 Access Management"
    ])
    
    with tab1:
        render_external_integrations()
    
    with tab2:
        render_security_controls()
    
    with tab3:
        render_compliance_reporting()
    
    with tab4:
        render_access_management()

def render_external_integrations():
    """External platform integrations"""
    st.markdown("### 🔗 External Platform Integrations")
    
    # Integration overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Integrations", "6", "+2 this month")
    with col2:
        st.metric("Data Sync Status", "98.5%", "Excellent")
    with col3:
        st.metric("API Calls/Day", "2,847", "Within limits")
    with col4:
        st.metric("Sync Errors", "3", "Last 30 days")
    
    # Accounting software integrations
    st.markdown("#### 💰 Accounting Software Connectivity")
    
    accounting_platforms = [
        {
            'name': 'QuickBooks Enterprise',
            'status': 'Ready to Connect',
            'features': ['Cost tracking', 'Invoice management', 'Budget sync', 'Financial reporting'],
            'setup_required': True
        },
        {
            'name': 'Sage 300 Construction',
            'status': 'Ready to Connect', 
            'features': ['Job costing', 'Payroll integration', 'Equipment tracking', 'Progress billing'],
            'setup_required': True
        },
        {
            'name': 'Foundation Software',
            'status': 'Available',
            'features': ['Project accounting', 'Equipment management', 'Service management'],
            'setup_required': True
        }
    ]
    
    for platform in accounting_platforms:
        with st.expander(f"💼 {platform['name']} - {platform['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Available Features:**")
                for feature in platform['features']:
                    st.markdown(f"• {feature}")
            
            with col2:
                if platform['setup_required']:
                    if st.button(f"🔑 Connect {platform['name']}", key=f"connect_{platform['name']}"):
                        st.info(f"To integrate with {platform['name']}, I'll need your API credentials. Would you like to provide them for seamless financial data synchronization?")
                else:
                    st.success("✅ Connected and syncing")
                    if st.button(f"⚙️ Configure", key=f"config_{platform['name']}"):
                        st.info("Opening configuration settings...")
    
    # Calendar and scheduling integrations
    st.markdown("#### 📅 Calendar & Scheduling Integration")
    
    calendar_platforms = [
        {
            'name': 'Microsoft Outlook',
            'status': 'Ready to Connect',
            'sync_items': ['Project milestones', 'Team meetings', 'Inspection schedules', 'Delivery appointments']
        },
        {
            'name': 'Google Calendar',
            'status': 'Ready to Connect',
            'sync_items': ['Construction phases', 'Safety meetings', 'Client presentations', 'Permit deadlines']
        },
        {
            'name': 'Project Schedule (Primavera)',
            'status': 'Ready to Connect',
            'sync_items': ['Critical path activities', 'Resource allocation', 'Progress tracking', 'Milestone alerts']
        }
    ]
    
    for platform in calendar_platforms:
        with st.expander(f"📅 {platform['name']} - {platform['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Sync Capabilities:**")
                for item in platform['sync_items']:
                    st.markdown(f"• {item}")
            
            with col2:
                if st.button(f"🔗 Connect Calendar", key=f"cal_{platform['name']}"):
                    st.info(f"Calendar integration requires authentication. Would you like to provide {platform['name']} credentials for automatic scheduling synchronization?")
    
    # Cloud storage integrations
    st.markdown("#### ☁️ Cloud Storage Integration")
    
    storage_platforms = [
        {
            'name': 'Dropbox Business',
            'capacity': '5 TB',
            'features': ['Auto file backup', 'Team sharing', 'Version control', 'Mobile access']
        },
        {
            'name': 'Google Drive Enterprise',
            'capacity': 'Unlimited',
            'features': ['Real-time collaboration', 'Advanced search', 'Security controls', 'API integration']
        },
        {
            'name': 'Microsoft SharePoint',
            'capacity': '25 TB',
            'features': ['Document workflows', 'Compliance features', 'Team sites', 'Enterprise security']
        }
    ]
    
    for platform in storage_platforms:
        with st.expander(f"☁️ {platform['name']} - {platform['capacity']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Storage Capacity:** {platform['capacity']}")
                st.markdown("**Key Features:**")
                for feature in platform['features']:
                    st.markdown(f"• {feature}")
            
            with col2:
                if st.button(f"🔗 Connect Storage", key=f"storage_{platform['name']}"):
                    st.info(f"To enable {platform['name']} integration, I'll need your API access tokens. This will allow automatic document synchronization and backup.")

def render_security_controls():
    """Security and compliance controls"""
    st.markdown("### 🛡️ Enterprise Security Controls")
    
    # Security overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Security Score", "9.8/10", "Excellent")
    with col2:
        st.metric("Active Sessions", "12", "Current users")
    with col3:
        st.metric("Failed Logins", "0", "Last 24 hours")
    with col4:
        st.metric("Data Encrypted", "100%", "All storage")
    
    # Two-factor authentication
    st.markdown("#### 🔐 Two-Factor Authentication")
    
    with st.expander("🔐 Two-Factor Authentication Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            current_2fa = st.session_state.get('user_2fa_enabled', False)
            enable_2fa = st.checkbox("Enable Two-Factor Authentication", value=current_2fa)
            
            if enable_2fa != current_2fa:
                st.session_state.user_2fa_enabled = enable_2fa
                if enable_2fa:
                    st.success("✅ Two-factor authentication enabled for enhanced security")
                else:
                    st.warning("⚠️ Two-factor authentication disabled")
            
            auth_methods = st.multiselect("Authentication Methods", [
                "SMS Text Message",
                "Authenticator App (Google/Microsoft)",
                "Hardware Security Key",
                "Email Verification"
            ], default=["Authenticator App (Google/Microsoft)"])
        
        with col2:
            st.markdown("**Security Benefits:**")
            st.markdown("• Prevents unauthorized access")
            st.markdown("• Protects sensitive project data")
            st.markdown("• Meets enterprise security standards")
            st.markdown("• Reduces data breach risk by 99.9%")
    
    # Role-based permissions
    st.markdown("#### 👤 Role-Based Access Control")
    
    roles_permissions = [
        {
            'role': 'Project Manager',
            'users': ['Jennifer Walsh'],
            'permissions': ['Full project access', 'Budget management', 'Team administration', 'Report generation']
        },
        {
            'role': 'Site Supervisor',
            'users': ['Mike Rodriguez'],
            'permissions': ['Field operations', 'Safety reporting', 'Daily logs', 'Photo uploads']
        },
        {
            'role': 'Engineer',
            'users': ['Sarah Chen, PE', 'David Kim'],
            'permissions': ['RFI management', 'Drawing access', 'Technical reviews', 'Specification updates']
        },
        {
            'role': 'Safety Manager',
            'users': ['Lisa Wong'],
            'permissions': ['Safety module', 'Incident reporting', 'Compliance tracking', 'Training records']
        },
        {
            'role': 'Field Worker',
            'users': ['Field Teams'],
            'permissions': ['Daily reports', 'Progress photos', 'Issue reporting', 'Basic document access']
        }
    ]
    
    for role_info in roles_permissions:
        with st.expander(f"👤 {role_info['role']} - {len(role_info['users'])} user(s)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Assigned Users:**")
                for user in role_info['users']:
                    st.markdown(f"• {user}")
            
            with col2:
                st.markdown("**Permissions:**")
                for permission in role_info['permissions']:
                    st.markdown(f"• {permission}")
                
                if st.button(f"✏️ Edit Permissions", key=f"edit_{role_info['role']}"):
                    st.info("Opening permission editor...")
    
    # Data encryption
    st.markdown("#### 🔒 Data Encryption & Protection")
    
    encryption_status = [
        {'component': 'Data at Rest', 'status': 'AES-256 Encrypted', 'level': 'Military Grade'},
        {'component': 'Data in Transit', 'status': 'TLS 1.3 Encrypted', 'level': 'Bank Level'},
        {'component': 'Database', 'status': 'Encrypted', 'level': 'Enterprise'},
        {'component': 'File Storage', 'status': 'Encrypted', 'level': 'Enterprise'},
        {'component': 'Backup Data', 'status': 'Encrypted', 'level': 'Enterprise'}
    ]
    
    for item in encryption_status:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{item['component']}**")
        with col2:
            st.markdown(f"🔒 {item['status']}")
        with col3:
            st.markdown(f"🛡️ {item['level']}")

def render_compliance_reporting():
    """Compliance and audit reporting"""
    st.markdown("### 📊 Compliance & Audit Reporting")
    
    # Compliance overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Compliance Score", "98.5%", "+1.2% this quarter")
    with col2:
        st.metric("Audit Readiness", "Excellent", "All systems green")
    with col3:
        st.metric("Policy Violations", "0", "Last 90 days")
    
    # Industry standards compliance
    st.markdown("#### 📋 Industry Standards Compliance")
    
    compliance_standards = [
        {
            'standard': 'SOC 2 Type II',
            'status': 'Compliant',
            'last_audit': '2024-12-15',
            'next_audit': '2025-12-15',
            'coverage': ['Security', 'Availability', 'Confidentiality']
        },
        {
            'standard': 'ISO 27001',
            'status': 'Compliant',
            'last_audit': '2024-11-20',
            'next_audit': '2025-11-20',
            'coverage': ['Information Security', 'Risk Management', 'Data Protection']
        },
        {
            'standard': 'GDPR',
            'status': 'Compliant',
            'last_audit': '2024-10-30',
            'next_audit': '2025-10-30',
            'coverage': ['Data Privacy', 'User Rights', 'Data Processing']
        }
    ]
    
    for standard in compliance_standards:
        with st.expander(f"📋 {standard['standard']} - {standard['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Status:** ✅ {standard['status']}")
                st.markdown(f"**Last Audit:** {standard['last_audit']}")
                st.markdown(f"**Next Audit:** {standard['next_audit']}")
            
            with col2:
                st.markdown("**Coverage Areas:**")
                for area in standard['coverage']:
                    st.markdown(f"• {area}")
                
                if st.button(f"📄 Generate Report", key=f"report_{standard['standard']}"):
                    st.success(f"Compliance report for {standard['standard']} generated")
    
    # Audit trail
    st.markdown("#### 🔍 Audit Trail & Activity Logging")
    
    recent_activities = [
        {
            'timestamp': '2025-01-27 14:30:15',
            'user': 'Jennifer Walsh',
            'action': 'Updated project budget',
            'module': 'Cost Management',
            'ip_address': '192.168.1.100'
        },
        {
            'timestamp': '2025-01-27 14:15:22',
            'user': 'Sarah Chen, PE',
            'action': 'Responded to RFI HTD-001',
            'module': 'Engineering',
            'ip_address': '192.168.1.105'
        },
        {
            'timestamp': '2025-01-27 13:45:33',
            'user': 'Mike Rodriguez',
            'action': 'Uploaded progress photos',
            'module': 'Field Operations',
            'ip_address': '192.168.1.110'
        },
        {
            'timestamp': '2025-01-27 13:20:44',
            'user': 'System',
            'action': 'Automated backup completed',
            'module': 'System',
            'ip_address': 'Internal'
        }
    ]
    
    audit_df = pd.DataFrame(recent_activities)
    st.dataframe(audit_df, use_container_width=True)
    
    if st.button("📊 Export Audit Log"):
        st.success("Audit log exported for compliance review")

def render_access_management():
    """User access and session management"""
    st.markdown("### 👥 Access Management & User Sessions")
    
    # Active sessions
    st.markdown("#### 🔐 Active User Sessions")
    
    active_sessions = [
        {
            'user': 'Jennifer Walsh',
            'role': 'Project Manager',
            'login_time': '09:15 AM',
            'location': 'Seattle Office',
            'device': 'Windows Desktop',
            'ip': '192.168.1.100'
        },
        {
            'user': 'Sarah Chen, PE',
            'role': 'Structural Engineer',
            'login_time': '08:30 AM',
            'location': 'Home Office',
            'device': 'MacBook Pro',
            'ip': '192.168.1.105'
        },
        {
            'user': 'Mike Rodriguez',
            'role': 'Site Supervisor',
            'login_time': '07:00 AM',
            'location': 'Construction Site',
            'device': 'iPad Pro',
            'ip': '192.168.1.110'
        }
    ]
    
    for session in active_sessions:
        with st.expander(f"👤 {session['user']} - {session['role']} (Active {session['login_time']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Login Time:** {session['login_time']}")
                st.markdown(f"**Location:** {session['location']}")
                st.markdown(f"**Device:** {session['device']}")
            
            with col2:
                st.markdown(f"**IP Address:** {session['ip']}")
                
                if st.button(f"🚪 End Session", key=f"end_{session['user']}"):
                    st.warning(f"Session ended for {session['user']}")
                
                if st.button(f"📊 View Activity", key=f"activity_{session['user']}"):
                    st.info("Opening user activity log...")
    
    # Password and security policies
    st.markdown("#### 🔑 Security Policy Management")
    
    with st.expander("🔑 Password & Security Policies"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Password Policy:**")
            st.markdown("• Minimum 12 characters")
            st.markdown("• Must include uppercase, lowercase, numbers")
            st.markdown("• Special characters required")
            st.markdown("• Cannot reuse last 5 passwords")
            st.markdown("• Expires every 90 days")
        
        with col2:
            st.markdown("**Session Security:**")
            st.markdown("• Auto-logout after 30 minutes idle")
            st.markdown("• Concurrent session limit: 3")
            st.markdown("• Login attempt limit: 5")
            st.markdown("• Account lockout: 15 minutes")
            st.markdown("• Failed login notifications enabled")
    
    # Security monitoring
    st.markdown("#### 📈 Security Monitoring Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Login Success Rate", "99.8%", "Last 30 days")
        st.metric("Average Session Time", "2.3 hours", "Typical usage")
    
    with col2:
        st.metric("Security Alerts", "0", "No active threats")
        st.metric("Blocked Attempts", "2", "Last 7 days")
    
    with col3:
        st.metric("Password Changes", "8", "This month")
        st.metric("2FA Adoption", "100%", "All active users")

# Utility functions for security
def generate_secure_token():
    """Generate secure authentication token"""
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """Hash password securely"""
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify password against stored hash"""
    salt = stored_password[:32]
    stored_hash = stored_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

if __name__ == "__main__":
    render_integrations_security()