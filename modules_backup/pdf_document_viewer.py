"""
Highland Tower Development - PDF Document Viewer
Pure Python implementation with PDF.js integration for drawing management and markup.
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

def render_pdf_document_viewer():
    """Highland Tower Development - Advanced PDF Document Viewer"""
    
    st.markdown("""
    <div class="module-header">
        <h1>📄 Highland Tower Development - Document Viewer</h1>
        <p>$45.5M Project - Drawing Management & Document Collaboration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize document data
    initialize_highland_document_data()
    
    # Document overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", "847", "Drawings, specs, reports")
    with col2:
        st.metric("Active Drawings", "234", "Current revision")
    with col3:
        st.metric("Pending Reviews", "23", "Awaiting approval")
    with col4:
        st.metric("Markup Items", "156", "Active annotations")
    
    # Main document tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Document Viewer",
        "🗂️ Drawing Sets", 
        "✏️ Markup Tools",
        "📋 Review Workflow",
        "📊 Document Reports"
    ])
    
    with tab1:
        render_document_viewer()
    
    with tab2:
        render_drawing_sets()
    
    with tab3:
        render_markup_tools()
    
    with tab4:
        render_review_workflow()
    
    with tab5:
        render_document_reports()

def initialize_highland_document_data():
    """Initialize Highland Tower Development document data"""
    
    if "highland_documents" not in st.session_state:
        st.session_state.highland_documents = [
            {
                "document_id": "HTD-A-001",
                "title": "Highland Tower - Site Plan",
                "type": "Drawing",
                "discipline": "Architecture",
                "revision": "Rev 12",
                "date": "2024-05-28",
                "author": "Highland Design Associates",
                "status": "Current",
                "file_size": "2.4 MB",
                "page_count": 1,
                "markup_count": 3,
                "category": "Site Plans"
            },
            {
                "document_id": "HTD-A-101",
                "title": "Highland Tower - Floor Plans L1-L3",
                "type": "Drawing",
                "discipline": "Architecture", 
                "revision": "Rev 8",
                "date": "2024-05-25",
                "author": "Highland Design Associates",
                "status": "Current",
                "file_size": "5.2 MB",
                "page_count": 3,
                "markup_count": 12,
                "category": "Floor Plans"
            },
            {
                "document_id": "HTD-S-201",
                "title": "Highland Tower - Structural Framing Plans",
                "type": "Drawing",
                "discipline": "Structural",
                "revision": "Rev 6",
                "date": "2024-05-27",
                "author": "Structural Engineering LLC",
                "status": "Under Review",
                "file_size": "8.1 MB",
                "page_count": 15,
                "markup_count": 7,
                "category": "Structural Plans"
            },
            {
                "document_id": "HTD-M-301",
                "title": "Highland Tower - HVAC Plans & Details",
                "type": "Drawing",
                "discipline": "HVAC",
                "revision": "Rev 4",
                "date": "2024-05-20",
                "author": "MEP Engineering Group",
                "status": "Needs Revision",
                "file_size": "6.7 MB",
                "page_count": 8,
                "markup_count": 18,
                "category": "MEP Plans"
            },
            {
                "document_id": "HTD-SPEC-001",
                "title": "Highland Tower - Technical Specifications",
                "type": "Specification",
                "discipline": "General",
                "revision": "Rev 3",
                "date": "2024-05-15",
                "author": "Highland Design Associates",
                "status": "Current",
                "file_size": "12.8 MB",
                "page_count": 245,
                "markup_count": 45,
                "category": "Specifications"
            }
        ]
    
    if "highland_markups" not in st.session_state:
        st.session_state.highland_markups = [
            {
                "markup_id": "MU-001",
                "document_id": "HTD-A-101",
                "page": 1,
                "type": "Cloud",
                "x": 250,
                "y": 180,
                "width": 120,
                "height": 80,
                "comment": "Verify door swing clearance in corridor",
                "author": "John Smith",
                "date": "2024-05-28",
                "status": "Open",
                "priority": "Medium"
            },
            {
                "markup_id": "MU-002",
                "document_id": "HTD-S-201",
                "page": 3,
                "type": "Arrow",
                "x": 400,
                "y": 220,
                "width": 60,
                "height": 40,
                "comment": "Beam size needs verification per structural calc",
                "author": "Mike Rodriguez",
                "date": "2024-05-27",
                "status": "Resolved",
                "priority": "High"
            },
            {
                "markup_id": "MU-003",
                "document_id": "HTD-M-301",
                "page": 2,
                "type": "Rectangle",
                "x": 300,
                "y": 150,
                "width": 100,
                "height": 60,
                "comment": "Duct routing conflicts with structural - coordinate",
                "author": "Sarah Johnson",
                "date": "2024-05-26",
                "status": "Open",
                "priority": "High"
            }
        ]

