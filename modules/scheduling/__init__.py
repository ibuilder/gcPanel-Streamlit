"""
Project Scheduling module for the gcPanel Construction Management Dashboard.

This module provides project scheduling features including Gantt charts,
milestone tracking, roadmap visualization, and resource management.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Initialize session state variables for this module
def initialize_schedule_session_state():
    """Initialize session state variables for the Schedule module"""
    if 'show_milestone_form' not in st.session_state:
        st.session_state.show_milestone_form = False
        
    if 'show_progress_update_form' not in st.session_state:
        st.session_state.show_progress_update_form = False
        
    if 'show_allocation_form' not in st.session_state:
        st.session_state.show_allocation_form = False
        
    if 'show_timeline_form' not in st.session_state:
        st.session_state.show_timeline_form = False
        
    if 'show_task_edit' not in st.session_state:
        st.session_state.show_task_edit = False
        
    if 'edit_task_id' not in st.session_state:
        st.session_state.edit_task_id = None
        
    if 'edit_task_category' not in st.session_state:
        st.session_state.edit_task_category = ""

def render_scheduling():
    """Render the project scheduling module"""
    
    # Initialize session state variables
    initialize_schedule_session_state()
    
    # Header
    st.title("Project Schedule")
    
    # Action buttons at top
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    with action_col1:
        if st.button("➕ Add Milestone", type="primary", key="add_milestone_btn", use_container_width=True):
            st.session_state.show_milestone_form = True
    
    with action_col2:
        if st.button("📊 Update Progress", type="primary", key="update_progress_btn", use_container_width=True):
            st.session_state.show_progress_update_form = True
    
    with action_col3:
        if st.button("👥 Update Allocation", type="primary", key="update_allocation_btn", use_container_width=True):
            st.session_state.show_allocation_form = True
    
    with action_col4:
        if st.button("📅 Edit Timeline", type="primary", key="edit_timeline_btn", use_container_width=True):
            st.session_state.show_timeline_form = True
    
    # Project Info
    with st.container():
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.markdown("**Project Value:** $45.5M | **Area:** 168,500 sq ft | **Timeline:** Jan 2025 - Dec 2025")
        with cols[2]:
            st.markdown("**Overall Progress:**")
            overall_progress = 75  # Sample progress percentage
            st.progress(overall_progress / 100)
            st.markdown(f"**{overall_progress}% Complete**")
            
    # Forms (they will only display if their session state variable is True)
    if st.session_state.get("show_milestone_form", False):
        with st.form("milestone_form"):
            st.subheader("Add New Milestone")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                milestone_name = st.text_input("Milestone Name", key="new_milestone_name")
                milestone_date = st.date_input("Target Date", key="new_milestone_date")
                milestone_type = st.selectbox(
                    "Milestone Type", 
                    ["Project", "Engineering", "Construction", "Financial", "Regulatory", "Other"],
                    key="new_milestone_type"
                )
            
            with form_col2:
                milestone_status = st.selectbox(
                    "Status", 
                    ["Not Started", "In Progress", "Complete", "At Risk", "Delayed"],
                    key="new_milestone_status"
                )
                milestone_priority = st.selectbox(
                    "Priority", 
                    ["Low", "Medium", "High", "Critical"],
                    key="new_milestone_priority"
                )
                milestone_owner = st.text_input("Owner", key="new_milestone_owner")
            
            milestone_description = st.text_area("Description", key="new_milestone_description")
            
            # Predecessor milestones
            st.subheader("Predecessor Milestones")
            st.multiselect(
                "Select predecessors",
                ["Design Approval", "Site Mobilization", "Foundation Complete", "Topping Out", "Building Dry-In"],
                key="new_milestone_predecessors"
            )
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_milestone = st.form_submit_button("Save")
            with submit_col2:
                cancel_milestone = st.form_submit_button("Cancel")
            
            if submit_milestone:
                st.success(f"Milestone '{milestone_name}' added successfully")
                st.session_state.show_milestone_form = False
                st.rerun()
            
            if cancel_milestone:
                st.session_state.show_milestone_form = False
                st.rerun()
    
    # Update Progress Form
    if st.session_state.get("show_progress_update_form", False):
        with st.form("progress_update_form"):
            st.subheader("Update Task Progress")
            
            # Sample tasks to update
            tasks_to_update = [
                {"Task": "Building Envelope", "Current Progress": 95, "ID": "task_1"},
                {"Task": "MEP Systems", "Current Progress": 85, "ID": "task_2"},
                {"Task": "Interior Finishes", "Current Progress": 60, "ID": "task_3"},
                {"Task": "Commissioning", "Current Progress": 20, "ID": "task_4"},
                {"Task": "Closeout", "Current Progress": 10, "ID": "task_5"}
            ]
            
            # Create sliders for each task
            for task in tasks_to_update:
                st.slider(
                    f"{task['Task']} Progress",
                    0, 100, task["Current Progress"],
                    key=f"progress_{task['ID']}"
                )
            
            # Notes field
            progress_notes = st.text_area("Update Notes", placeholder="Describe progress updates and any issues encountered", key="progress_notes")
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_progress = st.form_submit_button("Save")
            with submit_col2:
                cancel_progress = st.form_submit_button("Cancel")
            
            if submit_progress:
                st.success("Progress updated successfully")
                st.session_state.show_progress_update_form = False
                st.rerun()
            
            if cancel_progress:
                st.session_state.show_progress_update_form = False
                st.rerun()
    
    # Update Allocation Form
    if st.session_state.get("show_allocation_form", False):
        with st.form("allocation_form"):
            st.subheader("Update Resource Allocation")
            
            # Sample team members
            team_members = [
                "John Smith (Project Manager)",
                "Sarah Johnson (Architect)",
                "Mike Chen (Civil Engineer)",
                "Emma Wilson (MEP Lead)",
                "David Garcia (Superintendent)"
            ]
            
            # Sample tasks for allocation
            allocation_tasks = [
                "Building Envelope",
                "MEP Systems",
                "Interior Finishes",
                "Commissioning",
                "Closeout Documentation"
            ]
            
            # Create a multiselect for each task
            for task in allocation_tasks:
                st.multiselect(
                    f"Team Members for {task}",
                    team_members,
                    key=f"allocation_{task.lower().replace(' ', '_')}"
                )
            
            # Effort allocation
            st.subheader("Effort Allocation (%)")
            
            effort_col1, effort_col2 = st.columns(2)
            
            with effort_col1:
                for team_member in team_members[:3]:
                    st.slider(
                        team_member,
                        0, 100, 20,
                        key=f"effort_{team_member.split('(')[0].strip().lower().replace(' ', '_')}"
                    )
            
            with effort_col2:
                for team_member in team_members[3:]:
                    st.slider(
                        team_member,
                        0, 100, 20,
                        key=f"effort_{team_member.split('(')[0].strip().lower().replace(' ', '_')}"
                    )
            
            # Notes
            allocation_notes = st.text_area("Allocation Notes", key="allocation_notes")
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_allocation = st.form_submit_button("Save")
            with submit_col2:
                cancel_allocation = st.form_submit_button("Cancel")
            
            if submit_allocation:
                st.success("Resource allocation updated successfully")
                st.session_state.show_allocation_form = False
                st.rerun()
            
            if cancel_allocation:
                st.session_state.show_allocation_form = False
                st.rerun()
    
    # Edit Timeline Form
    if st.session_state.get("show_timeline_form", False):
        with st.form("timeline_form"):
            st.subheader("Edit Project Timeline")
            
            # Sample project phases to edit
            timeline_phases = [
                {"Phase": "Building Envelope", "Start": "2025-06-15", "End": "2025-08-30", "ID": "phase_1"},
                {"Phase": "MEP Systems", "Start": "2025-07-01", "End": "2025-09-30", "ID": "phase_2"},
                {"Phase": "Interior Finishes", "Start": "2025-08-15", "End": "2025-11-15", "ID": "phase_3"},
                {"Phase": "Commissioning", "Start": "2025-10-15", "End": "2025-11-30", "ID": "phase_4"},
                {"Phase": "Closeout", "Start": "2025-11-15", "End": "2025-12-31", "ID": "phase_5"}
            ]
            
            for phase in timeline_phases:
                st.markdown(f"**{phase['Phase']}**")
                cols = st.columns(2)
                
                with cols[0]:
                    start_date = st.date_input(
                        "Start Date", 
                        pd.to_datetime(phase["Start"]),
                        key=f"start_{phase['ID']}"
                    )
                
                with cols[1]:
                    end_date = st.date_input(
                        "End Date", 
                        pd.to_datetime(phase["End"]),
                        key=f"end_{phase['ID']}"
                    )
                
                st.markdown("---")
            
            # Notes
            timeline_notes = st.text_area("Timeline Update Notes", key="timeline_notes")
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_timeline = st.form_submit_button("Save")
            with submit_col2:
                cancel_timeline = st.form_submit_button("Cancel")
            
            if submit_timeline:
                st.success("Timeline updated successfully")
                st.session_state.show_timeline_form = False
                st.rerun()
            
            if cancel_timeline:
                st.session_state.show_timeline_form = False
                st.rerun()
                
    # Task edit functionality
    if st.session_state.get("show_task_edit", False):
        task_id = st.session_state.get("edit_task_id", None)
        task_category = st.session_state.get("edit_task_category", "")
        task_data = None
        
        # In a real application, we would fetch task data from a database
        # For this demo, we'll use sample data
        if task_id:
            task_data = {
                "id": task_id,
                "name": f"Task {task_id}",
                "category": task_category,
                "description": "Sample task description for demonstration purposes.",
                "start_date": datetime.now() - timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=30),
                "progress": 60,
                "status": "In Progress",
                "assigned_to": ["John Smith", "Sarah Johnson"],
                "priority": "Medium",
                "dependencies": ["Task 102", "Task 105"]
            }
        
        with st.form("task_edit_form"):
            st.subheader(f"Edit Task: {task_data['name'] if task_data else ''}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                task_name = st.text_input("Task Name", value=task_data['name'] if task_data else "", key="edit_task_name")
                task_category_select = st.selectbox(
                    "Category",
                    ["Permits & Approvals", "Structural", "Building Envelope", "MEP Systems", 
                     "Interior Finishes", "Life Safety", "External Areas", "Closeout Documentation"],
                    index=0 if not task_data else ["Permits & Approvals", "Structural", "Building Envelope", "MEP Systems", 
                                                  "Interior Finishes", "Life Safety", "External Areas", "Closeout Documentation"].index(task_data['category']),
                    key="edit_task_category_select"
                )
                task_progress = st.slider(
                    "Progress (%)", 
                    0, 100, 
                    value=task_data['progress'] if task_data else 0,
                    key="edit_task_progress"
                )
                task_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High", "Critical"],
                    index=1 if not task_data else ["Low", "Medium", "High", "Critical"].index(task_data['priority']),
                    key="edit_task_priority"
                )
            
            with col2:
                task_status = st.selectbox(
                    "Status",
                    ["Not Started", "In Progress", "On Hold", "Complete", "Cancelled"],
                    index=1 if not task_data else ["Not Started", "In Progress", "On Hold", "Complete", "Cancelled"].index(task_data['status']),
                    key="edit_task_status"
                )
                task_start = st.date_input(
                    "Start Date",
                    value=task_data['start_date'] if task_data else datetime.now(),
                    key="edit_task_start"
                )
                task_end = st.date_input(
                    "End Date",
                    value=task_data['end_date'] if task_data else datetime.now() + timedelta(days=14),
                    key="edit_task_end"
                )
                task_assigned = st.multiselect(
                    "Assigned To",
                    ["John Smith", "Sarah Johnson", "Mike Chen", "Emma Wilson", "David Garcia"],
                    default=task_data['assigned_to'] if task_data else [],
                    key="edit_task_assigned"
                )
            
            task_description = st.text_area(
                "Description",
                value=task_data['description'] if task_data else "",
                height=100,
                key="edit_task_description"
            )
            
            task_dependencies = st.multiselect(
                "Dependencies",
                ["Task 101", "Task 102", "Task 103", "Task 104", "Task 105", "Task 106"],
                default=task_data['dependencies'] if task_data else [],
                key="edit_task_dependencies"
            )
            
            # Attachments
            st.subheader("Attachments")
            st.file_uploader("Add Attachments", accept_multiple_files=True, key="edit_task_attachments")
            
            if task_data:
                st.markdown("**Current Attachments:**")
                st.markdown("- Task_Specification.pdf")
                st.markdown("- Requirements.docx")
            
            # Comments
            st.subheader("Comments")
            if task_data:
                st.markdown("**John Smith** (2 days ago): Updated the task requirements based on owner feedback.")
                st.markdown("**Sarah Johnson** (1 day ago): Coordinated with MEP team on system requirements.")
            
            new_comment = st.text_area("Add Comment", "", key="edit_task_comment")
            
            # Form buttons
            button_col1, button_col2, button_col3 = st.columns([1, 1, 4])
            with button_col1:
                save_button = st.form_submit_button("Save Changes")
            with button_col2:
                cancel_button = st.form_submit_button("Cancel")
            
            if save_button:
                st.success(f"Task '{task_name}' updated successfully!")
                st.session_state.show_task_edit = False
                st.rerun()
            
            if cancel_button:
                st.session_state.show_task_edit = False
                st.rerun()
            
    # Tab navigation for scheduling sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gantt Chart", "Milestones", "Timeline", "Progress Tracking", "Resources"])
    
    # Gantt Chart Tab
    with tab1:
        render_gantt_chart()
    
    # Milestones Tab
    with tab2:
        render_milestones()
    
    # Timeline Tab (from Roadmap)
    with tab3:
        from modules.scheduling.timeline import render_timeline
        render_timeline()
        
    # Progress Tracking Tab (from Roadmap)
    with tab4:
        from modules.scheduling.progress_tracking import render_milestone_progress
        render_milestone_progress()
        
    # Resources Tab
    with tab5:
        render_resources()

def render_gantt_chart():
    """Render the Gantt chart section"""
    
    st.header("Project Gantt Chart")
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range selector
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30), key="gantt_start_date")
    
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=180), key="gantt_end_date")
    
    with col3:
        # Filter by phase
        phase = st.selectbox("Phase", ["All", "Pre-Construction", "Foundation", "Structure", "MEP", "Finishes", "Close-Out"], key="gantt_phase")
    
    # Sample data for tasks
    project_tasks = generate_sample_tasks()
    
    # Filter by date range and phase
    filtered_tasks = project_tasks.copy()
    
    filtered_tasks = filtered_tasks[
        (filtered_tasks['Start'].dt.date >= start_date) & 
        (filtered_tasks['Finish'].dt.date <= end_date)
    ]
    
    if phase != "All":
        filtered_tasks = filtered_tasks[filtered_tasks['Phase'] == phase]
    
    # Display project stats
    st.subheader("Project Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        total_tasks = len(filtered_tasks)
        st.metric("Total Tasks", total_tasks)
    
    with stat_col2:
        completed_tasks = len(filtered_tasks[filtered_tasks['Complete'] == 100])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with stat_col3:
        on_track = len(filtered_tasks[filtered_tasks['Status'] == 'On Track'])
        on_track_rate = (on_track / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("On Track", f"{on_track_rate:.1f}%")
    
    with stat_col4:
        delayed = len(filtered_tasks[filtered_tasks['Status'] == 'Delayed'])
        st.metric("Delayed Tasks", delayed)
    
    # Create Gantt chart using Plotly
    fig = create_gantt_chart(filtered_tasks)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display tasks in a table
    st.subheader("Task List")
    
    # Format the table with progress bars
    for i, row in filtered_tasks.iterrows():
        with st.expander(f"{row['Task']} - {row['Complete']}% Complete", expanded=False):
            task_col1, task_col2 = st.columns(2)
            
            with task_col1:
                st.markdown(f"**ID:** {row['Task ID']}")
                st.markdown(f"**Task:** {row['Task']}")
                st.markdown(f"**Phase:** {row['Phase']}")
                st.markdown(f"**Resource:** {row['Resource']}")
            
            with task_col2:
                st.markdown(f"**Start:** {row['Start'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Finish:** {row['Finish'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Status:** {row['Status']}")
                st.markdown(f"**Dependencies:** {row['Dependencies']}")
            
            # Progress bar
            st.progress(row['Complete'] / 100, f"progress_bar_{i}")
    
    # Task update form
    st.divider()
    st.subheader("Update Task Progress")
    
    update_col1, update_col2 = st.columns(2)
    
    with update_col1:
        selected_task = st.selectbox("Select Task", filtered_tasks['Task'].tolist(), key="update_task_select")
    
    with update_col2:
        selected_task_data = filtered_tasks[filtered_tasks['Task'] == selected_task].iloc[0]
        current_progress = float(selected_task_data['Complete'])
        new_progress = st.slider("Progress (%)", 0.0, 100.0, current_progress, 5.0, key="update_task_progress")
    
    # Update button
    if st.button("Update Progress", type="primary", key="update_gantt_progress_btn"):
        st.success(f"Task '{selected_task}' progress updated to {new_progress}%")
        st.rerun()

def render_milestones():
    """Render the milestones section"""
    
    st.header("Project Milestones")
    
    # Sample data for milestones
    milestones = [
        {
            "id": f"MS-{2025}-{i:03d}",
            "name": random.choice([
                "Project Kickoff", "Foundation Complete", "Steel Structure Complete", 
                "Building Dry-In", "MEP Rough-In Complete", "Interior Framing Complete",
                "Drywall Complete", "Finishes Start", "Substantial Completion", "Final Completion"
            ]),
            "date": datetime.now() + timedelta(days=random.randint(-30, 180)),
            "status": random.choice(["Completed", "On Track", "At Risk", "Delayed"]),
            "description": f"Milestone description {i}",
            "owner": random.choice(["John Doe", "Jane Smith", "Project Manager", "Client"]),
        } for i in range(1, 11)
    ]
    
    df = pd.DataFrame(milestones)
    df['completion'] = df['status'].apply(lambda x: 100 if x == "Completed" else 0)
    
    # Filter and sort milestones
    milestone_status = st.multiselect(
        "Filter by Status", 
        ["Completed", "On Track", "At Risk", "Delayed"],
        default=["Completed", "On Track", "At Risk", "Delayed"],
        key="milestone_status_filter"
    )
    
    filtered_df = df[df['status'].isin(milestone_status)].sort_values('date')
    
    # Milestone timeline chart
    st.subheader("Milestone Timeline")
    
    # Convert to the format needed for Plotly
    timeline_data = []
    for _, row in filtered_df.iterrows():
        # No need to include color in the data
        timeline_data.append(dict(
            Task=row['name'],
            Start=row['date'],
            Finish=row['date'] + timedelta(days=1),  # Make it a point by setting finish close to start
            Status=row['status'],
            Resource=row['owner'],
            Description=row['description']
        ))
    
    timeline_df = pd.DataFrame(timeline_data)
    
    # Create the milestone timeline chart
    if not timeline_df.empty:
        # Create a single fixed color list based on the number of tasks
        num_tasks = len(timeline_df)
        status_colors = ['rgb(31, 119, 180)'] * num_tasks  # Use a consistent blue color
        
        fig = ff.create_gantt(
            timeline_df, 
            colors=status_colors,
            index_col='Status',
            show_colorbar=False,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True,
            title="Project Milestones"
        )
        
        # Format the chart
        fig.update_layout(
            autosize=True,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis_title="Date",
            yaxis_title="Milestone",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Milestone cards
    st.subheader("Milestone Details")
    
    # Calculate days until or since milestone
    today = datetime.now().date()
    
    for i, milestone in filtered_df.iterrows():
        milestone_date = milestone['date'].date()
        days_diff = (milestone_date - today).days
        
        if days_diff > 0:
            days_text = f"{days_diff} days remaining"
        elif days_diff < 0:
            days_text = f"{abs(days_diff)} days ago"
        else:
            days_text = "Today"
        
        # Set card color based on status
        if milestone['status'] == "Completed":
            card_color = "#d4edda"
            text_color = "#155724"
        elif milestone['status'] == "On Track":
            card_color = "#d1ecf1"
            text_color = "#0c5460"
        elif milestone['status'] == "At Risk":
            card_color = "#fff3cd"
            text_color = "#856404"
        else:  # Delayed
            card_color = "#f8d7da"
            text_color = "#721c24"
        
        # Render milestone card
        st.markdown(
            f"""
            <div style="background-color: {card_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <h4 style="color: {text_color}; margin: 0;">{milestone['name']}</h4>
                        <p style="margin: 5px 0;">{milestone['description']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-weight: bold; margin: 0;">{milestone['date'].strftime('%Y-%m-%d')}</p>
                        <p style="margin: 5px 0;">{days_text}</p>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div>
                        <p style="margin: 0;"><strong>Owner:</strong> {milestone['owner']}</p>
                    </div>
                    <div>
                        <p style="font-weight: bold; color: {text_color}; margin: 0;">{milestone['status']}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Add milestone form
    st.divider()
    if st.button("Add New Milestone", type="primary", key="add_milestone_btn"):
        st.session_state.show_milestone_form = True
    
    # Display form if button was clicked
    if st.session_state.get("show_milestone_form", False):
        with st.form("milestone_form"):
            st.subheader("New Milestone")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                ms_name = st.text_input("Milestone Name", "", key="ms_name")
                ms_date = st.date_input("Target Date", datetime.now() + timedelta(days=30), key="ms_date")
                ms_owner = st.text_input("Owner", "Project Manager", key="ms_owner")
            
            with form_col2:
                ms_status = st.selectbox("Status", ["On Track", "At Risk", "Delayed", "Completed"], key="ms_status")
                ms_description = st.text_area("Description", "", key="ms_description")
            
            submitted = st.form_submit_button("Add Milestone")
            
            if submitted:
                st.success(f"Milestone '{ms_name}' added successfully!")
                st.session_state.show_milestone_form = False
                st.rerun()

def render_resources():
    """Render the resources section"""
    
    st.header("Resource Allocation")
    
    # Sample data for resources
    resources = [
        {
            "id": f"RES-{i:03d}",
            "name": random.choice(["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Project Manager", "Superintendent", "Foreman"]),
            "role": random.choice(["Project Manager", "Superintendent", "Foreman", "Laborer", "Engineer", "Architect", "Inspector"]),
            "allocation": random.randint(25, 100),
            "tasks": random.randint(1, 8),
            "start_date": datetime.now() + timedelta(days=random.randint(-30, 0)),
            "end_date": datetime.now() + timedelta(days=random.randint(30, 180)),
        } for i in range(1, 16)
    ]
    
    df = pd.DataFrame(resources)
    
    # Resource allocation chart
    st.subheader("Resource Allocation")
    
    # Bar chart of allocation percentages
    fig = px.bar(
        df, 
        x="name", 
        y="allocation",
        color="allocation",
        labels={"name": "Resource", "allocation": "Allocation (%)"},
        color_continuous_scale=["green", "yellow", "red"],
        range_color=[0, 100],
        title="Resource Allocation Percentage"
    )
    
    # Add a horizontal line at 80% to show overallocation threshold
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="red",
        annotation_text="Optimal Threshold",
        annotation_position="bottom right"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Task count by resource
    st.subheader("Tasks Per Resource")
    task_fig = px.bar(
        df, 
        x="name", 
        y="tasks",
        color="role",
        labels={"name": "Resource", "tasks": "Number of Tasks"},
        title="Number of Tasks by Resource"
    )
    
    task_fig.update_layout(height=400)
    st.plotly_chart(task_fig, use_container_width=True)
    
    # Resource details table
    st.subheader("Resource Details")
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Resource update form
    st.divider()
    st.subheader("Update Resource Allocation")
    
    update_col1, update_col2 = st.columns(2)
    
    with update_col1:
        selected_resource = st.selectbox("Select Resource", df['name'].tolist(), key="update_resource_select")
    
    with update_col2:
        selected_resource_data = df[df['name'] == selected_resource].iloc[0]
        current_allocation = float(selected_resource_data['allocation'])
        new_allocation = st.slider("Allocation (%)", 0.0, 100.0, current_allocation, 5.0, key="update_resource_allocation")
    
    # Update button
    if st.button("Update Allocation", type="primary", key="update_allocation_btn"):
        st.success(f"Resource '{selected_resource}' allocation updated to {new_allocation}%")
        st.rerun()

def generate_sample_tasks():
    """Generate sample project tasks for Gantt chart"""
    # Create tasks with realistic dependencies
    tasks = []
    phases = ["Pre-Construction", "Foundation", "Structure", "MEP", "Finishes", "Close-Out"]
    resources = ["Project Manager", "Superintendent", "Foreman", "Subcontractor", "Engineer", "Architect", "Inspector"]
    
    # Create a start date for the project
    project_start = datetime.now() - timedelta(days=30)
    
    # Pre-Construction tasks
    tasks.append({
        "Task ID": "T001",
        "Task": "Project Kickoff",
        "Phase": "Pre-Construction",
        "Resource": "Project Manager",
        "Start": project_start,
        "Finish": project_start + timedelta(days=1),
        "Complete": 100,
        "Dependencies": "",
        "Status": "Completed"
    })
    
    tasks.append({
        "Task ID": "T002",
        "Task": "Design Development",
        "Phase": "Pre-Construction",
        "Resource": "Architect",
        "Start": project_start + timedelta(days=1),
        "Finish": project_start + timedelta(days=15),
        "Complete": 100,
        "Dependencies": "T001",
        "Status": "Completed"
    })
    
    tasks.append({
        "Task ID": "T003",
        "Task": "Permitting",
        "Phase": "Pre-Construction",
        "Resource": "Project Manager",
        "Start": project_start + timedelta(days=15),
        "Finish": project_start + timedelta(days=30),
        "Complete": 100,
        "Dependencies": "T002",
        "Status": "Completed"
    })
    
    # Foundation tasks
    tasks.append({
        "Task ID": "T004",
        "Task": "Site Preparation",
        "Phase": "Foundation",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=30),
        "Finish": project_start + timedelta(days=40),
        "Complete": 100,
        "Dependencies": "T003",
        "Status": "Completed"
    })
    
    tasks.append({
        "Task ID": "T005",
        "Task": "Excavation",
        "Phase": "Foundation",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=40),
        "Finish": project_start + timedelta(days=50),
        "Complete": 90,
        "Dependencies": "T004",
        "Status": "On Track"
    })
    
    tasks.append({
        "Task ID": "T006",
        "Task": "Foundation Construction",
        "Phase": "Foundation",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=50),
        "Finish": project_start + timedelta(days=70),
        "Complete": 75,
        "Dependencies": "T005",
        "Status": "On Track"
    })
    
    # Structure tasks
    tasks.append({
        "Task ID": "T007",
        "Task": "Steel Framing",
        "Phase": "Structure",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=70),
        "Finish": project_start + timedelta(days=85),
        "Complete": 50,
        "Dependencies": "T006",
        "Status": "Delayed"
    })
    
    tasks.append({
        "Task ID": "T008",
        "Task": "Concrete Slabs",
        "Phase": "Structure",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=85),
        "Finish": project_start + timedelta(days=95),
        "Complete": 30,
        "Dependencies": "T007",
        "Status": "On Track"
    })
    
    tasks.append({
        "Task ID": "T009",
        "Task": "Roof Construction",
        "Phase": "Structure",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=95),
        "Finish": project_start + timedelta(days=110),
        "Complete": 10,
        "Dependencies": "T008",
        "Status": "On Track"
    })
    
    # MEP tasks
    tasks.append({
        "Task ID": "T010",
        "Task": "Electrical Rough-In",
        "Phase": "MEP",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=95),
        "Finish": project_start + timedelta(days=120),
        "Complete": 20,
        "Dependencies": "T008",
        "Status": "On Track"
    })
    
    tasks.append({
        "Task ID": "T011",
        "Task": "Plumbing Rough-In",
        "Phase": "MEP",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=95),
        "Finish": project_start + timedelta(days=115),
        "Complete": 25,
        "Dependencies": "T008",
        "Status": "On Track"
    })
    
    tasks.append({
        "Task ID": "T012",
        "Task": "HVAC Installation",
        "Phase": "MEP",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=100),
        "Finish": project_start + timedelta(days=125),
        "Complete": 15,
        "Dependencies": "T008",
        "Status": "On Track"
    })
    
    # Finishes tasks
    tasks.append({
        "Task ID": "T013",
        "Task": "Drywall Installation",
        "Phase": "Finishes",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=125),
        "Finish": project_start + timedelta(days=145),
        "Complete": 0,
        "Dependencies": "T010,T011,T012",
        "Status": "Not Started"
    })
    
    tasks.append({
        "Task ID": "T014",
        "Task": "Painting",
        "Phase": "Finishes",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=145),
        "Finish": project_start + timedelta(days=160),
        "Complete": 0,
        "Dependencies": "T013",
        "Status": "Not Started"
    })
    
    tasks.append({
        "Task ID": "T015",
        "Task": "Flooring Installation",
        "Phase": "Finishes",
        "Resource": "Subcontractor",
        "Start": project_start + timedelta(days=145),
        "Finish": project_start + timedelta(days=155),
        "Complete": 0,
        "Dependencies": "T013",
        "Status": "Not Started"
    })
    
    # Close-Out tasks
    tasks.append({
        "Task ID": "T016",
        "Task": "Punch List",
        "Phase": "Close-Out",
        "Resource": "Project Manager",
        "Start": project_start + timedelta(days=160),
        "Finish": project_start + timedelta(days=170),
        "Complete": 0,
        "Dependencies": "T014,T015",
        "Status": "Not Started"
    })
    
    tasks.append({
        "Task ID": "T017",
        "Task": "Final Inspections",
        "Phase": "Close-Out",
        "Resource": "Inspector",
        "Start": project_start + timedelta(days=170),
        "Finish": project_start + timedelta(days=175),
        "Complete": 0,
        "Dependencies": "T016",
        "Status": "Not Started"
    })
    
    tasks.append({
        "Task ID": "T018",
        "Task": "Project Handover",
        "Phase": "Close-Out",
        "Resource": "Project Manager",
        "Start": project_start + timedelta(days=175),
        "Finish": project_start + timedelta(days=180),
        "Complete": 0,
        "Dependencies": "T017",
        "Status": "Not Started"
    })
    
    return pd.DataFrame(tasks)

def create_gantt_chart(df):
    """Create a Gantt chart from the task dataframe"""
    # Define colors based on status
    colors = {
        'Completed': 'rgb(0, 128, 0)',         # Green
        'On Track': 'rgb(54, 162, 235)',       # Blue
        'Delayed': 'rgb(255, 99, 132)',        # Red
        'Not Started': 'rgb(211, 211, 211)'    # Light Gray
    }
    
    # Convert to the format needed for Plotly
    gantt_data = []
    for _, row in df.iterrows():
        gantt_data.append(dict(
            Task=row['Task'],
            Start=row['Start'],
            Finish=row['Finish'],
            Resource=row['Resource'],
            Complete=row['Complete'],
            Status=row['Status'],
            Dependencies=row['Dependencies']
        ))
    
    gantt_df = pd.DataFrame(gantt_data)
    
    # Create the Gantt chart
    fig = ff.create_gantt(
        gantt_df, 
        colors=[colors.get(task['Status'], 'rgb(54, 162, 235)') for task in gantt_data],
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
        title="Project Schedule Gantt Chart"
    )
    
    # Format the chart
    fig.update_layout(
        autosize=True,
        height=600,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Timeline",
        yaxis_title="Task",
    )
    
    return fig