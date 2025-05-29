"""
Engineering Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Engineering - gcPanel", page_icon="⚙️", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("⚙️ Engineering Management")
st.markdown("Highland Tower Development - Engineering Documentation & Analysis")
st.markdown("---")

if 'engineering_items' not in st.session_state:
    st.session_state.engineering_items = []

tab1, tab2, tab3 = st.tabs(["📝 Engineering Tasks", "📊 Documentation", "🔧 Analysis"])

with tab1:
    st.subheader("📝 Create Engineering Task")
    
    with st.form("engineering_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title", placeholder="Engineering task description")
            discipline = st.selectbox("Engineering Discipline", 
                ["Structural", "Mechanical", "Electrical", "Civil", "Geotechnical", "Environmental"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            engineer = st.text_input("Assigned Engineer", placeholder="Lead engineer name")
        
        with col2:
            project_phase = st.selectbox("Project Phase", 
                ["Design Development", "Construction Documents", "Construction Administration", "Closeout"])
            due_date = st.date_input("Due Date")
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, format="%.1f")
            drawing_numbers = st.text_input("Drawing Numbers", placeholder="Related drawing references")
        
        scope = st.text_area("Scope of Work", placeholder="Detailed engineering scope...")
        requirements = st.text_area("Technical Requirements", placeholder="Specifications and requirements...")
        
        submitted = st.form_submit_button("⚙️ Create Task", type="primary", use_container_width=True)
        
        if submitted and task_title:
            new_task = {
                "id": f"ENG-{len(st.session_state.engineering_items) + 1:03d}",
                "title": task_title,
                "discipline": discipline,
                "priority": priority,
                "engineer": engineer,
                "project_phase": project_phase,
                "due_date": str(due_date),
                "estimated_hours": estimated_hours,
                "drawing_numbers": drawing_numbers,
                "scope": scope,
                "requirements": requirements,
                "status": "Planning",
                "created_date": str(date.today())
            }
            st.session_state.engineering_items.insert(0, new_task)
            st.success(f"Engineering task {new_task['id']} created successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Engineering Documentation")
    
    if st.session_state.engineering_items:
        df = pd.DataFrame(st.session_state.engineering_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search tasks...")
        with col2:
            discipline_filter = st.selectbox("Discipline", ["All", "Structural", "Mechanical", "Electrical"])
        with col3:
            phase_filter = st.selectbox("Phase", ["All", "Design Development", "Construction Documents"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df['discipline'] == discipline_filter]
            
        if phase_filter != "All":
            filtered_df = filtered_df[filtered_df['project_phase'] == phase_filter]
        
        st.write(f"**Total Engineering Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No engineering tasks created. Create your first task above!")

with tab3:
    st.subheader("🔧 Engineering Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Tasks", "16", "2")
    
    with col2:
        st.metric("Completed", "28", "4")
    
    with col3:
        st.metric("Drawing Revisions", "12", "3")
    
    with col4:
        st.metric("Design Changes", "8", "1")