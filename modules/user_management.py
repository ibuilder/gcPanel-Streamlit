"""
User Management Module - Highland Tower Development
Enterprise-grade user administration with role-based access control
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import hashlib

def render():
    """Render the comprehensive User Management module"""
    st.title("👥 User Management - Highland Tower Development")
    st.markdown("**Enterprise User Administration & Role-Based Access Control**")
    
    # Initialize session state for user data
    if 'users' not in st.session_state:
        st.session_state.users = get_sample_users()
    if 'user_roles' not in st.session_state:
        st.session_state.user_roles = get_user_roles()
    if 'user_permissions' not in st.session_state:
        st.session_state.user_permissions = get_permissions_matrix()
    
    # User management overview
    total_users = len(st.session_state.users)
    active_users = len([u for u in st.session_state.users if u['status'] == 'Active'])
    pending_users = len([u for u in st.session_state.users if u['status'] == 'Pending'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", total_users, "Highland Tower Team")
    with col2:
        st.metric("Active Users", active_users, f"{active_users/total_users*100:.0f}% of total")
    with col3:
        st.metric("Pending Approval", pending_users, "Awaiting activation")
    with col4:
        st.metric("User Satisfaction", "94.2%", "+2.3% this month")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 User Directory", "🔐 Roles & Permissions", "➕ Add New User", "📊 User Analytics", "⚙️ User Settings", "📋 Audit Log"
    ])
    
    with tab1:
        render_user_directory()
    
    with tab2:
        render_roles_permissions()
    
    with tab3:
        render_add_user()
    
    with tab4:
        render_user_analytics()
    
    with tab5:
        render_user_settings()
    
    with tab6:
        render_audit_log()

def render_user_directory():
    """Complete user directory with management functions"""
    st.subheader("👤 Highland Tower Development - User Directory")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Invite New User", type="primary"):
            st.session_state.show_invite_form = True
    with col2:
        if st.button("📊 Export Directory"):
            st.success("✅ User directory exported to Excel")
    with col3:
        if st.button("📧 Bulk Email"):
            st.session_state.show_bulk_email = True
    with col4:
        if st.button("🔄 Sync Active Directory"):
            st.info("🔄 Syncing with company Active Directory...")
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search users", placeholder="Name, email, or role...")
    with col2:
        role_filter = st.selectbox("Filter by Role", ["All Roles"] + [role['name'] for role in st.session_state.user_roles])
    with col3:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Pending", "Suspended"])
    
    # Display users
    users_df = pd.DataFrame(st.session_state.users)
    
    # Apply filters
    if search_query:
        mask = users_df.apply(lambda x: search_query.lower() in str(x).lower(), axis=1)
        users_df = users_df[mask]
    
    if role_filter != "All Roles":
        users_df = users_df[users_df['role'] == role_filter]
    
    if status_filter != "All":
        users_df = users_df[users_df['status'] == status_filter]
    
    st.markdown("### User Directory")
    
    for idx, user in users_df.iterrows():
        with st.expander(f"👤 {user['name']} - {user['role']} ({user['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Status color coding
                status_colors = {
                    "Active": "#28a745",
                    "Inactive": "#6c757d",
                    "Pending": "#ffc107",
                    "Suspended": "#dc3545"
                }
                
                status_color = status_colors.get(user['status'], "#6c757d")
                
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Email:</strong> {user['email']}<br>
                <strong>Phone:</strong> {user['phone']}<br>
                <strong>Company:</strong> {user['company']}<br>
                <strong>Department:</strong> {user['department']}<br>
                <strong>Last Login:</strong> {user['last_login']}<br>
                <strong>Access Level:</strong> {user['access_level']}<br>
                <strong>Created:</strong> {user['created_date']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_user_{user['user_id']}"):
                    st.session_state.edit_user_id = user['user_id']
                    st.session_state.show_user_edit = True
                
                if user['status'] == 'Active':
                    if st.button("⏸️ Suspend", key=f"suspend_user_{user['user_id']}"):
                        # Update user status
                        for i, u in enumerate(st.session_state.users):
                            if u['user_id'] == user['user_id']:
                                st.session_state.users[i]['status'] = 'Suspended'
                                break
                        st.warning("⏸️ User suspended")
                        st.rerun()
                elif user['status'] == 'Suspended':
                    if st.button("▶️ Activate", key=f"activate_user_{user['user_id']}"):
                        for i, u in enumerate(st.session_state.users):
                            if u['user_id'] == user['user_id']:
                                st.session_state.users[i]['status'] = 'Active'
                                break
                        st.success("▶️ User reactivated")
                        st.rerun()
                
                if st.button("🔐 Reset Password", key=f"reset_pwd_{user['user_id']}"):
                    st.success("📧 Password reset email sent")

def render_roles_permissions():
    """Role-based access control management"""
    st.subheader("🔐 Roles & Permissions Management")
    
    # Role overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 User Roles")
        
        for role in st.session_state.user_roles:
            user_count = len([u for u in st.session_state.users if u['role'] == role['name']])
            
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin: 8px 0; background: white;">
                    <h5>{role['icon']} {role['name']}</h5>
                    <p style="color: #666; margin: 4px 0;">{role['description']}</p>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Users: {user_count}</span>
                        <span style="color: {role['color']}; font-weight: bold;">{role['access_level']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⚙️ Configure {role['name']}", key=f"config_{role['name']}"):
                    st.session_state.config_role = role['name']
                    st.session_state.show_role_config = True
    
    with col2:
        st.markdown("#### 🔒 Permission Matrix")
        
        # Display permissions matrix
        permissions_df = pd.DataFrame(st.session_state.user_permissions)
        st.dataframe(permissions_df, use_container_width=True)
        
        if st.button("📝 Edit Permissions Matrix", use_container_width=True):
            st.session_state.show_permissions_edit = True

def render_add_user():
    """Add new user with role assignment"""
    st.subheader("➕ Add New User to Highland Tower Development")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="John Smith")
            email = st.text_input("Email Address *", placeholder="john.smith@company.com")
            phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
            company = st.selectbox("Company *", 
                                 ["Highland Tower Development", "Highland Construction", "Elite MEP", 
                                  "Premium Plumbing", "Steel Fabricators Inc", "Other"])
        
        with col2:
            role = st.selectbox("User Role *", [r['name'] for r in st.session_state.user_roles])
            department = st.selectbox("Department", 
                                    ["Construction", "Engineering", "Safety", "Quality", "Finance", "Administration"])
            access_level = st.selectbox("Access Level", ["Full Access", "Limited Access", "View Only", "Module Specific"])
            start_date = st.date_input("Start Date", value=datetime.now())
        
        # Special permissions
        st.markdown("#### 🔐 Special Permissions")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            admin_access = st.checkbox("System Administrator")
            financial_access = st.checkbox("Financial Data Access")
        with col2:
            report_access = st.checkbox("Executive Reports")
            audit_access = st.checkbox("Audit Log Access")
        with col3:
            mobile_access = st.checkbox("Mobile App Access")
            api_access = st.checkbox("API Access")
        
        # Account settings
        temporary_password = st.text_input("Temporary Password", type="password", 
                                         help="User will be required to change on first login")
        
        send_welcome_email = st.checkbox("Send welcome email with login instructions", value=True)
        require_password_change = st.checkbox("Require password change on first login", value=True)
        
        submitted = st.form_submit_button("👤 Create User Account", type="primary")
        
        if submitted and full_name and email and role:
            # Create new user
            new_user = {
                'user_id': f"USR-HTD-{len(st.session_state.users) + 1:03d}",
                'name': full_name,
                'email': email,
                'phone': phone,
                'company': company,
                'role': role,
                'department': department,
                'access_level': access_level,
                'status': 'Active',
                'last_login': 'Never',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'created_by': st.session_state.get('current_user', 'System Admin'),
                'special_permissions': {
                    'admin_access': admin_access,
                    'financial_access': financial_access,
                    'report_access': report_access,
                    'audit_access': audit_access,
                    'mobile_access': mobile_access,
                    'api_access': api_access
                }
            }
            
            # Add to session state
            st.session_state.users.append(new_user)
            
            st.success(f"✅ User account created successfully!")
            st.success(f"👤 User ID: {new_user['user_id']}")
            
            if send_welcome_email:
                st.info("📧 Welcome email sent with login instructions")
            
            st.rerun()

def render_user_analytics():
    """User activity and engagement analytics"""
    st.subheader("📊 User Analytics & Activity")
    
    # User activity metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Active Users", "18", "75% of total")
    with col2:
        st.metric("Avg Session Time", "42 min", "+8 min vs last week")
    with col3:
        st.metric("Module Usage", "87%", "High engagement")
    with col4:
        st.metric("Mobile Usage", "34%", "Growing trend")
    
    # Analytics charts
    col1, col2 = st.columns(2)
    
    with col1:
        # User activity over time
        activity_data = pd.DataFrame({
            'Date': pd.date_range('2025-05-01', periods=25),
            'Active_Users': [12, 15, 18, 16, 19, 17, 20, 18, 16, 19, 21, 17, 18, 20, 19, 17, 18, 20, 19, 18, 17, 19, 18, 20, 18],
            'Total_Sessions': [45, 52, 61, 58, 67, 59, 72, 65, 58, 69, 75, 62, 66, 73, 68, 61, 66, 72, 69, 65, 62, 68, 66, 72, 65]
        })
        
        fig = px.line(activity_data, x='Date', y=['Active_Users', 'Total_Sessions'],
                     title="User Activity Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Module usage distribution
        module_usage = pd.DataFrame({
            'Module': ['Dashboard', 'Field Operations', 'Cost Management', 'Quality Control', 'Safety'],
            'Usage_Count': [245, 189, 156, 134, 112]
        })
        
        fig = px.bar(module_usage, x='Module', y='Usage_Count',
                    title="Module Usage Statistics")
        st.plotly_chart(fig, use_container_width=True)

def render_user_settings():
    """User preference and system settings"""
    st.subheader("⚙️ User Management Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔐 Security Settings")
        password_policy = st.selectbox("Password Policy", 
                                     ["Standard", "Strong", "Enterprise", "Custom"])
        session_timeout = st.slider("Session Timeout (minutes)", 15, 480, 60)
        two_factor_auth = st.checkbox("Require Two-Factor Authentication", value=True)
        login_attempts = st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
        
        st.markdown("#### 📧 Notification Settings")
        welcome_emails = st.checkbox("Send welcome emails to new users", value=True)
        password_reminders = st.checkbox("Send password expiry reminders", value=True)
        account_alerts = st.checkbox("Send security alerts", value=True)
    
    with col2:
        st.markdown("#### 👥 Default User Settings")
        default_role = st.selectbox("Default Role for New Users", 
                                  [r['name'] for r in st.session_state.user_roles])
        default_access = st.selectbox("Default Access Level", 
                                    ["View Only", "Limited Access", "Full Access"])
        auto_approval = st.checkbox("Auto-approve new user registrations", value=False)
        
        st.markdown("#### 🔄 Integration Settings")
        ad_sync = st.checkbox("Sync with Active Directory", value=False)
        sso_enabled = st.checkbox("Enable Single Sign-On", value=False)
        api_access_default = st.checkbox("Enable API access by default", value=False)
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ User management settings saved successfully!")

def render_audit_log():
    """User activity audit log"""
    st.subheader("📋 User Activity Audit Log")
    
    # Audit log filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.selectbox("Date Range", ["Today", "Last 7 Days", "Last 30 Days", "Custom Range"])
    with col2:
        action_filter = st.selectbox("Action Type", ["All Actions", "Login", "Logout", "Create", "Edit", "Delete", "View"])
    with col3:
        user_filter = st.selectbox("User", ["All Users"] + [u['name'] for u in st.session_state.users])
    
    # Sample audit log data
    audit_data = [
        {
            "Timestamp": "2025-05-25 14:32:15",
            "User": "John Smith",
            "Action": "Login",
            "Module": "Dashboard",
            "IP_Address": "192.168.1.45",
            "Details": "Successful login from Chrome browser"
        },
        {
            "Timestamp": "2025-05-25 14:28:03",
            "User": "Sarah Chen", 
            "Action": "Create",
            "Module": "Quality Control",
            "IP_Address": "192.168.1.67",
            "Details": "Created new inspection QC-HTD-20250525-001"
        },
        {
            "Timestamp": "2025-05-25 14:15:22",
            "User": "Mike Torres",
            "Action": "Edit",
            "Module": "Cost Management", 
            "IP_Address": "192.168.1.23",
            "Details": "Updated budget item COST-HTD-0045"
        },
        {
            "Timestamp": "2025-05-25 13:58:41",
            "User": "Jennifer Walsh",
            "Action": "View",
            "Module": "Safety",
            "IP_Address": "192.168.1.89",
            "Details": "Viewed safety report for Level 13"
        }
    ]
    
    audit_df = pd.DataFrame(audit_data)
    st.dataframe(audit_df, use_container_width=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Export to Excel"):
            st.success("📄 Audit log exported to Excel")
    with col2:
        if st.button("📧 Email Report"):
            st.success("📧 Audit report emailed to administrators")
    with col3:
        if st.button("🔍 Advanced Search"):
            st.info("🔍 Opening advanced audit search...")

def get_sample_users():
    """Generate sample user data for Highland Tower Development"""
    return [
        {
            'user_id': 'USR-HTD-001',
            'name': 'John Smith',
            'email': 'john.smith@highland-construction.com',
            'phone': '(555) 123-4567',
            'company': 'Highland Construction',
            'role': 'Project Manager',
            'department': 'Construction',
            'access_level': 'Full Access',
            'status': 'Active',
            'last_login': '2025-05-25 09:15',
            'created_date': '2025-01-15'
        },
        {
            'user_id': 'USR-HTD-002',
            'name': 'Sarah Chen',
            'email': 'sarah.chen@elite-mep.com',
            'phone': '(555) 234-5678',
            'company': 'Elite MEP',
            'role': 'MEP Coordinator',
            'department': 'Engineering',
            'access_level': 'Limited Access',
            'status': 'Active',
            'last_login': '2025-05-25 08:45',
            'created_date': '2025-02-01'
        },
        {
            'user_id': 'USR-HTD-003',
            'name': 'Mike Torres',
            'email': 'mike.torres@highland-construction.com',
            'phone': '(555) 345-6789',
            'company': 'Highland Construction',
            'role': 'Safety Manager',
            'department': 'Safety',
            'access_level': 'Full Access',
            'status': 'Active',
            'last_login': '2025-05-24 16:30',
            'created_date': '2025-01-20'
        },
        {
            'user_id': 'USR-HTD-004',
            'name': 'Jennifer Walsh',
            'email': 'jennifer.walsh@highland-tower.com',
            'phone': '(555) 456-7890',
            'company': 'Highland Tower Development',
            'role': 'QC Inspector',
            'department': 'Quality',
            'access_level': 'Limited Access',
            'status': 'Active',
            'last_login': '2025-05-25 11:20',
            'created_date': '2025-02-15'
        }
    ]

def get_user_roles():
    """Define user roles for Highland Tower Development"""
    return [
        {
            'name': 'Project Manager',
            'icon': '👨‍💼',
            'description': 'Full project oversight and management authority',
            'access_level': 'Full Access',
            'color': '#007bff'
        },
        {
            'name': 'Construction Manager',
            'icon': '🏗️',
            'description': 'Field operations and construction coordination',
            'access_level': 'Full Access',
            'color': '#28a745'
        },
        {
            'name': 'MEP Coordinator',
            'icon': '⚡',
            'description': 'Mechanical, electrical, and plumbing coordination',
            'access_level': 'Limited Access',
            'color': '#ffc107'
        },
        {
            'name': 'Safety Manager',
            'icon': '🦺',
            'description': 'Safety compliance and risk management',
            'access_level': 'Full Access',
            'color': '#dc3545'
        },
        {
            'name': 'QC Inspector',
            'icon': '🔍',
            'description': 'Quality control and inspection authority',
            'access_level': 'Limited Access',
            'color': '#6f42c1'
        },
        {
            'name': 'Field Supervisor',
            'icon': '👷',
            'description': 'On-site supervision and daily operations',
            'access_level': 'Limited Access',
            'color': '#fd7e14'
        }
    ]

def get_permissions_matrix():
    """Define permissions matrix for roles"""
    return [
        {'Module': 'Dashboard', 'Project Manager': '✅', 'Construction Manager': '✅', 'MEP Coordinator': '✅', 'Safety Manager': '✅', 'QC Inspector': '✅'},
        {'Module': 'Cost Management', 'Project Manager': '✅', 'Construction Manager': '👁️', 'MEP Coordinator': '❌', 'Safety Manager': '❌', 'QC Inspector': '❌'},
        {'Module': 'Quality Control', 'Project Manager': '✅', 'Construction Manager': '✅', 'MEP Coordinator': '👁️', 'Safety Manager': '✅', 'QC Inspector': '✅'},
        {'Module': 'Safety', 'Project Manager': '✅', 'Construction Manager': '✅', 'MEP Coordinator': '👁️', 'Safety Manager': '✅', 'QC Inspector': '👁️'},
        {'Module': 'Scheduling', 'Project Manager': '✅', 'Construction Manager': '✅', 'MEP Coordinator': '✏️', 'Safety Manager': '👁️', 'QC Inspector': '👁️'},
        {'Module': 'Documents', 'Project Manager': '✅', 'Construction Manager': '✅', 'MEP Coordinator': '✅', 'Safety Manager': '✅', 'QC Inspector': '✅'}
    ]

if __name__ == "__main__":
    render()