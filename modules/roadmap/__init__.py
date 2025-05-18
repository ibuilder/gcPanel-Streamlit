"""
Project Roadmap module for gcPanel Construction Management Dashboard.

This module provides visualization of project milestones, phases and progress
with Gantt charts and interactive timeline views.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Initialize session state variables for this module
def initialize_roadmap_session_state():
    """Initialize session state variables for the Roadmap module"""
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

def render_roadmap():
    """Render the project roadmap page."""
    
    st.title("Project Roadmap")
    
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
        st.subheader("Highland Tower Development")
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.markdown("**Project Value:** $45.5M | **Area:** 168,500 sq ft | **Timeline:** Jan 2025 - Dec 2025")
        with cols[2]:
            st.markdown("**Overall Progress:**")
            overall_progress = 75  # Sample progress percentage
            st.progress(overall_progress / 100)
            st.markdown(f"**{overall_progress}% Complete**")
    
    # Add Milestone Form
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
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Timeline", "Milestone Progress", "Closeout Roadmap"])
    
    # Timeline Tab
    with tab1:
        render_timeline()
    
    # Milestone Progress Tab
    with tab2:
        render_milestone_progress()
    
    # Closeout Roadmap Tab
    with tab3:
        render_closeout_roadmap()

def render_timeline():
    """Render the project timeline view."""
    
    # Sample project phase data
    phases = [
        {"Task": "Pre-Construction", "Start": "2024-10-01", "Finish": "2025-01-15", "Completion": 100, "Description": "Planning and design phase"},
        {"Task": "Site Preparation", "Start": "2025-01-16", "Finish": "2025-02-28", "Completion": 100, "Description": "Site clearing and utility setup"},
        {"Task": "Foundation", "Start": "2025-03-01", "Finish": "2025-04-30", "Completion": 100, "Description": "Foundation and support work"},
        {"Task": "Structural Frame", "Start": "2025-05-01", "Finish": "2025-07-15", "Completion": 100, "Description": "Steel/concrete structural frame"},
        {"Task": "Building Envelope", "Start": "2025-06-15", "Finish": "2025-08-30", "Completion": 95, "Description": "Exterior walls and roof"},
        {"Task": "MEP Systems", "Start": "2025-07-01", "Finish": "2025-09-30", "Completion": 85, "Description": "Mechanical, electrical, plumbing"},
        {"Task": "Interior Finishes", "Start": "2025-08-15", "Finish": "2025-11-15", "Completion": 60, "Description": "Walls, flooring, ceilings"},
        {"Task": "Commissioning", "Start": "2025-10-15", "Finish": "2025-11-30", "Completion": 20, "Description": "Testing and systems verification"},
        {"Task": "Closeout", "Start": "2025-11-15", "Finish": "2025-12-31", "Completion": 10, "Description": "Final documentation and handover"}
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(phases)
    
    # Convert date strings to datetime for plotting
    df["Start"] = pd.to_datetime(df["Start"])
    df["Finish"] = pd.to_datetime(df["Finish"])
    
    # Add "In Progress" status
    df["Status"] = df["Completion"].apply(lambda x: "Complete" if x == 100 else "In Progress")
    
    # Create color mapping
    color_map = {"Complete": "#28a745", "In Progress": "#17a2b8"}
    
    # Create Gantt chart
    fig = px.timeline(
        df, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Status",
        color_discrete_map=color_map,
        hover_data=["Completion", "Description"]
    )
    
    # Update layout
    fig.update_layout(
        title="Project Timeline",
        xaxis_title="Date",
        yaxis_title="Project Phase",
        height=500,
        xaxis=dict(
            type='date',
            tickformat='%b %Y',
            tickangle=45,
            showgrid=True
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add vertical line for today
    today = datetime.now()
    fig.add_vline(x=today, line_width=2, line_dash="dash", line_color="red", annotation_text="Today")
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add textual milestone summary
    st.subheader("Key Milestones")
    
    # Sample milestones
    milestones = [
        {"Milestone": "Design Approval", "Date": "2025-01-10", "Status": "Complete"},
        {"Milestone": "Site Mobilization", "Date": "2025-01-20", "Status": "Complete"},
        {"Milestone": "Foundation Complete", "Date": "2025-04-28", "Status": "Complete"},
        {"Milestone": "Topping Out", "Date": "2025-07-10", "Status": "Complete"},
        {"Milestone": "Building Dry-In", "Date": "2025-08-25", "Status": "In Progress"},
        {"Milestone": "MEP Systems Complete", "Date": "2025-09-30", "Status": "In Progress"},
        {"Milestone": "Elevator Certification", "Date": "2025-10-20", "Status": "Not Started"},
        {"Milestone": "Substantial Completion", "Date": "2025-11-30", "Status": "Not Started"},
        {"Milestone": "Final Completion", "Date": "2025-12-20", "Status": "Not Started"}
    ]
    
    # Convert to DataFrame
    milestone_df = pd.DataFrame(milestones)
    
    # Style the milestones
    def color_status(val):
        if val == "Complete":
            return 'background-color: #28a745; color: white'
        elif val == "In Progress":
            return 'background-color: #17a2b8; color: white'
        else:
            return 'background-color: #6c757d; color: white'
    
    # Display milestones
    st.dataframe(milestone_df.style.applymap(color_status, subset=['Status']), hide_index=True, use_container_width=True)

def render_milestone_progress():
    """Render the milestone progress view."""
    
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
    
    # Sample milestone categories and their progress
    milestone_categories = [
        {"Category": "Permits & Approvals", "Progress": 80, "Items Complete": 16, "Total Items": 20},
        {"Category": "Structural", "Progress": 100, "Items Complete": 7, "Total Items": 7},
        {"Category": "Building Envelope", "Progress": 90, "Items Complete": 9, "Total Items": 10},
        {"Category": "MEP Systems", "Progress": 70, "Items Complete": 21, "Total Items": 30},
        {"Category": "Interior Finishes", "Progress": 50, "Items Complete": 15, "Total Items": 30},
        {"Category": "Life Safety", "Progress": 85, "Items Complete": 17, "Total Items": 20},
        {"Category": "External Areas", "Progress": 60, "Items Complete": 6, "Total Items": 10},
        {"Category": "Closeout Documentation", "Progress": 25, "Items Complete": 10, "Total Items": 40}
    ]
    
    df = pd.DataFrame(milestone_categories)
    
    # Create metrics at the top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_progress = df["Progress"].mean()
        st.metric("Average Progress", f"{avg_progress:.1f}%")
    
    with col2:
        total_complete = df["Items Complete"].sum()
        total_items = df["Total Items"].sum()
        st.metric("Tasks Complete", f"{total_complete}/{total_items}")
    
    with col3:
        on_track_count = len(df[df["Progress"] >= 70])
        st.metric("Categories On Track", f"{on_track_count}/{len(df)}")
    
    with col4:
        days_remaining = (datetime(2025, 12, 31) - datetime.now()).days
        st.metric("Days to Completion", days_remaining)
    
    # Create progress bars for each category
    st.subheader("Progress by Category")
    
    # Sort by progress descending
    df = df.sort_values("Progress", ascending=False)
    
    # Display progress bars
    for i, row in df.iterrows():
        category = row["Category"]
        progress = row["Progress"]
        items_complete = row["Items Complete"]
        total_items = row["Total Items"]
        
        # Determine color based on progress
        if progress >= 70:
            color = "#28a745"  # Green for good progress
        elif progress >= 40:
            color = "#ffc107"  # Yellow for medium progress
        else:
            color = "#dc3545"  # Red for low progress
        
        # Create columns for layout
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{category}** ({items_complete}/{total_items} items)")
            st.progress(progress / 100)
        
        with col2:
            st.markdown(f"<h4 style='color:{color};text-align:center;'>{progress}%</h4>", unsafe_allow_html=True)
            
        with col3:
            task_id = 100 + i
            if st.button("Edit Tasks", key=f"edit_tasks_{category.replace(' ', '_')}"):
                st.session_state.show_task_edit = True
                st.session_state.edit_task_id = task_id
                st.session_state.edit_task_category = category
                st.rerun()
        
        # Show tasks for the first few categories
        if i < 3:  # Only show for first three categories
            with st.expander(f"{category} Tasks"):
                # Generate sample tasks based on the category
                tasks = []
                for j in range(4):
                    task_status = "Complete" if j < (items_complete * 4) // total_items else "In Progress"
                    task_progress = 100 if task_status == "Complete" else 50
                    
                    task_name = ""
                    assigned_to = ""
                    
                    if category == "Permits & Approvals":
                        permits = ["Building Permit", "Excavation Permit", "Electrical Permit", "Plumbing Permit"]
                        task_name = permits[j % len(permits)]
                        assigned_to = "John Smith" if j % 2 == 0 else "Sarah Johnson"
                    elif category == "Structural":
                        structural_tasks = ["Foundation Review", "Column Layout", "Beam Design", "Bracing Installation"]
                        task_name = structural_tasks[j % len(structural_tasks)]
                        assigned_to = "Mike Chen"
                    elif category == "Building Envelope":
                        envelope_tasks = ["Window Installation", "Exterior Cladding", "Roof Installation", "Moisture Barrier"]
                        task_name = envelope_tasks[j % len(envelope_tasks)]
                        assigned_to = "Emma Wilson" if j % 2 == 0 else "David Garcia"
                    elif category == "MEP Systems":
                        mep_tasks = ["HVAC Design", "Electrical Layout", "Plumbing Systems", "Fire Protection"]
                        task_name = mep_tasks[j % len(mep_tasks)]
                        assigned_to = "Emma Wilson"
                    else:
                        task_name = f"Task {j+1} for {category}"
                        assigned_to = "John Smith"
                    
                    due_date = (datetime.now() + timedelta(days=30 + j*15)).strftime("%Y-%m-%d")
                    tasks.append({
                        "Task": task_name,
                        "Status": task_status,
                        "Progress": task_progress,
                        "Due Date": due_date,
                        "Assigned To": assigned_to
                    })
                
                tasks_df = pd.DataFrame(tasks)
                
                # Custom styles for different status values
                def color_status(val):
                    if val == "Complete":
                        return 'background-color: #d4edda; color: #155724'
                    elif val == "In Progress":
                        return 'background-color: #fff3cd; color: #856404'
                    elif val == "Not Started":
                        return 'background-color: #f8f9fa; color: #6c757d'
                    elif val == "At Risk":
                        return 'background-color: #f8d7da; color: #721c24'
                    return ''
                
                # Display the tasks table with styled status column
                st.dataframe(
                    tasks_df.style.applymap(color_status, subset=['Status']),
                    hide_index=True,
                    use_container_width=True
                )
    
    # Create a radar chart for progress visualization
    st.subheader("Progress Overview")
    
    # Create radar chart
    categories = df["Category"].tolist()
    progress = df["Progress"].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=progress,
        theta=categories,
        fill='toself',
        name='Progress',
        line_color='#1e88e5',
        fillcolor='rgba(30, 136, 229, 0.5)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=500,
        margin=dict(l=80, r=80, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_closeout_roadmap():
    """Render the closeout specific roadmap."""
    
    st.subheader("Closeout Process Roadmap")
    
    # Create a more detailed view of the closeout process
    closeout_steps = [
        {
            "Phase": "Substantial Completion",
            "Status": "In Progress",
            "Progress": 40,
            "Start Date": "2025-10-15",
            "End Date": "2025-11-15",
            "Tasks": [
                {"Task": "Building Department Final Inspection", "Status": "Scheduled", "Date": "2025-10-25"},
                {"Task": "Fire Marshal Final Inspection", "Status": "In Progress", "Date": "2025-10-20"},
                {"Task": "Elevator Inspection", "Status": "Scheduled", "Date": "2025-10-22"},
                {"Task": "TAB Report Completion", "Status": "In Progress", "Date": "2025-10-30"},
                {"Task": "Punch List Creation", "Status": "Complete", "Date": "2025-10-10"}
            ]
        },
        {
            "Phase": "Systems Training & Handover",
            "Status": "In Progress",
            "Progress": 30,
            "Start Date": "2025-10-25",
            "End Date": "2025-11-25",
            "Tasks": [
                {"Task": "HVAC Systems Training", "Status": "Complete", "Date": "2025-10-28"},
                {"Task": "Building Management System Training", "Status": "Complete", "Date": "2025-11-02"},
                {"Task": "Fire Alarm Training", "Status": "Complete", "Date": "2025-11-05"},
                {"Task": "Electrical Systems Training", "Status": "Scheduled", "Date": "2025-11-10"},
                {"Task": "Plumbing Systems Training", "Status": "Not Started", "Date": "2025-11-15"}
            ]
        },
        {
            "Phase": "Documentation Finalization",
            "Status": "In Progress",
            "Progress": 25,
            "Start Date": "2025-11-01",
            "End Date": "2025-12-15",
            "Tasks": [
                {"Task": "As-Built Drawings Collection", "Status": "In Progress", "Date": "2025-11-15"},
                {"Task": "O&M Manuals Compilation", "Status": "In Progress", "Date": "2025-11-20"},
                {"Task": "Warranty Documentation", "Status": "In Progress", "Date": "2025-11-25"},
                {"Task": "Final Commissioning Report", "Status": "Not Started", "Date": "2025-12-05"},
                {"Task": "Certificate of Occupancy Application", "Status": "Not Started", "Date": "2025-12-10"}
            ]
        },
        {
            "Phase": "Financial Closeout",
            "Status": "Not Started",
            "Progress": 10,
            "Start Date": "2025-11-15",
            "End Date": "2025-12-31",
            "Tasks": [
                {"Task": "Final Payment Application", "Status": "In Progress", "Date": "2025-11-20"},
                {"Task": "Lien Waivers Collection", "Status": "In Progress", "Date": "2025-11-30"},
                {"Task": "Retainage Release", "Status": "Not Started", "Date": "2025-12-15"},
                {"Task": "Final Cost Report", "Status": "Not Started", "Date": "2025-12-20"},
                {"Task": "Project Financial Closure", "Status": "Not Started", "Date": "2025-12-31"}
            ]
        }
    ]
    
    # Create a timeline view for the phases
    phase_data = []
    for phase in closeout_steps:
        phase_data.append({
            "Task": phase["Phase"],
            "Start": phase["Start Date"],
            "Finish": phase["End Date"],
            "Completion": phase["Progress"],
            "Status": phase["Status"]
        })
    
    # Convert to DataFrame
    phase_df = pd.DataFrame(phase_data)
    
    # Convert date strings to datetime for plotting
    phase_df["Start"] = pd.to_datetime(phase_df["Start"])
    phase_df["Finish"] = pd.to_datetime(phase_df["Finish"])
    
    # Create color mapping
    color_map = {
        "Complete": "#28a745", 
        "In Progress": "#17a2b8",
        "Not Started": "#6c757d"
    }
    
    # Create Gantt chart
    fig = px.timeline(
        phase_df, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Status",
        color_discrete_map=color_map,
        hover_data=["Completion"]
    )
    
    # Update layout
    fig.update_layout(
        title="Closeout Timeline",
        xaxis_title="Date",
        yaxis_title="Phase",
        height=300,
        xaxis=dict(
            type='date',
            tickformat='%b %d',
            showgrid=True
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add vertical line for today
    today = datetime.now()
    fig.add_vline(x=today, line_width=2, line_dash="dash", line_color="red", annotation_text="Today")
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Display phase details with expandable sections
    for phase in closeout_steps:
        with st.expander(f"{phase['Phase']} - {phase['Progress']}% Complete", expanded=True):
            # Progress bar
            st.progress(phase["Progress"] / 100)
            
            # Phase dates
            st.markdown(f"**Timeline:** {phase['Start Date']} to {phase['End Date']}")
            
            # Tasks table
            task_df = pd.DataFrame(phase["Tasks"])
            
            # Style the tasks
            def color_task_status(val):
                if val == "Complete":
                    return 'background-color: #28a745; color: white'
                elif val == "In Progress":
                    return 'background-color: #17a2b8; color: white'
                elif val == "Scheduled":
                    return 'background-color: #fd7e14; color: white'
                else:
                    return 'background-color: #6c757d; color: white'
            
            # Display tasks
            st.dataframe(
                task_df.style.applymap(color_task_status, subset=['Status']), 
                hide_index=True, 
                use_container_width=True
            )
    
    # Add closeout checklist stats
    st.subheader("Closeout Checklist Status")
    
    # Mock checklist data
    checklist_data = {
        "Category": ["Occupancy Permits", "Owner Training", "Financial Closeout", "Warranties", "O&M Manuals", "Final Documentation", "Punch List"],
        "Complete": [2, 3, 1, 10, 5, 2, 75],
        "Total": [5, 5, 7, 15, 25, 20, 120]
    }
    
    checklist_df = pd.DataFrame(checklist_data)
    checklist_df["Progress"] = (checklist_df["Complete"] / checklist_df["Total"] * 100).round(1)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    for i, row in checklist_df.iterrows():
        progress = row["Progress"]
        
        # Determine color based on progress
        if progress >= 70:
            color = "#28a745"  # Green
        elif progress >= 40:
            color = "#ffc107"  # Yellow
        else:
            color = "#dc3545"  # Red
            
        fig.add_trace(go.Bar(
            y=[row["Category"]],
            x=[progress],
            orientation='h',
            marker=dict(color=color),
            text=f"{progress}%",
            textposition='auto',
            name=row["Category"],
            hovertemplate=f"<b>{row['Category']}</b><br>" +
                          f"Complete: {row['Complete']}/{row['Total']}<br>" +
                          f"Progress: {progress}%<extra></extra>"
        ))
    
    fig.update_layout(
        height=400,
        title="Closeout Progress by Category",
        yaxis=dict(
            title="",
            categoryorder="total ascending"
        ),
        xaxis=dict(
            title="Completion Percentage",
            range=[0, 100]
        ),
        barmode='group',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)