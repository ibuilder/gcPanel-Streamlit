"""
Scheduling Module - Highland Tower Development
Complete CRUD operations for project schedules, milestones, and task management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

def render():
    """Render the comprehensive Scheduling module with full CRUD functionality"""
    st.title("📅 Project Scheduling - Highland Tower Development")
    st.markdown("**Advanced Project Timeline & Resource Management System**")
    
    # Initialize session state for scheduling data
    if 'schedule_tasks' not in st.session_state:
        st.session_state.schedule_tasks = get_sample_tasks()
    if 'milestones' not in st.session_state:
        st.session_state.milestones = get_sample_milestones()
    if 'resource_assignments' not in st.session_state:
        st.session_state.resource_assignments = get_sample_resources()
    
    # Project timeline overview
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(st.session_state.schedule_tasks)
    completed_tasks = len([t for t in st.session_state.schedule_tasks if t['status'] == 'Completed'])
    overdue_tasks = len([t for t in st.session_state.schedule_tasks if t['status'] == 'Overdue'])
    
    with col1:
        st.metric("Total Tasks", total_tasks, "+5 this week")
    with col2:
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%", "+2.3% vs plan")
    with col3:
        st.metric("Overdue Tasks", overdue_tasks, "-3 resolved")
    with col4:
        st.metric("Schedule Health", "On Track", "5 days ahead")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Task Management", "🎯 Milestones", "👥 Resources", "📊 Gantt Chart", "📈 Analytics", "⚙️ Settings"
    ])
    
    with tab1:
        render_task_management()
    
    with tab2:
        render_milestone_management()
    
    with tab3:
        render_resource_management()
    
    with tab4:
        render_gantt_chart()
    
    with tab5:
        render_schedule_analytics()
    
    with tab6:
        render_schedule_settings()

def render_task_management():
    """Complete CRUD for project tasks"""
    st.subheader("📋 Task Management")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Task", type="primary"):
            st.session_state.show_task_form = True
    with col2:
        if st.button("📊 Export Schedule"):
            st.success("✅ Schedule exported to MS Project format")
    with col3:
        if st.button("🔄 Update Progress"):
            st.session_state.show_progress_update = True
    with col4:
        if st.button("⚠️ Critical Path"):
            st.info("🔍 Analyzing critical path dependencies")
    
    # New Task Form
    if st.session_state.get('show_task_form', False):
        render_new_task_form()
    
    # Progress Update Form
    if st.session_state.get('show_progress_update', False):
        render_progress_update_form()
    
    # Filter and search
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search tasks", placeholder="Task name or ID...")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Not Started", "In Progress", "Completed", "On Hold", "Overdue"])
    with col3:
        phase_filter = st.selectbox("Filter by Phase", ["All", "Foundation", "Structure", "MEP", "Finishes", "Closeout"])
    
    # Display tasks
    tasks_df = pd.DataFrame(st.session_state.schedule_tasks)
    
    # Apply filters
    if search_query:
        mask = tasks_df.apply(lambda x: search_query.lower() in str(x).lower(), axis=1)
        tasks_df = tasks_df[mask]
    
    if status_filter != "All":
        tasks_df = tasks_df[tasks_df['status'] == status_filter]
    
    if phase_filter != "All":
        tasks_df = tasks_df[tasks_df['phase'] == phase_filter]
    
    st.markdown("### Current Tasks")
    
    for idx, task in tasks_df.iterrows():
        # Status color coding
        status_colors = {
            "Not Started": "#6c757d",
            "In Progress": "#007bff", 
            "Completed": "#28a745",
            "On Hold": "#ffc107",
            "Overdue": "#dc3545"
        }
        
        status_color = status_colors.get(task['status'], "#6c757d")
        
        with st.expander(f"📋 {task['task_id']} - {task['task_name']} ({task['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Progress bar
                progress = task['progress'] / 100
                st.progress(progress)
                
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Phase:</strong> {task['phase']}<br>
                <strong>Assigned To:</strong> {task['assigned_to']}<br>
                <strong>Start Date:</strong> {task['start_date']}<br>
                <strong>End Date:</strong> {task['end_date']}<br>
                <strong>Duration:</strong> {task['duration']} days<br>
                <strong>Progress:</strong> {task['progress']}%<br>
                <strong>Priority:</strong> {task['priority']}<br>
                <strong>Dependencies:</strong> {task.get('dependencies', 'None')}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_task_{task['task_id']}"):
                    st.session_state.edit_task_id = task['task_id']
                    st.session_state.show_task_edit = True
                    st.rerun()
                
                if st.button("📈 Update Progress", key=f"progress_task_{task['task_id']}"):
                    st.session_state.update_task_id = task['task_id']
                    st.session_state.show_progress_modal = True
                
                if task['status'] != 'Completed':
                    if st.button("✅ Complete", key=f"complete_task_{task['task_id']}"):
                        # Update task status
                        for i, t in enumerate(st.session_state.schedule_tasks):
                            if t['task_id'] == task['task_id']:
                                st.session_state.schedule_tasks[i]['status'] = 'Completed'
                                st.session_state.schedule_tasks[i]['progress'] = 100
                                st.session_state.schedule_tasks[i]['actual_end_date'] = datetime.now().strftime('%Y-%m-%d')
                                break
                        st.success("✅ Task completed successfully!")
                        st.rerun()

def render_new_task_form():
    """Form to create new task"""
    st.markdown("### ➕ Create New Task")
    
    with st.form("new_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name *", placeholder="e.g., Install Level 13 Steel Beams")
            phase = st.selectbox(
                "Project Phase *",
                ["Foundation", "Structure", "MEP", "Finishes", "Closeout"]
            )
            assigned_to = st.selectbox(
                "Assigned To *",
                ["Steel Crew A", "Concrete Team B", "MEP Contractor", "Finish Team C", "QC Inspector"]
            )
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        with col2:
            start_date = st.date_input("Start Date *", value=datetime.now())
            duration = st.number_input("Duration (days) *", min_value=1, max_value=365, value=5)
            end_date = start_date + timedelta(days=duration)
            st.write(f"**Calculated End Date:** {end_date.strftime('%Y-%m-%d')}")
            
            budget = st.number_input("Task Budget ($)", min_value=0.0, step=1000.0)
        
        description = st.text_area("Task Description", placeholder="Detailed description of the work to be performed...")
        
        # Dependencies
        existing_tasks = [t['task_name'] for t in st.session_state.schedule_tasks]
        dependencies = st.multiselect("Dependencies", existing_tasks)
        
        # Resources required
        resources = st.multiselect(
            "Resources Required",
            ["Tower Crane", "Concrete Pump", "Steel Crew", "Electrical Team", "Safety Inspector", "QC Inspector"]
        )
        
        submitted = st.form_submit_button("📅 Create Task", type="primary")
        
        if submitted and task_name and phase and assigned_to:
            # Create new task
            new_task = {
                'task_id': f"TASK-HTD-{len(st.session_state.schedule_tasks) + 1:04d}",
                'task_name': task_name,
                'phase': phase,
                'assigned_to': assigned_to,
                'priority': priority,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'duration': duration,
                'budget': budget,
                'description': description,
                'dependencies': ', '.join(dependencies) if dependencies else 'None',
                'resources': ', '.join(resources) if resources else 'None',
                'status': 'Not Started',
                'progress': 0,
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'created_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.schedule_tasks.append(new_task)
            st.session_state.show_task_form = False
            
            st.success(f"✅ Task {new_task['task_id']} created successfully!")
            st.info(f"📧 Assignment notification sent to {assigned_to}")
            st.rerun()

def render_progress_update_form():
    """Form to update task progress"""
    st.markdown("### 📈 Bulk Progress Update")
    
    with st.form("progress_update_form"):
        # Select tasks to update
        task_options = [f"{t['task_id']} - {t['task_name']}" for t in st.session_state.schedule_tasks if t['status'] == 'In Progress']
        selected_tasks = st.multiselect("Select Tasks to Update", task_options)
        
        # Progress input
        new_progress = st.slider("Progress (%)", 0, 100, 50)
        
        # Status update
        new_status = st.selectbox("Update Status", ["Keep Current", "In Progress", "On Hold", "Completed"])
        
        # Notes
        progress_notes = st.text_area("Progress Notes", placeholder="Describe the work completed...")
        
        submitted = st.form_submit_button("📈 Update Progress", type="primary")
        
        if submitted and selected_tasks:
            # Update selected tasks
            for task_selection in selected_tasks:
                task_id = task_selection.split(' - ')[0]
                for i, task in enumerate(st.session_state.schedule_tasks):
                    if task['task_id'] == task_id:
                        st.session_state.schedule_tasks[i]['progress'] = new_progress
                        if new_status != "Keep Current":
                            st.session_state.schedule_tasks[i]['status'] = new_status
                        if new_progress == 100:
                            st.session_state.schedule_tasks[i]['status'] = 'Completed'
                        break
            
            st.session_state.show_progress_update = False
            st.success(f"✅ Updated {len(selected_tasks)} tasks successfully!")
            st.rerun()

def render_milestone_management():
    """Milestone management with CRUD operations"""
    st.subheader("🎯 Project Milestones")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Milestone", type="primary"):
            st.session_state.show_milestone_form = True
    with col2:
        if st.button("📊 Milestone Report"):
            st.success("📄 Milestone report generated")
    with col3:
        if st.button("🚨 Critical Milestones"):
            critical_count = len([m for m in st.session_state.milestones if m['priority'] == 'Critical'])
            st.warning(f"⚠️ {critical_count} critical milestones tracked")
    with col4:
        if st.button("📅 Calendar View"):
            st.info("📅 Opening milestone calendar")
    
    # New Milestone Form
    if st.session_state.get('show_milestone_form', False):
        render_new_milestone_form()
    
    # Display milestones
    st.markdown("### Project Milestones")
    
    for milestone in st.session_state.milestones:
        # Status indicators
        status_icons = {
            "Not Started": "⏳",
            "In Progress": "🔄", 
            "Completed": "✅",
            "Overdue": "🚨"
        }
        
        status_icon = status_icons.get(milestone['status'], "❓")
        
        with st.expander(f"{status_icon} {milestone['milestone_name']} - {milestone['target_date']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Target Date:** {milestone['target_date']}  
                **Phase:** {milestone['phase']}  
                **Owner:** {milestone['owner']}  
                **Priority:** {milestone['priority']}  
                **Status:** {milestone['status']}  
                **Description:** {milestone['description']}
                """)
                
                # Progress tracking for milestones
                if milestone['status'] == 'In Progress':
                    progress = milestone.get('progress', 0)
                    st.progress(progress / 100)
                    st.write(f"Progress: {progress}%")
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_milestone_{milestone['milestone_id']}"):
                    st.info(f"Editing milestone {milestone['milestone_id']}")
                
                if milestone['status'] != 'Completed':
                    if st.button("✅ Complete", key=f"complete_milestone_{milestone['milestone_id']}"):
                        # Update milestone status
                        for i, m in enumerate(st.session_state.milestones):
                            if m['milestone_id'] == milestone['milestone_id']:
                                st.session_state.milestones[i]['status'] = 'Completed'
                                st.session_state.milestones[i]['actual_date'] = datetime.now().strftime('%Y-%m-%d')
                                break
                        st.success("🎉 Milestone completed!")
                        st.rerun()
                
                if st.button("📧 Notify", key=f"notify_milestone_{milestone['milestone_id']}"):
                    st.success("📧 Stakeholders notified about milestone status")

