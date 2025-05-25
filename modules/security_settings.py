"""
Security Settings Module for gcPanel Highland Tower Development
Enterprise-grade security configuration and monitoring
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib

def render():
    """Render the Security Settings admin module"""
    
    st.markdown("""
    <div class="admin-header">
        <h1>🔐 Security Settings</h1>
        <p>Highland Tower Development - Security Configuration & Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Security tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Security Overview", "🔑 Authentication", "📋 Access Logs", "⚙️ Policies"])
    
    with tab1:
        st.markdown("### Security Status Dashboard")
        
        # Security metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="admin-metric">
                <h3>98%</h3>
                <p>Security Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="admin-metric">
                <h3>127</h3>
                <p>Days Secure</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="admin-metric">
                <h3>0</h3>
                <p>Active Threats</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="admin-metric">
                <h3>15</h3>
                <p>Active Sessions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent security events
        st.markdown("### Recent Security Events")
        
        security_events = {
            'Time': ['2 hours ago', '5 hours ago', '1 day ago', '2 days ago', '3 days ago'],
            'Event Type': ['Login Success', 'Password Change', 'Login Success', 'Failed Login', 'Role Change'],
            'User': ['Sarah Chen, PE', 'Mike Rodriguez', 'Jennifer Walsh', 'Unknown User', 'David Kim'],
            'IP Address': ['192.168.1.45', '192.168.1.67', '192.168.1.23', '203.0.113.45', '192.168.1.89'],
            'Risk Level': ['Low', 'Low', 'Low', 'Medium', 'Low'],
            'Action Taken': ['Logged', 'Logged', 'Logged', 'IP Blocked', 'Logged']
        }
        
        df_security = pd.DataFrame(security_events)
        st.dataframe(df_security, use_container_width=True)
        
        # Security alerts
        st.markdown("### Active Security Alerts")
        
        with st.expander("⚠️ Medium Priority: Unusual Login Pattern", expanded=True):
            st.warning("Multiple failed login attempts detected from IP 203.0.113.45")
            st.markdown("**Recommended Action:** IP has been temporarily blocked. Monitor for 24 hours.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔒 Permanent Block"):
                    st.success("IP 203.0.113.45 permanently blocked")
            with col2:
                if st.button("✅ Mark Resolved"):
                    st.success("Alert marked as resolved")
        
        with st.expander("ℹ️ Low Priority: Password Policy Update"):
            st.info("Recommend updating password policy to require 2FA for all admin accounts")
            if st.button("📋 Review Policy"):
                st.success("Redirecting to password policy settings...")
    
    with tab2:
        st.markdown("### Authentication Configuration")
        
        # Password policy
        st.markdown("#### Password Policy")
        with st.form("password_policy"):
            col1, col2 = st.columns(2)
            
            with col1:
                min_length = st.number_input("Minimum Length", min_value=8, max_value=32, value=12)
                require_uppercase = st.checkbox("Require Uppercase", value=True)
                require_lowercase = st.checkbox("Require Lowercase", value=True)
                require_numbers = st.checkbox("Require Numbers", value=True)
            
            with col2:
                require_symbols = st.checkbox("Require Special Characters", value=True)
                password_expiry = st.number_input("Password Expiry (days)", min_value=30, max_value=365, value=90)
                max_login_attempts = st.number_input("Max Failed Attempts", min_value=3, max_value=10, value=5)
                lockout_duration = st.number_input("Lockout Duration (minutes)", min_value=5, max_value=60, value=15)
            
            if st.form_submit_button("Update Password Policy"):
                st.success("✅ Password policy updated successfully!")
        
        # Two-factor authentication
        st.markdown("#### Two-Factor Authentication")
        col1, col2 = st.columns(2)
        
        with col1:
            enforce_2fa = st.selectbox("2FA Requirement", [
                "Optional for all users",
                "Required for admin users only", 
                "Required for all users",
                "Required for admin and managers"
            ], index=1)
            
            if st.button("Update 2FA Policy"):
                st.success(f"✅ 2FA policy updated: {enforce_2fa}")
        
        with col2:
            st.markdown("**Current 2FA Status:**")
            st.markdown("• Admin users: 1/1 enabled")
            st.markdown("• Manager users: 2/2 enabled") 
            st.markdown("• Standard users: 8/14 enabled")
            st.markdown("• Overall coverage: **79%**")
        
        # Session management
        st.markdown("#### Session Management")
        with st.form("session_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                session_timeout = st.number_input("Session Timeout (hours)", min_value=1, max_value=24, value=8)
                idle_timeout = st.number_input("Idle Timeout (minutes)", min_value=15, max_value=120, value=30)
            
            with col2:
                concurrent_sessions = st.number_input("Max Concurrent Sessions", min_value=1, max_value=5, value=2)
                force_https = st.checkbox("Force HTTPS", value=True)
            
            if st.form_submit_button("Update Session Settings"):
                st.success("✅ Session settings updated!")
    
    with tab3:
        st.markdown("### Access Logs & Audit Trail")
        
        # Log filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            log_date = st.date_input("Date", datetime.now().date())
        with col2:
            log_user = st.selectbox("User", ["All Users", "Jennifer Walsh", "Sarah Chen", "Mike Rodriguez", "David Kim"])
        with col3:
            log_action = st.selectbox("Action", ["All Actions", "Login", "Logout", "Create", "Update", "Delete", "View"])
        with col4:
            log_module = st.selectbox("Module", ["All Modules", "Dashboard", "Engineering", "Safety", "Cost Management"])
        
        # Access log data
        access_logs = {
            'Timestamp': ['2025-01-27 14:30:15', '2025-01-27 14:25:33', '2025-01-27 14:20:12', '2025-01-27 14:15:45', '2025-01-27 14:10:22'],
            'User': ['Sarah Chen, PE', 'Mike Rodriguez', 'Jennifer Walsh', 'David Kim', 'Lisa Wong'],
            'Action': ['UPDATE', 'CREATE', 'VIEW', 'LOGIN', 'DELETE'],
            'Module': ['Engineering', 'Field Operations', 'Dashboard', 'System', 'Safety'],
            'Resource': ['RFI-2025-045', 'Daily Report', 'Project Metrics', 'User Session', 'Safety Photo'],
            'IP Address': ['192.168.1.45', '192.168.1.67', '192.168.1.23', '192.168.1.89', '192.168.1.34'],
            'Status': ['Success', 'Success', 'Success', 'Success', 'Success'],
            'Details': ['Updated RFI status', 'Created daily report', 'Viewed dashboard', 'User login', 'Deleted old photo']
        }
        
        df_logs = pd.DataFrame(access_logs)
        st.dataframe(df_logs, use_container_width=True)
        
        # Export logs
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Export to Excel"):
                st.success("Access logs exported to Excel file")
        with col2:
            if st.button("📄 Generate Report"):
                st.success("Security audit report generated")
        with col3:
            if st.button("📧 Email Report"):
                st.success("Security report emailed to administrators")
        
        # Real-time monitoring
        st.markdown("### Real-Time Activity Monitor")
        
        with st.expander("🟢 Live Activity Feed", expanded=True):
            live_activity = [
                "14:35:22 - Sarah Chen accessed Engineering module",
                "14:35:18 - Mike Rodriguez updated daily report",
                "14:35:15 - David Kim uploaded safety photos", 
                "14:35:12 - Jennifer Walsh approved change order",
                "14:35:08 - Lisa Wong created cost estimate"
            ]
            
            for activity in live_activity:
                st.markdown(f"• {activity}")
            
            if st.button("🔄 Refresh Feed"):
                st.rerun()
    
    with tab4:
        st.markdown("### Security Policies & Compliance")
        
        # Compliance status
        st.markdown("#### Compliance Status")
        
        compliance_data = {
            'Standard': ['SOC 2 Type II', 'ISO 27001', 'NIST Cybersecurity', 'GDPR', 'Construction Industry Standards'],
            'Status': ['Compliant', 'Compliant', 'Partially Compliant', 'Compliant', 'Compliant'],
            'Last Audit': ['2024-12-15', '2024-11-20', '2025-01-10', '2024-10-30', '2024-09-15'],
            'Next Review': ['2025-06-15', '2025-05-20', '2025-04-10', '2025-04-30', '2025-03-15'],
            'Action Required': ['None', 'None', 'Update MFA policy', 'None', 'None']
        }
        
        df_compliance = pd.DataFrame(compliance_data)
        st.dataframe(df_compliance, use_container_width=True)
        
        # Security policies
        st.markdown("#### Security Policies")
        
        with st.expander("📋 Data Retention Policy"):
            st.markdown("""
            **Highland Tower Development Data Retention Policy**
            
            • **Project Data:** Retained for 7 years after project completion
            • **Financial Records:** Retained for 7 years per IRS requirements
            • **Safety Records:** Retained for 30 years per OSHA requirements
            • **User Activity Logs:** Retained for 2 years
            • **Backup Data:** Retained for 1 year with quarterly archival
            """)
            
            if st.button("📝 Edit Policy"):
                st.info("Opening policy editor...")
        
        with st.expander("🔒 Access Control Policy"):
            st.markdown("""
            **Highland Tower Development Access Control Policy**
            
            • **Principle of Least Privilege:** Users granted minimum access required
            • **Role-Based Access:** Access determined by job function and responsibilities  
            • **Regular Reviews:** Access reviewed quarterly
            • **Offboarding:** Access revoked within 24 hours of departure
            • **Contractor Access:** Limited duration with sponsor approval
            """)
            
            if st.button("📝 Edit Policy"):
                st.info("Opening policy editor...")
        
        with st.expander("🛡️ Incident Response Plan"):
            st.markdown("""
            **Highland Tower Development Incident Response Plan**
            
            **Phase 1: Detection & Analysis (0-1 hour)**
            • Automated monitoring alerts security team
            • Initial assessment and classification
            • Stakeholder notification
            
            **Phase 2: Containment & Eradication (1-4 hours)**
            • Isolate affected systems
            • Preserve evidence
            • Remove threat vectors
            
            **Phase 3: Recovery & Lessons Learned (4+ hours)**
            • Restore normal operations
            • Monitor for recurrence
            • Document and improve procedures
            """)
            
            if st.button("📝 Edit Plan"):
                st.info("Opening incident response editor...")
        
        # Security training
        st.markdown("#### Security Training Status")
        
        training_data = {
            'Training Module': ['Cybersecurity Basics', 'Phishing Awareness', 'Password Security', 'Data Protection', 'Incident Reporting'],
            'Completion Rate': ['94%', '88%', '100%', '82%', '76%'],
            'Last Updated': ['2024-12-01', '2024-11-15', '2024-10-30', '2024-12-10', '2024-09-20'],
            'Next Training': ['2025-06-01', '2025-02-15', '2025-04-30', '2025-06-10', '2025-03-20']
        }
        
        df_training = pd.DataFrame(training_data)
        st.dataframe(df_training, use_container_width=True)
        
        if st.button("📚 Schedule Security Training"):
            st.success("Security training scheduled for all Highland Tower Development team members")

if __name__ == "__main__":
    render()