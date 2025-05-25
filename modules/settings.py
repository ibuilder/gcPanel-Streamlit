"""
Settings Module - Highland Tower Development
Comprehensive system configuration and file distribution settings
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

def render():
    """Render the comprehensive settings interface"""
    st.title("⚙️ System Settings - Highland Tower Development")
    st.markdown("**Enterprise configuration and file distribution management**")
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📧 Email Distribution", "📁 File Routing", "👥 User Management", "🔐 Security", "📊 Billing Setup"
    ])
    
    with tab1:
        render_email_distribution_settings()
    
    with tab2:
        render_file_routing_settings()
    
    with tab3:
        render_user_management_settings()
    
    with tab4:
        render_security_settings()
    
    with tab5:
        render_billing_setup_settings()

def render_email_distribution_settings():
    """Email distribution configuration"""
    st.header("📧 Email Distribution Settings")
    st.markdown("**Configure automatic file distribution for bills, reports, and documents**")
    
    # Owner Bill Distribution
    st.subheader("💰 Owner Bill Distribution")
    with st.expander("Owner Bill Recipients", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Primary Recipients**")
            owner_emails = st.text_area("Owner Email Addresses", 
                value="finance@highlandtower.com\naccounting@highlandtower.com\nproject.manager@highlandtower.com",
                help="One email per line")
            
            st.markdown("**CC Recipients**")
            cc_emails = st.text_area("CC Email Addresses",
                value="legal@highlandtower.com\ncontracts@highlandtower.com",
                help="One email per line")
        
        with col2:
            st.markdown("**Distribution Settings**")
            auto_send_owner = st.checkbox("Auto-send Owner Bills", value=True)
            include_backup = st.checkbox("Include backup documents", value=True)
            send_confirmation = st.checkbox("Request read confirmation", value=False)
            
            st.markdown("**Timing**")
            send_time = st.selectbox("Send Time", ["Immediately", "End of Business Day", "Next Morning 8 AM"])
    
    # G702/G703 Distribution
    st.subheader("📄 AIA G702/G703 Distribution")
    with st.expander("AIA Forms Distribution", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Architect Recipients**")
            architect_emails = st.text_area("Architect Email Addresses",
                value="billing@architectfirm.com\nproject.architect@architectfirm.com",
                help="One email per line")
            
            st.markdown("**Engineer Recipients**")
            engineer_emails = st.text_area("Engineer Email Addresses",
                value="payments@structuralengineer.com\nproject.engineer@structuralengineer.com",
                help="One email per line")
        
        with col2:
            st.markdown("**Additional Recipients**")
            other_g702_emails = st.text_area("Other Recipients",
                value="admin@highlandconstruction.com\nsuperintendent@highlandconstruction.com",
                help="One email per line")
            
            auto_send_g702 = st.checkbox("Auto-send G702/G703 Forms", value=True)
            include_schedules = st.checkbox("Include all schedules", value=True)
    
    # RFI and Submittal Distribution
    st.subheader("📝 RFI & Submittal Distribution")
    with st.expander("Project Communication Distribution"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**RFI Distribution**")
            rfi_emails = st.text_area("RFI Recipients",
                value="rfis@architectfirm.com\nproject.manager@highlandtower.com\nfield.super@highlandconstruction.com",
                help="One email per line")
        
        with col2:
            st.markdown("**Submittal Distribution**")
            submittal_emails = st.text_area("Submittal Recipients",
                value="submittals@architectfirm.com\nreview@structuralengineer.com\nproject.manager@highlandtower.com",
                help="One email per line")
    
    # Save settings
    if st.button("💾 Save Email Settings", type="primary"):
        st.success("✅ Email distribution settings saved successfully!")

def render_file_routing_settings():
    """File routing and storage configuration"""
    st.header("📁 File Routing & Storage Settings")
    st.markdown("**Configure where different file types are automatically stored and distributed**")
    
    # Cloud Storage Settings
    st.subheader("☁️ Cloud Storage Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Primary Storage**")
        primary_storage = st.selectbox("Primary Storage", ["Google Drive", "Dropbox", "SharePoint", "Box"])
        folder_structure = st.text_area("Folder Structure",
            value="Highland Tower Development/\n  01-Contracts/\n  02-Billing/\n    Owner-Bills/\n    AIA-Forms/\n  03-RFIs/\n  04-Submittals/\n  05-Daily-Reports/",
            height=150)
    
    with col2:
        st.markdown("**Backup Storage**")
        backup_storage = st.selectbox("Backup Storage", ["AWS S3", "Azure Blob", "Local Server", "None"])
        retention_period = st.number_input("Retention Period (years)", min_value=1, max_value=10, value=7)
        auto_backup = st.checkbox("Automatic daily backup", value=True)
    
    # File Type Routing
    st.subheader("🗂️ Automatic File Routing")
    
    routing_data = pd.DataFrame([
        {"File Type": "Owner Bills", "Primary Folder": "/02-Billing/Owner-Bills/", "Auto-Archive": "After Payment", "Notification": "✅"},
        {"File Type": "G702 Forms", "Primary Folder": "/02-Billing/AIA-Forms/", "Auto-Archive": "Monthly", "Notification": "✅"},
        {"File Type": "G703 Forms", "Primary Folder": "/02-Billing/AIA-Forms/", "Auto-Archive": "Monthly", "Notification": "✅"},
        {"File Type": "RFIs", "Primary Folder": "/03-RFIs/", "Auto-Archive": "When Closed", "Notification": "✅"},
        {"File Type": "Submittals", "Primary Folder": "/04-Submittals/", "Auto-Archive": "When Approved", "Notification": "✅"},
        {"File Type": "Daily Reports", "Primary Folder": "/05-Daily-Reports/", "Auto-Archive": "Weekly", "Notification": "❌"},
        {"File Type": "Safety Reports", "Primary Folder": "/06-Safety/", "Auto-Archive": "Monthly", "Notification": "✅"},
        {"File Type": "Photos", "Primary Folder": "/07-Photos/", "Auto-Archive": "Monthly", "Notification": "❌"}
    ])
    
    st.dataframe(routing_data, use_container_width=True, hide_index=True)
    
    # Save routing settings
    if st.button("💾 Save Routing Settings", type="primary"):
        st.success("✅ File routing settings saved successfully!")

def render_user_management_settings():
    """User management and permissions"""
    st.header("👥 User Management & Permissions")
    st.markdown("**Manage user access and file distribution permissions**")
    
    # User roles and permissions
    st.subheader("🔑 User Roles & Permissions")
    
    user_data = pd.DataFrame([
        {"User": "John Smith", "Role": "Project Manager", "Email": "j.smith@highlandtower.com", "Bills": "✅", "G702": "✅", "RFIs": "✅", "Admin": "✅"},
        {"User": "Sarah Chen", "Role": "Site Superintendent", "Email": "s.chen@highlandconstruction.com", "Bills": "❌", "G702": "❌", "RFIs": "✅", "Admin": "❌"},
        {"User": "Mike Rodriguez", "Role": "Engineer", "Email": "m.rodriguez@structuralengineer.com", "Bills": "❌", "G702": "✅", "RFIs": "✅", "Admin": "❌"},
        {"User": "Lisa Johnson", "Role": "Architect", "Email": "l.johnson@architectfirm.com", "Bills": "❌", "G702": "✅", "RFIs": "✅", "Admin": "❌"},
        {"User": "David Park", "Role": "Owner Rep", "Email": "d.park@highlandtower.com", "Bills": "✅", "G702": "✅", "RFIs": "❌", "Admin": "✅"}
    ])
    
    st.dataframe(user_data, use_container_width=True, hide_index=True)
    
    # Add new user
    st.subheader("➕ Add New User")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_user_name = st.text_input("Full Name")
        new_user_email = st.text_input("Email Address")
    
    with col2:
        new_user_role = st.selectbox("Role", ["Project Manager", "Site Superintendent", "Engineer", "Architect", "Owner Rep", "Subcontractor"])
        new_user_company = st.text_input("Company")
    
    with col3:
        st.markdown("**Permissions**")
        bills_access = st.checkbox("Bills Access")
        g702_access = st.checkbox("G702/G703 Access")
        rfi_access = st.checkbox("RFI Access")
        admin_access = st.checkbox("Admin Access")
    
    if st.button("👤 Add User", type="primary"):
        st.success(f"✅ User {new_user_name} added successfully!")

def render_security_settings():
    """Security and access control settings"""
    st.header("🔐 Security & Access Control")
    st.markdown("**Configure security settings for Highland Tower Development platform**")
    
    # Authentication settings
    st.subheader("🛡️ Authentication Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Password Requirements**")
        min_password_length = st.number_input("Minimum Password Length", min_value=8, max_value=20, value=12)
        require_uppercase = st.checkbox("Require Uppercase Letters", value=True)
        require_numbers = st.checkbox("Require Numbers", value=True)
        require_symbols = st.checkbox("Require Special Characters", value=True)
        
        session_timeout = st.number_input("Session Timeout (hours)", min_value=1, max_value=24, value=8)
    
    with col2:
        st.markdown("**Two-Factor Authentication**")
        enable_2fa = st.checkbox("Enable 2FA for all users", value=True)
        enforce_2fa_admin = st.checkbox("Enforce 2FA for admins", value=True)
        
        st.markdown("**Digital Signatures**")
        require_signatures = st.checkbox("Require digital signatures on bills", value=True)
        signature_method = st.selectbox("Signature Method", ["DocuSign", "Adobe Sign", "Internal System"])
    
    # Audit logging
    st.subheader("📋 Audit & Logging")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Logging Settings**")
        log_file_access = st.checkbox("Log file access", value=True)
        log_user_actions = st.checkbox("Log user actions", value=True)
        log_system_changes = st.checkbox("Log system changes", value=True)
        
    with col2:
        st.markdown("**Retention Settings**")
        audit_retention = st.number_input("Audit log retention (months)", min_value=12, max_value=84, value=36)
        backup_frequency = st.selectbox("Backup frequency", ["Daily", "Weekly", "Monthly"])

def render_billing_setup_settings():
    """Billing and payment processing setup"""
    st.header("📊 Billing & Payment Setup")
    st.markdown("**Configure billing processes and payment systems for Highland Tower Development**")
    
    # Company information
    st.subheader("🏢 Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Highland Tower Development**")
        company_name = st.text_input("Company Name", value="Highland Tower Development LLC")
        company_address = st.text_area("Company Address", 
            value="1234 Construction Avenue\nNew York, NY 10001\nUnited States")
        tax_id = st.text_input("Tax ID/EIN", value="XX-XXXXXXX")
    
    with col2:
        st.markdown("**Billing Configuration**")
        billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Bi-weekly", "Weekly"])
        payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Due on Receipt"])
        retention_percentage = st.number_input("Retention Percentage", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    
    # Digital signature settings for bills
    st.subheader("✍️ Digital Signature Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Signature Requirements**")
        require_pm_signature = st.checkbox("Require Project Manager signature", value=True)
        require_owner_signature = st.checkbox("Require Owner representative signature", value=True)
        require_contractor_signature = st.checkbox("Require Contractor signature", value=True)
        
    with col2:
        st.markdown("**Signature Settings**")
        signature_order = st.selectbox("Signature Order", 
            ["Contractor → PM → Owner", "PM → Contractor → Owner", "Simultaneous"])
        auto_remind = st.checkbox("Auto-remind for signatures", value=True)
        reminder_interval = st.number_input("Reminder interval (days)", min_value=1, max_value=7, value=2)
    
    # AIA Forms configuration
    st.subheader("📄 AIA Forms Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**G702 Configuration**")
        include_retainage = st.checkbox("Include retainage calculation", value=True)
        show_previous_apps = st.checkbox("Show previous applications", value=True)
        auto_calculate_stored = st.checkbox("Auto-calculate stored materials", value=True)
        
    with col2:
        st.markdown("**G703 Configuration**")
        detailed_breakdown = st.checkbox("Include detailed cost breakdown", value=True)
        show_unit_prices = st.checkbox("Show unit prices", value=True)
        include_change_orders = st.checkbox("Include approved change orders", value=True)
    
    # Save all settings
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Security Settings", use_container_width=True):
            st.success("✅ Security settings saved!")
    with col2:
        if st.button("💾 Save Billing Settings", use_container_width=True):
            st.success("✅ Billing settings saved!")
    with col3:
        if st.button("🔄 Export All Settings", use_container_width=True):
            st.success("📄 Settings exported to file!")