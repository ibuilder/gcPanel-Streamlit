"""
Documents module for the gcPanel Construction Management Dashboard.

This module provides management for project documentation including:
1. Current set of plans
2. Ability to upload new documents
3. Current set of submittals (viewable PDFs)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os

# Import the PDF viewer functionality
from modules.pdf_viewer.pdf_viewer import PDFViewer


def render_documents():
    """Render the Documents module"""
    
    st.title("Documents")
    
    # Create tabs for different document types
    tab1, tab2, tab3 = st.tabs(["Construction Plans", "Submittals", "Project Documents"])
    
    # Construction Plans tab
    with tab1:
        render_plans()
    
    # Submittals tab (viewable PDFs)
    with tab2:
        render_submittal_pdfs()
    
    # Project Documents tab
    with tab3:
        render_project_documents()


def render_plans():
    """Render the Construction Plans section"""
    
    st.header("Construction Plans")
    
    # Upload new plans
    st.subheader("Upload New Plans")
    
    upload_col1, upload_col2 = st.columns([3, 1])
    
    with upload_col1:
        uploaded_file = st.file_uploader(
            "Upload new construction plans (PDF)",
            type=["pdf"],
            key="plan_uploader"
        )
    
    with upload_col2:
        plan_category = st.selectbox(
            "Plan Category",
            [
                "Architectural",
                "Structural",
                "Mechanical",
                "Electrical",
                "Plumbing",
                "Civil",
                "Fire Protection",
                "Landscape"
            ],
            key="plan_category"
        )
    
    if uploaded_file and st.button("Save Plan", type="primary", key="save_plan_btn"):
        # In a real app, this would save the file to storage
        st.success(f"Plan '{uploaded_file.name}' uploaded successfully!")
        st.session_state.uploaded_plan = None
        st.rerun()
    
    # Display current plans
    st.subheader("Current Plans")
    
    # Sample plans data
    plans = [
        {
            "id": 1,
            "name": "A-101 - Floor Plans Level 1",
            "category": "Architectural",
            "revision": "C",
            "date": datetime(2025, 1, 15),
            "uploaded_by": "John Smith",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 2.4
        },
        {
            "id": 2,
            "name": "A-102 - Floor Plans Level 2",
            "category": "Architectural",
            "revision": "B",
            "date": datetime(2025, 1, 15),
            "uploaded_by": "John Smith",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 2.1
        },
        {
            "id": 3,
            "name": "S-101 - Foundation Plan",
            "category": "Structural",
            "revision": "A",
            "date": datetime(2025, 1, 10),
            "uploaded_by": "Maria Garcia",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 3.2
        },
        {
            "id": 4,
            "name": "M-101 - HVAC Plans Level 1",
            "category": "Mechanical",
            "revision": "B",
            "date": datetime(2025, 1, 20),
            "uploaded_by": "David Jones",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 2.8
        },
        {
            "id": 5,
            "name": "E-101 - Electrical Plans Level 1",
            "category": "Electrical",
            "revision": "A",
            "date": datetime(2025, 1, 12),
            "uploaded_by": "Sarah Williams",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 1.9
        },
        {
            "id": 6,
            "name": "C-101 - Site Plan",
            "category": "Civil",
            "revision": "D",
            "date": datetime(2025, 1, 5),
            "uploaded_by": "Robert Brown",
            "file_path": "data/sample_pdfs/sample_drawing.pdf",
            "size_mb": 4.5
        }
    ]
    
    # Filters
    category_filter = st.multiselect(
        "Filter by Category",
        list(set(p["category"] for p in plans)),
        default=[],
        key="plans_category_filter"
    )
    
    # Apply filters
    filtered_plans = plans
    if category_filter:
        filtered_plans = [p for p in filtered_plans if p["category"] in category_filter]
    
    # Convert to DataFrame for display
    plans_df = pd.DataFrame(filtered_plans)
    
    # Format for display
    if not plans_df.empty:
        display_plans = plans_df.copy()
        display_plans["date"] = display_plans["date"].dt.strftime("%Y-%m-%d")
        display_plans["size"] = display_plans["size_mb"].apply(lambda x: f"{x:.1f} MB")
        display_plans["action"] = "View"
        
        # Drop unnecessary columns for display
        display_plans = display_plans.drop(columns=["id", "file_path", "size_mb"])
        
        # Reorder columns
        cols = ["name", "category", "revision", "date", "uploaded_by", "size", "action"]
        display_plans = display_plans[cols]
        
        # Display the plans table with view buttons
        st.dataframe(
            display_plans,
            column_config={
                "name": "Drawing Name",
                "category": "Category",
                "revision": "Rev",
                "date": "Date",
                "uploaded_by": "Uploaded By",
                "size": "Size",
                "action": st.column_config.ButtonColumn(
                    "Action",
                    help="View the document",
                )
            },
            hide_index=True
        )
        
        # Handle view button clicks
        if st.session_state.get("dataframe_clicked_row") and st.session_state.dataframe_clicked_row.get("action") == "View":
            row_index = st.session_state.dataframe_clicked_row_index
            selected_plan = plans[row_index]
            
            # Set the selected plan for viewing
            st.session_state.selected_document_path = selected_plan["file_path"]
            st.session_state.selected_document_name = selected_plan["name"]
            
            # Display the selected document
            if st.session_state.get("selected_document_path"):
                render_pdf_embed(
                    st.session_state.selected_document_path,
                    st.session_state.selected_document_name
                )
    else:
        st.info("No plans found matching the selected filters.")


def render_submittal_pdfs():
    """Render the Submittals PDFs section"""
    
    st.header("Submittal Documents")
    
    # Sample submittal documents
    submittal_docs = [
        {
            "id": 1,
            "number": "S-001",
            "title": "Structural Steel Shop Drawings",
            "spec_section": "05 12 00",
            "status": "Approved",
            "date_submitted": datetime(2025, 2, 5),
            "file_path": "data/sample_pdfs/sample_submittal.pdf",
            "size_mb": 5.2
        },
        {
            "id": 2,
            "number": "S-002",
            "title": "Concrete Mix Design",
            "spec_section": "03 30 00",
            "status": "Approved as Noted",
            "date_submitted": datetime(2025, 2, 10),
            "file_path": "data/sample_pdfs/sample_submittal.pdf",
            "size_mb": 3.7
        },
        {
            "id": 3,
            "number": "S-003",
            "title": "Curtain Wall System",
            "spec_section": "08 44 13",
            "status": "Revise and Resubmit",
            "date_submitted": datetime(2025, 2, 15),
            "file_path": "data/sample_pdfs/sample_submittal.pdf",
            "size_mb": 8.1
        },
        {
            "id": 4,
            "number": "S-004",
            "title": "HVAC Equipment",
            "spec_section": "23 00 00",
            "status": "Approved",
            "date_submitted": datetime(2025, 2, 20),
            "file_path": "data/sample_pdfs/sample_submittal.pdf",
            "size_mb": 6.4
        },
        {
            "id": 5,
            "number": "S-005",
            "title": "Electrical Fixtures",
            "spec_section": "26 50 00",
            "status": "Approved as Noted",
            "date_submitted": datetime(2025, 2, 25),
            "file_path": "data/sample_pdfs/sample_submittal.pdf",
            "size_mb": 4.9
        }
    ]
    
    # Filters
    status_filter = st.multiselect(
        "Filter by Status",
        list(set(doc["status"] for doc in submittal_docs)),
        default=[],
        key="submittal_docs_status_filter"
    )
    
    # Apply filters
    filtered_docs = submittal_docs
    if status_filter:
        filtered_docs = [doc for doc in filtered_docs if doc["status"] in status_filter]
    
    # Convert to DataFrame for display
    docs_df = pd.DataFrame(filtered_docs)
    
    # Format for display
    if not docs_df.empty:
        display_docs = docs_df.copy()
        display_docs["date_submitted"] = display_docs["date_submitted"].dt.strftime("%Y-%m-%d")
        display_docs["size"] = display_docs["size_mb"].apply(lambda x: f"{x:.1f} MB")
        display_docs["action"] = "View"
        
        # Drop unnecessary columns for display
        display_docs = display_docs.drop(columns=["id", "file_path", "size_mb"])
        
        # Reorder columns
        cols = ["number", "title", "spec_section", "status", "date_submitted", "size", "action"]
        display_docs = display_docs[cols]
        
        # Create a color map for status
        status_colors = {
            "Approved": "#38d39f",
            "Approved as Noted": "#f9c851",
            "Revise and Resubmit": "#ff5b5b",
            "Rejected": "#dc3545"
        }
        
        # Display the submittal documents table with view buttons
        st.dataframe(
            display_docs,
            column_config={
                "number": "Submittal #",
                "title": "Title",
                "spec_section": "Spec Section",
                "status": st.column_config.TextColumn(
                    "Status",
                    help="Approval status of the submittal",
                    width="medium",
                ),
                "date_submitted": "Date Submitted",
                "size": "Size",
                "action": st.column_config.ButtonColumn(
                    "Action",
                    help="View the document",
                )
            },
            hide_index=True
        )
        
        # Handle view button clicks
        if st.session_state.get("dataframe_clicked_row") and st.session_state.dataframe_clicked_row.get("action") == "View":
            row_index = st.session_state.dataframe_clicked_row_index
            selected_doc = submittal_docs[row_index]
            
            # Set the selected document for viewing
            st.session_state.selected_document_path = selected_doc["file_path"]
            st.session_state.selected_document_name = f"{selected_doc['number']} - {selected_doc['title']}"
            
            # Display the selected document
            if st.session_state.get("selected_document_path"):
                render_pdf_embed(
                    st.session_state.selected_document_path,
                    st.session_state.selected_document_name
                )
    else:
        st.info("No submittal documents found matching the selected filters.")


def render_project_documents():
    """Render the Project Documents section"""
    
    st.header("Project Documents")
    
    # Upload new document
    st.subheader("Upload New Document")
    
    upload_col1, upload_col2 = st.columns([3, 1])
    
    with upload_col1:
        uploaded_file = st.file_uploader(
            "Upload new project document (PDF)",
            type=["pdf"],
            key="document_uploader"
        )
    
    with upload_col2:
        doc_category = st.selectbox(
            "Document Category",
            [
                "Contract Documents",
                "Project Manual",
                "Specifications",
                "Permits",
                "Meeting Minutes",
                "Correspondence",
                "Reports",
                "Photos"
            ],
            key="document_category"
        )
    
    if uploaded_file and st.button("Save Document", type="primary", key="save_doc_btn"):
        # In a real app, this would save the file to storage
        st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
        st.session_state.uploaded_document = None
        st.rerun()
    
    # Display current project documents
    st.subheader("Current Documents")
    
    # Sample project documents
    documents = [
        {
            "id": 1,
            "name": "Project Manual.pdf",
            "category": "Project Manual",
            "date": datetime(2025, 1, 5),
            "uploaded_by": "John Smith",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 8.7
        },
        {
            "id": 2,
            "name": "Technical Specifications.pdf",
            "category": "Specifications",
            "date": datetime(2025, 1, 8),
            "uploaded_by": "Maria Garcia",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 12.3
        },
        {
            "id": 3,
            "name": "Building Permit.pdf",
            "category": "Permits",
            "date": datetime(2025, 1, 10),
            "uploaded_by": "David Jones",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 1.5
        },
        {
            "id": 4,
            "name": "Owner-Contractor Agreement.pdf",
            "category": "Contract Documents",
            "date": datetime(2025, 1, 3),
            "uploaded_by": "Sarah Williams",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 4.2
        },
        {
            "id": 5,
            "name": "Progress Meeting Minutes 01.pdf",
            "category": "Meeting Minutes",
            "date": datetime(2025, 2, 1),
            "uploaded_by": "Robert Brown",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 0.8
        },
        {
            "id": 6,
            "name": "Geotechnical Report.pdf",
            "category": "Reports",
            "date": datetime(2024, 12, 10),
            "uploaded_by": "Jennifer Johnson",
            "file_path": "data/sample_pdfs/sample_document.pdf",
            "size_mb": 15.6
        }
    ]
    
    # Filters
    category_filter = st.multiselect(
        "Filter by Category",
        list(set(doc["category"] for doc in documents)),
        default=[],
        key="documents_category_filter"
    )
    
    # Apply filters
    filtered_documents = documents
    if category_filter:
        filtered_documents = [doc for doc in filtered_documents if doc["category"] in category_filter]
    
    # Convert to DataFrame for display
    docs_df = pd.DataFrame(filtered_documents)
    
    # Format for display
    if not docs_df.empty:
        display_docs = docs_df.copy()
        display_docs["date"] = display_docs["date"].dt.strftime("%Y-%m-%d")
        display_docs["size"] = display_docs["size_mb"].apply(lambda x: f"{x:.1f} MB")
        display_docs["action"] = "View"
        
        # Drop unnecessary columns for display
        display_docs = display_docs.drop(columns=["id", "file_path", "size_mb"])
        
        # Reorder columns
        cols = ["name", "category", "date", "uploaded_by", "size", "action"]
        display_docs = display_docs[cols]
        
        # Display the documents table with view buttons
        st.dataframe(
            display_docs,
            column_config={
                "name": "Document Name",
                "category": "Category",
                "date": "Date",
                "uploaded_by": "Uploaded By",
                "size": "Size",
                "action": st.column_config.ButtonColumn(
                    "Action",
                    help="View the document",
                )
            },
            hide_index=True
        )
        
        # Handle view button clicks
        if st.session_state.get("dataframe_clicked_row") and st.session_state.dataframe_clicked_row.get("action") == "View":
            row_index = st.session_state.dataframe_clicked_row_index
            selected_doc = documents[row_index]
            
            # Set the selected document for viewing
            st.session_state.selected_document_path = selected_doc["file_path"]
            st.session_state.selected_document_name = selected_doc["name"]
            
            # Display the selected document
            if st.session_state.get("selected_document_path"):
                render_pdf_embed(
                    st.session_state.selected_document_path,
                    st.session_state.selected_document_name
                )
    else:
        st.info("No documents found matching the selected filters.")