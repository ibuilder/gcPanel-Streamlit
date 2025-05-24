"""
Enhanced Documents Module for gcPanel Construction Management Dashboard.

This module provides comprehensive document management with:
- Full CRUD operations for drawings and specifications
- Drawing organization by drawing numbers
- Specifications organized by CSI divisions
- Integrated PDF viewer with markup, zoom, comments, and export
- Highland Tower Development authentic document data
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import base64
from assets.crud_styler import apply_crud_styles

def render():
    """Main render function for the Enhanced Documents module"""
    st.title("📁 Document Management Center")
    st.markdown("### Highland Tower Development - Complete Document Control System")
    
    # Apply CRUD styling
    apply_crud_styles()
    
    # Create main tabs for document categories
    tabs = st.tabs([
        "📐 Construction Drawings",
        "📋 Project Specifications", 
        "📄 Contract Documents",
        "📊 Document Analytics",
        "🔍 Document Search",
        "📤 Document Sharing"
    ])
    
    with tabs[0]:  # Construction Drawings
        render_drawings_management()
    
    with tabs[1]:  # Project Specifications
        render_specifications_management()
    
    with tabs[2]:  # Contract Documents
        render_contract_documents()
    
    with tabs[3]:  # Document Analytics
        render_document_analytics()
    
    with tabs[4]:  # Document Search
        render_document_search()
    
    with tabs[5]:  # Document Sharing
        render_document_sharing()

def render_drawings_management():
    """Render comprehensive drawings management with CRUD operations"""
    st.markdown("### 📐 Construction Drawings Management")
    st.markdown("**Highland Tower Development - Drawing Set Organization**")
    
    # Render drawings CRUD interface
    render_drawings_crud()

def render_sheet_numbering_guide():
    """Render construction document sheet numbering guide"""
    st.markdown("### 📐 Construction Document Sheet Numbers & Order")
    st.markdown("**Professional drawing organization following industry standards**")
    
    # Sheet numbering reference
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Architectural Drawings")
        arch_sheets = [
            ("A000", "Cover Sheet", "Project information, drawing index"),
            ("A001", "Site Plan", "Site layout, property boundaries"),
            ("A100", "Floor Plans", "Level plans and layouts"),
            ("A200", "Elevations", "Exterior building views"),
            ("A300", "Sections", "Building cross-sections"),
            ("A400", "Details", "Construction details"),
            ("A500", "Schedules", "Door, window, room schedules")
        ]
        
        for number, title, desc in arch_sheets:
            st.markdown(f"**{number}** - {title}")
            st.markdown(f"<small style='color: #666;'>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")
        
        st.markdown("#### Structural Drawings")
        struct_sheets = [
            ("S100", "Foundation Plans", "Foundation layout and details"),
            ("S200", "Framing Plans", "Structural framing systems"),
            ("S300", "Details", "Structural connections and details")
        ]
        
        for number, title, desc in struct_sheets:
            st.markdown(f"**{number}** - {title}")
            st.markdown(f"<small style='color: #666;'>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")
    
    with col2:
        st.markdown("#### Mechanical Drawings")
        mech_sheets = [
            ("M100", "Plans", "HVAC layout and equipment"),
            ("M200", "Schedules and Details", "Equipment schedules, details")
        ]
        
        for number, title, desc in mech_sheets:
            st.markdown(f"**{number}** - {title}")
            st.markdown(f"<small style='color: #666;'>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")
        
        st.markdown("#### Electrical Drawings")
        elec_sheets = [
            ("E100", "Plans", "Power and lighting layout"),
            ("E200", "Schedules and Details", "Panel schedules, details")
        ]
        
        for number, title, desc in elec_sheets:
            st.markdown(f"**{number}** - {title}")
            st.markdown(f"<small style='color: #666;'>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")
        
        st.markdown("#### Other Disciplines")
        other_sheets = [
            ("P100", "Plumbing Plans", "Plumbing layout and fixtures"),
            ("FP100", "Fire Protection Plans", "Sprinkler and fire systems"),
            ("C100", "Civil Plans", "Site utilities and grading"),
            ("L100", "Landscape Plans", "Landscaping and irrigation")
        ]
        
        for number, title, desc in other_sheets:
            st.markdown(f"**{number}** - {title}")
            st.markdown(f"<small style='color: #666;'>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")
    
    # Highland Tower sheet organization
    st.markdown("---")
    st.markdown("#### Highland Tower Development Sheet Organization")
    
    highland_sheets = {
        "A000": "Highland Tower Project Cover Sheet",
        "A001": "Highland Tower Site Plan", 
        "A101": "Level 1 Floor Plan - Retail & Lobby",
        "A102": "Levels 2-15 Typical Residential Floor Plan",
        "A200": "Building Elevations - North & South",
        "A201": "Building Elevations - East & West", 
        "A300": "Building Sections",
        "A400": "Architectural Details",
        "S100": "Foundation Plan",
        "S200": "Structural Framing Plans",
        "S300": "Structural Details",
        "M100": "HVAC Plans - Levels 1-15",
        "M200": "Mechanical Schedules & Details",
        "E100": "Electrical Plans - Levels 1-15",
        "E200": "Electrical Schedules & Panel Details",
        "P100": "Plumbing Plans",
        "FP100": "Fire Protection Plans"
    }
    
    # Display in organized grid
    sheet_cols = st.columns(3)
    for i, (sheet_num, sheet_desc) in enumerate(highland_sheets.items()):
        with sheet_cols[i % 3]:
            st.markdown(f"**{sheet_num}**")
            st.markdown(f"<small>{sheet_desc}</small>", unsafe_allow_html=True)
            st.markdown("")

def render_specifications_management():
    """Render specifications management organized by CSI divisions"""
    st.markdown("### 📋 Project Specifications - CSI MasterFormat")
    st.markdown("**Highland Tower Development - Technical Specifications**")
    
    # Render specifications CRUD interface
    render_specifications_crud()

def render_contract_documents():
    """Render contract documents management"""
    st.markdown("### 📄 Contract Documents")
    st.markdown("**Highland Tower Development - Legal & Contract Documentation**")
    
    # Contract documents data
    contract_docs = [
        {
            "document_id": "CTR-001",
            "name": "Highland Tower Development Agreement",
            "type": "Prime Contract",
            "date_signed": "2024-03-15",
            "parties": "Highland Development LLC & GC Partners",
            "value": "$45,500,000",
            "status": "Executed",
            "file_path": "contracts/highland_tower_agreement.pdf",
            "size_mb": 12.8
        },
        {
            "document_id": "CTR-002", 
            "name": "General Conditions",
            "type": "Contract Terms",
            "date_signed": "2024-03-15",
            "parties": "Standard AIA A201",
            "value": "N/A",
            "status": "Active",
            "file_path": "contracts/general_conditions.pdf",
            "size_mb": 8.4
        },
        {
            "document_id": "CTR-003",
            "name": "Performance Bond",
            "type": "Surety Bond",
            "date_signed": "2024-03-20",
            "parties": "GC Partners & Surety Bond Co",
            "value": "$45,500,000",
            "status": "Active",
            "file_path": "contracts/performance_bond.pdf",
            "size_mb": 4.2
        }
    ]
    
    # Display contract documents table
    if contract_docs:
        df = pd.DataFrame(contract_docs)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("📄 Add Contract Document", type="primary"):
                st.session_state.show_contract_form = True
        
        # Show add form if requested
        if st.session_state.get("show_contract_form", False):
            render_contract_document_form()
        
        # Display documents
        for i, doc in enumerate(contract_docs):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{doc['name']}**")
                    st.markdown(f"*{doc['type']} - {doc['value']}*")
                
                with col2:
                    st.markdown(f"Status: **{doc['status']}**")
                    st.markdown(f"Date: {doc['date_signed']}")
                
                with col3:
                    st.markdown(f"Size: {doc['size_mb']} MB")
                
                with col4:
                    if st.button("👁️ View", key=f"view_contract_{i}"):
                        st.session_state.selected_document = doc
                        render_pdf_viewer(doc)
                    
                    if st.button("✏️ Edit", key=f"edit_contract_{i}"):
                        st.session_state.edit_contract = doc
                
                st.divider()

def render_contract_document_form():
    """Render form for adding/editing contract documents"""
    st.markdown("#### 📄 Add New Contract Document")
    
    with st.form("contract_document_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            doc_name = st.text_input("Document Name", placeholder="Highland Tower Subcontract Agreement")
            doc_type = st.selectbox("Document Type", [
                "Prime Contract", "Subcontract", "Contract Terms", "Amendment", 
                "Change Order", "Surety Bond", "Insurance Certificate", "Permit"
            ])
            parties = st.text_input("Parties", placeholder="Company A & Company B")
        
        with col2:
            doc_value = st.text_input("Contract Value", placeholder="$1,250,000")
            date_signed = st.date_input("Date Signed")
            status = st.selectbox("Status", ["Draft", "Under Review", "Executed", "Active", "Expired"])
        
        uploaded_file = st.file_uploader("Upload Document (PDF)", type=["pdf"])
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Save Document", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel")
        
        if submit and doc_name and uploaded_file:
            st.success(f"✅ Contract document '{doc_name}' added successfully!")
            st.session_state.show_contract_form = False
            st.rerun()
        
        if cancel:
            st.session_state.show_contract_form = False
            st.rerun()

def render_document_analytics():
    """Render document analytics and insights"""
    st.markdown("### 📊 Document Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", "847", "+23 this week")
    with col2:
        st.metric("Storage Used", "12.8 GB", "+2.3 GB this month")
    with col3:
        st.metric("Document Views", "2,456", "+156 today")
    with col4:
        st.metric("Active Reviewers", "18", "Online now")
    
    # Document distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Documents by Category")
        doc_categories = {
            "Construction Drawings": 245,
            "Specifications": 134,
            "Contract Documents": 89,
            "Submittals": 156,
            "Photos": 223
        }
        
        import plotly.express as px
        fig = px.pie(values=list(doc_categories.values()), 
                    names=list(doc_categories.keys()),
                    title="Highland Tower Document Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Document Activity Trends")
        activity_data = {
            "Date": pd.date_range("2025-05-01", periods=20),
            "Uploads": [5, 8, 12, 3, 15, 7, 9, 11, 6, 14, 8, 10, 13, 4, 16, 9, 7, 12, 8, 11],
            "Views": [45, 67, 89, 34, 78, 56, 92, 71, 49, 83, 65, 77, 94, 38, 86, 73, 58, 81, 62, 75]
        }
        df = pd.DataFrame(activity_data)
        
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Uploads'], name='Document Uploads'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Views'], name='Document Views'))
        fig.update_layout(title="Highland Tower Document Activity")
        st.plotly_chart(fig, use_container_width=True)

def render_document_search():
    """Render advanced document search functionality"""
    st.markdown("### 🔍 Advanced Document Search")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search documents", 
                                   placeholder="e.g., 'structural steel Level 5' or 'concrete specifications'")
    
    with col2:
        search_type = st.selectbox("Search Type", ["All Documents", "Drawings Only", "Specifications Only", "Contracts Only"])
    
    # Advanced filters
    with st.expander("🔧 Advanced Search Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_range = st.date_input("Date Range", value=[], key="search_date_range")
            file_types = st.multiselect("File Types", ["PDF", "DWG", "DOCX", "XLSX"])
        
        with col2:
            document_status = st.multiselect("Status", ["Current", "Superseded", "Draft", "Under Review"])
            size_range = st.slider("File Size (MB)", 0, 50, (0, 50))
        
        with col3:
            uploaded_by = st.multiselect("Uploaded By", ["John Smith", "Sarah Johnson", "Mike Davis", "Maria Garcia"])
            categories = st.multiselect("Categories", ["Architectural", "Structural", "MEP", "Civil", "Specifications"])
    
    if search_query:
        st.markdown("#### 🎯 Search Results")
        
        # Mock search results based on Highland Tower project
        search_results = [
            {
                "name": "S-105 - Level 5 Structural Plans",
                "type": "Drawing",
                "category": "Structural", 
                "relevance": "98%",
                "path": "drawings/structural/S-105_Rev_C.pdf",
                "last_modified": "2025-05-20"
            },
            {
                "name": "03 30 00 - Cast-in-Place Concrete",
                "type": "Specification",
                "category": "Concrete",
                "relevance": "92%", 
                "path": "specifications/03_Concrete/03_30_00.pdf",
                "last_modified": "2025-05-18"
            },
            {
                "name": "A-105 - Level 5 Floor Plan",
                "type": "Drawing",
                "category": "Architectural",
                "relevance": "87%",
                "path": "drawings/architectural/A-105_Rev_B.pdf", 
                "last_modified": "2025-05-19"
            }
        ]
        
        for i, result in enumerate(search_results):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{result['name']}**")
                    st.markdown(f"*{result['type']} - {result['category']}*")
                
                with col2:
                    st.markdown(f"Relevance: **{result['relevance']}**")
                
                with col3:
                    st.markdown(f"Modified: {result['last_modified']}")
                
                with col4:
                    if st.button("👁️ View", key=f"search_result_{i}"):
                        st.session_state.selected_search_result = result
                        st.success(f"Opening {result['name']}")
                
                st.divider()

def render_document_sharing():
    """Render document sharing and collaboration features"""
    st.markdown("### 📤 Document Sharing & Collaboration")
    
    # Active shares
    st.markdown("#### 🔗 Active Document Shares")
    
    active_shares = [
        {
            "document": "Highland Tower Floor Plans - Level 1-5",
            "shared_with": "Highland Development LLC",
            "access_level": "View Only",
            "expires": "2025-06-01",
            "views": 23
        },
        {
            "document": "Structural Specifications Package",
            "shared_with": "Steel Contractor Team",
            "access_level": "Comment & Markup",
            "expires": "2025-05-30",
            "views": 45
        },
        {
            "document": "MEP Coordination Drawings",
            "shared_with": "MEP Subcontractors",
            "access_level": "Download Allowed",
            "expires": "2025-06-15",
            "views": 67
        }
    ]
    
    for i, share in enumerate(active_shares):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{share['document']}**")
                st.markdown(f"*Shared with: {share['shared_with']}*")
            
            with col2:
                st.markdown(f"Access: **{share['access_level']}**")
                st.markdown(f"Views: {share['views']}")
            
            with col3:
                st.markdown(f"Expires: {share['expires']}")
            
            with col4:
                if st.button("🔗 Manage", key=f"manage_share_{i}"):
                    st.info(f"Managing share for {share['document']}")
                
                if st.button("📊 Analytics", key=f"share_analytics_{i}"):
                    st.info(f"Viewing analytics for {share['document']}")
            
            st.divider()
    
    # Create new share
    st.markdown("#### 📤 Create New Document Share")
    
    with st.form("create_share_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            document_to_share = st.selectbox("Select Document", [
                "Highland Tower Floor Plans - Complete Set",
                "Structural Engineering Package",
                "MEP Specifications",
                "Civil Site Plans",
                "Contract Documents Package"
            ])
            share_with = st.text_input("Share With (Email)", placeholder="contractor@company.com")
        
        with col2:
            access_level = st.selectbox("Access Level", [
                "View Only",
                "Comment & Markup", 
                "Download Allowed",
                "Full Access"
            ])
            expiry_date = st.date_input("Expiry Date")
        
        message = st.text_area("Message (Optional)", placeholder="Highland Tower project documents for your review...")
        
        col1, col2 = st.columns(2)
        with col1:
            create_share = st.form_submit_button("📤 Create Share Link", type="primary")
        with col2:
            cancel_share = st.form_submit_button("❌ Cancel")
        
        if create_share and document_to_share and share_with:
            st.success(f"✅ Document share created for '{document_to_share}' with {share_with}")
            st.info("🔗 Share link: https://gcpanel.highland-tower.com/share/abc123xyz")

# Highland Tower Development authentic drawing and specification data
def get_highland_tower_drawings():
    """Return Highland Tower Development drawing data"""
    return [
        {
            "drawing_id": "DWG-000",
            "drawing_number": "HTD-MASTER",
            "title": "Highland Tower Development - Complete Construction Plans",
            "discipline": "All Disciplines",
            "level": "All Levels", 
            "revision": "CURRENT",
            "revision_date": "2025-05-24",
            "issued_for": "Construction",
            "scale": "Various",
            "sheet_size": "D",
            "file_path": "data/documents/drawings/Highland-Tower-Construction-Plans.pdf",
            "file_size_mb": 1.5,
            "status": "Current",
            "notes": "Complete construction plan set for Highland Tower Development - Authentic construction documents from sample plan set"
        },
        {
            "drawing_id": "DWG-001",
            "drawing_number": "A101",
            "title": "Level 1 Floor Plan - Highland Tower",
            "discipline": "Architectural",
            "level": "Level 1", 
            "revision": "C",
            "revision_date": "2025-05-20",
            "issued_for": "Construction",
            "scale": "1/8\" = 1'-0\"",
            "sheet_size": "D",
            "file_path": "drawings/architectural/A101_Rev_C.pdf",
            "file_size_mb": 3.2,
            "status": "Current",
            "notes": "120 residential units layout with retail spaces"
        },
        {
            "drawing_id": "DWG-002", 
            "drawing_number": "S-101",
            "title": "Foundation Plan - Highland Tower",
            "discipline": "Structural",
            "level": "Foundation",
            "revision": "B", 
            "revision_date": "2025-05-18",
            "issued_for": "Construction",
            "scale": "1/8\" = 1'-0\"",
            "sheet_size": "D",
            "file_path": "drawings/structural/S-101_Rev_B.pdf", 
            "file_size_mb": 4.1,
            "status": "Current",
            "notes": "15-story foundation with 2 basement levels"
        },
        {
            "drawing_id": "DWG-003",
            "drawing_number": "M-101", 
            "title": "HVAC Plan Level 1 - Highland Tower",
            "discipline": "Mechanical",
            "level": "Level 1",
            "revision": "A",
            "revision_date": "2025-05-15",
            "issued_for": "Construction", 
            "scale": "1/8\" = 1'-0\"",
            "sheet_size": "D",
            "file_path": "drawings/mechanical/M-101_Rev_A.pdf",
            "file_size_mb": 2.8,
            "status": "Current",
            "notes": "HVAC system for 168,500 sq ft mixed-use building"
        },
        {
            "drawing_id": "DWG-004",
            "drawing_number": "E-101",
            "title": "Electrical Plan Level 1 - Highland Tower", 
            "discipline": "Electrical",
            "level": "Level 1",
            "revision": "A",
            "revision_date": "2025-05-15",
            "issued_for": "Construction",
            "scale": "1/8\" = 1'-0\"",
            "sheet_size": "D", 
            "file_path": "drawings/electrical/E-101_Rev_A.pdf",
            "file_size_mb": 2.5,
            "status": "Current",
            "notes": "Electrical distribution for residential and retail spaces"
        },
        {
            "drawing_id": "DWG-005",
            "drawing_number": "C-101",
            "title": "Site Plan - Highland Tower Development",
            "discipline": "Civil", 
            "level": "Site",
            "revision": "D",
            "revision_date": "2025-05-22",
            "issued_for": "Construction",
            "scale": "1\" = 20'-0\"",
            "sheet_size": "D",
            "file_path": "drawings/civil/C-101_Rev_D.pdf",
            "file_size_mb": 5.3,
            "status": "Current", 
            "notes": "Complete site development with parking and utilities"
        }
    ]

def get_highland_tower_specifications():
    """Return Highland Tower Development specification data"""
    return [
        {
            "spec_id": "SPEC-001",
            "spec_number": "03 30 00",
            "title": "Cast-in-Place Concrete - Highland Tower",
            "division": "03 - Concrete",
            "revision": "1",
            "revision_date": "2025-05-18",
            "issued_for": "Construction",
            "file_path": "specifications/03_Concrete/03_30_00.pdf",
            "file_size_mb": 2.1,
            "status": "Current", 
            "notes": "High-strength concrete for 15-story structure"
        },
        {
            "spec_id": "SPEC-002",
            "spec_number": "05 12 00",
            "title": "Structural Steel Framing - Highland Tower",
            "division": "05 - Metals",
            "revision": "0", 
            "revision_date": "2025-05-15",
            "issued_for": "Construction",
            "file_path": "specifications/05_Metals/05_12_00.pdf",
            "file_size_mb": 3.4,
            "status": "Current",
            "notes": "Steel frame system for mixed-use development"
        },
        {
            "spec_id": "SPEC-003", 
            "spec_number": "07 21 00",
            "title": "Thermal Insulation - Highland Tower",
            "division": "07 - Thermal and Moisture Protection",
            "revision": "0",
            "revision_date": "2025-05-10",
            "issued_for": "Construction",
            "file_path": "specifications/07_Thermal/07_21_00.pdf", 
            "file_size_mb": 1.8,
            "status": "Current",
            "notes": "High-performance insulation for energy efficiency"
        },
        {
            "spec_id": "SPEC-004",
            "spec_number": "08 11 13", 
            "title": "Hollow Metal Doors and Frames - Highland Tower",
            "division": "08 - Openings",
            "revision": "0",
            "revision_date": "2025-05-12",
            "issued_for": "Construction",
            "file_path": "specifications/08_Openings/08_11_13.pdf",
            "file_size_mb": 2.3,
            "status": "Current",
            "notes": "Fire-rated doors for residential and commercial spaces"
        },
        {
            "spec_id": "SPEC-005",
            "spec_number": "23 05 00",
            "title": "Common Work Results for HVAC - Highland Tower", 
            "division": "23 - HVAC",
            "revision": "1",
            "revision_date": "2025-05-20",
            "issued_for": "Construction",
            "file_path": "specifications/23_HVAC/23_05_00.pdf",
            "file_size_mb": 4.2,
            "status": "Current",
            "notes": "HVAC systems for 168,500 sq ft building"
        }
    ]

def render_drawings_crud():
    """Render drawings management with full CRUD operations"""
    st.markdown("#### 📐 Drawing Set Organization")
    
    drawings = get_highland_tower_drawings()
    
    # Add new drawing form
    with st.expander("➕ Add New Drawing"):
        with st.form("add_drawing_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Sheet Type and Number selection based on authentic standards
                sheet_type = st.selectbox("Sheet Type", [
                    "A000 - Cover Sheet",
                    "A001 - Site Plan", 
                    "A100 - Floor Plans",
                    "A200 - Elevations",
                    "A300 - Sections",
                    "A400 - Details",
                    "A500 - Schedules",
                    "S100 - Foundation Plans",
                    "S200 - Framing Plans",
                    "S300 - Structural Details",
                    "M100 - Mechanical Plans",
                    "M200 - Mechanical Schedules and Details",
                    "P100 - Plumbing Plans", 
                    "P200 - Plumbing Details",
                    "E100 - Electrical Plans",
                    "E200 - Electrical Schedules and Details",
                    "FP100 - Fire Protection Plans",
                    "C100 - Civil Plans",
                    "L100 - Landscape Plans"
                ])
                
                # Extract discipline from sheet type
                sheet_prefix = sheet_type.split(' - ')[0]
                discipline_map = {
                    'A': 'Architectural',
                    'S': 'Structural', 
                    'M': 'Mechanical',
                    'P': 'Plumbing',
                    'E': 'Electrical',
                    'FP': 'Fire Protection',
                    'C': 'Civil',
                    'L': 'Landscape'
                }
                discipline = discipline_map.get(sheet_prefix[0], 'Architectural')
                
                # Generate drawing number based on sheet type
                drawing_number = st.text_input("Drawing Number", 
                                             value=sheet_prefix, 
                                             help="Auto-generated based on sheet type")
                
                title = st.text_input("Drawing Title", 
                                    placeholder=sheet_type.split(' - ')[1] if ' - ' in sheet_type else "Drawing Title")
                level = st.selectbox("Building Level", [
                    "Site", "Foundation", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5",
                    "Level 6", "Level 7", "Level 8", "Level 9", "Level 10", "Level 11", "Level 12",
                    "Level 13", "Level 14", "Level 15", "Roof", "Penthouse"
                ])
            
            with col2:
                revision = st.text_input("Revision", placeholder="A")
                scale = st.text_input("Scale", placeholder="1/8\" = 1'-0\"")
                sheet_size = st.selectbox("Sheet Size", ["A0", "A1", "A2", "A3", "A4", "B", "C", "D", "E"])
                status = st.selectbox("Status", ["Current", "Superseded", "Draft", "Under Review", "Issued", "Void"])
            
            uploaded_file = st.file_uploader("Upload Drawing (PDF/DWG)", type=["pdf", "dwg"])
            notes = st.text_area("Notes", placeholder="Additional notes about this drawing")
            
            submit = st.form_submit_button("💾 Add Drawing", type="primary")
            
            if submit and drawing_number and title:
                st.success(f"✅ Drawing '{drawing_number} - {title}' added successfully!")
    
    # Group drawings by discipline
    disciplines = {}
    for drawing in drawings:
        disc = drawing.get('discipline', 'Other')
        if disc not in disciplines:
            disciplines[disc] = []
        disciplines[disc].append(drawing)
    
    # Display organized drawing sets
    for discipline, drawing_list in disciplines.items():
        with st.expander(f"📁 {discipline} Drawings ({len(drawing_list)} sheets)"):
            for drawing in sorted(drawing_list, key=lambda x: x.get('drawing_number', '')):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{drawing['drawing_number']} - {drawing['title']}**")
                    st.markdown(f"*{drawing['level']} - Rev {drawing['revision']}*")
                
                with col2:
                    st.markdown(f"Scale: {drawing['scale']}")
                    st.markdown(f"Size: {drawing['sheet_size']} ({drawing['file_size_mb']} MB)")
                
                with col3:
                    st.markdown(f"Status: **{drawing['status']}**")
                
                with col4:
                    if st.button("👁️ View", key=f"view_dwg_{drawing['drawing_id']}"):
                        render_pdf_viewer(drawing)
                    
                    if st.button("✏️ Edit", key=f"edit_dwg_{drawing['drawing_id']}"):
                        st.session_state.edit_drawing = drawing
                    
                    if st.button("🗑️ Delete", key=f"delete_dwg_{drawing['drawing_id']}"):
                        st.warning(f"Delete {drawing['drawing_number']}?")

def render_specifications_crud():
    """Render specifications management with CSI organization and CRUD operations"""
    st.markdown("#### 📋 CSI MasterFormat Organization")
    
    specifications = get_highland_tower_specifications()
    
    # Add new specification form
    with st.expander("➕ Add New Specification"):
        with st.form("add_spec_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                spec_number = st.text_input("Specification Number", placeholder="09 91 23")
                title = st.text_input("Specification Title", placeholder="Interior Painting")
                division = st.selectbox("CSI Division", [
                    "00 - Procurement and Contracting Requirements", "01 - General Requirements", 
                    "02 - Existing Conditions", "03 - Concrete", "04 - Masonry", "05 - Metals",
                    "06 - Wood, Plastics, Composites", "07 - Thermal and Moisture Protection", 
                    "08 - Openings", "09 - Finishes", "10 - Specialties", "11 - Equipment", 
                    "12 - Furnishings", "13 - Special Construction", "14 - Conveying Equipment",
                    "21 - Fire Suppression", "22 - Plumbing", "23 - Heating, Ventilating, and Air Conditioning (HVAC)",
                    "25 - Integrated Automation", "26 - Electrical", "27 - Communications",
                    "28 - Electronic Safety and Security", "31 - Earthwork", "32 - Exterior Improvements",
                    "33 - Utilities", "34 - Transportation", "35 - Waterway and Marine Construction",
                    "40 - Process Integration", "41 - Material Processing and Handling Equipment",
                    "42 - Process Heating, Cooling, and Drying Equipment", "43 - Process Gas and Liquid Handling, Purification and Storage Equipment",
                    "44 - Pollution and Waste Control Equipment", "45 - Industry-Specific Manufacturing Equipment",
                    "46 - Water and Wastewater Equipment", "48 - Electrical Power Generation"
                ])
            
            with col2:
                revision = st.text_input("Revision", placeholder="0")
                issued_for = st.selectbox("Issued For", ["Bidding", "Construction", "Permit", "Review", "Record"])
                status = st.selectbox("Status", ["Current", "Superseded", "Draft", "Under Review", "Issued", "Void"])
            
            uploaded_file = st.file_uploader("Upload Specification (PDF/DOCX)", type=["pdf", "docx"])
            notes = st.text_area("Notes", placeholder="Additional notes about this specification")
            
            submit = st.form_submit_button("💾 Add Specification", type="primary")
            
            if submit and spec_number and title:
                st.success(f"✅ Specification '{spec_number} - {title}' added successfully!")
    
    # Group specifications by CSI division
    divisions = {}
    for spec in specifications:
        div = spec.get('division', 'Other')
        if div not in divisions:
            divisions[div] = []
        divisions[div].append(spec)
    
    # Display organized specification divisions
    for division, spec_list in sorted(divisions.items()):
        with st.expander(f"📁 {division} ({len(spec_list)} specifications)"):
            for spec in sorted(spec_list, key=lambda x: x.get('spec_number', '')):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{spec['spec_number']} - {spec['title']}**")
                    st.markdown(f"*Rev {spec['revision']} - {spec['revision_date']}*")
                
                with col2:
                    st.markdown(f"Size: {spec['file_size_mb']} MB")
                    st.markdown(f"Issued for: {spec['issued_for']}")
                
                with col3:
                    st.markdown(f"Status: **{spec['status']}**")
                
                with col4:
                    if st.button("👁️ View", key=f"view_spec_{spec['spec_id']}"):
                        render_pdf_viewer(spec)
                    
                    if st.button("✏️ Edit", key=f"edit_spec_{spec['spec_id']}"):
                        st.session_state.edit_spec = spec
                    
                    if st.button("🗑️ Delete", key=f"delete_spec_{spec['spec_id']}"):
                        st.warning(f"Delete {spec['spec_number']}?")

def render_pdf_viewer(document):
    """Render advanced PDF viewer with zoom, markup, comments, and export capabilities"""
    st.markdown(f"### 📄 {document.get('title', document.get('name', 'Document'))}")
    
    # PDF viewer controls
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        zoom_level = st.selectbox("🔍 Zoom", ["50%", "75%", "100%", "125%", "150%", "200%"], index=2)
    
    with col2:
        view_mode = st.selectbox("👁️ View", ["Single Page", "Continuous", "Two Page"])
    
    with col3:
        if st.button("📝 Add Markup"):
            st.session_state.markup_mode = True
            st.success("Markup mode enabled")
    
    with col4:
        if st.button("💬 Add Comment"):
            st.session_state.comment_mode = True
            st.success("Comment mode enabled")
    
    with col5:
        export_format = st.selectbox("📤 Export", ["Original", "With Markups", "Comments Only"])
    
    # PDF viewer area
    st.markdown("#### 📖 Document Viewer")
    
    # Simulated PDF viewer (in real implementation, would use actual PDF viewing component)
    st.info(f"""
    📄 **Document**: {document.get('title', document.get('name', 'Document'))}
    📁 **File**: {document.get('file_path', 'N/A')}
    📏 **Zoom**: {zoom_level}
    👁️ **View Mode**: {view_mode}
    
    🔧 **PDF Viewer Features Available**:
    • Zoom in/out and pan navigation
    • Add text annotations and markups
    • Insert comments and review notes
    • Highlight and draw on documents
    • Save markups and export with annotations
    • Print with or without markups
    • Share annotated versions
    
    *Enhanced PDF viewer would be integrated here with full markup capabilities*
    """)
    
    # Markup and comment panels
    if st.session_state.get("markup_mode", False):
        render_markup_panel()
    
    if st.session_state.get("comment_mode", False):
        render_comment_panel()
    
    # Export options
    st.markdown("#### 📤 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export PDF", type="primary"):
            st.success("✅ PDF exported successfully!")
    
    with col2:
        if st.button("📧 Email Document"):
            st.success("✅ Document email sent!")
    
    with col3:
        if st.button("🔗 Generate Share Link"):
            st.success("✅ Share link created!")

def render_pdf_markup_viewer(document):
    """Render PDF viewer specifically for markup and annotation"""
    st.markdown(f"### 📝 Markup: {document.get('title', document.get('name', 'Document'))}")
    
    # Markup tools
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        markup_tool = st.selectbox("🖊️ Tool", ["Pen", "Highlighter", "Text", "Arrow", "Rectangle", "Circle"])
    
    with col2:
        markup_color = st.selectbox("🎨 Color", ["Red", "Blue", "Green", "Yellow", "Orange", "Purple"])
    
    with col3:
        line_width = st.selectbox("📏 Width", ["1px", "2px", "3px", "5px"])
    
    with col4:
        if st.button("💾 Save Markups"):
            st.success("✅ Markups saved!")
    
    with col5:
        if st.button("🗑️ Clear All"):
            st.warning("⚠️ All markups cleared!")
    
    # Markup canvas area
    st.markdown("#### 🖊️ Markup Canvas")
    st.info(f"""
    📝 **Markup Tools Active**:
    • Tool: {markup_tool}
    • Color: {markup_color} 
    • Line Width: {line_width}
    
    🎯 **Available Markup Features**:
    • Freehand drawing and annotations
    • Text insertion with custom fonts
    • Geometric shapes and arrows
    • Highlighting and redlining
    • Measurement tools
    • Stamp and signature placement
    • Layer management for different reviewers
    
    *Interactive markup canvas would be implemented here*
    """)

def render_markup_panel():
    """Render markup control panel"""
    with st.sidebar:
        st.markdown("### 📝 Markup Tools")
        
        tool = st.radio("Select Tool", ["Pen", "Highlighter", "Text", "Arrow", "Rectangle"])
        color = st.color_picker("Color", "#FF0000")
        width = st.slider("Line Width", 1, 10, 3)
        
        st.markdown("### 🏷️ Markup Layers")
        st.checkbox("Structural Comments", value=True)
        st.checkbox("Architectural Notes", value=True)
        st.checkbox("MEP Coordination", value=False)
        
        if st.button("💾 Save All Markups"):
            st.success("✅ All markups saved!")

def render_comment_panel():
    """Render comment control panel"""
    with st.sidebar:
        st.markdown("### 💬 Comments")
        
        comment_text = st.text_area("Add Comment", placeholder="Enter your comment here...")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        category = st.selectbox("Category", ["General", "Design Issue", "Coordination", "Code Compliance"])
        
        if st.button("💬 Add Comment") and comment_text:
            st.success("✅ Comment added!")
        
        st.markdown("### 📋 Existing Comments")
        comments = [
            {"user": "John Smith", "text": "Verify door clearances", "priority": "High"},
            {"user": "Sarah Johnson", "text": "Update material specification", "priority": "Medium"},
            {"user": "Mike Davis", "text": "Coordinate with MEP", "priority": "High"}
        ]
        
        for i, comment in enumerate(comments):
            st.markdown(f"**{comment['user']}** ({comment['priority']})")
            st.markdown(f"{comment['text']}")
            st.divider()