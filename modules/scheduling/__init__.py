"""
Project Scheduling module for the gcPanel Construction Management Dashboard.

This module provides project scheduling features including Gantt charts,
milestone tracking, and critical path analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import random

def render_scheduling():
    """Render the project scheduling module"""
    
    # Header
    st.title("Project Schedule")
    
    # Tab navigation for scheduling sections
    tab1, tab2, tab3 = st.tabs(["Gantt Chart", "Milestones", "Resources"])
    
    # Gantt Chart Tab
    with tab1:
        render_gantt_chart()
    
    # Milestones Tab
    with tab2:
        render_milestones()
    
    # Resources Tab
    with tab3:
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
    if st.button("Update Progress", type="primary", key="update_progress_btn"):
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
        # Define fixed colors based on status
        colors = {
            "Completed": "green",
            "On Track": "blue",
            "At Risk": "orange",
            "Delayed": "red"
        }
        
        status_colors = [colors.get(status, "blue") for status in timeline_df['Status'].tolist()]
        
        fig = ff.create_gantt(
            timeline_df, 
            colors=status_colors,
            index_col='Status',
            show_colorbar=True,
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