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

def render_roadmap():
    """Render the project roadmap page."""
    
    st.title("Project Roadmap")
    
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
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{category}** ({items_complete}/{total_items} items)")
            st.progress(progress / 100)
        
        with col2:
            st.markdown(f"<h4 style='color:{color};text-align:center;'>{progress}%</h4>", unsafe_allow_html=True)
    
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