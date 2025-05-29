"""
Scheduling Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Scheduling - gcPanel", page_icon="📅", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📅 Project Scheduling")
st.markdown("Highland Tower Development - Schedule Management & Planning")
st.markdown("---")

if 'schedule_items' not in st.session_state:
    st.session_state.schedule_items = [
        {
            "id": "SCH-001",
            "task_name": "Foundation Excavation",
            "start_date": "2024-01-15",
            "end_date": "2024-02-15",
            "duration": 31,
            "predecessor": "",
            "resource": "Excavation Crew",
            "progress": 100,
            "status": "Completed"
        },
        {
            "id": "SCH-002",
            "task_name": "Foundation Pour",
            "start_date": "2024-02-16",
            "end_date": "2024-03-30",
            "duration": 43,
            "predecessor": "SCH-001",
            "resource": "Concrete Crew",
            "progress": 85,
            "status": "In Progress"
        }
    ]

tab1, tab2, tab3 = st.tabs(["📊 Schedule View", "📝 Add Schedule Item", "📈 Progress Tracking"])

with tab1:
    st.subheader("📊 Project Schedule")
    
    if st.session_state.schedule_items:
        df = pd.DataFrame(st.session_state.schedule_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search schedule items...", key="scheduling_search_1")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Not Started", "In Progress", "Completed", "Delayed"])
        with col3:
            resource_filter = st.selectbox("Resource", ["All", "Excavation Crew", "Concrete Crew", "Steel Crew"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
        if resource_filter != "All":
            filtered_df = filtered_df[filtered_df['resource'] == resource_filter]
        
        st.write(f"**Total Schedule Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No schedule items created. Add your first schedule item in the Add tab!")

with tab2:
    st.subheader("📝 Add Schedule Item")
    
    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name", placeholder="Activity description")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            duration = st.number_input("Duration (days)", min_value=1, value=1)
        
        with col2:
            predecessor = st.text_input("Predecessor", placeholder="Previous task ID")
            resource = st.text_input("Resource", placeholder="Assigned crew/team")
            progress = st.slider("Progress %", 0, 100, 0)
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        description = st.text_area("Task Description", placeholder="Detailed task description...")
        
        submitted = st.form_submit_button("📅 Add to Schedule", type="primary", use_container_width=True)
        
        if submitted and task_name:
            new_task = {
                "id": f"SCH-{len(st.session_state.schedule_items) + 1:03d}",
                "task_name": task_name,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "duration": duration,
                "predecessor": predecessor,
                "resource": resource,
                "progress": progress,
                "priority": priority,
                "description": description,
                "status": "Not Started" if progress == 0 else "In Progress" if progress < 100 else "Completed"
            }
            st.session_state.schedule_items.insert(0, new_task)
            st.success(f"Schedule item {new_task['id']} added successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Project Schedule")
    
    if st.session_state.schedule_items:
        df = pd.DataFrame(st.session_state.schedule_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search tasks...")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Not Started", "In Progress", "Completed"])
        with col3:
            resource_filter = st.selectbox("Resource", ["All"] + list(df['resource'].unique()) if len(df) > 0 else ["All"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
        if resource_filter != "All":
            filtered_df = filtered_df[filtered_df['resource'] == resource_filter]
        
        st.write(f"**Total Schedule Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No schedule items created. Add your first task above!")

with tab3:
    st.subheader("📈 Schedule Progress")
    
    if st.session_state.schedule_items:
        df = pd.DataFrame(st.session_state.schedule_items)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tasks = len(df)
            st.metric("Total Tasks", total_tasks)
        
        with col2:
            completed = len(df[df['status'] == 'Completed'])
            st.metric("Completed", completed)
        
        with col3:
            in_progress = len(df[df['status'] == 'In Progress'])
            st.metric("In Progress", in_progress)
        
        with col4:
            avg_progress = df['progress'].mean()
            st.metric("Avg Progress", f"{avg_progress:.0f}%")
    else:
        st.info("No schedule data available for progress tracking.")