"""
Quality Control Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Quality Control - gcPanel", page_icon="🔍", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🔍 Quality Control")
st.markdown("Highland Tower Development - Quality Assurance & Inspection Management")
st.markdown("---")

if 'quality_items' not in st.session_state:
    st.session_state.quality_items = []

tab1, tab2, tab3 = st.tabs(["📊 QC Records", "📝 Create Quality Check", "📈 Quality Metrics"])

with tab1:
    st.subheader("📊 Quality Control Records")
    
    if st.session_state.quality_items:
        df = pd.DataFrame(st.session_state.quality_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search QC records...", key="quality_control_search_1")
        with col2:
            type_filter = st.selectbox("Type", ["All", "Material Test", "Visual Inspection", "Performance Test"])
        with col3:
            result_filter = st.selectbox("Result", ["All", "Pass", "Fail", "Conditional"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
            
        if result_filter != "All":
            filtered_df = filtered_df[filtered_df['result'] == result_filter]
        
        st.write(f"**Total QC Records:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No quality control records available. Create your first QC check in the Create tab!")

with tab2:
    st.subheader("📝 Create Quality Check")
    
    with st.form("quality_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            inspection_type = st.selectbox("Inspection Type", 
                ["Visual Inspection", "Dimensional Check", "Material Testing", "Safety Compliance", "Code Compliance"])
            work_item = st.text_input("Work Item", placeholder="Component or area being inspected")
            inspector = st.text_input("Inspector", value=st.session_state.get('user_name', ''))
            inspection_date = st.date_input("Inspection Date", value=date.today())
        
        with col2:
            location = st.text_input("Location", placeholder="Building area, floor, grid")
            contractor = st.text_input("Contractor", placeholder="Responsible contractor")
            specification_ref = st.text_input("Specification Reference", placeholder="Spec section")
            drawing_ref = st.text_input("Drawing Reference", placeholder="Drawing numbers")
        
        inspection_criteria = st.text_area("Inspection Criteria", placeholder="Standards and requirements to check...")
        findings = st.text_area("Findings", placeholder="Inspection results and observations...")
        
        col3, col4 = st.columns(2)
        with col3:
            result = st.selectbox("Result", ["Pass", "Fail", "Conditional Pass", "Re-inspection Required"])
        with col4:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        corrective_actions = st.text_area("Corrective Actions", placeholder="Required actions if failed...")
        
        submitted = st.form_submit_button("🔍 Submit QC Check", type="primary", use_container_width=True)
        
        if submitted and work_item:
            new_qc = {
                "id": f"QC-{len(st.session_state.quality_items) + 1:03d}",
                "inspection_type": inspection_type,
                "work_item": work_item,
                "inspector": inspector,
                "inspection_date": str(inspection_date),
                "location": location,
                "contractor": contractor,
                "specification_ref": specification_ref,
                "drawing_ref": drawing_ref,
                "inspection_criteria": inspection_criteria,
                "findings": findings,
                "result": result,
                "priority": priority,
                "corrective_actions": corrective_actions,
                "status": "Completed" if result == "Pass" else "Action Required"
            }
            st.session_state.quality_items.insert(0, new_qc)
            st.success(f"Quality check {new_qc['id']} submitted successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Quality Control Records")
    
    if st.session_state.quality_items:
        df = pd.DataFrame(st.session_state.quality_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search QC records...")
        with col2:
            result_filter = st.selectbox("Result", ["All", "Pass", "Fail", "Conditional Pass"])
        with col3:
            type_filter = st.selectbox("Type", ["All", "Visual Inspection", "Material Testing", "Safety Compliance"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if result_filter != "All":
            filtered_df = filtered_df[filtered_df['result'] == result_filter]
            
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['inspection_type'] == type_filter]
        
        st.write(f"**Total QC Records:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No quality control records. Create your first QC check above!")

with tab3:
    st.subheader("📈 Quality Metrics")
    
    if st.session_state.quality_items:
        df = pd.DataFrame(st.session_state.quality_items)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_inspections = len(df)
            st.metric("Total Inspections", total_inspections)
        
        with col2:
            pass_rate = len(df[df['result'] == 'Pass']) / len(df) * 100 if len(df) > 0 else 0
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        
        with col3:
            failed = len(df[df['result'] == 'Fail'])
            st.metric("Failed Inspections", failed)
        
        with col4:
            pending_actions = len(df[df['status'] == 'Action Required'])
            st.metric("Pending Actions", pending_actions)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Inspections", "0")
        with col2:
            st.metric("Pass Rate", "N/A")
        with col3:
            st.metric("Failed Inspections", "0")
        with col4:
            st.metric("Pending Actions", "0")