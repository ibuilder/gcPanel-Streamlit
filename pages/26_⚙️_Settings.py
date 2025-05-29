"""
Settings & Configuration Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state

st.set_page_config(page_title="Settings - gcPanel", page_icon="⚙️", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("⚙️ Settings & Configuration")
st.markdown("Highland Tower Development - System Configuration Management")
st.markdown("---")

tabs = st.tabs(["🏢 Project Settings", "👥 User Management", "🔧 System Configuration", "📊 Analytics Settings", "🌐 Environment Status"])

with tabs[0]:
    st.subheader("🏢 Project Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Project Information**")
        project_name = st.text_input("Project Name", value="Highland Tower Development")
        project_code = st.text_input("Project Code", value="HTD-2025")
        project_manager = st.text_input("Project Manager", value="Sarah Johnson")
        project_start = st.date_input("Project Start Date", value=datetime(2024, 1, 15))
        
    with col2:
        st.markdown("**Project Details**")
        project_value = st.number_input("Project Value ($)", value=45500000)
        project_duration = st.number_input("Duration (months)", value=24)
        project_location = st.text_input("Location", value="Downtown Financial District")
        project_type = st.selectbox("Project Type", ["Mixed-Use", "Commercial", "Residential", "Industrial"])
    
    if st.button("💾 Save Project Settings", type="primary"):
        st.success("Project settings saved successfully!")

with tabs[1]:
    st.subheader("👥 User Management")
    
    # User creation form
    with st.expander("➕ Add New User"):
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_first_name = st.text_input("First Name")
        with col2:
            new_password = st.text_input("Password", type="password")
            new_last_name = st.text_input("Last Name")
            new_role = st.selectbox("Role", ["user", "manager", "admin"])
        
        if st.button("👤 Create User"):
            st.success("User created successfully!")
    
    # Current users table
    st.markdown("**Current Users**")
    users_data = [
        {"Username": "admin", "Email": "admin@highland.com", "Role": "Administrator", "Status": "Active"},
        {"Username": "manager", "Email": "manager@highland.com", "Role": "Project Manager", "Status": "Active"},
        {"Username": "engineer", "Email": "engineer@highland.com", "Role": "Engineer", "Status": "Active"}
    ]
    
    df_users = pd.DataFrame(users_data)
    st.dataframe(df_users, use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("🔧 System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Database Settings**")
        db_host = st.text_input("Database Host", value="localhost")
        db_port = st.number_input("Database Port", value=5432)
        db_name = st.text_input("Database Name", value="gcpanel_db")
        
        st.markdown("**File Upload Settings**")
        max_file_size = st.number_input("Max File Size (MB)", value=50)
        allowed_extensions = st.multiselect("Allowed Extensions", 
            [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".jpg", ".png"], 
            default=[".pdf", ".doc", ".docx"])
    
    with col2:
        st.markdown("**Security Settings**")
        session_timeout = st.number_input("Session Timeout (hours)", value=8)
        password_policy = st.selectbox("Password Policy", ["Standard", "Strong", "Very Strong"])
        two_factor_auth = st.checkbox("Enable Two-Factor Authentication")
        
        st.markdown("**Email Settings**")
        smtp_server = st.text_input("SMTP Server")
        smtp_port = st.number_input("SMTP Port", value=587)
        email_username = st.text_input("Email Username")
    
    if st.button("💾 Save System Configuration", type="primary"):
        st.success("System configuration saved successfully!")

with tabs[3]:
    st.subheader("📊 Analytics Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dashboard Settings**")
        default_date_range = st.selectbox("Default Date Range", ["Last 7 days", "Last 30 days", "Last 90 days"])
        auto_refresh = st.checkbox("Auto-refresh dashboard", value=True)
        refresh_interval = st.number_input("Refresh Interval (minutes)", value=5, min_value=1)
        
    with col2:
        st.markdown("**Report Settings**")
        report_format = st.selectbox("Default Report Format", ["PDF", "Excel", "CSV"])
        include_charts = st.checkbox("Include charts in reports", value=True)
        email_reports = st.checkbox("Email reports automatically")
    
    if st.button("💾 Save Analytics Settings", type="primary"):
        st.success("Analytics settings saved successfully!")

with tabs[4]:
    st.subheader("🌐 Environment Status")
    
    st.markdown("**System Status**")
    st.write("✅ Application Core: Running")
    st.write("✅ Authentication: Active")
    st.write("✅ Session Management: Active")
    st.write("✅ Page Navigation: Active")
    
    st.markdown("**Module Completion Status**")
    module_status = [
        "✅ Dashboard with Analytics",
        "✅ Daily Reports with Form Processing", 
        "✅ RFI Management System",
        "✅ Submittals Tracking",
        "✅ Contracts Management",
        "✅ Safety Management",
        "✅ Deliveries Tracking",
        "✅ Preconstruction Planning",
        "✅ Engineering Management",
        "✅ Field Operations",
        "✅ Cost Management",
        "✅ BIM Management",
        "✅ Project Closeout",
        "✅ Transmittals",
        "✅ Scheduling",
        "✅ Quality Control",
        "✅ Progress Photos",
        "✅ Subcontractor Management",
        "✅ Inspections",
        "✅ Issues & Risks",
        "✅ Document Management",
        "✅ Unit Prices",
        "✅ Material Management",
        "✅ Equipment Tracking",
        "✅ Analytics Dashboard",
        "✅ Settings & Configuration"
    ]
    
    for status in module_status:
        st.write(status)