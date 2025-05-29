"""
Transmittals Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Transmittals - gcPanel", page_icon="📺", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📺 Transmittals Management")
st.markdown("Highland Tower Development - Document Transmittal Tracking")
st.markdown("---")

if 'transmittals' not in st.session_state:
    st.session_state.transmittals = []

tab1, tab2 = st.tabs(["📝 Create Transmittal", "📊 Transmittal Log"])

with tab1:
    st.subheader("📝 Create New Transmittal")
    
    with st.form("transmittal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            transmittal_number = st.text_input("Transmittal Number", 
                value=f"TX-{len(st.session_state.transmittals) + 1:03d}", disabled=True)
            to_company = st.text_input("To (Company)", placeholder="Recipient company")
            to_attention = st.text_input("Attention", placeholder="Recipient contact person")
            project_name = st.text_input("Project", value="Highland Tower Development")
        
        with col2:
            transmittal_date = st.date_input("Date", value=date.today())
            from_company = st.text_input("From (Company)", placeholder="Sender company")
            delivery_method = st.selectbox("Delivery Method", 
                ["Email", "Hand Delivery", "Courier", "Mail", "FTP", "Cloud"])
            copies_to = st.text_input("Copies To", placeholder="Additional recipients")
        
        subject = st.text_input("Subject", placeholder="Purpose of transmittal")
        description = st.text_area("Description", placeholder="Description of transmitted documents...")
        
        st.markdown("**Document List**")
        doc_count = st.number_input("Number of Documents", min_value=1, max_value=20, value=1)
        
        documents = []
        for i in range(doc_count):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                doc_title = st.text_input(f"Document {i+1} Title", key=f"doc_title_{i}")
            with col_b:
                doc_number = st.text_input(f"Document {i+1} Number", key=f"doc_number_{i}")
            with col_c:
                doc_revision = st.text_input(f"Rev", key=f"doc_rev_{i}", value="0")
            
            if doc_title:
                documents.append({
                    "title": doc_title,
                    "number": doc_number,
                    "revision": doc_revision
                })
        
        submitted = st.form_submit_button("📤 Send Transmittal", type="primary", use_container_width=True)
        
        if submitted and to_company and subject:
            new_transmittal = {
                "id": transmittal_number,
                "date": str(transmittal_date),
                "to_company": to_company,
                "to_attention": to_attention,
                "from_company": from_company,
                "project_name": project_name,
                "subject": subject,
                "description": description,
                "delivery_method": delivery_method,
                "copies_to": copies_to,
                "documents": documents,
                "document_count": len(documents),
                "status": "Sent",
                "created_by": st.session_state.get('user_name', 'User')
            }
            st.session_state.transmittals.insert(0, new_transmittal)
            st.success(f"Transmittal {new_transmittal['id']} created successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Transmittal Log")
    
    if st.session_state.transmittals:
        df = pd.DataFrame(st.session_state.transmittals)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search transmittals...")
        with col2:
            company_filter = st.selectbox("To Company", ["All"] + list(df['to_company'].unique()) if len(df) > 0 else ["All"])
        with col3:
            method_filter = st.selectbox("Delivery Method", ["All", "Email", "Hand Delivery", "Courier"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if company_filter != "All":
            filtered_df = filtered_df[filtered_df['to_company'] == company_filter]
            
        if method_filter != "All":
            filtered_df = filtered_df[filtered_df['delivery_method'] == method_filter]
        
        st.write(f"**Total Transmittals:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No transmittals created. Create your first transmittal above!")