def render_document_viewer():
    """Render interactive PDF document viewer"""
    
    st.subheader("📄 Highland Tower Development - Document Viewer")
    
    # Document selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**📋 Document Selection:**")
        
        # Filter options
        discipline_filter = st.selectbox("Filter by Discipline", 
                                       ["All", "Architecture", "Structural", "HVAC", "Electrical", "General"])
        
        type_filter = st.selectbox("Filter by Type", 
                                 ["All", "Drawing", "Specification", "Report", "Manual"])
        
        status_filter = st.selectbox("Filter by Status", 
                                   ["All", "Current", "Under Review", "Needs Revision", "Superseded"])
        
        # Apply filters
        filtered_docs = st.session_state.highland_documents
        if discipline_filter != "All":
            filtered_docs = [d for d in filtered_docs if d['discipline'] == discipline_filter]
        if type_filter != "All":
            filtered_docs = [d for d in filtered_docs if d['type'] == type_filter]
        if status_filter != "All":
            filtered_docs = [d for d in filtered_docs if d['status'] == status_filter]
        
        # Document list
        st.markdown("**📄 Available Documents:**")
        
        if filtered_docs:
            doc_options = [f"{doc['document_id']} - {doc['title'][:30]}..." for doc in filtered_docs]
            selected_doc_idx = st.selectbox("Select Document", range(len(doc_options)), format_func=lambda x: doc_options[x])
            selected_doc = filtered_docs[selected_doc_idx]
            
            # Document info
            st.markdown("**📊 Document Information:**")
            st.write(f"**ID:** {selected_doc['document_id']}")
            st.write(f"**Type:** {selected_doc['type']}")
            st.write(f"**Discipline:** {selected_doc['discipline']}")
            st.write(f"**Revision:** {selected_doc['revision']}")
            st.write(f"**Date:** {selected_doc['date']}")
            st.write(f"**Author:** {selected_doc['author']}")
            st.write(f"**Status:** {selected_doc['status']}")
            st.write(f"**Pages:** {selected_doc['page_count']}")
            st.write(f"**File Size:** {selected_doc['file_size']}")
            st.write(f"**Markups:** {selected_doc['markup_count']}")
            
            # Document actions
            st.markdown("**📋 Document Actions:**")
            
            if st.button("📥 Download Original", key="download_original"):
                st.info(f"Downloading {selected_doc['title']}...")
            
            if st.button("📤 Upload New Revision", key="upload_revision"):
                st.session_state.show_upload_form = True
            
            if st.button("✏️ Add Markup", key="add_markup"):
                st.session_state.markup_mode = True
                st.info("Markup mode activated - click on viewer to add markups")
            
            if st.button("📋 Generate Report", key="generate_report"):
                st.info("Generating markup report...")
        
        else:
            st.info("No documents match the selected filters.")
    
    with col2:
        st.markdown("**📄 Document Viewer:**")
        
        if filtered_docs:
            # Create the PDF viewer component
            viewer_html = generate_pdf_viewer_html(selected_doc, st.session_state.highland_markups)
            
            # Display the PDF viewer
            components.html(viewer_html, height=700)
            
            # Page navigation
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("◀ Previous Page", key="prev_page"):
                    st.info("Navigate to previous page")
            
            with col2:
                current_page = st.number_input("Page", min_value=1, max_value=selected_doc['page_count'], value=1)
                st.write(f"of {selected_doc['page_count']} pages")
            
            with col3:
                if st.button("Next Page ▶", key="next_page"):
                    st.info("Navigate to next page")

