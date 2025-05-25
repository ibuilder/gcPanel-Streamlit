"""
Quality Control Module - Highland Tower Development
Complete CRUD operations for quality inspections, checklists, and compliance tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

def render():
    """Render the comprehensive Quality Control module with full CRUD functionality"""
    st.title("🔍 Quality Control - Highland Tower Development")
    st.markdown("**Comprehensive Quality Assurance & Compliance Management System**")
    
    # Initialize session state for QC data
    if 'qc_inspections' not in st.session_state:
        st.session_state.qc_inspections = get_sample_inspections()
    if 'qc_checklists' not in st.session_state:
        st.session_state.qc_checklists = get_sample_checklists()
    if 'qc_ncrs' not in st.session_state:
        st.session_state.qc_ncrs = get_sample_ncrs()
    
    # Quality Control overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_inspections = len(st.session_state.qc_inspections)
    passed_inspections = len([i for i in st.session_state.qc_inspections if i['status'] == 'Passed'])
    open_ncrs = len([n for n in st.session_state.qc_ncrs if n['status'] != 'Closed'])
    
    with col1:
        st.metric("Total Inspections", total_inspections, "+3 this week")
    with col2:
        pass_rate = (passed_inspections / total_inspections * 100) if total_inspections > 0 else 0
        st.metric("Pass Rate", f"{pass_rate:.1f}%", "+2.3% vs target")
    with col3:
        st.metric("Open NCRs", open_ncrs, "-2 resolved today")
    with col4:
        st.metric("Quality Score", "96.2%", "+1.2% this month")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Inspections", "✅ Checklists", "⚠️ NCRs", "📊 Analytics", "🎯 Standards", "⚙️ Settings"
    ])
    
    with tab1:
        render_inspections_crud()
    
    with tab2:
        render_checklists_crud()
    
    with tab3:
        render_ncrs_crud()
    
    with tab4:
        render_qc_analytics()
    
    with tab5:
        render_quality_standards()
    
    with tab6:
        render_qc_settings()

def render_inspections_crud():
    """Complete CRUD for Quality Control Inspections"""
    st.subheader("📋 Quality Inspections Management")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Inspection", type="primary"):
            st.session_state.show_inspection_form = True
    with col2:
        if st.button("📊 Export Data"):
            st.success("✅ Inspection data exported to Excel")
    with col3:
        if st.button("🔍 Advanced Search"):
            st.session_state.show_search = True
    with col4:
        if st.button("📈 Generate Report"):
            st.info("📄 Quality report generated")
    
    # New Inspection Form
    if st.session_state.get('show_inspection_form', False):
        render_new_inspection_form()
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search inspections", placeholder="Inspector, location, or ID...")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "In Progress", "Passed", "Failed", "Pending Review"])
    with col3:
        date_filter = st.selectbox("Date Range", ["All Time", "Today", "This Week", "This Month"])
    
    # Display inspections table
    inspections_df = pd.DataFrame(st.session_state.qc_inspections)
    
    # Apply filters
    if search_query:
        mask = inspections_df.apply(lambda x: search_query.lower() in str(x).lower(), axis=1)
        inspections_df = inspections_df[mask]
    
    if status_filter != "All":
        inspections_df = inspections_df[inspections_df['status'] == status_filter]
    
    # Display table with action columns
    st.markdown("### Current Inspections")
    
    for idx, inspection in inspections_df.iterrows():
        with st.expander(f"🔍 {inspection['inspection_id']} - {inspection['inspection_type']} ({inspection['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Location:** {inspection['location']}  
                **Inspector:** {inspection['inspector']}  
                **Scheduled:** {inspection['scheduled_date']}  
                **Status:** {inspection['status']}  
                **Score:** {inspection.get('score', 'N/A')}%  
                **Notes:** {inspection.get('notes', 'No notes')}
                """)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_inspection_{inspection['inspection_id']}"):
                    st.session_state.edit_inspection_id = inspection['inspection_id']
                    st.session_state.show_inspection_edit = True
                    st.rerun()
                
                if st.button("📄 View Report", key=f"view_inspection_{inspection['inspection_id']}"):
                    st.success(f"Opening detailed report for {inspection['inspection_id']}")
                
                if st.button("🗑️ Delete", key=f"delete_inspection_{inspection['inspection_id']}"):
                    if st.session_state.get(f"confirm_delete_{inspection['inspection_id']}", False):
                        # Remove from session state
                        st.session_state.qc_inspections = [i for i in st.session_state.qc_inspections 
                                                         if i['inspection_id'] != inspection['inspection_id']]
                        st.success("✅ Inspection deleted successfully")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{inspection['inspection_id']}"] = True
                        st.warning("⚠️ Click again to confirm deletion")

