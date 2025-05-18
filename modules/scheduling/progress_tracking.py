"""
Progress tracking components for the Schedule module.

This module provides visualization and tracking of project progress by categories.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_milestone_progress():
    """Render the milestone progress view."""
    
    st.header("Progress Tracking")
    
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
            # Ensure i is an integer before using it in calculations
            task_id = 100 + (i if isinstance(i, int) else 0)
            # Create a safe key by converting category to a string and replacing spaces
            category_key = str(category).replace(' ', '_') if category else 'unknown'
            if st.button("Edit Tasks", key=f"edit_tasks_{category_key}"):
                st.session_state.show_task_edit = True
                st.session_state.edit_task_id = task_id
                st.session_state.edit_task_category = category
                st.rerun()
        
        # Show tasks for the first few categories
        if isinstance(i, int) and i < 3:  # Only show for first three categories
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
                # Using map instead of applymap (which is deprecated)
                st.dataframe(
                    tasks_df.style.map(color_status, subset=['Status']),
                    hide_index=True,
                    use_container_width=True
                )
    
    # Create a radar chart for progress visualization
    st.subheader("Progress Overview")
    
    # Create radar chart
    # Convert categories and progress to list if they are pandas Series
    try:
        categories = df["Category"].tolist() if hasattr(df["Category"], "tolist") else list(df["Category"])
        progress = df["Progress"].tolist() if hasattr(df["Progress"], "tolist") else list(df["Progress"])
    except Exception as e:
        st.error(f"Error converting data for chart: {e}")
        categories = ["Planning", "Design", "Foundation", "Structure", "Finishes"]
        progress = [75, 60, 45, 30, 10]
    
    # Create the figure - ensure proper imports at the top of file
    import plotly.graph_objects as go_objects
    fig = go_objects.Figure()
    
    # Add the scatter polar trace
    fig.add_trace(go_objects.Scatterpolar(
        r=progress,
        theta=categories,
        fill='toself',
        line=dict(color='rgba(32, 128, 64, 1)'),
        fillcolor='rgba(32, 128, 64, 0.5)',
        name='Progress'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)