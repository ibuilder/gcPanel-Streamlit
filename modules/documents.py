"""
Documents module for gcPanel.

This module provides document management functionality including
file uploading, categorization, search, and version control.
Includes AI-powered smart document search capabilities and
real-time collaboration features for team editing and commenting.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import mobile optimizations
from utils.mobile.responsive_layout import add_mobile_styles
from utils.mobile.pwa_support import setup_pwa

# Import AI features
from utils.ai.document_search import SmartDocumentSearch

# Import collaboration features
from utils.collaboration.realtime_collaboration import render_document_collaboration, render_comment_thread

def render_documents():
    """Render the documents management interface."""
    # Apply mobile optimization and PWA support
    add_mobile_styles()
    setup_pwa()
    
    # Initialize smart document search
    smart_search = SmartDocumentSearch()
    
    # Page header
    st.header("Document Management")
    
    # Create tabs for different document views
    tabs = st.tabs(["📋 Current Set", "📖 Specifications", "📁 All Documents", "🔍 Smart Search", "⬆️ Upload"])
    
    # Current Set tab
    with tabs[0]:
        render_current_set()
    
    # Specifications tab
    with tabs[1]:
        render_specifications()
    
    # All Documents tab
    with tabs[2]:
        render_document_list()
    
    # Smart Search tab - AI-powered search with NLP
    with tabs[3]:
        st.subheader("Smart Document Search")
        
        # Search input
        search_query = st.text_input("Search documents in natural language", 
                                placeholder="e.g., 'Find foundation specs for Highland Tower'")
        
        # Search method selection (basic or semantic)
        search_method = st.radio("Search method", ["Basic", "Semantic (AI-powered)"], horizontal=True)
        
        # Filters
        with st.expander("Advanced Filters"):
            col1, col2 = st.columns(2)
            
            with col1:
                filter_type = st.selectbox("Document Type", ["Any", "Specification", "Report", "Design Document", "Schedule"])
            
            with col2:
                filter_status = st.selectbox("Status", ["Any", "Approved", "In Review", "Final", "Current"])
            
            # Author filter
            filter_author = st.selectbox("Author", ["Any", "John Smith", "Sarah Johnson", "Mike Chen", "Lisa Rodriguez"])
        
        # Search button
        if st.button("Search") or search_query:
            # Build filters
            filters = {}
            
            if filter_type != "Any":
                filters["type"] = filter_type
                
            if filter_status != "Any":
                filters["status"] = filter_status
                
            if filter_author != "Any":
                filters["author"] = filter_author
            
            # Perform search
            if search_method == "Basic":
                results = smart_search.search(search_query, filters)
            else:
                results = smart_search.semantic_search(search_query, filters)
            
            # Display results
            if results:
                st.markdown(f"### {len(results)} Results Found")
                
                for doc in results:
                    with st.expander(f"{doc['title']} ({doc['type']})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Author:** {doc['author']}")
                            st.markdown(f"**Last Updated:** {doc['updated_at'].split('T')[0]}")
                            st.markdown(f"**Status:** {doc['status']} (v{doc['version']})")
                        
                        with col2:
                            st.markdown("**Tags:**")
                            tags_html = " ".join([f'<span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' for tag in doc['tags']])
                            st.markdown(tags_html, unsafe_allow_html=True)
                        
                        st.markdown("**Content:**")
                        st.text(doc['content'])
                        
                        # Show extracted information button
                        if st.button("Extract Key Information", key=f"extract_{doc['id']}"):
                            with st.spinner("Analyzing document..."):
                                # Extract key information
                                key_info = smart_search.extract_key_information(doc['id'])
                                
                                if key_info:
                                    st.markdown("### Key Information Extracted")
                                    
                                    if key_info["measurements"]:
                                        st.markdown("**Measurements:**")
                                        st.markdown(", ".join(key_info["measurements"]))
                                    
                                    if key_info["specifications"]:
                                        st.markdown("**Specifications/Standards:**")
                                        st.markdown(", ".join(key_info["specifications"]))
            else:
                st.info("No documents found matching your search criteria.")
        
        # Example searches
        st.markdown("### Example Searches")
        examples = [
            "foundation specifications",
            "HVAC system details",
            "structural analysis",
            "construction timeline",
            "electrical requirements"
        ]
        
        for i, example in enumerate(examples):
            if st.button(example, key=f"example_{i}"):
                # Set search query and trigger search
                search_query = example
                st.session_state.search_query = example
                st.rerun()
    
    # Recent Documents tab
    with tabs[2]:
        render_recent_documents()
    
    # Favorites tab
    with tabs[3]:
        render_favorite_documents()
        
    # Collaboration tab
    with tabs[4]:
        render_document_collaboration_features()
    
    # Upload tab
    with tabs[5]:
        render_document_upload()

def render_document_list():
    """Render a list of all documents."""
    st.subheader("All Documents")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        doc_type = st.selectbox("Document Type", ["All", "Drawing", "Specification", "Contract", "Permit", "Report", "Manual"])
    
    with col2:
        discipline = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"])
    
    with col3:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Name (A-Z)", "Name (Z-A)"])
    
    # Search bar
    search = st.text_input("Search documents by name, number, or keyword")
    
    # Highland Tower Development - Authentic Project Documents
    documents = [
        # Architectural Drawings
        {"id": "A-101", "name": "Highland Tower - Floor Plans Level 1-15", "type": "Drawing", "discipline": "Architectural", "date": "2025-05-20", "version": "Rev C", "status": "Current", "size": "36\"x24\"", "sheets": "15 sheets"},
        {"id": "A-102", "name": "Highland Tower - Building Elevations", "type": "Drawing", "discipline": "Architectural", "date": "2025-05-18", "version": "Rev B", "status": "Current", "size": "36\"x24\"", "sheets": "8 sheets"},
        {"id": "A-201", "name": "Highland Tower - Residential Unit Plans", "type": "Drawing", "discipline": "Architectural", "date": "2025-05-15", "version": "Rev A", "status": "Current", "size": "24\"x36\"", "sheets": "12 sheets"},
        
        # Structural Drawings  
        {"id": "S-101", "name": "Highland Tower - Foundation Plan", "type": "Drawing", "discipline": "Structural", "date": "2025-05-18", "version": "Rev B", "status": "Current", "size": "36\"x24\"", "sheets": "6 sheets"},
        {"id": "S-201", "name": "Highland Tower - Framing Plans L1-15", "type": "Drawing", "discipline": "Structural", "date": "2025-05-16", "version": "Rev A", "status": "Current", "size": "36\"x24\"", "sheets": "18 sheets"},
        {"id": "S-301", "name": "Highland Tower - Connection Details", "type": "Drawing", "discipline": "Structural", "date": "2025-05-14", "version": "Rev A", "status": "Current", "size": "24\"x36\"", "sheets": "8 sheets"},
        
        # MEP Systems
        {"id": "M-101", "name": "Highland Tower - HVAC Plans L1-15", "type": "Drawing", "discipline": "Mechanical", "date": "2025-05-15", "version": "Rev A", "status": "Current", "size": "36\"x24\"", "sheets": "20 sheets"},
        {"id": "E-101", "name": "Highland Tower - Electrical Plans L1-15", "type": "Drawing", "discipline": "Electrical", "date": "2025-05-17", "version": "Rev B", "status": "Current", "size": "36\"x24\"", "sheets": "22 sheets"},
        {"id": "P-101", "name": "Highland Tower - Plumbing Plans L1-15", "type": "Drawing", "discipline": "Plumbing", "date": "2025-05-12", "version": "Rev A", "status": "Current", "size": "36\"x24\"", "sheets": "16 sheets"},
        
        # Civil/Site Plans
        {"id": "C-001", "name": "Highland Tower - Site Plan & Grading", "type": "Drawing", "discipline": "Civil", "date": "2025-05-10", "version": "Rev C", "status": "Current", "size": "30\"x42\"", "sheets": "4 sheets"},
        {"id": "C-101", "name": "Highland Tower - Utility Plans", "type": "Drawing", "discipline": "Civil", "date": "2025-05-08", "version": "Rev B", "status": "Current", "size": "30\"x42\"", "sheets": "6 sheets"},
        
        # Project Specifications
        {"id": "SPEC-03", "name": "Division 03 - Concrete Specifications", "type": "Specification", "discipline": "Structural", "date": "2025-05-05", "version": "Rev B", "status": "Approved", "pages": "45 pages", "csi": "03 30 00"},
        {"id": "SPEC-05", "name": "Division 05 - Metals Specifications", "type": "Specification", "discipline": "Structural", "date": "2025-05-03", "version": "Rev A", "status": "Approved", "pages": "32 pages", "csi": "05 12 00"},
        {"id": "SPEC-23", "name": "Division 23 - HVAC Specifications", "type": "Specification", "discipline": "Mechanical", "date": "2025-05-07", "version": "Rev A", "status": "Approved", "pages": "67 pages", "csi": "23 00 00"},
        {"id": "SPEC-26", "name": "Division 26 - Electrical Specifications", "type": "Specification", "discipline": "Electrical", "date": "2025-05-06", "version": "Rev B", "status": "Approved", "pages": "54 pages", "csi": "26 00 00"},
        
        # 3D Models & BIM Files
        {"id": "BIM-001", "name": "Highland Tower - Architectural BIM Model", "type": "Model", "discipline": "Architectural", "date": "2025-05-20", "version": "Rev C", "status": "Current", "software": "Revit 2024", "size": "1.2 GB"},
        {"id": "BIM-002", "name": "Highland Tower - Structural BIM Model", "type": "Model", "discipline": "Structural", "date": "2025-05-18", "version": "Rev B", "status": "Current", "software": "Revit 2024", "size": "856 MB"},
        {"id": "BIM-003", "name": "Highland Tower - MEP BIM Model", "type": "Model", "discipline": "Mechanical", "date": "2025-05-15", "version": "Rev A", "status": "Current", "software": "Revit 2024", "size": "1.4 GB"},
        {"id": "BIM-004", "name": "Highland Tower - Federated Model", "type": "Model", "discipline": "All", "date": "2025-05-22", "version": "Rev D", "status": "Current", "software": "Navisworks", "size": "2.8 GB"},
        
        # Project Reports
        {"id": "RPT-001", "name": "Highland Tower - Geotechnical Report", "type": "Report", "discipline": "Civil", "date": "2024-12-15", "version": "Final", "status": "Approved", "pages": "89 pages", "consultant": "Geo Solutions"},
        {"id": "RPT-002", "name": "Highland Tower - Environmental Assessment", "type": "Report", "discipline": "Environmental", "date": "2024-11-20", "version": "Final", "status": "Approved", "pages": "67 pages", "consultant": "EnviroTech"},
        {"id": "RPT-003", "name": "Highland Tower - Traffic Impact Study", "type": "Report", "discipline": "Civil", "date": "2024-10-25", "version": "Final", "status": "Approved", "pages": "42 pages", "consultant": "Traffic Solutions"},
        
        # Contract Documents
        {"id": "CNT-001", "name": "Highland Tower - Prime Contract Agreement", "type": "Contract", "discipline": "All", "date": "2024-09-01", "version": "Final", "status": "Executed", "value": "$45.5M", "type_contract": "Lump Sum"},
        {"id": "CNT-002", "name": "Highland Tower - General Conditions", "type": "Contract", "discipline": "All", "date": "2024-09-01", "version": "Final", "status": "Executed", "pages": "156 pages", "aia": "A201-2017"},
        
        # Permits & Approvals
        {"id": "PER-001", "name": "Highland Tower - Building Permit", "type": "Permit", "discipline": "All", "date": "2025-01-15", "version": "Final", "status": "Issued", "permit_no": "BP-2025-0142", "authority": "City Planning"},
        {"id": "PER-002", "name": "Highland Tower - Foundation Permit", "type": "Permit", "discipline": "Structural", "date": "2025-02-01", "version": "Final", "status": "Issued", "permit_no": "FP-2025-0089", "authority": "Building Dept"}
    ]
    
    # Filter documents
    if doc_type != "All":
        documents = [doc for doc in documents if doc["type"] == doc_type]
    
    if discipline != "All":
        documents = [doc for doc in documents if doc["discipline"] == discipline]
    
    if search:
        documents = [doc for doc in documents if search.lower() in doc["name"].lower() or search.lower() in doc["id"].lower()]
    
    # Sort documents
    if sort_by == "Date (Newest)":
        documents.sort(key=lambda x: x["date"], reverse=True)
    elif sort_by == "Date (Oldest)":
        documents.sort(key=lambda x: x["date"])
    elif sort_by == "Name (A-Z)":
        documents.sort(key=lambda x: x["name"])
    elif sort_by == "Name (Z-A)":
        documents.sort(key=lambda x: x["name"], reverse=True)
    
    # Create a DataFrame for better display
    df = pd.DataFrame(documents)
    
    # Style the dataframe
    df_styled = df.style.format({
        "date": lambda x: x  # Already in the right format
    })
    
    # Define hover style
    hover_style = {
        "selector": "tr:hover",
        "props": [("background-color", "#f0f2f6")]
    }
    
    # Apply styles
    df_styled = df_styled.set_table_styles([hover_style])
    
    # Display table
    st.dataframe(df_styled, use_container_width=True, hide_index=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("View Selected", key="view_doc")
    
    with col2:
        st.button("Edit Selected", key="edit_doc")
    
    with col3:
        st.button("Download Selected", key="download_doc")
    
    with col4:
        st.button("Delete Selected", key="delete_doc")

def render_recent_documents():
    """Render a list of recently accessed documents."""
    st.subheader("Recent Documents")
    
    # Generate sample recent document data
    recent_docs = [
        {"id": "DOC-006", "name": "HVAC Design", "type": "Drawing", "accessed": "Today, 10:30 AM", "notes": "Reviewed comments from mechanical engineer"},
        {"id": "DOC-003", "name": "General Conditions", "type": "Contract", "accessed": "Today, 9:15 AM", "notes": "Updated payment terms"},
        {"id": "DOC-010", "name": "Facade Details", "type": "Drawing", "accessed": "Yesterday, 4:45 PM", "notes": "Checked curtain wall connections"},
        {"id": "DOC-002", "name": "Electrical Specifications", "type": "Specification", "accessed": "Yesterday, 2:30 PM", "notes": "Reviewed panel schedules"},
        {"id": "DOC-009", "name": "Structural Calculations", "type": "Report", "accessed": "2 days ago", "notes": "Verified wind load calculations"}
    ]
    
    # Display recent documents with more detailed cards
    for doc in recent_docs:
        st.markdown(f"""
        <div style="border: 1px solid #e6e6e6; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div style="font-weight: bold; font-size: 16px;">{doc['name']}</div>
                <div style="color: #666; font-size: 14px;">{doc['accessed']}</div>
            </div>
            <div style="display: flex; margin-bottom: 10px;">
                <div style="background-color: #e6e6e6; border-radius: 12px; padding: 3px 10px; margin-right: 10px; font-size: 12px;">{doc['id']}</div>
                <div style="background-color: #e6e6e6; border-radius: 12px; padding: 3px 10px; font-size: 12px;">{doc['type']}</div>
            </div>
            <div style="font-size: 14px; color: #444;">{doc['notes']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_favorite_documents():
    """Render a list of favorite documents."""
    st.subheader("Favorite Documents")
    
    # Generate sample favorite document data
    favorites = [
        {"id": "DOC-001", "name": "Foundation Drawings", "type": "Drawing", "date_favorited": "2025-02-10", "notes": "Important reference for site work"},
        {"id": "DOC-005", "name": "Soil Analysis Report", "type": "Report", "date_favorited": "2025-02-15", "notes": "Contains key assumptions for foundation design"},
        {"id": "DOC-003", "name": "General Conditions", "type": "Contract", "date_favorited": "2025-02-20", "notes": "Reference for all contractual matters"}
    ]
    
    # Display favorites in a grid
    col1, col2 = st.columns(2)
    
    for i, doc in enumerate(favorites):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="border: 1px solid #e6e6e6; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-weight: bold; font-size: 16px;">{doc['name']}</div>
                    <div style="color: gold; font-size: 20px;">★</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="background-color: #e6e6e6; border-radius: 12px; padding: 3px 10px; margin-right: 10px; font-size: 12px;">{doc['id']}</span>
                    <span style="background-color: #e6e6e6; border-radius: 12px; padding: 3px 10px; font-size: 12px;">{doc['type']}</span>
                </div>
                <div style="font-size: 14px; color: #444; margin-bottom: 10px;">{doc['notes']}</div>
                <div style="font-size: 12px; color: #666;">Favorited on: {doc['date_favorited']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # No favorites message
    if not favorites:
        st.info("You haven't marked any documents as favorites yet.")

def render_document_collaboration_features():
    """Render real-time collaboration features for documents."""
    st.subheader("Document Collaboration")
    
    # Select document to collaborate on
    documents = [
        "DOC-001: Foundation Drawings", 
        "DOC-002: Electrical Specifications", 
        "DOC-003: General Conditions",
        "DOC-006: HVAC Design",
        "DOC-010: Facade Details"
    ]
    
    selected_doc = st.selectbox("Select Document to Collaborate On", documents)
    
    # Tabs for different collaboration features
    collab_tabs = st.tabs(["Document Editor", "Comments", "Version History", "Activity Log"])
    
    # Document Editor tab
    with collab_tabs[0]:
        st.subheader(f"Editing: {selected_doc}")
        
        # Mock document content
        initial_content = """# Foundation Specifications

## 1. General Requirements

The foundation system shall be designed to support all applied loads, including both dead and live loads, as well as lateral loads such as wind and seismic forces. All work shall comply with ACI 318 and local building codes.

## 2. Materials

### 2.1 Concrete
- Compressive Strength: 4,000 psi at 28 days
- Water-Cement Ratio: Maximum 0.45
- Air Content: 5-7%

### 2.2 Reinforcement
- Deformed Bars: ASTM A615, Grade 60
- Welded Wire Fabric: ASTM A1064
"""
        
        # Collaborative text editor
        edited_content = st.text_area("Document Content", value=initial_content, height=400)
        
        # Show who's currently editing
        st.markdown("""
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <div style="font-size: 14px;">Currently editing:</div>
            <div style="background-color: #e6f7ff; border-radius: 12px; padding: 0 10px; font-size: 14px;">John Smith</div>
            <div style="background-color: #fff7e6; border-radius: 12px; padding: 0 10px; font-size: 14px;">Sarah Johnson</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.button("Save Changes")
        with col2:
            st.button("Revert Changes")
        with col3:
            st.button("Create New Version")
    
    # Comments tab
    with collab_tabs[1]:
        st.subheader("Comments & Discussions")
        
        # Discussion thread for the document
        render_comment_thread(document_id=selected_doc.split(":")[0])
        
        # Add new comment form
        st.subheader("Add Comment")
        comment_text = st.text_area("Comment", placeholder="Type your comment here...", height=100)
        
        # Comment options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            comment_type = st.radio("Comment Type", ["General", "Question", "Issue", "Suggestion"], horizontal=True)
            mention_users = st.multiselect("Mention Users", ["John Smith", "Sarah Johnson", "Mike Chen", "Lisa Rodriguez"])
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            if st.button("Post Comment"):
                if comment_text:
                    st.success("Comment posted successfully!")
                    st.session_state.comment_text = ""
                    st.rerun()
                else:
                    st.error("Please enter a comment.")
    
    # Version History tab
    with collab_tabs[2]:
        st.subheader("Version History")
        
        # Version list
        versions = [
            {"version": "v3.2", "date": "2025-05-15", "author": "John Smith", "changes": "Updated concrete specifications and added notes for frost protection."},
            {"version": "v3.1", "date": "2025-05-01", "author": "Sarah Johnson", "changes": "Fixed reinforcement spacing requirements."},
            {"version": "v3.0", "date": "2025-04-20", "author": "Mike Chen", "changes": "Major revision to comply with updated building codes."},
            {"version": "v2.1", "date": "2025-03-15", "author": "John Smith", "changes": "Added waterproofing details."},
            {"version": "v2.0", "date": "2025-02-28", "author": "Lisa Rodriguez", "changes": "Updated foundation type to address soil report findings."},
            {"version": "v1.0", "date": "2025-01-20", "author": "John Smith", "changes": "Initial document creation."}
        ]
        
        # Display versions as a timeline
        for i, ver in enumerate(versions):
            col1, col2 = st.columns([1, 5])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="background-color: {'#1f77b4' if i == 0 else '#aaa'}; color: white; width: 40px; height: 40px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                        {ver['version']}
                    </div>
                    <div style="height: 30px; width: 2px; background-color: #ddd; margin-top: 5px; {'' if i < len(versions)-1 else 'display: none;'}"></div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: {5 if i < len(versions)-1 else 0}px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: bold;">{ver['date']}</span>
                        <span style="color: #666;">{ver['author']}</span>
                    </div>
                    <div style="margin-top: 5px;">{ver['changes']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Compare versions buttons
            if i > 0:
                col3, col4 = st.columns([4, 1])
                with col4:
                    st.button(f"Compare to {versions[i-1]['version']}", key=f"compare_{i}")
    
    # Activity Log tab
    with collab_tabs[3]:
        st.subheader("Activity Log")
        
        # Activity data
        activities = [
            {"action": "Edited document", "user": "John Smith", "time": "10 minutes ago", "details": "Updated concrete specifications."},
            {"action": "Added comment", "user": "Sarah Johnson", "time": "30 minutes ago", "details": "Question about reinforcement spacing."},
            {"action": "Viewed document", "user": "Mike Chen", "time": "1 hour ago", "details": ""},
            {"action": "Created new version", "user": "John Smith", "time": "2 hours ago", "details": "Version 3.2 created."},
            {"action": "Mentioned you", "user": "Lisa Rodriguez", "time": "Yesterday", "details": "In comment: 'Can @CurrentUser please review this section?'"},
            {"action": "Resolved comment", "user": "Sarah Johnson", "time": "Yesterday", "details": "Marked comment as resolved."},
            {"action": "Downloaded document", "user": "Mike Chen", "time": "2 days ago", "details": ""}
        ]
        
        # Activity filters
        col1, col2 = st.columns(2)
        
        with col1:
            action_filter = st.multiselect("Filter by Action", 
                                         ["All", "Viewed", "Edited", "Downloaded", "Commented", "Created version", "Resolved comment", "Mentioned"], 
                                         default=["All"])
        
        with col2:
            user_filter = st.multiselect("Filter by User",
                                       ["All", "John Smith", "Sarah Johnson", "Mike Chen", "Lisa Rodriguez"],
                                       default=["All"])
        
        # Display activities
        for activity in activities:
            # Apply filters
            if ("All" not in action_filter and not any(a.lower() in activity["action"].lower() for a in action_filter)) or \
               ("All" not in user_filter and activity["user"] not in user_filter):
                continue
                
            st.markdown(f"""
            <div style="display: flex; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                <div style="width: 40px; height: 40px; background-color: #f0f0f0; border-radius: 20px; margin-right: 15px; display: flex; align-items: center; justify-content: center;">
                    {activity["user"][0]}
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500;">{activity["user"]} {activity["action"]}</div>
                    <div style="color: #666; font-size: 12px;">{activity["time"]}</div>
                    <div style="font-size: 14px; margin-top: 5px;">{activity["details"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_current_set():
    """Render Highland Tower Development current drawing set"""
    st.header("📋 Current Drawing Set - Highland Tower Development")
    st.markdown("**Project No. HTD-2024-001 | 15-Story Mixed-Use Development**")
    
    # Drawing set overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sheets", "287")
    col2.metric("Last Revision", "Rev 08")
    col3.metric("Issue Date", "May 20, 2025")
    col4.metric("Next Update", "June 3, 2025")
    
    # Drawing categories
    drawing_tabs = st.tabs(["🏗️ Architectural", "⚡ Structural", "🔧 MEP", "🌐 Civil", "📋 General"])
    
    with drawing_tabs[0]:
        st.subheader("Architectural Drawings")
        arch_drawings = [
            {"Sheet": "A-001", "Title": "Cover Sheet & Drawing Index", "Rev": "08", "Date": "2025-05-20"},
            {"Sheet": "A-100", "Title": "Site Plan & Context", "Rev": "07", "Date": "2025-05-15"},
            {"Sheet": "A-101", "Title": "Ground Floor Plan", "Rev": "08", "Date": "2025-05-20"},
            {"Sheet": "A-102", "Title": "Typical Floor Plan (Levels 2-14)", "Rev": "06", "Date": "2025-05-10"},
            {"Sheet": "A-103", "Title": "Penthouse Floor Plan", "Rev": "05", "Date": "2025-05-05"},
            {"Sheet": "A-200", "Title": "Building Elevations - North & South", "Rev": "07", "Date": "2025-05-15"},
            {"Sheet": "A-201", "Title": "Building Elevations - East & West", "Rev": "07", "Date": "2025-05-15"},
            {"Sheet": "A-300", "Title": "Building Sections", "Rev": "06", "Date": "2025-05-10"},
            {"Sheet": "A-400", "Title": "Wall Sections & Details", "Rev": "08", "Date": "2025-05-20"},
            {"Sheet": "A-500", "Title": "Interior Details & Finishes", "Rev": "05", "Date": "2025-05-05"}
        ]
        
        for drawing in arch_drawings:
            col1, col2, col3, col4 = st.columns([2, 4, 1, 2])
            col1.write(f"**{drawing['Sheet']}**")
            col2.write(drawing['Title'])
            col3.write(drawing['Rev'])
            col4.write(drawing['Date'])
    
    with drawing_tabs[1]:
        st.subheader("Structural Drawings")
        struct_drawings = [
            {"Sheet": "S-001", "Title": "Structural General Notes", "Rev": "06", "Date": "2025-05-18"},
            {"Sheet": "S-100", "Title": "Foundation Plan", "Rev": "08", "Date": "2025-05-20"},
            {"Sheet": "S-200", "Title": "Ground Floor Framing Plan", "Rev": "07", "Date": "2025-05-15"},
            {"Sheet": "S-201", "Title": "Typical Floor Framing Plan", "Rev": "06", "Date": "2025-05-10"},
            {"Sheet": "S-300", "Title": "Column Schedule & Details", "Rev": "08", "Date": "2025-05-20"},
            {"Sheet": "S-400", "Title": "Connection Details", "Rev": "07", "Date": "2025-05-15"}
        ]
        
        for drawing in struct_drawings:
            col1, col2, col3, col4 = st.columns([2, 4, 1, 2])
            col1.write(f"**{drawing['Sheet']}**")
            col2.write(drawing['Title'])
            col3.write(drawing['Rev'])
            col4.write(drawing['Date'])

def render_specifications():
    """Render Highland Tower Development project specifications"""
    st.header("📖 Project Specifications - Highland Tower Development")
    st.markdown("**CSI MasterFormat 2018 Edition | 16 Divisions**")
    
    # Specifications overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sections", "156")
    col2.metric("Current Version", "3.2")
    col3.metric("Last Updated", "May 18, 2025")
    col4.metric("Completion", "94%")
    
    # CSI Divisions
    spec_tabs = st.tabs(["📋 General", "🏗️ Sitework", "🧱 Concrete", "⚡ Metals", "🔧 Mechanical", "💡 Electrical"])
    
    with spec_tabs[0]:
        st.subheader("Division 01 - General Requirements")
        general_specs = [
            {"Section": "01 1000", "Title": "Summary", "Status": "Complete", "Pages": "12"},
            {"Section": "01 2500", "Title": "Substitution Procedures", "Status": "Complete", "Pages": "8"},
            {"Section": "01 3300", "Title": "Submittal Procedures", "Status": "Complete", "Pages": "15"},
            {"Section": "01 4000", "Title": "Quality Requirements", "Status": "Complete", "Pages": "22"},
            {"Section": "01 5000", "Title": "Temporary Facilities", "Status": "Complete", "Pages": "18"},
            {"Section": "01 7000", "Title": "Execution & Closeout", "Status": "Complete", "Pages": "25"}
        ]
        
        for spec in general_specs:
            col1, col2, col3, col4 = st.columns([2, 4, 2, 1])
            col1.write(f"**{spec['Section']}**")
            col2.write(spec['Title'])
            col3.write(f"✅ {spec['Status']}")
            col4.write(f"{spec['Pages']}p")
    
    with spec_tabs[1]:
        st.subheader("Division 03 - Concrete")
        concrete_specs = [
            {"Section": "03 3000", "Title": "Cast-in-Place Concrete", "Status": "Complete", "Pages": "28"},
            {"Section": "03 4000", "Title": "Precast Concrete", "Status": "Complete", "Pages": "22"},
            {"Section": "03 5000", "Title": "Cementitious Decks", "Status": "Complete", "Pages": "15"}
        ]
        
        for spec in concrete_specs:
            col1, col2, col3, col4 = st.columns([2, 4, 2, 1])
            col1.write(f"**{spec['Section']}**")
            col2.write(spec['Title'])
            col3.write(f"✅ {spec['Status']}")
            col4.write(f"{spec['Pages']}p")

def render_document_upload_with_pdf_viewer():
    """Enhanced document upload with PDF viewing and markup capabilities"""
    st.header("⬆️ Document Upload & PDF Viewer")
    st.markdown("**Upload, view, and markup construction documents for Highland Tower Development**")
    
    # Upload section
    st.subheader("📤 Upload New Document")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Select file to upload",
            type=["pdf", "dwg", "xlsx", "docx", "jpg", "png"],
            help="Supported formats: PDF, DWG, Excel, Word, Images"
        )
        
        if uploaded_file:
            # Document metadata form
            with st.form("document_metadata"):
                doc_title = st.text_input("Document Title", value=uploaded_file.name.split('.')[0])
                doc_category = st.selectbox("Category", [
                    "Architectural Drawings", "Structural Drawings", "MEP Drawings", 
                    "Specifications", "Submittals", "RFIs", "Reports", "Photos"
                ])
                doc_phase = st.selectbox("Project Phase", [
                    "Design Development", "Construction Documents", "Construction", "Closeout"
                ])
                doc_tags = st.text_input("Tags (comma-separated)", placeholder="foundation, concrete, level-13")
                
                submit_doc = st.form_submit_button("📁 Upload Document")
                
                if submit_doc:
                    # Process upload
                    st.success(f"✅ Document '{doc_title}' uploaded successfully!")
                    st.info("📋 Document has been added to the Highland Tower project database.")
    
    with col2:
        st.markdown("**📊 Upload Statistics**")
        st.metric("Total Documents", "1,247")
        st.metric("This Week", "23", "+8")
        st.metric("Storage Used", "45.2 GB", "+2.1 GB")
    
    # PDF Viewer and Markup section
    st.divider()
    st.subheader("📄 PDF Viewer & Markup Tools")
    
    # Sample PDF documents for demonstration
    sample_docs = [
        "A-101 Ground Floor Plan.pdf",
        "S-100 Foundation Plan.pdf", 
        "M-200 HVAC Layout.pdf",
        "Spec Section 03 3000 Concrete.pdf"
    ]
    
    selected_doc = st.selectbox("Select document to view:", sample_docs)
    
    if selected_doc:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Viewing: {selected_doc}**")
            
            # PDF viewer placeholder (would integrate with actual PDF viewer)
            st.markdown("""
            <div style="border: 2px solid #e1e5e9; border-radius: 8px; padding: 20px; text-align: center; background-color: #f8f9fa;">
                <h4>📄 PDF Viewer</h4>
                <p><strong>{}</strong></p>
                <p>🔍 Zoom: 100% | Page 1 of 24</p>
                <div style="margin: 20px 0;">
                    <button style="margin: 5px; padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px;">🔍 Zoom In</button>
                    <button style="margin: 5px; padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px;">🔍 Zoom Out</button>
                    <button style="margin: 5px; padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px;">✏️ Markup</button>
                    <button style="margin: 5px; padding: 8px 16px; background: #ffc107; color: black; border: none; border-radius: 4px;">💬 Comment</button>
                </div>
                <p style="color: #6c757d;">PDF content would display here with full markup capabilities</p>
            </div>
            """.format(selected_doc), unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🛠️ Markup Tools**")
            
            # Markup tool options
            markup_tool = st.radio("Select Tool:", [
                "✏️ Pen", "📝 Text", "🔲 Rectangle", "🔴 Circle", "➡️ Arrow", "📌 Pin"
            ])
            
            if markup_tool == "✏️ Pen":
                pen_color = st.color_picker("Pen Color", "#FF0000")
                pen_size = st.slider("Pen Size", 1, 10, 3)
            elif markup_tool == "📝 Text":
                text_content = st.text_area("Add Text", placeholder="Enter your comment...")
                text_color = st.color_picker("Text Color", "#000000")
            
            st.markdown("**💾 Actions**")
            if st.button("💾 Save Markups", use_container_width=True):
                st.success("✅ Markups saved!")
            if st.button("📤 Share Document", use_container_width=True):
                st.info("📧 Document shared with project team")
            if st.button("🖨️ Print", use_container_width=True):
                st.info("🖨️ Sending to printer...")
    
    # Recent markups
    st.divider()
    st.subheader("📋 Recent Document Activity")
    
    recent_activity = [
        {"doc": "A-101 Ground Floor Plan", "action": "Added markup", "user": "Mike Rodriguez", "time": "2 hours ago"},
        {"doc": "S-100 Foundation Plan", "action": "Added comment", "user": "Sarah Chen", "time": "5 hours ago"},
        {"doc": "Spec 03 3000", "action": "Approved revision", "user": "Project Manager", "time": "Yesterday"},
        {"doc": "M-200 HVAC Layout", "action": "Uploaded new version", "user": "MEP Engineer", "time": "2 days ago"}
    ]
    
    for activity in recent_activity:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        col1.write(f"📄 {activity['doc']}")
        col2.write(activity['action'])
        col3.write(activity['user'])
        col4.write(activity['time'])

def render_document_upload():
    """Render document upload interface."""
    st.subheader("Upload Document")
    
    # Document details form
    col1, col2 = st.columns(2)
    
    with col1:
        doc_name = st.text_input("Document Name")
        doc_type = st.selectbox("Document Type", ["Drawing", "Specification", "Contract", "Permit", "Report", "Manual"])
        doc_discipline = st.selectbox("Discipline", ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "General"])
    
    with col2:
        doc_number = st.text_input("Document Number")
        doc_version = st.text_input("Version", "1.0")
        doc_status = st.selectbox("Status", ["Draft", "In Review", "Approved", "Final", "Superseded"])
    
    # Tags
    doc_tags = st.text_input("Tags (comma separated)")
    
    # Description
    doc_description = st.text_area("Description")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "xlsx", "dwg", "rvt", "jpg", "png"])
    
    # Related documents
    related_docs = st.multiselect("Related Documents", ["DOC-001: Foundation Drawings", "DOC-002: Electrical Specifications", "DOC-003: General Conditions", "DOC-004: Building Permit"])
    
    # Notify team checkbox
    notify_team = st.checkbox("Notify Team")
    
    # Submit button
    if st.button("Upload Document"):
        if doc_name and uploaded_file:
            st.success("Document uploaded successfully!")
            
            # In a real application, this would save the document to storage and database
            
            # Show document details
            st.markdown("### Document Uploaded")
            st.markdown(f"**Name:** {doc_name}")
            st.markdown(f"**Type:** {doc_type}")
            st.markdown(f"**Number:** {doc_number}")
            st.markdown(f"**Version:** {doc_version}")
            st.markdown(f"**Status:** {doc_status}")
            st.markdown(f"**Tags:** {doc_tags}")
            
            # Option to view document or upload another
            col1, col2 = st.columns(2)
            
            with col1:
                st.button("View Document")
            
            with col2:
                if st.button("Upload Another"):
                    st.rerun()
        else:
            st.error("Please provide a document name and file to upload.")