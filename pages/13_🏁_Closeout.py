"""
Project Closeout Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Closeout - gcPanel", page_icon="🏁", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🏁 Project Closeout")
st.markdown("Highland Tower Development - Project Completion & Handover")
st.markdown("---")

if 'closeout_items' not in st.session_state:
    st.session_state.closeout_items = []

tab1, tab2, tab3 = st.tabs(["📋 Closeout Tasks", "📄 Documentation", "✅ Completion Status"])

with tab1:
    st.subheader("📋 Create Closeout Task")
    
    with st.form("closeout_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title", placeholder="Closeout task description")
            category = st.selectbox("Category", 
                ["Documentation", "Inspections", "Testing", "Training", "Warranties", "As-Built", "Commissioning"])
            responsible_party = st.text_input("Responsible Party", placeholder="Person or company responsible")
            due_date = st.date_input("Due Date")
        
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            completion_percentage = st.slider("Completion %", 0, 100, 0)
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, format="%.1f")
            dependencies = st.text_input("Dependencies", placeholder="Related tasks or requirements")
        
        description = st.text_area("Task Description", placeholder="Detailed description of closeout task...")
        deliverables = st.text_area("Required Deliverables", placeholder="What must be delivered...")
        
        submitted = st.form_submit_button("📋 Create Task", type="primary", use_container_width=True)
        
        if submitted and task_title:
            new_task = {
                "id": f"CO-{len(st.session_state.closeout_items) + 1:03d}",
                "title": task_title,
                "category": category,
                "responsible_party": responsible_party,
                "due_date": str(due_date),
                "priority": priority,
                "completion_percentage": completion_percentage,
                "estimated_hours": estimated_hours,
                "dependencies": dependencies,
                "description": description,
                "deliverables": deliverables,
                "status": "Not Started" if completion_percentage == 0 else "In Progress" if completion_percentage < 100 else "Completed",
                "created_date": str(date.today())
            }
            st.session_state.closeout_items.insert(0, new_task)
            st.success(f"Closeout task {new_task['id']} created successfully!")
            st.rerun()

with tab2:
    st.subheader("📄 Closeout Documentation")
    
    doc_categories = [
        "As-Built Drawings", "Operation & Maintenance Manuals", "Warranties & Guarantees",
        "Test Reports", "Inspection Certificates", "Training Materials", "Spare Parts Lists"
    ]
    
    for category in doc_categories:
        with st.expander(f"📁 {category}"):
            st.write(f"Status: In Progress")
            st.write(f"Documents Required: 12")
            st.write(f"Documents Received: 8")
            st.progress(8/12)

with tab3:
    st.subheader("✅ Project Completion Status")
    
    if st.session_state.closeout_items:
        df = pd.DataFrame(st.session_state.closeout_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search tasks...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Documentation", "Inspections", "Testing"])
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
        
        st.write(f"**Total Closeout Tasks:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No closeout tasks created. Create your first task above!")
    
    # Overall completion metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Completion", "82%", "5%")
    
    with col2:
        st.metric("Documentation", "78%", "8%")
    
    with col3:
        st.metric("Testing Complete", "95%", "2%")
    
    with col4:
        st.metric("Days to Handover", "45")