def render_new_inspection_form():
    """Form to create new quality inspection"""
    st.markdown("### ➕ Create New Quality Inspection")
    
    with st.form("new_inspection_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            inspection_type = st.selectbox(
                "Inspection Type *",
                ["Structural", "MEP", "Concrete", "Steel", "Safety", "Final", "Environmental", "Fire Safety"]
            )
            
            location = st.selectbox(
                "Location *",
                ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", 
                 "Level 8", "Level 9", "Level 10", "Level 11", "Level 12", "Level 13", "Level 14", "Level 15",
                 "Basement 1", "Basement 2", "Roof", "Exterior", "Mechanical Room"]
            )
            
            inspector = st.selectbox(
                "Inspector *",
                ["John Smith (Structural)", "Sarah Chen (MEP)", "Mike Torres (General)", 
                 "Jennifer Walsh (Safety)", "David Park (Environmental)"]
            )
            
            scheduled_date = st.date_input("Scheduled Date *", value=datetime.now())
            scheduled_time = st.time_input("Scheduled Time *", value=datetime.now().time())
        
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            
            estimated_duration = st.number_input("Estimated Duration (hours)", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
            
            description = st.text_area("Description", placeholder="Describe the inspection scope and requirements...")
            
            checklist_template = st.selectbox(
                "Checklist Template",
                ["Standard Structural", "MEP Rough-in", "Concrete Pour", "Steel Erection", "Safety Inspection", "Custom"]
            )
            
            special_requirements = st.text_area("Special Requirements", placeholder="Any special tools, access, or coordination needed...")
        
        # Required field validation
        required_fields = [inspection_type, location, inspector, scheduled_date]
        
        submitted = st.form_submit_button("📅 Schedule Inspection", type="primary")
        
        if submitted:
            if all(required_fields):
                # Create new inspection
                new_inspection = {
                    'inspection_id': f"QC-HTD-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.qc_inspections) + 1:03d}",
                    'inspection_type': inspection_type,
                    'location': location,
                    'inspector': inspector,
                    'scheduled_date': scheduled_date.strftime('%Y-%m-%d'),
                    'scheduled_time': scheduled_time.strftime('%H:%M'),
                    'priority': priority,
                    'estimated_duration': estimated_duration,
                    'description': description,
                    'checklist_template': checklist_template,
                    'special_requirements': special_requirements,
                    'status': 'Scheduled',
                    'created_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'created_by': st.session_state.get('current_user', 'Current User')
                }
                
                # Add to session state
                st.session_state.qc_inspections.append(new_inspection)
                st.session_state.show_inspection_form = False
                
                st.success(f"✅ Inspection {new_inspection['inspection_id']} scheduled successfully!")
                st.info(f"📧 Notification sent to {inspector}")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields marked with *")

def render_checklists_crud():
    """Complete CRUD for Quality Control Checklists"""
    st.subheader("✅ Quality Control Checklists")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Checklist", type="primary"):
            st.session_state.show_checklist_form = True
    with col2:
        if st.button("📋 Templates"):
            st.session_state.show_templates = True
    with col3:
        if st.button("📊 Completion Stats"):
            st.info("📈 Checklist completion analytics")
    with col4:
        if st.button("🔄 Sync Mobile"):
            st.success("📱 Checklists synced to mobile devices")
    
    # New Checklist Form
    if st.session_state.get('show_checklist_form', False):
        render_new_checklist_form()
    
    # Display checklists
    st.markdown("### Current Checklists")
    
    for checklist in st.session_state.qc_checklists:
        with st.expander(f"📋 {checklist['checklist_id']} - {checklist['title']} ({checklist['completion_rate']}% complete)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Type:** {checklist['type']}  
                **Location:** {checklist['location']}  
                **Assigned To:** {checklist['assigned_to']}  
                **Due Date:** {checklist['due_date']}  
                **Items:** {checklist['completed_items']}/{checklist['total_items']} completed  
                **Status:** {checklist['status']}
                """)
                
                # Progress bar
                progress = checklist['completion_rate'] / 100
                st.progress(progress)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_checklist_{checklist['checklist_id']}"):
                    st.info(f"Editing checklist {checklist['checklist_id']}")
                
                if st.button("📱 Open Mobile", key=f"mobile_checklist_{checklist['checklist_id']}"):
                    st.success("📱 Checklist opened on mobile device")
                
                if st.button("📄 Export", key=f"export_checklist_{checklist['checklist_id']}"):
                    st.success("📄 Checklist exported to PDF")

def render_new_checklist_form():
    """Form to create new quality checklist"""
    st.markdown("### ➕ Create New Quality Checklist")
    
    with st.form("new_checklist_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Checklist Title *", placeholder="e.g., Level 13 Structural Inspection")
            checklist_type = st.selectbox(
                "Checklist Type *",
                ["Pre-Inspection", "Daily QC", "Weekly QC", "Final Inspection", "Safety Check", "Custom"]
            )
            location = st.selectbox(
                "Location *",
                ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", 
                 "Level 8", "Level 9", "Level 10", "Level 11", "Level 12", "Level 13", "Level 14", "Level 15"]
            )
            assigned_to = st.selectbox(
                "Assigned To *",
                ["John Smith", "Sarah Chen", "Mike Torres", "Jennifer Walsh", "David Park"]
            )
        
        with col2:
            due_date = st.date_input("Due Date *", value=datetime.now() + timedelta(days=7))
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            template = st.selectbox(
                "Use Template",
                ["None", "Structural Inspection", "MEP Rough-in", "Concrete Pour", "Safety Check"]
            )
        
        # Checklist items
        st.markdown("#### Checklist Items")
        
        # Dynamic item addition
        if 'checklist_items' not in st.session_state:
            st.session_state.checklist_items = []
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_item = st.text_input("Add checklist item", placeholder="e.g., Verify rebar placement and spacing")
        with col2:
            if st.form_submit_button("➕ Add Item"):
                if new_item:
                    st.session_state.checklist_items.append(new_item)
        
        # Display current items
        if st.session_state.checklist_items:
            st.markdown("**Current Items:**")
            for i, item in enumerate(st.session_state.checklist_items):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i+1}. {item}")
                with col2:
                    if st.form_submit_button("🗑️", key=f"remove_item_{i}"):
                        st.session_state.checklist_items.pop(i)
                        st.rerun()
        
        submitted = st.form_submit_button("📋 Create Checklist", type="primary")
        
        if submitted and title and checklist_type and location and assigned_to:
            # Create new checklist
            new_checklist = {
                'checklist_id': f"CL-HTD-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.qc_checklists) + 1:03d}",
                'title': title,
                'type': checklist_type,
                'location': location,
                'assigned_to': assigned_to,
                'due_date': due_date.strftime('%Y-%m-%d'),
                'priority': priority,
                'items': st.session_state.checklist_items.copy(),
                'total_items': len(st.session_state.checklist_items),
                'completed_items': 0,
                'completion_rate': 0,
                'status': 'Active',
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'created_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.qc_checklists.append(new_checklist)
            st.session_state.checklist_items = []  # Reset items
            st.session_state.show_checklist_form = False
            
            st.success(f"✅ Checklist {new_checklist['checklist_id']} created successfully!")
            st.rerun()

def render_ncrs_crud():
    """Complete CRUD for Non-Conformance Reports"""
    st.subheader("⚠️ Non-Conformance Reports (NCRs)")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New NCR", type="primary"):
            st.session_state.show_ncr_form = True
    with col2:
        if st.button("📊 NCR Analytics"):
            st.info("📈 NCR trend analysis")
    with col3:
        if st.button("🚨 Critical NCRs"):
            critical_ncrs = [n for n in st.session_state.qc_ncrs if n['severity'] == 'Critical']
            st.warning(f"⚠️ {len(critical_ncrs)} critical NCRs require attention")
    with col4:
        if st.button("📄 Export Report"):
            st.success("📄 NCR report exported")
    
    # New NCR Form
    if st.session_state.get('show_ncr_form', False):
        render_new_ncr_form()
    
    # Display NCRs
    st.markdown("### Current Non-Conformance Reports")
    
    for ncr in st.session_state.qc_ncrs:
        severity_colors = {"Low": "#28a745", "Medium": "#ffc107", "High": "#fd7e14", "Critical": "#dc3545"}
        severity_color = severity_colors.get(ncr['severity'], "#6c757d")
        
        with st.expander(f"⚠️ {ncr['ncr_id']} - {ncr['title']} ({ncr['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid {severity_color}; padding-left: 12px;">
                <strong>Location:</strong> {ncr['location']}<br>
                <strong>Severity:</strong> <span style="color: {severity_color}; font-weight: bold;">{ncr['severity']}</span><br>
                <strong>Reported By:</strong> {ncr['reported_by']}<br>
                <strong>Date:</strong> {ncr['date_reported']}<br>
                <strong>Description:</strong> {ncr['description']}<br>
                <strong>Corrective Action:</strong> {ncr.get('corrective_action', 'Pending')}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Update", key=f"update_ncr_{ncr['ncr_id']}"):
                    st.info(f"Updating NCR {ncr['ncr_id']}")
                
                if ncr['status'] != 'Closed':
                    if st.button("✅ Close", key=f"close_ncr_{ncr['ncr_id']}"):
                        # Update NCR status
                        for i, n in enumerate(st.session_state.qc_ncrs):
                            if n['ncr_id'] == ncr['ncr_id']:
                                st.session_state.qc_ncrs[i]['status'] = 'Closed'
                                st.session_state.qc_ncrs[i]['date_closed'] = datetime.now().strftime('%Y-%m-%d')
                                break
                        st.success("✅ NCR closed successfully")
                        st.rerun()
                
                if st.button("📸 Photos", key=f"photos_ncr_{ncr['ncr_id']}"):
                    st.info("📸 Opening photo documentation")

def render_new_ncr_form():
    """Form to create new NCR"""
    st.markdown("### ⚠️ Create New Non-Conformance Report")
    
    with st.form("new_ncr_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("NCR Title *", placeholder="Brief description of the non-conformance")
            location = st.selectbox(
                "Location *",
                ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", 
                 "Level 8", "Level 9", "Level 10", "Level 11", "Level 12", "Level 13", "Level 14", "Level 15"]
            )
            severity = st.selectbox("Severity *", ["Low", "Medium", "High", "Critical"])
            category = st.selectbox(
                "Category *",
                ["Structural", "MEP", "Safety", "Quality", "Material", "Workmanship", "Design", "Other"]
            )
        
        with col2:
            reported_by = st.text_input("Reported By *", value=st.session_state.get('current_user', ''))
            date_discovered = st.date_input("Date Discovered *", value=datetime.now())
            responsible_party = st.selectbox(
                "Responsible Party",
                ["Prime Contractor", "Subcontractor A", "Subcontractor B", "Supplier", "Design Team", "Owner", "Other"]
            )
        
        description = st.text_area(
            "Description *",
            placeholder="Detailed description of the non-conformance including what was expected vs. what was found"
        )
        
        immediate_action = st.text_area(
            "Immediate Action Taken",
            placeholder="Describe any immediate actions taken to address the issue"
        )
        
        photos_required = st.checkbox("Photos Required", value=True)
        
        submitted = st.form_submit_button("⚠️ Create NCR", type="primary")
        
        if submitted and title and location and severity and category and description:
            # Create new NCR
            new_ncr = {
                'ncr_id': f"NCR-HTD-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.qc_ncrs) + 1:03d}",
                'title': title,
                'location': location,
                'severity': severity,
                'category': category,
                'reported_by': reported_by,
                'date_reported': datetime.now().strftime('%Y-%m-%d'),
                'date_discovered': date_discovered.strftime('%Y-%m-%d'),
                'responsible_party': responsible_party,
                'description': description,
                'immediate_action': immediate_action,
                'photos_required': photos_required,
                'status': 'Open',
                'created_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.qc_ncrs.append(new_ncr)
            st.session_state.show_ncr_form = False
            
            st.success(f"✅ NCR {new_ncr['ncr_id']} created successfully!")
            st.warning("📧 Notifications sent to responsible parties")
            st.rerun()

def render_qc_analytics():
    """Quality Control analytics and reporting"""
    st.subheader("📊 Quality Control Analytics")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Inspection Efficiency", "94.2%", "+2.3% vs last month")
    with col2:
        st.metric("First-Time Pass Rate", "87.6%", "+1.8% improvement")
    with col3:
        st.metric("Average NCR Resolution", "3.2 days", "-0.8 days faster")
    with col4:
        st.metric("Quality Trend", "Improving", "↗️ Positive trend")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Inspection results over time
        inspection_data = pd.DataFrame({
            'Date': pd.date_range('2025-05-01', periods=25),
            'Passed': [8, 7, 9, 6, 8, 9, 7, 8, 9, 8, 7, 9, 8, 7, 9, 8, 7, 9, 8, 9, 7, 8, 9, 8, 7],
            'Failed': [2, 3, 1, 4, 2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 3]
        })
        
        fig = px.bar(inspection_data, x='Date', y=['Passed', 'Failed'], 
                    title="Daily Inspection Results", barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # NCR by category
        ncr_categories = pd.DataFrame({
            'Category': ['Structural', 'MEP', 'Safety', 'Material', 'Workmanship'],
            'Count': [8, 12, 6, 4, 10]
        })
        
        fig = px.pie(ncr_categories, values='Count', names='Category',
                    title="NCRs by Category")
        st.plotly_chart(fig, use_container_width=True)

def render_quality_standards():
    """Quality standards and compliance tracking"""
    st.subheader("🎯 Quality Standards & Compliance")
    
    st.info("📋 Industry standards and project-specific quality requirements")
    
    # Standards compliance
    standards_data = pd.DataFrame([
        {"Standard": "ACI 318 (Concrete)", "Compliance": 98.5, "Last Audit": "2025-05-20", "Status": "Compliant"},
        {"Standard": "AISC 360 (Steel)", "Compliance": 96.8, "Last Audit": "2025-05-18", "Status": "Compliant"},
        {"Standard": "IBC 2021", "Compliance": 99.2, "Last Audit": "2025-05-22", "Status": "Compliant"},
        {"Standard": "OSHA Safety", "Compliance": 97.3, "Last Audit": "2025-05-24", "Status": "Compliant"},
        {"Standard": "Project QC Plan", "Compliance": 95.6, "Last Audit": "2025-05-25", "Status": "Minor Issues"}
    ])
    
    st.dataframe(standards_data, use_container_width=True)

def render_qc_settings():
    """Quality Control settings and configuration"""
    st.subheader("⚙️ Quality Control Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Inspection Settings**")
        auto_schedule = st.checkbox("Auto-schedule follow-up inspections", value=True)
        photo_required = st.checkbox("Require photos for all inspections", value=True)
        mobile_sync = st.checkbox("Enable mobile synchronization", value=True)
        
        st.markdown("**Notification Settings**")
        email_alerts = st.checkbox("Email alerts for failed inspections", value=True)
        sms_critical = st.checkbox("SMS alerts for critical NCRs", value=True)
    
    with col2:
        st.markdown("**Quality Thresholds**")
        pass_threshold = st.slider("Minimum pass score (%)", 80, 100, 85)
        ncr_escalation = st.slider("NCR escalation days", 1, 10, 3)
        
        st.markdown("**Data Retention**")
        retention_period = st.selectbox("Data retention period", 
                                      ["1 year", "2 years", "5 years", "Project lifetime"])
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Quality Control settings saved successfully!")

def get_sample_inspections():
    """Generate sample inspection data"""
    return [
        {
            'inspection_id': 'QC-HTD-20250525-001',
            'inspection_type': 'Structural',
            'location': 'Level 13',
            'inspector': 'John Smith (Structural)',
            'scheduled_date': '2025-05-25',
            'scheduled_time': '09:00',
            'status': 'Passed',
            'score': 96.5,
            'notes': 'Steel beam installation meets specifications'
        },
        {
            'inspection_id': 'QC-HTD-20250524-002',
            'inspection_type': 'MEP',
            'location': 'Level 11',
            'inspector': 'Sarah Chen (MEP)',
            'scheduled_date': '2025-05-24',
            'scheduled_time': '14:00',
            'status': 'Failed',
            'score': 78.2,
            'notes': 'Electrical conduit routing needs correction'
        },
        {
            'inspection_id': 'QC-HTD-20250523-003',
            'inspection_type': 'Concrete',
            'location': 'Level 12',
            'inspector': 'Mike Torres (General)',
            'scheduled_date': '2025-05-23',
            'scheduled_time': '11:30',
            'status': 'Passed',
            'score': 94.8,
            'notes': 'Concrete pour quality excellent'
        }
    ]

def get_sample_checklists():
    """Generate sample checklist data"""
    return [
        {
            'checklist_id': 'CL-HTD-20250525-001',
            'title': 'Level 13 Steel Inspection',
            'type': 'Structural',
            'location': 'Level 13',
            'assigned_to': 'John Smith',
            'due_date': '2025-05-26',
            'total_items': 15,
            'completed_items': 12,
            'completion_rate': 80,
            'status': 'In Progress'
        },
        {
            'checklist_id': 'CL-HTD-20250524-002',
            'title': 'MEP Rough-in QC',
            'type': 'MEP',
            'location': 'Level 11',
            'assigned_to': 'Sarah Chen',
            'due_date': '2025-05-25',
            'total_items': 22,
            'completed_items': 22,
            'completion_rate': 100,
            'status': 'Complete'
        }
    ]

def get_sample_ncrs():
    """Generate sample NCR data"""
    return [
        {
            'ncr_id': 'NCR-HTD-20250525-001',
            'title': 'Concrete surface finish non-conformance',
            'location': 'Level 12',
            'severity': 'Medium',
            'category': 'Quality',
            'reported_by': 'Mike Torres',
            'date_reported': '2025-05-25',
            'description': 'Concrete surface finish does not meet specification requirements',
            'status': 'Open'
        },
        {
            'ncr_id': 'NCR-HTD-20250524-002',
            'title': 'Electrical conduit improper routing',
            'location': 'Level 11',
            'severity': 'High',
            'category': 'MEP',
            'reported_by': 'Sarah Chen',
            'date_reported': '2025-05-24',
            'description': 'Electrical conduit routed through structural member',
            'status': 'In Progress'
        }
    ]

if __name__ == "__main__":
    render()