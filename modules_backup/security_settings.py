"""
Security Settings Module - Highland Tower Development
Enterprise-grade security configuration and compliance management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import secrets
import string

def render():
    """Render the comprehensive Security Settings module"""
    st.title("🔐 Security Settings - Highland Tower Development")
    st.markdown("**Enterprise Security Configuration & Compliance Management**")
    
    # Initialize session state for security data
    if 'security_policies' not in st.session_state:
        st.session_state.security_policies = get_security_policies()
    if 'access_logs' not in st.session_state:
        st.session_state.access_logs = get_sample_access_logs()
    if 'security_alerts' not in st.session_state:
        st.session_state.security_alerts = get_security_alerts()
    
    # Security overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Security Score", "98.5%", "+1.2% this month", help="Overall security compliance rating")
    with col2:
        st.metric("Active Sessions", "18", "Current logged-in users")
    with col3:
        st.metric("Failed Logins", "3", "Last 24 hours")
    with col4:
        st.metric("Security Alerts", "2", "Requiring attention")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔒 Access Control", "🛡️ Security Policies", "🔔 Security Alerts", "📊 Compliance", "🔍 Audit Trail", "⚙️ System Security"
    ])
    
    with tab1:
        render_access_control()
    
    with tab2:
        render_security_policies()
    
    with tab3:
        render_security_alerts()
    
    with tab4:
        render_compliance_management()
    
    with tab5:
        render_audit_trail()
    
    with tab6:
        render_system_security()

def render_access_control():
    """Access control and authentication settings"""
    st.subheader("🔒 Access Control & Authentication")
    
    # Authentication settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔐 Authentication Settings")
        
        with st.form("auth_settings"):
            password_policy = st.selectbox("Password Policy", 
                                         ["Standard", "Strong", "Enterprise", "Custom"])
            
            if password_policy == "Custom":
                min_length = st.slider("Minimum Length", 8, 20, 12)
                require_uppercase = st.checkbox("Require Uppercase", value=True)
                require_lowercase = st.checkbox("Require Lowercase", value=True)
                require_numbers = st.checkbox("Require Numbers", value=True)
                require_symbols = st.checkbox("Require Special Characters", value=True)
            
            session_timeout = st.slider("Session Timeout (minutes)", 15, 480, 60)
            max_login_attempts = st.number_input("Max Failed Login Attempts", 3, 10, 5)
            account_lockout_duration = st.slider("Account Lockout Duration (minutes)", 5, 60, 15)
            
            two_factor_auth = st.checkbox("Require Two-Factor Authentication", value=True)
            if two_factor_auth:
                tfa_method = st.selectbox("2FA Method", ["SMS", "Email", "Authenticator App", "All Methods"])
            
            single_sign_on = st.checkbox("Enable Single Sign-On (SSO)", value=False)
            if single_sign_on:
                sso_provider = st.selectbox("SSO Provider", ["Azure AD", "Google Workspace", "Okta", "Custom SAML"])
            
            if st.form_submit_button("💾 Save Authentication Settings"):
                st.success("✅ Authentication settings saved successfully!")
                st.info("🔄 Changes will take effect for new login sessions")
    
    with col2:
        st.markdown("#### 🚪 Access Control Lists")
        
        # IP whitelist management
        st.markdown("**📍 IP Address Whitelist**")
        
        with st.expander("Manage IP Whitelist"):
            new_ip = st.text_input("Add IP Address", placeholder="192.168.1.100")
            ip_description = st.text_input("Description", placeholder="Office network")
            
            if st.button("➕ Add IP Address"):
                if new_ip:
                    st.success(f"✅ Added {new_ip} to whitelist")
            
            # Display current whitelist
            ip_whitelist = [
                {"IP": "192.168.1.0/24", "Description": "Highland Construction Office", "Added": "2025-01-15"},
                {"IP": "10.0.0.0/16", "Description": "Project Site Network", "Added": "2025-02-01"},
                {"IP": "203.45.67.89", "Description": "Remote Engineer VPN", "Added": "2025-03-10"}
            ]
            
            ip_df = pd.DataFrame(ip_whitelist)
            st.dataframe(ip_df, use_container_width=True)
        
        # Device management
        st.markdown("**📱 Device Management**")
        
        device_policy = st.selectbox("Device Access Policy", 
                                   ["Allow All Devices", "Registered Devices Only", "Corporate Devices Only"])
        
        mobile_access = st.checkbox("Allow Mobile Access", value=True)
        offline_access = st.checkbox("Allow Offline Mode", value=True)
        
        if st.button("🔄 Refresh Device List"):
            st.info("📱 Scanning for connected devices...")

def render_security_policies():
    """Security policies and compliance rules"""
    st.subheader("🛡️ Security Policies & Compliance Rules")
    
    # Policy management
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Current Security Policies")
        
        for policy in st.session_state.security_policies:
            status_color = "#28a745" if policy['status'] == 'Active' else "#dc3545"
            
            with st.expander(f"📋 {policy['name']} - {policy['status']}"):
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Category:</strong> {policy['category']}<br>
                <strong>Description:</strong> {policy['description']}<br>
                <strong>Compliance:</strong> {policy['compliance_standard']}<br>
                <strong>Last Updated:</strong> {policy['last_updated']}<br>
                <strong>Next Review:</strong> {policy['next_review']}
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✏️ Edit Policy", key=f"edit_policy_{policy['id']}"):
                        st.session_state.edit_policy_id = policy['id']
                        st.session_state.show_policy_edit = True
                
                with col_b:
                    if policy['status'] == 'Active':
                        if st.button("⏸️ Disable", key=f"disable_policy_{policy['id']}"):
                            st.warning("⏸️ Policy disabled")
                    else:
                        if st.button("▶️ Enable", key=f"enable_policy_{policy['id']}"):
                            st.success("▶️ Policy enabled")
    
    with col2:
        st.markdown("#### ➕ Create New Security Policy")
        
        with st.form("new_policy_form"):
            policy_name = st.text_input("Policy Name *", placeholder="Data Encryption Policy")
            policy_category = st.selectbox("Category *", 
                                         ["Data Protection", "Access Control", "Network Security", 
                                          "Physical Security", "Incident Response", "Compliance"])
            
            compliance_standard = st.selectbox("Compliance Standard", 
                                             ["SOC 2", "ISO 27001", "NIST", "GDPR", "HIPAA", "Custom"])
            
            policy_description = st.text_area("Policy Description *", 
                                            placeholder="Detailed description of the security policy...")
            
            enforcement_level = st.selectbox("Enforcement Level", 
                                           ["Mandatory", "Recommended", "Optional"])
            
            review_frequency = st.selectbox("Review Frequency", 
                                          ["Monthly", "Quarterly", "Semi-Annual", "Annual"])
            
            if st.form_submit_button("📋 Create Policy"):
                if policy_name and policy_category and policy_description:
                    new_policy = {
                        'id': f"POL-HTD-{len(st.session_state.security_policies) + 1:03d}",
                        'name': policy_name,
                        'category': policy_category,
                        'description': policy_description,
                        'compliance_standard': compliance_standard,
                        'enforcement_level': enforcement_level,
                        'status': 'Active',
                        'last_updated': datetime.now().strftime('%Y-%m-%d'),
                        'next_review': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                        'created_by': st.session_state.get('current_user', 'System Admin')
                    }
                    
                    st.session_state.security_policies.append(new_policy)
                    st.success(f"✅ Security policy {new_policy['id']} created successfully!")
                    st.rerun()

def render_security_alerts():
    """Security alerts and threat monitoring"""
    st.subheader("🔔 Security Alerts & Threat Monitoring")
    
    # Alert overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Critical Alerts", "2", "Immediate attention")
    with col2:
        st.metric("High Priority", "5", "This week")
    with col3:
        st.metric("Medium Priority", "12", "Under monitoring")
    with col4:
        st.metric("Resolved Today", "8", "Security team active")
    
    # Current security alerts
    st.markdown("### 🚨 Current Security Alerts")
    
    for alert in st.session_state.security_alerts:
        priority_colors = {
            "Critical": "#dc3545",
            "High": "#fd7e14",
            "Medium": "#ffc107",
            "Low": "#28a745"
        }
        
        priority_color = priority_colors.get(alert['priority'], "#6c757d")
        
        with st.expander(f"🚨 {alert['title']} - {alert['priority']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid {priority_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Type:</strong> {alert['type']}<br>
                <strong>Description:</strong> {alert['description']}<br>
                <strong>Source:</strong> {alert['source']}<br>
                <strong>Detected:</strong> {alert['detected_time']}<br>
                <strong>Impact:</strong> {alert['impact']}<br>
                <strong>Recommended Action:</strong> {alert['recommended_action']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔍 Investigate", key=f"investigate_{alert['id']}"):
                    st.info("🔍 Opening detailed investigation...")
                
                if st.button("✅ Resolve", key=f"resolve_{alert['id']}"):
                    st.success("✅ Alert resolved and documented")
                
                if st.button("📧 Escalate", key=f"escalate_{alert['id']}"):
                    st.warning("📧 Alert escalated to security team")
    
    # Threat monitoring dashboard
    st.markdown("### 📊 Threat Monitoring Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Security events over time
        events_data = pd.DataFrame({
            'Date': pd.date_range('2025-05-01', periods=25),
            'Failed_Logins': [2, 1, 3, 5, 2, 1, 4, 3, 2, 6, 1, 2, 3, 4, 2, 1, 5, 3, 2, 4, 1, 2, 3, 2, 1],
            'Suspicious_Activity': [0, 1, 0, 2, 1, 0, 1, 0, 1, 2, 0, 1, 0, 1, 0, 0, 2, 1, 0, 1, 0, 1, 0, 0, 1]
        })
        
        fig = px.line(events_data, x='Date', y=['Failed_Logins', 'Suspicious_Activity'],
                     title="Security Events Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Alert distribution
        alert_distribution = pd.DataFrame({
            'Priority': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [2, 5, 12, 8]
        })
        
        fig = px.pie(alert_distribution, values='Count', names='Priority',
                    title="Security Alerts by Priority")
        st.plotly_chart(fig, use_container_width=True)

def render_compliance_management():
    """Compliance monitoring and reporting"""
    st.subheader("📊 Compliance Management & Reporting")
    
    # Compliance overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Compliance", "96.8%", "+2.1% this quarter")
    with col2:
        st.metric("SOC 2 Compliance", "98.5%", "Excellent")
    with col3:
        st.metric("ISO 27001", "95.2%", "Good standing")
    with col4:
        st.metric("Industry Standards", "97.1%", "Above average")
    
    # Compliance frameworks
    st.markdown("### 📋 Compliance Frameworks")
    
    compliance_frameworks = [
        {
            "Framework": "SOC 2 Type II",
            "Status": "Compliant",
            "Score": "98.5%",
            "Last_Audit": "2025-03-15",
            "Next_Audit": "2025-09-15",
            "Findings": "2 Minor"
        },
        {
            "Framework": "ISO 27001:2013",
            "Status": "Compliant", 
            "Score": "95.2%",
            "Last_Audit": "2025-02-20",
            "Next_Audit": "2025-08-20",
            "Findings": "3 Minor"
        },
        {
            "Framework": "NIST Cybersecurity Framework",
            "Status": "Compliant",
            "Score": "97.1%",
            "Last_Audit": "2025-04-10",
            "Next_Audit": "2025-10-10", 
            "Findings": "1 Medium"
        },
        {
            "Framework": "Construction Industry Security",
            "Status": "Compliant",
            "Score": "96.8%",
            "Last_Audit": "2025-04-25",
            "Next_Audit": "2025-10-25",
            "Findings": "None"
        }
    ]
    
    compliance_df = pd.DataFrame(compliance_frameworks)
    st.dataframe(compliance_df, use_container_width=True)
    
    # Compliance actions
    st.markdown("### 📝 Compliance Actions Required")
    
    compliance_actions = [
        "Update password policy documentation for SOC 2 compliance",
        "Complete quarterly security awareness training",
        "Review and update incident response procedures",
        "Conduct annual penetration testing",
        "Update vendor security assessments"
    ]
    
    for i, action in enumerate(compliance_actions):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"• {action}")
        with col2:
            if st.button("✅ Complete", key=f"complete_action_{i}"):
                st.success("✅ Action marked as complete")

def render_audit_trail():
    """Security audit trail and logging"""
    st.subheader("🔍 Security Audit Trail")
    
    # Audit controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.selectbox("Date Range", ["Today", "Last 7 Days", "Last 30 Days", "Custom Range"])
    with col2:
        event_type = st.selectbox("Event Type", ["All Events", "Login", "Data Access", "Configuration", "Security"])
    with col3:
        user_filter = st.selectbox("User", ["All Users", "John Smith", "Sarah Chen", "Mike Torres", "System"])
    
    # Audit log display
    st.markdown("### 📋 Security Audit Log")
    
    audit_df = pd.DataFrame(st.session_state.access_logs)
    st.dataframe(audit_df, use_container_width=True)
    
    # Audit analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Audit Statistics")
        st.metric("Total Events", "1,247", "Last 30 days")
        st.metric("Security Events", "89", "7.1% of total")
        st.metric("Failed Access", "23", "1.8% of attempts")
        st.metric("Policy Violations", "5", "All resolved")
    
    with col2:
        # Export options
        st.markdown("#### 📤 Export Options")
        
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("📄 Audit log exported to Excel format")
        
        if st.button("📧 Email Report", use_container_width=True):
            st.success("📧 Audit report emailed to administrators")
        
        if st.button("🔍 Advanced Search", use_container_width=True):
            st.info("🔍 Opening advanced audit search interface")

def render_system_security():
    """System-level security configurations"""
    st.subheader("⚙️ System Security Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛡️ Network Security")
        
        with st.form("network_security"):
            firewall_enabled = st.checkbox("Enable Firewall", value=True)
            intrusion_detection = st.checkbox("Intrusion Detection System", value=True)
            ddos_protection = st.checkbox("DDoS Protection", value=True)
            
            ssl_enforcement = st.checkbox("Enforce SSL/TLS", value=True)
            if ssl_enforcement:
                ssl_version = st.selectbox("Minimum TLS Version", ["TLS 1.2", "TLS 1.3"])
            
            vpn_access = st.checkbox("VPN Required for Remote Access", value=True)
            
            if st.form_submit_button("🔧 Update Network Security"):
                st.success("✅ Network security settings updated!")
        
        st.markdown("#### 🔐 Data Encryption")
        
        with st.form("encryption_settings"):
            data_at_rest = st.checkbox("Encrypt Data at Rest", value=True)
            if data_at_rest:
                encryption_algorithm = st.selectbox("Encryption Algorithm", ["AES-256", "AES-128"])
            
            data_in_transit = st.checkbox("Encrypt Data in Transit", value=True)
            database_encryption = st.checkbox("Database Encryption", value=True)
            backup_encryption = st.checkbox("Encrypted Backups", value=True)
            
            if st.form_submit_button("🔒 Update Encryption Settings"):
                st.success("✅ Encryption settings updated!")
    
    with col2:
        st.markdown("#### 🔄 Backup & Recovery")
        
        with st.form("backup_settings"):
            automated_backups = st.checkbox("Automated Daily Backups", value=True)
            backup_retention = st.slider("Backup Retention (days)", 7, 365, 90)
            
            offsite_backup = st.checkbox("Offsite Backup Storage", value=True)
            backup_encryption = st.checkbox("Encrypt Backup Files", value=True)
            
            recovery_testing = st.selectbox("Recovery Testing Frequency", 
                                          ["Monthly", "Quarterly", "Semi-Annual"])
            
            if st.form_submit_button("💾 Update Backup Settings"):
                st.success("✅ Backup settings updated!")
        
        st.markdown("#### 📊 Security Monitoring")
        
        security_monitoring = pd.DataFrame([
            {"Component": "Firewall", "Status": "Active", "Last_Check": "2025-05-25 14:30"},
            {"Component": "Antivirus", "Status": "Active", "Last_Check": "2025-05-25 14:25"},
            {"Component": "IDS/IPS", "Status": "Active", "Last_Check": "2025-05-25 14:20"},
            {"Component": "SSL Certificate", "Status": "Valid", "Last_Check": "2025-05-25 14:15"},
            {"Component": "Backup System", "Status": "Active", "Last_Check": "2025-05-25 02:00"}
        ])
        
        st.dataframe(security_monitoring, use_container_width=True)
        
        if st.button("🔄 Run Security Scan", use_container_width=True):
            st.info("🔍 Running comprehensive security scan...")

def get_security_policies():
    """Generate sample security policies for Highland Tower Development"""
    return [
        {
            'id': 'POL-HTD-001',
            'name': 'Password Security Policy',
            'category': 'Access Control',
            'description': 'Defines password requirements for all Highland Tower Development users',
            'compliance_standard': 'SOC 2',
            'enforcement_level': 'Mandatory',
            'status': 'Active',
            'last_updated': '2025-03-15',
            'next_review': '2025-06-15'
        },
        {
            'id': 'POL-HTD-002',
            'name': 'Data Classification Policy',
            'category': 'Data Protection',
            'description': 'Classification and handling of sensitive project information',
            'compliance_standard': 'ISO 27001',
            'enforcement_level': 'Mandatory',
            'status': 'Active',
            'last_updated': '2025-02-20',
            'next_review': '2025-08-20'
        },
        {
            'id': 'POL-HTD-003',
            'name': 'Incident Response Policy',
            'category': 'Incident Response',
            'description': 'Procedures for responding to security incidents',
            'compliance_standard': 'NIST',
            'enforcement_level': 'Mandatory',
            'status': 'Active',
            'last_updated': '2025-04-10',
            'next_review': '2025-10-10'
        }
    ]

def get_security_alerts():
    """Generate sample security alerts"""
    return [
        {
            'id': 'ALT-HTD-001',
            'title': 'Multiple failed login attempts detected',
            'type': 'Authentication',
            'priority': 'High',
            'description': 'User account "contractor_temp" has 5 failed login attempts in 10 minutes',
            'source': 'Authentication System',
            'detected_time': '2025-05-25 13:45',
            'impact': 'Potential brute force attack',
            'recommended_action': 'Temporarily lock account and investigate'
        },
        {
            'id': 'ALT-HTD-002',
            'title': 'Unusual data access pattern detected',
            'type': 'Data Access',
            'priority': 'Medium',
            'description': 'User accessed 50+ cost management records outside normal hours',
            'source': 'Data Loss Prevention',
            'detected_time': '2025-05-25 02:30',
            'impact': 'Potential data exfiltration',
            'recommended_action': 'Review access logs and contact user'
        }
    ]

def get_sample_access_logs():
    """Generate sample access logs for Highland Tower Development"""
    return [
        {
            "Timestamp": "2025-05-25 14:32:15",
            "User": "john.smith@highland-construction.com",
            "Event": "Successful Login",
            "IP_Address": "192.168.1.45",
            "Location": "Highland Construction Office",
            "Details": "Chrome browser, Windows 10"
        },
        {
            "Timestamp": "2025-05-25 14:28:03",
            "User": "sarah.chen@elite-mep.com",
            "Event": "Document Access",
            "IP_Address": "192.168.1.67",
            "Location": "Elite MEP Office",
            "Details": "Accessed engineering drawings folder"
        },
        {
            "Timestamp": "2025-05-25 14:15:22",
            "User": "mike.torres@highland-construction.com",
            "Event": "Configuration Change",
            "IP_Address": "192.168.1.23",
            "Location": "Project Site Trailer",
            "Details": "Updated safety reporting settings"
        },
        {
            "Timestamp": "2025-05-25 13:58:41",
            "User": "System",
            "Event": "Automated Backup",
            "IP_Address": "10.0.0.1",
            "Location": "Server Room",
            "Details": "Daily backup completed successfully"
        }
    ]

if __name__ == "__main__":
    render()