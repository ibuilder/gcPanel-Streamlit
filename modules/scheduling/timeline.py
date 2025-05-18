"""
Timeline components for the Schedule module.

This module provides timeline visualization functionality for project phases and milestones.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_timeline():
    """Render the project timeline view."""
    
    st.header("Project Timeline")
    
    # Sample project phases
    phases = [
        {"Task": "Design & Planning", "Start": "2025-01-01", "Finish": "2025-03-15", "Completion": 100, "Description": "Project design and approvals"},
        {"Task": "Site Preparation", "Start": "2025-03-01", "Finish": "2025-05-30", "Completion": 100, "Description": "Clearing, excavation, foundation"},
        {"Task": "Structural Frame", "Start": "2025-04-15", "Finish": "2025-07-15", "Completion": 100, "Description": "Steel/concrete structural elements"},
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
    
    # Add vertical line for today - use string date format to avoid type errors
    today_str = datetime.now().strftime("%Y-%m-%d")
    try:
        fig.add_vline(x=today_str, line_width=2, line_dash="dash", line_color="red", annotation_text="Today")
    except TypeError as e:
        st.warning(f"Could not add today's date line to the chart: {e}")
        st.info("This does not affect the functionality of the timeline.")
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add textual milestone summary
    st.subheader("Key Milestones")
    
    # Sample milestones
    milestones = [
        {"Milestone": "Design Approval", "Date": "2025-01-10", "Status": "Complete"},
        {"Milestone": "Site Mobilization", "Date": "2025-01-20", "Status": "Complete"},
        {"Milestone": "Foundation Complete", "Date": "2025-04-15", "Status": "Complete"},
        {"Milestone": "Topping Out", "Date": "2025-07-01", "Status": "Complete"},
        {"Milestone": "Building Dry-In", "Date": "2025-08-15", "Status": "Complete"},
        {"Milestone": "MEP Rough-In Complete", "Date": "2025-09-01", "Status": "In Progress"},
        {"Milestone": "Interior Finishes Start", "Date": "2025-08-20", "Status": "In Progress"},
        {"Milestone": "Systems Testing", "Date": "2025-10-20", "Status": "Not Started"},
        {"Milestone": "Substantial Completion", "Date": "2025-11-30", "Status": "Not Started"},
        {"Milestone": "Final Completion", "Date": "2025-12-15", "Status": "Not Started"}
    ]
    
    milestone_df = pd.DataFrame(milestones)
    
    # Color status values
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
    
    # Display milestones
    st.dataframe(milestone_df.style.map(color_status, subset=['Status']), hide_index=True, use_container_width=True)