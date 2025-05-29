"""
Preconstruction Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Preconstruction - gcPanel", page_icon="🏗️", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🏗️ Preconstruction Management")
st.markdown("Highland Tower Development - Preconstruction Planning & Coordination")
st.markdown("---")

if 'preconstruction_tasks' not in st.session_state:
    st.session_state.preconstruction_tasks = []

tab1, tab2, tab3 = st.tabs(["📊 Task Tracking", "📋 Create Planning Task", "📈 Progress"])

with tab1:
    st.subheader("📊 Preconstruction Tasks")
    
    if st.session_state.preconstruction_tasks:
        df = pd.DataFrame(st.session_state.preconstruction_tasks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search tasks...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Design Review", "Permitting", "Estimating"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Not Started", "In Progress", "Completed"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Tasks:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No preconstruction tasks created. Create your first task in the Create tab!")

with tab2:
    st.subheader("📋 Create Planning Task")
    
    with st.form("preconstruction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title", placeholder="Preconstruction task description")
            category = st.selectbox("Category", 
                ["Design Review", "Permitting", "Estimating", "Scheduling", "Procurement", "Logistics"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            assigned_to = st.text_input("Assigned To", placeholder="Team member or department")
        
        with col2:
            start_date = st.date_input("Start Date")
            due_date = st.date_input("Due Date")
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, format="%.1f")
            dependencies = st.text_input("Dependencies", placeholder="Related tasks or requirements")
        
        description = st.text_area("Task Description", placeholder="Detailed description of the task...")
        deliverables = st.text_area("Expected Deliverables", placeholder="What should be produced...")
        
        submitted = st.form_submit_button("📝 Create Task", type="primary", use_container_width=True)
        
        if submitted and task_title:
            new_task = {
                "id": f"PC-{len(st.session_state.preconstruction_tasks) + 1:03d}",
                "title": task_title,
                "category": category,
                "priority": priority,
                "assigned_to": assigned_to,
                "start_date": str(start_date),
                "due_date": str(due_date),
                "estimated_hours": estimated_hours,
                "dependencies": dependencies,
                "description": description,
                "deliverables": deliverables,
                "status": "Not Started",
                "created_by": st.session_state.get('user_name', 'User'),
                "created_date": str(date.today())
            }
            st.session_state.preconstruction_tasks.insert(0, new_task)
            st.success(f"Task {new_task['id']} created successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Preconstruction Tasks")
    
    if st.session_state.preconstruction_tasks:
        df = pd.DataFrame(st.session_state.preconstruction_tasks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search tasks...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Design Review", "Permitting", "Estimating"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Not Started", "In Progress", "Completed"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Tasks:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No preconstruction tasks created. Create your first task above!")

with tab3:
    st.subheader("📈 Preconstruction Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", "24", "3")
    
    with col2:
        st.metric("Completed", "18", "2")
    
    with col3:
        st.metric("In Progress", "4", "1")
    
    with col4:
        st.metric("Completion %", "75%", "8%")