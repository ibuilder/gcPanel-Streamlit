"""
Document Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Documents - gcPanel", page_icon="📁", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📁 Document Management")
st.markdown("Highland Tower Development - Project Document Repository")
st.markdown("---")

if 'documents' not in st.session_state:
    st.session_state.documents = []

tab1, tab2, tab3 = st.tabs(["📤 Upload Document", "📁 Document Library", "🔍 Search & Filter"])

with tab1:
    st.subheader("📤 Upload New Document")
    
    with st.form("document_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            document_title = st.text_input("Document Title", placeholder="Descriptive document name")
            document_type = st.selectbox("Document Type", 
                ["Drawings", "Specifications", "Contracts", "Reports", "Photos", "Correspondence", "Permits", "Other"])
            discipline = st.selectbox("Discipline", 
                ["General", "Architectural", "Structural", "Mechanical", "Electrical", "Civil"])
            version = st.text_input("Version/Revision", placeholder="e.g., Rev 1, v2.0")
        
        with col2:
            upload_date = st.date_input("Upload Date", value=date.today())
            uploaded_by = st.text_input("Uploaded By", value=st.session_state.get('user_name', ''))
            project_phase = st.selectbox("Project Phase", 
                ["Pre-Design", "Design Development", "Construction Documents", "Construction", "Closeout"])
            confidentiality = st.selectbox("Confidentiality", ["Public", "Internal", "Confidential", "Restricted"])
        
        description = st.text_area("Description", placeholder="Document description and purpose...")
        keywords = st.text_input("Keywords", placeholder="Comma-separated keywords for search")
        
        # File upload
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'dwg', 'jpg', 'png'])
        
        submitted = st.form_submit_button("📁 Upload Document", type="primary", use_container_width=True)
        
        if submitted and document_title:
            file_size = "N/A"
            file_name = "No file selected"
            if uploaded_file:
                file_size = f"{len(uploaded_file.getvalue()) / 1024:.1f} KB"
                file_name = uploaded_file.name
            
            new_document = {
                "id": f"DOC-{len(st.session_state.documents) + 1:03d}",
                "title": document_title,
                "type": document_type,
                "discipline": discipline,
                "version": version,
                "upload_date": str(upload_date),
                "uploaded_by": uploaded_by,
                "project_phase": project_phase,
                "confidentiality": confidentiality,
                "description": description,
                "keywords": keywords,
                "file_name": file_name,
                "file_size": file_size,
                "status": "Active"
            }
            st.session_state.documents.insert(0, new_document)
            st.success(f"Document {new_document['id']} uploaded successfully!")
            st.rerun()

with tab2:
    st.subheader("📁 Document Library")
    
    if st.session_state.documents:
        df = pd.DataFrame(st.session_state.documents)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search documents...")
        with col2:
            type_filter = st.selectbox("Document Type", ["All", "Drawings", "Specifications", "Contracts"])
        with col3:
            discipline_filter = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
            
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df['discipline'] == discipline_filter]
        
        st.write(f"**Total Documents:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No documents uploaded. Upload your first document above!")

with tab3:
    st.subheader("🔍 Advanced Search & Analytics")
    
    if st.session_state.documents:
        df = pd.DataFrame(st.session_state.documents)
        
        # Document statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_docs = len(df)
            st.metric("Total Documents", total_docs)
        
        with col2:
            recent_docs = len(df[pd.to_datetime(df['upload_date']) >= pd.Timestamp.now() - pd.Timedelta(days=7)])
            st.metric("Added This Week", recent_docs)
        
        with col3:
            drawings_count = len(df[df['type'] == 'Drawings'])
            st.metric("Drawings", drawings_count)
        
        with col4:
            specs_count = len(df[df['type'] == 'Specifications'])
            st.metric("Specifications", specs_count)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Documents", "0")
        with col2:
            st.metric("Added This Week", "0")
        with col3:
            st.metric("Drawings", "0")
        with col4:
            st.metric("Specifications", "0")