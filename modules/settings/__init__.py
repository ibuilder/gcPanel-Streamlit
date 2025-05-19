"""
Settings module for gcPanel Construction Management Dashboard.

This module renders the application settings and preferences.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_settings():
    """Render the settings page."""
    
    st.header("Settings")
    
    # Settings categories
    categories = st.tabs(["User Profile", "Appearance", "Notifications", "Data Management", "System", "Integrations"])
    
    with categories[0]:  # User Profile
        render_user_profile()
        
    with categories[1]:  # Appearance
        render_appearance_settings()
        
    with categories[2]:  # Notifications
        render_notification_settings()
        
    with categories[3]:  # Data Management
        render_data_management()
        
    with categories[4]:  # System
        render_system_settings()
        
    with categories[5]:  # Integrations
        from modules.settings.integrations import render_integration_settings
        render_integration_settings()

def render_user_profile():
    """Render user profile settings."""
    
    # User data
    user_data = {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "Administrator",
        "phone": "206-555-1234",
        "company": "General Contractor Inc.",
        "last_login": "May 17, 2025 09:45 AM"
    }
    
    # Profile section
    st.subheader("User Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Avatar section
        st.markdown(
            """
            <div class="dashboard-card" style="padding: 1.5rem; text-align: center;">
                <div style="width: 120px; height: 120px; border-radius: 50%; background-color: #3e79f7; color: white; 
                           font-size: 3rem; display: flex; justify-content: center; align-items: center; 
                           margin: 0 auto 1rem auto;">
                    A
                </div>
                <button style="background-color: #f8f9fa; border: 1px solid #e9ecef; color: #6c757d; 
                             padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-size: 0.9rem;">
                    Change Photo
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # User info form
        with st.form("user_profile_form"):
            name = st.text_input("Full Name", value=user_data["name"])
            email = st.text_input("Email", value=user_data["email"])
            phone = st.text_input("Phone", value=user_data["phone"])
            company = st.text_input("Company", value=user_data["company"])
            
            # Form row with two columns
            col1, col2 = st.columns(2)
            with col1:
                role = st.selectbox("Role", ["Administrator", "Project Manager", "Engineer", "Superintendent", "Field User"], index=0)
            with col2:
                timezone = st.selectbox("Timezone", ["Pacific Time", "Mountain Time", "Central Time", "Eastern Time"], index=0)
            
            # Submit button
            submit = st.form_submit_button("Save Changes", type="primary")
            
            if submit:
                st.success("Profile updated successfully!")
    
    # Password section
    st.subheader("Change Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submit = st.form_submit_button("Update Password")
        
        if submit:
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill all password fields")
            elif new_password != confirm_password:
                st.error("New passwords do not match")
            else:
                st.success("Password updated successfully!")

def render_appearance_settings():
    """Render appearance settings."""
    
    st.subheader("Appearance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Theme settings
        st.markdown(
            """
            <div class="dashboard-card" style="height: 100%;">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Theme</h3>
            """,
            unsafe_allow_html=True
        )
        
        theme_mode = st.radio("Theme Mode", ["Light", "Dark"], index=0 if st.session_state.get("theme_mode", "light") == "light" else 1)
        
        if theme_mode == "Light" and st.session_state.get("theme_mode") != "light":
            st.session_state.theme_mode = "light"
            st.success("Theme mode set to Light")
        elif theme_mode == "Dark" and st.session_state.get("theme_mode") != "dark":
            st.session_state.theme_mode = "dark"
            st.success("Theme mode set to Dark")
        
        # Color palette options
        st.write("Color Palette")
        color_options = {
            "Blue": "#3e79f7",
            "Green": "#38d39f",
            "Purple": "#727cf5", 
            "Red": "#ff5b5b"
        }
        
        # Display color options
        cols = st.columns(4)
        for i, (color_name, color_value) in enumerate(color_options.items()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <div style="width: 30px; height: 30px; border-radius: 50%; background-color: {color_value}; 
                                  margin: 0 auto 0.3rem auto; cursor: pointer; border: 2px solid {'#e9ecef' if color_value != st.session_state.get('theme_color', '#3e79f7') else '#2c3e50'};"></div>
                        <div style="font-size: 0.8rem;">{color_name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Layout settings
        st.markdown(
            """
            <div class="dashboard-card" style="height: 100%;">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Layout</h3>
            """,
            unsafe_allow_html=True
        )
        
        # Sidebar options
        sidebar_collapsed = st.checkbox("Collapse sidebar by default", value=False)
        
        # Card style options
        card_style = st.radio("Card Style", ["Default", "Flat", "Bordered"], index=0)
        
        # Font size
        font_size = st.slider("Font Size", min_value=80, max_value=120, value=100, step=5, format="%d%%")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_notification_settings():
    """Render notification settings."""
    
    st.subheader("Notification Settings")
    
    # Email notifications
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown("### Email Notifications")
    
    email_notifications = st.checkbox("Enable email notifications", value=True)
    
    if email_notifications:
        st.write("Select which notifications to receive by email:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("RFI responses", value=True)
            st.checkbox("Submittal status changes", value=True)
            st.checkbox("Document uploads", value=True)
        
        with col2:
            st.checkbox("Task assignments", value=True)
            st.checkbox("Project status changes", value=False)
            st.checkbox("Meeting reminders", value=True)
    
    # Email frequency
    if email_notifications:
        email_frequency = st.radio("Email Digest Frequency", ["Immediate", "Daily Digest", "Weekly Digest"], index=0)
        
        if email_frequency != "Immediate":
            st.write(f"You will receive a {email_frequency.lower()} summary of all notifications.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # In-app notifications
    st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown("### In-App Notifications")
    
    in_app_notifications = st.checkbox("Enable in-app notifications", value=True, key="enable_in_app_notif")
    
    if in_app_notifications:
        st.write("Select which notifications to receive within the app:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("RFI responses", value=True, key="notif_rfi_responses")
            st.checkbox("Submittal status changes", value=True, key="notif_submittal_status")
            st.checkbox("Document uploads", value=True, key="notif_document_uploads")
        
        with col2:
            st.checkbox("Task assignments", value=True, key="notif_task_assignments")
            st.checkbox("Project status changes", value=True, key="notif_project_status")
            st.checkbox("Meeting reminders", value=True, key="notif_meeting_reminders")
    
    desktop_notifications = st.checkbox("Enable desktop notifications", value=False)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_data_management():
    """Render data management settings."""
    
    st.subheader("Data Management")
    
    # Export data options
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown("### Export Data")
    
    st.write("Export project data for backup or external use.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Export All Data (JSON)", key="export_all_json")
    
    with col2:
        st.button("Export All Data (Excel)", key="export_all_excel")
    
    with col3:
        st.button("Export All Data (CSV)", key="export_all_csv")
    
    # Select specific data to export
    export_options = st.multiselect(
        "Select specific data to export:", 
        ["Project Information", "RFIs", "Submittals", "Daily Reports", "Inspections", "Contacts", "Schedule"],
        default=["Project Information"]
    )
    
    if export_options:
        col1, col2 = st.columns(2)
        with col1:
            st.button("Export Selected Data", key="export_selected")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data import options
    st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown("### Import Data")
    
    st.write("Import data from external sources.")
    
    uploaded_file = st.file_uploader("Upload data file (JSON, Excel, or CSV)", type=["json", "xlsx", "csv"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            import_action = st.radio("Import Action", ["Merge with existing data", "Replace existing data"], index=0)
        
        with col2:
            st.button("Process Import", key="process_import")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data purge options
    st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown("### Data Management")
    
    st.write("Manage project data in the system.")
    
    purge_options = st.multiselect(
        "Select data types to purge:", 
        ["Deleted Documents", "Archived Projects", "System Logs", "Revision History"],
        default=[]
    )
    
    if purge_options:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Purge Selected Data", key="purge_data"):
                st.warning("This action cannot be undone.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_settings():
    """Render system settings."""
    
    st.subheader("System Settings")
    
    # System info
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown("### System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Application Version:** 1.0.0 <br>
        **Database Version:** 1.0.0 <br>
        **Last Update:** May 15, 2025 <br>
        **Server Time:** UTC
        """, unsafe_allow_html=True)
    
    with col2:
        st.button("Check for Updates", key="check_updates")
        st.button("System Diagnostics", key="system_diagnostics")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User management
    st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown("### User Management")
    
    tab1, tab2 = st.tabs(["Users", "Roles"])
    
    with tab1:
        user_data = [
            {"name": "Admin User", "email": "admin@example.com", "role": "Administrator", "status": "Active"},
            {"name": "John Smith", "email": "john.smith@example.com", "role": "Project Manager", "status": "Active"},
            {"name": "Sarah Johnson", "email": "sarah.johnson@example.com", "role": "Engineer", "status": "Active"},
            {"name": "Robert Chen", "email": "robert.chen@example.com", "role": "Superintendent", "status": "Active"},
            {"name": "Jessica Williams", "email": "jessica.williams@example.com", "role": "BIM Coordinator", "status": "Inactive"}
        ]
        
        user_df = pd.DataFrame(user_data)
        st.dataframe(user_df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Add User", key="add_user")
        with col2:
            st.button("Edit Selected User", key="edit_user")
        with col3:
            st.button("Deactivate Selected User", key="deactivate_user")
    
    with tab2:
        role_data = [
            {"role": "Administrator", "access_level": "Full", "users": 1},
            {"role": "Project Manager", "access_level": "High", "users": 1},
            {"role": "Engineer", "access_level": "Medium", "users": 1},
            {"role": "Superintendent", "access_level": "Medium", "users": 1},
            {"role": "BIM Coordinator", "access_level": "Medium", "users": 1},
            {"role": "Field User", "access_level": "Low", "users": 0}
        ]
        
        role_df = pd.DataFrame(role_data)
        st.dataframe(role_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Add Role", key="add_role")
        with col2:
            st.button("Edit Selected Role", key="edit_role")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Integrations
    st.markdown('<div class="dashboard-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown("### Integrations")
    
    integrations = [
        {"name": "Email Service", "status": "Connected", "last_sync": "May 17, 2025"},
        {"name": "Weather API", "status": "Connected", "last_sync": "May 17, 2025"},
        {"name": "Calendar", "status": "Not Connected", "last_sync": "-"},
        {"name": "Document Storage", "status": "Connected", "last_sync": "May 17, 2025"}
    ]
    
    for integration in integrations:
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.write(f"**{integration['name']}**")
        
        with col2:
            if integration['status'] == "Connected":
                st.markdown(f"<span style='color: #38d39f;'>●</span> {integration['status']}", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #6c757d;'>●</span> {integration['status']}", unsafe_allow_html=True)
        
        with col3:
            if integration['status'] == "Connected":
                st.button("Disconnect", key=f"disconnect_{integration['name'].lower().replace(' ', '_')}")
            else:
                st.button("Connect", key=f"connect_{integration['name'].lower().replace(' ', '_')}")
    
    st.markdown('</div>', unsafe_allow_html=True)