def render_drawing_sets():
    """Render drawing sets management"""
    
    st.subheader("🗂️ Highland Tower Development - Drawing Sets")
    
    st.info("**🗂️ Drawing Sets:** Organize documents into logical sets for distribution and coordination.")
    
    # Drawing sets overview
    drawing_sets = [
        {
            "set_id": "SET-001",
            "name": "Permit Set - Highland Tower",
            "description": "Complete permit submission package",
            "document_count": 47,
            "last_updated": "2024-05-28",
            "status": "Current",
            "distribution": ["City Planning", "Building Department", "Fire Marshal"]
        },
        {
            "set_id": "SET-002", 
            "name": "Construction Documents - Phase 1",
            "description": "Foundation and below grade construction",
            "document_count": 23,
            "last_updated": "2024-05-25",
            "status": "Issued for Construction",
            "distribution": ["General Contractor", "Structural Sub", "Concrete Sub"]
        },
        {
            "set_id": "SET-003",
            "name": "Construction Documents - Phase 2", 
            "description": "Superstructure and envelope",
            "document_count": 65,
            "last_updated": "2024-05-20",
            "status": "Under Review",
            "distribution": ["General Contractor", "Steel Sub", "Envelope Sub"]
        },
        {
            "set_id": "SET-004",
            "name": "MEP Coordination Set",
            "description": "Coordinated MEP systems drawings",
            "document_count": 34,
            "last_updated": "2024-05-15",
            "status": "Coordination Required",
            "distribution": ["MEP Contractors", "BIM Coordinator"]
        }
    ]
    
    # Display drawing sets
    for drawing_set in drawing_sets:
        status_color = {
            "Current": "🟢", 
            "Issued for Construction": "🟢", 
            "Under Review": "🟡", 
            "Coordination Required": "🔴"
        }.get(drawing_set['status'], "⚪")
        
        with st.expander(f"{status_color} {drawing_set['name']} ({drawing_set['document_count']} docs)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Set ID:** {drawing_set['set_id']}")
                st.write(f"**Description:** {drawing_set['description']}")
                st.write(f"**Document Count:** {drawing_set['document_count']}")
                st.write(f"**Last Updated:** {drawing_set['last_updated']}")
                st.write(f"**Status:** {drawing_set['status']}")
            
            with col2:
                st.write("**Distribution List:**")
                for recipient in drawing_set['distribution']:
                    st.write(f"• {recipient}")
            
            # Set actions
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📥 Download Set", key=f"download_set_{drawing_set['set_id']}"):
                    st.info(f"Downloading {drawing_set['name']}...")
            
            with col2:
                if st.button("📧 Distribute", key=f"distribute_{drawing_set['set_id']}"):
                    st.info("Sending to distribution list...")
            
            with col3:
                if st.button("✏️ Edit Set", key=f"edit_set_{drawing_set['set_id']}"):
                    st.info("Edit set functionality...")
            
            with col4:
                if st.button("📋 Print List", key=f"print_list_{drawing_set['set_id']}"):
                    st.info("Generating drawing list...")

