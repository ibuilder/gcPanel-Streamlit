"""
Documents module for the gcPanel Construction Management Dashboard.

This module provides management for project documentation including:
1. Current set of plans
2. Specifications
3. Project documents (contract documents, permits, etc.)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os

# Import the PDF viewer helper
from modules.documents.pdf_helper import display_pdf_document


def render_documents():
    """Render the Documents module"""
    
    st.title("Documents")
    
    # Create tabs for different document types
    tab1, tab2, tab3 = st.tabs(["Construction Plans", "Specifications", "Project Documents"])
    
    # Construction Plans tab
    with tab1:
        render_plans()
    
    # Specifications tab
    with tab2:
        render_specifications()
    
    # Project Documents tab
    with tab3:
        render_project_documents()


def render_plans():
    """Render the Construction Plans section"""
    
    # Header with Upload button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Construction Plans")
    
    with col3:
        if st.button("Upload New Plans", type="primary", key="upload_plans_top"):
            st.session_state.show_plans_upload = True
    
    # Display upload form based on session state
    if st.session_state.get("show_plans_upload", False):
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
            
            # Add buttons for submission and cancel
            if st.button("Submit", type="primary", key="submit_plan_upload"):
                if uploaded_file:
                    st.success("Plan uploaded successfully!")
                    st.session_state.show_plans_upload = False
                    st.rerun()
                else:
                    st.error("Please select a file to upload")
                    
            if st.button("Cancel", key="cancel_plan_upload"):
                st.session_state.show_plans_upload = False
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
        clicked = st.dataframe(
            display_plans,
            column_config={
                "name": "Drawing Name",
                "category": "Category",
                "revision": "Rev",
                "date": "Date",
                "uploaded_by": "Uploaded By",
                "size": "Size",
                "action": "Action"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add separate view buttons for each plan
        st.write("### View Plans")
        for i, plan in enumerate(filtered_plans):
            if st.button(f"View {plan['name']}", key=f"view_plan_{i}"):
                # Set the selected plan for viewing
                st.session_state.selected_document_path = plan["file_path"]
                st.session_state.selected_document_name = plan["name"]
                st.rerun()
        
        # Display the selected document
        if st.session_state.get("selected_document_path"):
            display_pdf_document(
                st.session_state.selected_document_path,
                st.session_state.selected_document_name
            )
    else:
        st.info("No plans found matching the selected filters.")

def render_specifications():
    """Render the Specifications section"""
    
    st.header("Specifications")
    
    # Upload new specification section
    st.subheader("Upload New Specification")
    
    upload_col1, upload_col2 = st.columns([3, 1])
    
    with upload_col1:
        uploaded_file = st.file_uploader(
            "Upload new specification section (PDF)",
            type=["pdf"],
            key="spec_uploader"
        )
    
    with upload_col2:
        spec_division = st.selectbox(
            "Division",
            [
                "01 - General Requirements",
                "02 - Existing Conditions",
                "03 - Concrete",
                "04 - Masonry",
                "05 - Metals",
                "06 - Wood, Plastics, and Composites",
                "07 - Thermal and Moisture Protection",
                "08 - Openings",
                "09 - Finishes",
                "10 - Specialties",
                "11 - Equipment",
                "12 - Furnishings",
                "13 - Special Construction",
                "14 - Conveying Equipment",
                "21 - Fire Suppression",
                "22 - Plumbing",
                "23 - HVAC",
                "26 - Electrical",
                "27 - Communications",
                "28 - Electronic Safety and Security",
                "31 - Earthwork",
                "32 - Exterior Improvements",
                "33 - Utilities"
            ],
            key="spec_division"
        )
    
    if uploaded_file and st.button("Save Specification", type="primary", key="save_spec_btn"):
        # In a real app, this would save the file to storage
        st.success(f"Specification '{uploaded_file.name}' uploaded successfully!")
        st.session_state.uploaded_spec = None
        st.rerun()
    
    # Display current specifications
    st.subheader("Project Specifications")
    
    # Sample specifications data
    specifications = [
        {
            "id": 1,
            "number": "03 30 00",
            "title": "Cast-in-Place Concrete",
            "division": "03 - Concrete",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 1.8
        },
        {
            "id": 2,
            "number": "04 20 00",
            "title": "Unit Masonry",
            "division": "04 - Masonry",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 2.2
        },
        {
            "id": 3,
            "number": "05 12 00",
            "title": "Structural Steel Framing",
            "division": "05 - Metals",
            "revision": "1",
            "date": datetime(2025, 1, 15),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 3.1
        },
        {
            "id": 4,
            "number": "07 21 00",
            "title": "Thermal Insulation",
            "division": "07 - Thermal and Moisture Protection",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 1.5
        },
        {
            "id": 5,
            "number": "08 11 13",
            "title": "Hollow Metal Doors and Frames",
            "division": "08 - Openings",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 2.0
        },
        {
            "id": 6,
            "number": "09 91 23",
            "title": "Interior Painting",
            "division": "09 - Finishes",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 1.7
        },
        {
            "id": 7,
            "number": "22 14 00",
            "title": "Facility Storm Drainage",
            "division": "22 - Plumbing",
            "revision": "0",
            "date": datetime(2025, 1, 10),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 2.3
        },
        {
            "id": 8,
            "number": "26 05 00",
            "title": "Common Work Results for Electrical",
            "division": "26 - Electrical",
            "revision": "1",
            "date": datetime(2025, 1, 15),
            "file_path": "data/sample_pdfs/sample_specification.pdf",
            "size_mb": 3.5
        }
    ]
    
    # Group specifications by division
    divisions = {}
    for spec in specifications:
        if spec["division"] not in divisions:
            divisions[spec["division"]] = []
        divisions[spec["division"]].append(spec)
    
    # Display specifications by division
    for division, specs in sorted(divisions.items()):
        with st.expander(division, expanded=True):
            # Create DataFrame for this division
            df = pd.DataFrame(specs)
            df["date"] = df["date"].dt.strftime("%Y-%m-%d")
            df["size"] = df["size_mb"].apply(lambda x: f"{x:.1f} MB")
            
            # Format for display
            display_df = df[["number", "title", "revision", "date", "size"]]
            
            # Display the table
            st.dataframe(
                display_df,
                column_config={
                    "number": "Section",
                    "title": "Title",
                    "revision": "Rev",
                    "date": "Date",
                    "size": "Size"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Add view buttons for each specification
            cols = st.columns(len(specs))
            for i, (col, spec) in enumerate(zip(cols, specs)):
                with col:
                    if st.button(f"View {spec['number']}", key=f"view_spec_{spec['id']}"):
                        st.session_state.selected_document_path = spec["file_path"]
                        st.session_state.selected_document_name = f"{spec['number']} - {spec['title']}"
                        st.rerun()
    
    # Display the selected document
    if st.session_state.get("selected_document_path"):
        display_pdf_document(
            st.session_state.selected_document_path,
            st.session_state.selected_document_name
        )


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
            "category": "Project Manual",
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
        
        # Drop unnecessary columns for display
        display_docs = display_docs.drop(columns=["id", "file_path", "size_mb"])
        
        # Reorder columns
        cols = ["name", "category", "date", "uploaded_by", "size"]
        display_docs = display_docs[cols]
        
        # Display the documents table
        st.dataframe(
            display_docs,
            column_config={
                "name": "Document Name",
                "category": "Category",
                "date": "Date",
                "uploaded_by": "Uploaded By",
                "size": "Size"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add view buttons for each document
        st.write("### View Documents")
        doc_cols = st.columns(3)
        for i, doc in enumerate(filtered_documents):
            col_index = i % 3
            with doc_cols[col_index]:
                if st.button(f"View {doc['name']}", key=f"view_doc_{doc['id']}"):
                    st.session_state.selected_document_path = doc["file_path"]
                    st.session_state.selected_document_name = doc["name"]
                    st.rerun()
        
        # Display the selected document
        if st.session_state.get("selected_document_path"):
            display_pdf_document(
                st.session_state.selected_document_path,
                st.session_state.selected_document_name
            )
    else:
        st.info("No documents found matching the selected filters.")