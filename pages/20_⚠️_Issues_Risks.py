"""
Issues & Risks Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Issues & Risks - gcPanel", page_icon="⚠️", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("⚠️ Issues & Risks Management")
st.markdown("Highland Tower Development - Risk Assessment & Issue Tracking")
st.markdown("---")

if 'issues_risks' not in st.session_state:
    st.session_state.issues_risks = []

tab1, tab2, tab3 = st.tabs(["📊 Issues & Risks Log", "📝 Report Issue/Risk", "📈 Risk Analysis"])

with tab1:
    st.subheader("📊 Issues & Risks Log")
    
    if st.session_state.issues_risks:
        df = pd.DataFrame(st.session_state.issues_risks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search issues/risks...")
        with col2:
            type_filter = st.selectbox("Type", ["All", "Issue", "Risk", "Change Request"])
        with col3:
            priority_filter = st.selectbox("Priority", ["All", "Low", "Medium", "High", "Critical"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
            
        if priority_filter != "All":
            filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
        
        st.write(f"**Total Issues/Risks:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No issues or risks reported. Report your first issue/risk in the Report tab!")

with tab2:
    st.subheader("📝 Report New Issue or Risk")
    
    with st.form("issue_risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_type = st.selectbox("Type", ["Issue", "Risk"])
            category = st.selectbox("Category", 
                ["Schedule", "Budget", "Safety", "Quality", "Technical", "Environmental", "Regulatory", "Resource"])
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            probability = st.selectbox("Probability", ["Low", "Medium", "High"]) if item_type == "Risk" else st.selectbox("Impact", ["Low", "Medium", "High"])
        
        with col2:
            identified_date = st.date_input("Identified Date", value=date.today())
            identified_by = st.text_input("Identified By", value=st.session_state.get('user_name', ''))
            assigned_to = st.text_input("Assigned To", placeholder="Person responsible for resolution")
            target_date = st.date_input("Target Resolution Date")
        
        title = st.text_input("Title", placeholder="Brief description of the issue or risk")
        description = st.text_area("Detailed Description", placeholder="Comprehensive description of the issue or risk...")
        
        if item_type == "Issue":
            impact = st.text_area("Current Impact", placeholder="How is this issue currently affecting the project...")
            immediate_actions = st.text_area("Immediate Actions Taken", placeholder="Actions already implemented...")
        else:
            potential_impact = st.text_area("Potential Impact", placeholder="What could happen if this risk materializes...")
            mitigation_strategy = st.text_area("Mitigation Strategy", placeholder="How to prevent or minimize this risk...")
        
        submitted = st.form_submit_button("⚠️ Submit Issue/Risk", type="primary", use_container_width=True)
        
        if submitted and title:
            new_item = {
                "id": f"IR-{len(st.session_state.issues_risks) + 1:03d}",
                "type": item_type,
                "category": category,
                "severity": severity,
                "probability_impact": probability if item_type == "Risk" else severity,
                "identified_date": str(identified_date),
                "identified_by": identified_by,
                "assigned_to": assigned_to,
                "target_date": str(target_date),
                "title": title,
                "description": description,
                "status": "Open",
                "created_date": str(date.today())
            }
            
            if item_type == "Issue":
                new_item["current_impact"] = impact
                new_item["immediate_actions"] = immediate_actions
            else:
                new_item["potential_impact"] = potential_impact
                new_item["mitigation_strategy"] = mitigation_strategy
            
            st.session_state.issues_risks.insert(0, new_item)
            st.success(f"{item_type} {new_item['id']} submitted successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Issues & Risks Log")
    
    if st.session_state.issues_risks:
        df = pd.DataFrame(st.session_state.issues_risks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search items...")
        with col2:
            type_filter = st.selectbox("Type", ["All", "Issue", "Risk"])
        with col3:
            severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Critical"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
            
        if severity_filter != "All":
            filtered_df = filtered_df[filtered_df['severity'] == severity_filter]
        
        st.write(f"**Total Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No issues or risks reported. Report your first item above!")

with tab3:
    st.subheader("📈 Risk Analysis Dashboard")
    
    if st.session_state.issues_risks:
        df = pd.DataFrame(st.session_state.issues_risks)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(df)
            st.metric("Total Items", total_items)
        
        with col2:
            open_items = len(df[df['status'] == 'Open'])
            st.metric("Open Items", open_items)
        
        with col3:
            high_severity = len(df[df['severity'].isin(['High', 'Critical'])])
            st.metric("High/Critical", high_severity, delta_color="inverse")
        
        with col4:
            risks_count = len(df[df['type'] == 'Risk'])
            st.metric("Active Risks", risks_count)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", "0")
        with col2:
            st.metric("Open Items", "0")
        with col3:
            st.metric("High/Critical", "0")
        with col4:
            st.metric("Active Risks", "0")