def render_markup_tools():
    """Render markup and annotation tools"""
    
    st.subheader("✏️ Highland Tower Development - Markup Tools")
    
    st.info("**✏️ Markup Tools:** Add annotations, comments, and markups to Highland Tower Development drawings.")
    
    # Active markups
    st.markdown("**📝 Active Markups:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "Resolved", "Closed"])
    with col3:
        author_filter = st.selectbox("Filter by Author", ["All", "John Smith", "Mike Rodriguez", "Sarah Johnson"])
    
    # Apply filters to markups
    filtered_markups = st.session_state.highland_markups
    if priority_filter != "All":
        filtered_markups = [m for m in filtered_markups if m['priority'] == priority_filter]
    if status_filter != "All":
        filtered_markups = [m for m in filtered_markups if m['status'] == status_filter]
    if author_filter != "All":
        filtered_markups = [m for m in filtered_markups if m['author'] == author_filter]
    
    # Display markups
    for markup in filtered_markups:
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(markup['priority'], "⚪")
        status_color = {"Open": "🔴", "Resolved": "🟢", "Closed": "⚪"}.get(markup['status'], "⚪")
        
        with st.expander(f"{priority_color} {markup['markup_id']} - {markup['comment'][:50]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Document:** {markup['document_id']}")
                st.write(f"**Page:** {markup['page']}")
                st.write(f"**Type:** {markup['type']}")
                st.write(f"**Priority:** {markup['priority']}")
                st.write(f"**Status:** {status_color} {markup['status']}")
            
            with col2:
                st.write(f"**Author:** {markup['author']}")
                st.write(f"**Date:** {markup['date']}")
                st.write(f"**Location:** ({markup['x']}, {markup['y']})")
                st.write(f"**Size:** {markup['width']} x {markup['height']}")
            
            st.write(f"**Comment:** {markup['comment']}")
            
            # Markup actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if markup['status'] == 'Open' and st.button("✅ Resolve", key=f"resolve_markup_{markup['markup_id']}"):
                    # Update markup status
                    for i, m in enumerate(st.session_state.highland_markups):
                        if m['markup_id'] == markup['markup_id']:
                            st.session_state.highland_markups[i]['status'] = 'Resolved'
                            break
                    st.success("Markup resolved!")
                    st.rerun()
            
            with col2:
                if st.button("📄 View Document", key=f"view_doc_{markup['markup_id']}"):
                    st.info(f"Opening document {markup['document_id']}...")
            
            with col3:
                if st.button("✏️ Edit Markup", key=f"edit_markup_{markup['markup_id']}"):
                    st.session_state[f"show_edit_markup_{markup['markup_id']}"] = True
    
    # Add new markup form
    st.markdown("---")
    st.markdown("**➕ Add New Markup:**")
    
    with st.form("add_markup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            document_options = [f"{doc['document_id']} - {doc['title'][:30]}..." for doc in st.session_state.highland_documents]
            selected_doc = st.selectbox("Select Document", range(len(document_options)), format_func=lambda x: document_options[x])
            
            page_number = st.number_input("Page Number", min_value=1, value=1)
            markup_type = st.selectbox("Markup Type", ["Cloud", "Arrow", "Rectangle", "Circle", "Text", "Highlight"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        with col2:
            x_position = st.number_input("X Position", min_value=0, value=100)
            y_position = st.number_input("Y Position", min_value=0, value=100)
            width = st.number_input("Width", min_value=10, value=100)
            height = st.number_input("Height", min_value=10, value=60)
        
        comment = st.text_area("Comment*", placeholder="Describe the issue or note...")
        author = st.text_input("Author", value="Current User")
        
        if st.form_submit_button("➕ Add Markup"):
            if comment:
                new_markup = {
                    "markup_id": f"MU-{len(st.session_state.highland_markups) + 1:03d}",
                    "document_id": st.session_state.highland_documents[selected_doc]['document_id'],
                    "page": page_number,
                    "type": markup_type,
                    "x": x_position,
                    "y": y_position,
                    "width": width,
                    "height": height,
                    "comment": comment,
                    "author": author,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Open",
                    "priority": priority
                }
                
                st.session_state.highland_markups.append(new_markup)
                st.success("Markup added successfully!")
                st.rerun()
            else:
                st.error("Please enter a comment!")

def render_review_workflow():
    """Render document review workflow"""
    
    st.subheader("📋 Highland Tower Development - Review Workflow")
    
    st.info("**📋 Review Workflow:** Manage document review cycles and approval processes for Highland Tower drawings.")
    
    # Review status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pending Reviews", "23", "Awaiting review")
    with col2:
        st.metric("In Review", "8", "Active reviews")
    with col3:
        st.metric("Approved", "145", "Completed reviews")
    with col4:
        st.metric("Avg Review Time", "3.2 days", "Per document")
    
    # Review workflow stages
    st.markdown("**🔄 Review Workflow Stages:**")
    
    workflow_stages = [
        {"stage": "Submission", "documents": 5, "avg_time": "1 day", "status": "🟢 On Track"},
        {"stage": "Technical Review", "documents": 12, "avg_time": "2 days", "status": "🟡 Delayed"},
        {"stage": "Coordination Review", "documents": 8, "avg_time": "1.5 days", "status": "🟢 On Track"},
        {"stage": "Final Approval", "documents": 3, "avg_time": "0.5 days", "status": "🟢 On Track"},
        {"stage": "Distribution", "documents": 2, "avg_time": "0.2 days", "status": "🟢 On Track"}
    ]
    
    for stage in workflow_stages:
        with st.expander(f"{stage['status']} {stage['stage']} - {stage['documents']} documents"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Documents in Stage:** {stage['documents']}")
            with col2:
                st.write(f"**Average Time:** {stage['avg_time']}")
            with col3:
                st.write(f"**Status:** {stage['status']}")
    
    # Recent review activity
    st.markdown("**📅 Recent Review Activity:**")
    
    review_activity = [
        {"date": "2024-05-28", "document": "HTD-A-101", "reviewer": "John Smith", "action": "Approved", "notes": "Ready for construction"},
        {"date": "2024-05-28", "document": "HTD-S-201", "reviewer": "Mike Rodriguez", "action": "Needs Revision", "notes": "Beam sizes require verification"},
        {"date": "2024-05-27", "document": "HTD-M-301", "reviewer": "Sarah Johnson", "action": "Under Review", "notes": "Checking HVAC routing conflicts"},
        {"date": "2024-05-27", "document": "HTD-A-001", "reviewer": "Design Team", "action": "Approved", "notes": "Site plan approved with minor notes"}
    ]
    
    for activity in review_activity:
        action_color = {"Approved": "🟢", "Needs Revision": "🔴", "Under Review": "🟡"}.get(activity['action'], "⚪")
        
        st.write(f"**{activity['date']}** - {action_color} {activity['document']} - {activity['action']} by {activity['reviewer']}")
        st.write(f"   *{activity['notes']}*")

def render_document_reports():
    """Render document reports and analytics"""
    
    st.subheader("📊 Highland Tower Development - Document Reports")
    
    # Document statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Document Statistics:**")
        
        doc_stats = {
            "Document Type": ["Drawings", "Specifications", "Reports", "Manuals", "Submittals"],
            "Count": [234, 45, 78, 23, 156],
            "Current": [198, 42, 65, 20, 134],
            "Under Review": [25, 2, 8, 2, 15],
            "Superseded": [11, 1, 5, 1, 7]
        }
        
        doc_stats_df = pd.DataFrame(doc_stats)
        st.dataframe(doc_stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**📈 Review Performance:**")
        
        # Create review performance chart
        import plotly.express as px
        
        review_data = {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Reviews Completed": [23, 28, 31, 25],
            "Average Review Time": [3.5, 3.2, 2.8, 3.1]
        }
        
        fig = px.bar(review_data, x="Week", y="Reviews Completed", 
                    title="Weekly Review Completion")
        st.plotly_chart(fig, use_container_width=True)
    
    # Markup summary
    st.markdown("**✏️ Markup Summary:**")
    
    markup_summary = {
        "Priority": ["High", "Medium", "Low"],
        "Open": [8, 15, 12],
        "Resolved": [45, 67, 89],
        "Total": [53, 82, 101]
    }
    
    markup_df = pd.DataFrame(markup_summary)
    st.dataframe(markup_df, use_container_width=True, hide_index=True)

def generate_pdf_viewer_html(document: Dict[str, Any], markups: List[Dict[str, Any]]) -> str:
    """Generate HTML for PDF document viewer with markup support"""
    
    # Filter markups for this document
    doc_markups = [m for m in markups if m['document_id'] == document['document_id']]
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; background: #f0f0f0; }}
            #viewer {{ width: 100%; height: 700px; position: relative; }}
            #pdf-canvas {{ 
                border: 1px solid #ddd; 
                background: white; 
                display: block; 
                margin: 0 auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            .markup {{ 
                position: absolute; 
                border: 2px solid red; 
                background: rgba(255,0,0,0.1);
                cursor: pointer;
                z-index: 10;
            }}
            .markup-cloud {{ 
                border: 2px dashed red; 
                border-radius: 50%;
                background: rgba(255,0,0,0.1);
            }}
            .markup-arrow {{ 
                border: 2px solid blue; 
                background: rgba(0,0,255,0.1);
            }}
            .markup-text {{ 
                background: rgba(255,255,0,0.3);
                border: 1px solid orange;
            }}
            .markup-tooltip {{
                position: absolute;
                background: black;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 20;
                max-width: 200px;
                display: none;
            }}
            .document-info {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 12px;
                z-index: 5;
            }}
            .zoom-controls {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255,255,255,0.9);
                padding: 5px;
                border-radius: 5px;
                z-index: 5;
            }}
        </style>
    </head>
    <body>
        <div id="viewer">
            <div class="document-info">
                <strong>Highland Tower Development</strong><br>
                Document: {document['document_id']}<br>
                Title: {document['title']}<br>
                Revision: {document['revision']}<br>
                Date: {document['date']}<br>
                Pages: {document['page_count']}<br>
                Markups: {document['markup_count']}
            </div>
            
            <div class="zoom-controls">
                <button onclick="zoomIn()">🔍+</button>
                <button onclick="zoomOut()">🔍-</button>
                <button onclick="resetZoom()">⚪</button>
                <span id="zoom-level">100%</span>
            </div>
            
            <canvas id="pdf-canvas"></canvas>
            
            <div id="markup-container">
                <!-- Markups will be rendered here -->
            </div>
        </div>
        
        <script>
            // PDF.js setup
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
            
            let pdfDoc = null;
            let pageNum = 1;
            let pageRendering = false;
            let pageNumPending = null;
            let scale = 1.0;
            let canvas = document.getElementById('pdf-canvas');
            let ctx = canvas.getContext('2d');
            
            // Sample PDF data (in real implementation, this would be the actual PDF)
            const pdfData = createSamplePDF();
            
            // Load PDF
            pdfjsLib.getDocument({{data: pdfData}}).promise.then(function(pdfDoc_) {{
                pdfDoc = pdfDoc_;
                renderPage(pageNum);
                renderMarkups();
            }});
            
            function renderPage(num) {{
                pageRendering = true;
                pdfDoc.getPage(num).then(function(page) {{
                    let viewport = page.getViewport({{scale: scale}});
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    
                    let renderContext = {{
                        canvasContext: ctx,
                        viewport: viewport
                    }};
                    
                    let renderTask = page.render(renderContext);
                    renderTask.promise.then(function() {{
                        pageRendering = false;
                        if (pageNumPending !== null) {{
                            renderPage(pageNumPending);
                            pageNumPending = null;
                        }}
                        renderMarkups();
                    }});
                }});
            }}
            
            function renderMarkups() {{
                const container = document.getElementById('markup-container');
                container.innerHTML = '';
                
                const markups = {json.dumps(doc_markups)};
                
                markups.forEach(function(markup) {{
                    if (markup.page === pageNum) {{
                        const markupEl = document.createElement('div');
                        markupEl.className = 'markup markup-' + markup.type.toLowerCase();
                        markupEl.style.left = (markup.x * scale) + 'px';
                        markupEl.style.top = (markup.y * scale) + 'px';
                        markupEl.style.width = (markup.width * scale) + 'px';
                        markupEl.style.height = (markup.height * scale) + 'px';
                        
                        // Add tooltip
                        const tooltip = document.createElement('div');
                        tooltip.className = 'markup-tooltip';
                        tooltip.textContent = markup.comment + ' (' + markup.author + ')';
                        
                        markupEl.appendChild(tooltip);
                        
                        markupEl.addEventListener('mouseenter', function() {{
                            tooltip.style.display = 'block';
                        }});
                        
                        markupEl.addEventListener('mouseleave', function() {{
                            tooltip.style.display = 'none';
                        }});
                        
                        container.appendChild(markupEl);
                    }}
                }});
            }}
            
            function zoomIn() {{
                scale *= 1.2;
                renderPage(pageNum);
                updateZoomLevel();
            }}
            
            function zoomOut() {{
                scale /= 1.2;
                renderPage(pageNum);
                updateZoomLevel();
            }}
            
            function resetZoom() {{
                scale = 1.0;
                renderPage(pageNum);
                updateZoomLevel();
            }}
            
            function updateZoomLevel() {{
                document.getElementById('zoom-level').textContent = Math.round(scale * 100) + '%';
            }}
            
            function createSamplePDF() {{
                // Create a simple sample PDF for demonstration
                // In real implementation, this would be the actual PDF data
                const samplePdfBase64 = "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPD4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GIDQgMCBSCj4+Cj4+Ci9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKNCAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL0xlbmd0aCA0NAo+PgpzdHJlYW0KQlQKL0YgMTIgVGYKMTAwIDcwMCBUZAooSGlnaGxhbmQgVG93ZXIgRGV2ZWxvcG1lbnQpIFRqCkVUCmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDA5IDAwMDAwIG4gCjAwMDAwMDAwNTggMDAwMDAgbiAKMDAwMDAwMDExNSAwMDAwMCBuIAowMDAwMDAwMjQ1IDAwMDAwIG4gCjAwMDAwMDAzMjMgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA2Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgo0MTYKJSVFT0Y=";
                return atob(samplePdfBase64);
            }}
        </script>
    </body>
    </html>
    """