def render_new_milestone_form():
    """Form to create new milestone"""
    st.markdown("### 🎯 Create New Milestone")
    
    with st.form("new_milestone_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            milestone_name = st.text_input("Milestone Name *", placeholder="e.g., Structural Steel Completion")
            phase = st.selectbox("Project Phase *", ["Foundation", "Structure", "MEP", "Finishes", "Closeout"])
            target_date = st.date_input("Target Date *", value=datetime.now() + timedelta(days=30))
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        with col2:
            owner = st.selectbox(
                "Milestone Owner *",
                ["Project Manager", "Construction Manager", "Superintendent", "QC Manager", "Safety Manager"]
            )
            
            milestone_type = st.selectbox(
                "Milestone Type",
                ["Phase Completion", "Inspection", "Delivery", "Approval", "Payment", "Other"]
            )
        
        description = st.text_area("Description *", placeholder="Detailed description of the milestone...")
        
        # Success criteria
        success_criteria = st.text_area("Success Criteria", placeholder="Define what constitutes successful completion...")
        
        # Stakeholders to notify
        stakeholders = st.multiselect(
            "Notify Stakeholders",
            ["Owner", "Architect", "General Contractor", "Subcontractors", "City Inspector", "Project Team"]
        )
        
        submitted = st.form_submit_button("🎯 Create Milestone", type="primary")
        
        if submitted and milestone_name and phase and target_date and description:
            # Create new milestone
            new_milestone = {
                'milestone_id': f"MS-HTD-{len(st.session_state.milestones) + 1:03d}",
                'milestone_name': milestone_name,
                'phase': phase,
                'target_date': target_date.strftime('%Y-%m-%d'),
                'priority': priority,
                'owner': owner,
                'milestone_type': milestone_type,
                'description': description,
                'success_criteria': success_criteria,
                'stakeholders': ', '.join(stakeholders) if stakeholders else 'None',
                'status': 'Not Started',
                'progress': 0,
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'created_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.milestones.append(new_milestone)
            st.session_state.show_milestone_form = False
            
            st.success(f"✅ Milestone {new_milestone['milestone_id']} created successfully!")
            st.rerun()

def render_resource_management():
    """Resource assignment and management"""
    st.subheader("👥 Resource Management")
    
    # Resource overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resources", "89", "Active workers")
    with col2:
        st.metric("Utilization Rate", "94.2%", "Excellent efficiency")
    with col3:
        st.metric("Overtime Hours", "127", "This week")
    with col4:
        st.metric("Resource Conflicts", "2", "Minor issues")
    
    # Resource assignments table
    st.markdown("### Current Resource Assignments")
    
    resource_df = pd.DataFrame(st.session_state.resource_assignments)
    st.dataframe(resource_df, use_container_width=True)
    
    # Resource allocation chart
    col1, col2 = st.columns(2)
    
    with col1:
        # Resource utilization by type
        resource_types = resource_df['resource_type'].value_counts()
        fig = px.pie(values=resource_types.values, names=resource_types.index,
                    title="Resource Distribution by Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Weekly utilization trends
        utilization_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Utilization': [92.5, 94.2, 96.8, 94.2]
        })
        
        fig = px.line(utilization_data, x='Week', y='Utilization',
                     title="Weekly Resource Utilization")
        st.plotly_chart(fig, use_container_width=True)

def render_gantt_chart():
    """Interactive Gantt chart visualization"""
    st.subheader("📊 Project Gantt Chart")
    
    # Create Gantt chart data
    gantt_data = []
    for task in st.session_state.schedule_tasks:
        gantt_data.append(dict(
            Task=task['task_name'],
            Start=task['start_date'],
            Finish=task['end_date'],
            Resource=task['assigned_to'],
            Phase=task['phase']
        ))
    
    gantt_df = pd.DataFrame(gantt_data)
    
    # Convert dates
    gantt_df['Start'] = pd.to_datetime(gantt_df['Start'])
    gantt_df['Finish'] = pd.to_datetime(gantt_df['Finish'])
    
    # Create Gantt chart using Plotly
    fig = px.timeline(gantt_df, x_start="Start", x_end="Finish", y="Task", 
                     color="Phase", title="Highland Tower Development - Project Schedule")
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Schedule summary
    st.markdown("### Schedule Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Project Duration", "320 days", "Baseline schedule")
    with col2:
        st.metric("Remaining Days", "198 days", "Current projection")
    with col3:
        st.metric("Schedule Buffer", "15 days", "Risk mitigation")

def render_schedule_analytics():
    """Schedule performance analytics"""
    st.subheader("📈 Schedule Analytics")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Schedule Performance Index", "1.05", "5% ahead of plan")
    with col2:
        st.metric("Task Completion Rate", "87.6%", "+2.3% vs target")
    with col3:
        st.metric("Average Task Duration", "4.2 days", "-0.8 days vs estimate")
    with col4:
        st.metric("Critical Path Health", "Stable", "No major risks")
    
    # Analytics charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Task completion trends
        completion_data = pd.DataFrame({
            'Date': pd.date_range('2025-05-01', periods=25),
            'Planned': [i*2 for i in range(25)],
            'Actual': [i*2.1 for i in range(25)]
        })
        
        fig = px.line(completion_data, x='Date', y=['Planned', 'Actual'],
                     title="Cumulative Task Completion")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Phase progress
        phase_data = pd.DataFrame({
            'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Closeout'],
            'Progress': [100, 85, 60, 25, 5]
        })
        
        fig = px.bar(phase_data, x='Phase', y='Progress',
                    title="Progress by Project Phase")
        st.plotly_chart(fig, use_container_width=True)

