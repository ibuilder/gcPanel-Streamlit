"""
User Management Module for gcPanel Highland Tower Development
Enterprise-grade user administration with role-based access control
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import secrets

def render():
    """Render the User Management admin module"""
    
    st.markdown("""
    <div class="admin-header">
        <h1>👥 User Management</h1>
        <p>Highland Tower Development - Team Administration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Management Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Active Users", "➕ Add User", "🔐 Roles & Permissions", "📊 User Analytics"])
    
    with tab1:
        st.markdown("### Current Highland Tower Team")
        
        # Sample user data for Highland Tower Development
        users_data = {
            'User ID': ['HTD-001', 'HTD-002', 'HTD-003', 'HTD-004', 'HTD-005', 'HTD-006'],
            'Full Name': ['Jennifer Walsh, AIA', 'Sarah Chen, PE', 'Mike Rodriguez', 'David Kim', 'Lisa Wong', 'Alex Thompson'],
            'Email': ['jennifer.walsh@highlandtower.com', 'sarah.chen@highlandtower.com', 'mike.rodriguez@highlandtower.com', 
                     'david.kim@highlandtower.com', 'lisa.wong@highlandtower.com', 'alex.thompson@highlandtower.com'],
            'Role': ['Project Manager', 'Structural Engineer', 'Site Supervisor', 'MEP Supervisor', 'Safety Manager', 'Cost Estimator'],
            'Department': ['Management', 'Engineering', 'Field Operations', 'MEP', 'Safety', 'Cost Management'],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active'],
            'Last Login': ['2 hours ago', '5 hours ago', '1 day ago', '3 hours ago', '1 hour ago', '4 hours ago'],
            'Phone': ['555-0101', '555-0102', '555-0103', '555-0104', '555-0105', '555-0106']
        }
        
        df_users = pd.DataFrame(users_data)
        
        # Search and filter
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search users", placeholder="Name, email, or role...")
        with col2:
            filter_role = st.selectbox("Filter by Role", ["All Roles", "Project Manager", "Engineer", "Supervisor", "Safety Manager"])
        with col3:
            filter_status = st.selectbox("Filter by Status", ["All Status", "Active", "Inactive", "Pending"])
        
        # Apply filters
        filtered_df = df_users.copy()
        if search_term:
            mask = filtered_df.apply(lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)
            filtered_df = filtered_df[mask]
        
        # Display users table
        st.markdown('<div class="admin-table">', unsafe_allow_html=True)
        
        for index, user in filtered_df.iterrows():
            with st.expander(f"👤 {user['Full Name']} - {user['Role']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**User ID:** {user['User ID']}")
                    st.markdown(f"**Email:** {user['Email']}")
                    st.markdown(f"**Department:** {user['Department']}")
                    st.markdown(f"**Phone:** {user['Phone']}")
                
                with col2:
                    st.markdown(f"**Status:** <span class='status-badge active'>{user['Status']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Last Login:** {user['Last Login']}")
                    
                    # Action buttons
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    with col_btn1:
                        if st.button("✏️ Edit", key=f"edit_{user['User ID']}"):
                            st.info(f"Editing {user['Full Name']}")
                    with col_btn2:
                        if st.button("🔒 Reset Password", key=f"reset_{user['User ID']}"):
                            st.success(f"Password reset email sent to {user['Email']}")
                    with col_btn3:
                        if st.button("📧 Send Message", key=f"message_{user['User ID']}"):
                            st.info(f"Opening message composer for {user['Full Name']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Add New Team Member")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_full_name = st.text_input("Full Name*", placeholder="John Smith, PE")
                new_email = st.text_input("Email Address*", placeholder="john.smith@highlandtower.com")
                new_phone = st.text_input("Phone Number", placeholder="555-0107")
                new_employee_id = st.text_input("Employee ID", placeholder="HTD-007")
            
            with col2:
                new_role = st.selectbox("Role*", [
                    "Project Manager", "Assistant Project Manager", 
                    "Structural Engineer", "MEP Engineer", "Civil Engineer",
                    "Site Supervisor", "Assistant Supervisor", "Foreman",
                    "Safety Manager", "Safety Coordinator",
                    "Cost Estimator", "Scheduler", "Quality Control",
                    "Document Controller", "Admin Assistant"
                ])
                new_department = st.selectbox("Department*", [
                    "Management", "Engineering", "Field Operations", 
                    "Safety", "Cost Management", "Quality Control", "Administration"
                ])
                new_access_level = st.selectbox("Access Level*", [
                    "Full Access", "Manager Access", "Standard Access", "Limited Access", "View Only"
                ])
                start_date = st.date_input("Start Date", datetime.now().date())
            
            # Additional permissions
            st.markdown("**Module Access Permissions:**")
            col_perm1, col_perm2, col_perm3 = st.columns(3)
            
            with col_perm1:
                dashboard_access = st.checkbox("Dashboard", value=True)
                preconstruction_access = st.checkbox("PreConstruction", value=True)
                engineering_access = st.checkbox("Engineering", value=True)
            
            with col_perm2:
                field_ops_access = st.checkbox("Field Operations", value=True)
                safety_access = st.checkbox("Safety", value=True)
                cost_mgmt_access = st.checkbox("Cost Management", value=True)
            
            with col_perm3:
                contracts_access = st.checkbox("Contracts", value=False)
                bim_access = st.checkbox("BIM", value=False)
                admin_access = st.checkbox("Administration", value=False)
            
            submit_new_user = st.form_submit_button("➕ Add Team Member", use_container_width=True)
            
            if submit_new_user:
                if new_full_name and new_email and new_role and new_department:
                    st.success(f"✅ {new_full_name} has been added to the Highland Tower Development team!")
                    st.info(f"📧 Welcome email sent to {new_email} with login credentials")
                    st.info(f"🔐 Temporary password: {''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))}")
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab3:
        st.markdown("### Role-Based Access Control")
        
        # Role definitions
        roles_data = {
            'Role': ['Admin', 'Project Manager', 'Engineer', 'Supervisor', 'Safety Manager', 'Standard User'],
            'Users': [1, 2, 3, 2, 1, 8],
            'Dashboard': ['✅', '✅', '✅', '✅', '✅', '✅'],
            'Engineering': ['✅', '✅', '✅', '⚠️', '❌', '👁️'],
            'Cost Management': ['✅', '✅', '⚠️', '❌', '❌', '👁️'],
            'Administration': ['✅', '❌', '❌', '❌', '❌', '❌'],
            'Safety Override': ['✅', '✅', '❌', '❌', '✅', '❌']
        }
        
        df_roles = pd.DataFrame(roles_data)
        st.dataframe(df_roles, use_container_width=True)
        
        st.markdown("""
        **Legend:**
        - ✅ Full Access
        - ⚠️ Limited Access  
        - 👁️ Read Only
        - ❌ No Access
        """)
        
        # Role management
        st.markdown("### Create Custom Role")
        with st.form("create_role_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                role_name = st.text_input("Role Name", placeholder="Senior Engineer")
                role_description = st.text_area("Description", placeholder="Senior engineering role with project oversight")
            
            with col2:
                st.markdown("**Permissions:**")
                permissions = {}
                modules = ["Dashboard", "PreConstruction", "Engineering", "Field Operations", "Safety", "Cost Management", "Contracts", "BIM", "Analytics", "Documents", "Administration"]
                
                for module in modules:
                    permissions[module] = st.selectbox(f"{module}", ["No Access", "Read Only", "Limited Access", "Full Access"], key=f"perm_{module}")
            
            if st.form_submit_button("Create Role"):
                st.success(f"✅ Role '{role_name}' created successfully!")
    
    with tab4:
        st.markdown("### User Analytics & Activity")
        
        # User activity metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="admin-metric">
                <h3>17</h3>
                <p>Total Users</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="admin-metric">
                <h3>15</h3>
                <p>Active Today</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="admin-metric">
                <h3>94%</h3>
                <p>Login Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="admin-metric">
                <h3>2.3h</h3>
                <p>Avg Session</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activity
        st.markdown("### Recent User Activity")
        
        activity_data = {
            'Time': ['10:30 AM', '10:15 AM', '09:45 AM', '09:30 AM', '09:15 AM'],
            'User': ['Sarah Chen, PE', 'Mike Rodriguez', 'Jennifer Walsh', 'David Kim', 'Lisa Wong'],
            'Action': ['Updated RFI-2025-045', 'Submitted Daily Report', 'Approved Change Order CO-012', 'Uploaded Safety Photos', 'Created Cost Report'],
            'Module': ['RFIs', 'Field Operations', 'Contracts', 'Safety', 'Cost Management'],
            'IP Address': ['192.168.1.45', '192.168.1.67', '192.168.1.23', '192.168.1.89', '192.168.1.34']
        }
        
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True)
        
        # Export options
        st.markdown("### Export User Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export User List", use_container_width=True):
                st.success("User list exported to Excel")
        
        with col2:
            if st.button("📈 Export Activity Report", use_container_width=True):
                st.success("Activity report generated")
        
        with col3:
            if st.button("🔐 Export Access Report", use_container_width=True):
                st.success("Access permissions report created")

if __name__ == "__main__":
    render()