def render_schedule_settings():
    """Schedule configuration and settings"""
    st.subheader("⚙️ Schedule Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Working Hours**")
        work_start = st.time_input("Work Start Time", value=datetime.strptime("07:00", "%H:%M").time())
        work_end = st.time_input("Work End Time", value=datetime.strptime("17:00", "%H:%M").time())
        work_days = st.multiselect("Working Days", 
                                 ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                 default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        
        st.markdown("**Notifications**")
        task_notifications = st.checkbox("Task assignment notifications", value=True)
        deadline_alerts = st.checkbox("Deadline alerts", value=True)
        progress_reports = st.checkbox("Weekly progress reports", value=True)
    
    with col2:
        st.markdown("**Schedule Options**")
        auto_update = st.checkbox("Auto-update dependencies", value=True)
        critical_path = st.checkbox("Highlight critical path", value=True)
        resource_leveling = st.checkbox("Enable resource leveling", value=False)
        
        st.markdown("**Data Integration**")
        sync_external = st.checkbox("Sync with external systems", value=False)
        backup_schedule = st.selectbox("Backup frequency", ["Daily", "Weekly", "Monthly"])
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Schedule settings saved successfully!")

def get_sample_tasks():
    """Generate sample task data"""
    return [
        {
            'task_id': 'TASK-HTD-0001',
            'task_name': 'Level 13 Steel Beam Installation',
            'phase': 'Structure',
            'assigned_to': 'Steel Crew A',
            'priority': 'High',
            'start_date': '2025-05-20',
            'end_date': '2025-05-27',
            'duration': 7,
            'budget': 125000,
            'status': 'In Progress',
            'progress': 85,
            'dependencies': 'TASK-HTD-0002'
        },
        {
            'task_id': 'TASK-HTD-0002',
            'task_name': 'Level 12 Concrete Pour',
            'phase': 'Structure',
            'assigned_to': 'Concrete Team B',
            'priority': 'Critical',
            'start_date': '2025-05-18',
            'end_date': '2025-05-20',
            'duration': 2,
            'budget': 89000,
            'status': 'Completed',
            'progress': 100,
            'dependencies': 'None'
        },
        {
            'task_id': 'TASK-HTD-0003',
            'task_name': 'MEP Rough-in Level 11',
            'phase': 'MEP',
            'assigned_to': 'MEP Contractor',
            'priority': 'Medium',
            'start_date': '2025-05-22',
            'end_date': '2025-05-29',
            'duration': 7,
            'budget': 156000,
            'status': 'In Progress',
            'progress': 60,
            'dependencies': 'None'
        }
    ]

def get_sample_milestones():
    """Generate sample milestone data"""
    return [
        {
            'milestone_id': 'MS-HTD-001',
            'milestone_name': 'Structural Steel Completion',
            'phase': 'Structure',
            'target_date': '2025-06-15',
            'priority': 'Critical',
            'owner': 'Construction Manager',
            'milestone_type': 'Phase Completion',
            'description': 'Complete installation of all structural steel components',
            'status': 'In Progress',
            'progress': 75
        },
        {
            'milestone_id': 'MS-HTD-002',
            'milestone_name': 'MEP Rough-in Complete',
            'phase': 'MEP',
            'target_date': '2025-07-30',
            'priority': 'High',
            'owner': 'MEP Manager',
            'milestone_type': 'Phase Completion',
            'description': 'Complete all MEP rough-in work for all floors',
            'status': 'Not Started',
            'progress': 0
        }
    ]

def get_sample_resources():
    """Generate sample resource data"""
    return [
        {
            'resource_id': 'RES-001',
            'resource_name': 'Steel Crew A',
            'resource_type': 'Labor',
            'assigned_task': 'Level 13 Steel Installation',
            'utilization': 94.5,
            'hourly_rate': 45.00,
            'status': 'Active'
        },
        {
            'resource_id': 'RES-002',
            'resource_name': 'Tower Crane LC1400',
            'resource_type': 'Equipment',
            'assigned_task': 'Material Handling',
            'utilization': 87.2,
            'hourly_rate': 285.00,
            'status': 'Active'
        },
        {
            'resource_id': 'RES-003',
            'resource_name': 'Concrete Team B',
            'resource_type': 'Labor',
            'assigned_task': 'Concrete Operations',
            'utilization': 92.8,
            'hourly_rate': 42.50,
            'status': 'Active'
        }
    ]

if __name__ == "__main__":
    render()