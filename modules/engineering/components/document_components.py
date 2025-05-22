"""
Document Library components for the Engineering module.

This module provides the UI components for document management including:
- Document list view
- Document details view
- Document upload/edit form
- Document analysis
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go
import os

# Sample data for demonstration
def generate_sample_documents():
    """Generate sample document data for demonstration"""
    document_types = ["Drawing", "Specification", "Manual", "Report", "Contract", "Permit", "Certificate"]
    categories = ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "General"]
    statuses = ["Active", "Superseded", "Pending Review", "Archived"]
    
    documents = []
    
    for i in range(1, 30):
        # Generate random dates within a reasonable range
        date_added = datetime.now() - timedelta(days=random.randint(1, 180))
        
        # Some documents have revisions
        revision_count = random.randint(0, 5)
        
        # Status is more likely to be active for newer documents
        days_old = (datetime.now() - date_added).days
        if days_old < 30:
            status_weights = [0.8, 0.05, 0.15, 0.0]  # weights for statuses
        elif days_old < 90:
            status_weights = [0.6, 0.2, 0.1, 0.1]
        else:
            status_weights = [0.4, 0.3, 0.1, 0.2]
        
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        
        # Random document type and category
        doc_type = random.choice(document_types)
        category = random.choice(categories)
        
        # Format dates as strings for display
        date_added_str = date_added.strftime("%Y-%m-%d")
        
        # Generate last modified date - either same as added or later
        if revision_count > 0:
            last_modified = date_added + timedelta(days=random.randint(1, min(days_old, 60)))
            last_modified_str = last_modified.strftime("%Y-%m-%d")
        else:
            last_modified_str = date_added_str
        
        # Generate file size between 100 KB and 30 MB
        file_size = random.randint(100, 30000)
        if file_size < 1000:
            file_size_str = f"{file_size} KB"
        else:
            file_size_str = f"{file_size/1000:.1f} MB"
        
        # Create document record
        document = {
            "ID": f"DOC-{i:03d}",
            "Title": generate_document_title(doc_type, category),
            "Type": doc_type,
            "Category": category,
            "Status": status,
            "Revision": f"Rev {chr(65 + revision_count)}" if revision_count > 0 else "Rev A",
            "Date_Added": date_added_str,
            "Last_Modified": last_modified_str,
            "File_Size": file_size_str,
            "Added_By": random.choice(["J. Smith", "L. Johnson", "A. Martinez", "K. Wong", "S. Davis"]),
            "File_Format": generate_file_format(doc_type)
        }
        
        documents.append(document)
    
    return documents

def generate_document_title(doc_type, category):
    """Generate a realistic document title based on type and category"""
    if doc_type == "Drawing":
        drawing_types = {
            "Architectural": ["Floor Plan", "Elevation", "Section", "Detail", "Ceiling Plan", "Wall Section"],
            "Structural": ["Foundation Plan", "Framing Plan", "Connection Details", "Reinforcement", "Structural Details"],
            "Mechanical": ["HVAC Plan", "Ductwork Layout", "Equipment Schedule", "System Diagram", "Control Diagram"],
            "Electrical": ["Power Plan", "Lighting Plan", "Single Line Diagram", "Panel Schedule", "Riser Diagram"],
            "Plumbing": ["Plumbing Plan", "Riser Diagram", "Fixture Schedule", "Isometric View", "Detail"],
            "Civil": ["Site Plan", "Grading Plan", "Utility Plan", "Erosion Control", "Stormwater Management"],
            "General": ["Key Plan", "General Notes", "Legends and Symbols", "Phasing Plan", "Coordination Plan"]
        }
        
        drawing_type = random.choice(drawing_types.get(category, drawing_types["General"]))
        level = random.choice(["Level 1", "Level 2", "Level 3", "Basement", "Roof", "All Levels"])
        
        return f"{category} {drawing_type} - {level}"
        
    elif doc_type == "Specification":
        spec_sections = {
            "Architectural": ["08 11 13 - Hollow Metal Doors and Frames", "09 29 00 - Gypsum Board", 
                             "09 51 23 - Acoustical Tile Ceilings", "09 65 13 - Resilient Base and Accessories"],
            "Structural": ["03 30 00 - Cast-in-Place Concrete", "05 12 00 - Structural Steel Framing",
                          "05 50 00 - Metal Fabrications", "03 20 00 - Concrete Reinforcing"],
            "Mechanical": ["23 05 00 - Common Work Results for HVAC", "23 09 23 - Direct Digital Control",
                          "23 31 13 - Metal Ducts", "23 73 13 - Modular Indoor Central-Station Air-Handling Units"],
            "Electrical": ["26 05 19 - Low-Voltage Electrical Power Conductors", "26 24 16 - Panelboards",
                          "26 51 00 - Interior Lighting", "27 15 00 - Communications Horizontal Cabling"],
            "Plumbing": ["22 05 23 - General-Duty Valves for Plumbing", "22 11 16 - Domestic Water Piping",
                        "22 13 16 - Sanitary Waste and Vent Piping", "22 42 00 - Commercial Plumbing Fixtures"],
            "Civil": ["31 20 00 - Earth Moving", "32 12 16 - Asphalt Paving", 
                     "33 41 00 - Storm Utility Drainage Piping", "31 25 00 - Erosion and Sedimentation Controls"],
            "General": ["01 33 00 - Submittal Procedures", "01 77 00 - Closeout Procedures",
                       "01 78 39 - Project Record Documents", "01 91 13 - General Commissioning Requirements"]
        }
        
        return random.choice(spec_sections.get(category, spec_sections["General"]))
        
    elif doc_type == "Manual":
        manual_types = ["Operation and Maintenance", "Installation", "User", "Safety", "Training"]
        component = f"{category} Equipment"
        
        return f"{manual_types[random.randint(0, len(manual_types)-1)]} Manual - {component}"
        
    elif doc_type == "Report":
        report_types = ["Inspection", "Progress", "Testing", "Quality Control", "Environmental", "Safety", "Engineering"]
        report_type = report_types[random.randint(0, len(report_types)-1)]
        
        return f"{category} {report_type} Report - {datetime.now().strftime('%B %Y')}"
        
    elif doc_type == "Contract":
        contract_types = ["Owner-Contractor Agreement", "Subcontract", "Purchase Order", 
                         "Change Order", "Professional Services", "General Conditions"]
        
        return f"{contract_types[random.randint(0, len(contract_types)-1)]} - {category} Scope"
        
    elif doc_type == "Permit":
        permit_types = ["Building", "Electrical", "Mechanical", "Plumbing", "Excavation", 
                       "Demolition", "Fire Protection", "Occupancy"]
        
        return f"{permit_types[random.randint(0, len(permit_types)-1)]} Permit"
        
    elif doc_type == "Certificate":
        cert_types = ["Compliance", "Substantial Completion", "Occupancy", 
                     "Material", "Equipment", "Testing", "Insurance"]
        
        return f"Certificate of {cert_types[random.randint(0, len(cert_types)-1)]} - {category}"
        
    else:
        return f"{category} {doc_type} - {random.randint(1000, 9999)}"

def generate_file_format(doc_type):
    """Generate a realistic file format based on document type"""
    if doc_type == "Drawing":
        return random.choice(["PDF", "DWG", "RVT", "DGN", "PDF"])
    elif doc_type == "Specification":
        return random.choice(["PDF", "DOC", "DOCX", "PDF"])
    elif doc_type == "Manual":
        return random.choice(["PDF", "DOC", "DOCX", "PDF"])
    elif doc_type == "Report":
        return random.choice(["PDF", "DOC", "DOCX", "XLS", "XLSX", "PDF"])
    elif doc_type == "Contract":
        return random.choice(["PDF", "DOC", "DOCX", "PDF"])
    elif doc_type == "Permit":
        return "PDF"
    elif doc_type == "Certificate":
        return "PDF"
    else:
        return random.choice(["PDF", "DOC", "XLS", "JPG", "PNG", "ZIP"])

def render_document_list():
    """Render the document library list view with filtering and sorting"""
    st.subheader("Document Library")
    
    # Get sample data
    documents = generate_sample_documents()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Document type filter
            doc_types = ["All Types"] + sorted(list(set(doc["Type"] for doc in documents)))
            selected_type = st.selectbox("Document Type", doc_types, key="doc_type_filter")
            
            # Category filter
            categories = ["All Categories"] + sorted(list(set(doc["Category"] for doc in documents)))
            selected_category = st.selectbox("Category", categories, key="doc_category_filter")
        
        with col2:
            # Status filter
            statuses = ["All Statuses"] + sorted(list(set(doc["Status"] for doc in documents)))
            selected_status = st.selectbox("Status", statuses, key="doc_status_filter")
            
            # File format filter
            formats = ["All Formats"] + sorted(list(set(doc["File_Format"] for doc in documents)))
            selected_format = st.selectbox("File Format", formats, key="doc_format_filter")
        
        with col3:
            # Date range filter
            min_date = min(datetime.strptime(doc["Date_Added"], "%Y-%m-%d") for doc in documents)
            max_date = max(datetime.strptime(doc["Last_Modified"], "%Y-%m-%d") for doc in documents)
            
            start_date = st.date_input(
                "From Date",
                value=min_date,
                key="doc_start_date"
            )
            
            end_date = st.date_input(
                "To Date",
                value=max_date,
                key="doc_end_date"
            )
            
            # Search field
            search_term = st.text_input("Search", key="doc_search", placeholder="Search documents...")
    
    # Filter the data based on selections
    filtered_docs = documents
    
    # Filter by document type
    if selected_type != "All Types":
        filtered_docs = [doc for doc in filtered_docs if doc["Type"] == selected_type]
    
    # Filter by category
    if selected_category != "All Categories":
        filtered_docs = [doc for doc in filtered_docs if doc["Category"] == selected_category]
    
    # Filter by status
    if selected_status != "All Statuses":
        filtered_docs = [doc for doc in filtered_docs if doc["Status"] == selected_status]
    
    # Filter by file format
    if selected_format != "All Formats":
        filtered_docs = [doc for doc in filtered_docs if doc["File_Format"] == selected_format]
    
    # Filter by date range (use last modified date)
    filtered_docs = [
        doc for doc in filtered_docs 
        if start_date <= datetime.strptime(doc["Last_Modified"], "%Y-%m-%d").date() <= end_date
    ]
    
    # Filter by search term
    if search_term:
        filtered_docs = [doc for doc in filtered_docs if 
                        search_term.lower() in doc["ID"].lower() or
                        search_term.lower() in doc["Title"].lower() or
                        search_term.lower() in doc["Type"].lower() or
                        search_term.lower() in doc["Category"].lower()]
    
    # Layout for action buttons
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        # Show item count
        st.caption(f"Showing {len(filtered_docs)} documents")
    
    with col2:
        # Upload button (for adding new documents)
        if st.button("⬆️ Upload", use_container_width=True):
            st.session_state.document_view = "add"
            st.rerun()
    
    # Analysis button
    if st.button("📊 View Analysis", use_container_width=True, key="view_analysis_documents"):
        st.session_state.document_view = "analysis"
        st.rerun()
    
    # Check if we have any results
    if not filtered_docs:
        st.info("No documents match your filters.")
        return
    
    # Add sorting options
    sort_options = {
        "Last Modified (Newest First)": lambda x: datetime.strptime(x["Last_Modified"], "%Y-%m-%d"),
        "Last Modified (Oldest First)": lambda x: datetime.strptime(x["Last_Modified"], "%Y-%m-%d"),
        "Title (A-Z)": lambda x: x["Title"],
        "Title (Z-A)": lambda x: x["Title"],
        "Document Type": lambda x: x["Type"],
        "Category": lambda x: x["Category"]
    }
    
    sort_by = st.selectbox(
        "Sort by:",
        list(sort_options.keys()),
        index=0,
        key="doc_sort_by"
    )
    
    # Apply sorting
    reverse_sort = False
    if sort_by == "Last Modified (Oldest First)" or sort_by == "Title (Z-A)":
        reverse_sort = True
    
    filtered_docs = sorted(filtered_docs, key=sort_options[sort_by], reverse=reverse_sort)
    
    # Display the filtered documents
    for doc in filtered_docs:
        # Create a container for each document
        doc_container = st.container()
        
        with doc_container:
            # Add a subtle divider between documents
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the document data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([1, 2, 1.5, 1.5, 0.5])
            
            with col1:
                # Document type and ID
                doc_icons = {
                    "Drawing": "📐",
                    "Specification": "📋",
                    "Manual": "📘",
                    "Report": "📊",
                    "Contract": "📜",
                    "Permit": "🔖",
                    "Certificate": "🎓"
                }
                
                st.write(f"{doc_icons.get(doc['Type'], '📄')} **{doc['ID']}**")
                
                # Status indicator with colored badge
                status_colors = {
                    "Active": "🟢",
                    "Superseded": "🟠",
                    "Pending Review": "🟡",
                    "Archived": "⚪"
                }
                
                st.caption(f"{status_colors.get(doc['Status'], '⚪')} {doc['Status']}")
            
            with col2:
                st.write(f"**{doc['Title']}**")
                st.caption(f"Format: {doc['File_Format']} | Size: {doc['File_Size']}")
            
            with col3:
                # Category and revision information
                st.write(f"**Category:** {doc['Category']}")
                st.caption(f"Revision: {doc['Revision']}")
            
            with col4:
                # Date information
                st.write(f"**Modified:** {doc['Last_Modified']}")
                st.caption(f"Added: {doc['Date_Added']} by {doc['Added_By']}")
            
            # Action buttons in a single column
            with col_actions:
                # Create buttons stacked in the actions column
                if st.button("👁️", key=f"view_{doc['ID']}", help="View document details"):
                    # Store document details in session state
                    st.session_state.selected_document_id = doc['ID'] 
                    st.session_state.selected_document_data = doc
                    # Set view mode
                    st.session_state["document_view"] = "view"
                    # Force refresh
                    st.rerun()
                
                if st.button("⬇️", key=f"download_{doc['ID']}", help="Download document"):
                    # This would trigger a download in a real app
                    st.toast(f"Downloading {doc['Title']} ({doc['File_Format']})")
                
                if st.button("✏️", key=f"edit_{doc['ID']}", help="Edit document metadata"):
                    # Store document data for editing
                    st.session_state.edit_document_id = doc['ID']
                    st.session_state.edit_document_data = doc
                    # Set edit mode 
                    st.session_state["document_view"] = "edit"
                    # Force refresh
                    st.rerun()

def render_document_details():
    """Render the document details view (single document view)"""
    st.subheader("Document Details")
    
    # Ensure we have a selected document
    if not st.session_state.get("selected_document_id"):
        st.error("No document selected. Please select a document from the library.")
        # Return to list view
        st.session_state.document_view = "list"
        st.rerun()
        return
    
    # Get the selected document data
    doc = st.session_state.get("selected_document_data", None)
    
    if not doc:
        # If somehow we have an ID but no data, try to find it
        docs = generate_sample_documents()
        doc = next((d for d in docs if d["ID"] == st.session_state.selected_document_id), None)
        
        if not doc:
            st.error(f"Document with ID {st.session_state.selected_document_id} not found.")
            # Return to list view
            st.session_state.document_view = "list"
            st.rerun()
            return
    
    # Display document details
    with st.container():
        # Document header with type icon
        doc_icons = {
            "Drawing": "📐",
            "Specification": "📋",
            "Manual": "📘",
            "Report": "📊",
            "Contract": "📜",
            "Permit": "🔖",
            "Certificate": "🎓"
        }
        
        # Header with document title
        st.markdown(f"## {doc_icons.get(doc['Type'], '📄')} {doc['Title']}")
        
        # Create columns for basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Status indicator
            status_colors = {
                "Active": "🟢",
                "Superseded": "🟠",
                "Pending Review": "🟡",
                "Archived": "⚪"
            }
            
            status_bg_color = {
                "Active": "#D1FAE5",  # Light green
                "Superseded": "#FFEDD5",  # Light orange
                "Pending Review": "#FEF3C7",  # Light yellow
                "Archived": "#F3F4F6"   # Light gray
            }
            
            st.markdown(
                f"<div style='background-color: {status_bg_color.get(doc['Status'], '#F3F4F6')}; padding: 8px; border-radius: 4px;'>"
                f"<strong>Status:</strong> {status_colors.get(doc['Status'], '⚪')} {doc['Status']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>ID:</strong> {doc['ID']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>Type:</strong> {doc['Type']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>Category:</strong> {doc['Category']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Document details section
        st.markdown("### Document Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**File Format:** {doc['File_Format']}")
            st.markdown(f"**File Size:** {doc['File_Size']}")
            st.markdown(f"**Revision:** {doc['Revision']}")
        
        with col2:
            st.markdown(f"**Date Added:** {doc['Date_Added']}")
            st.markdown(f"**Last Modified:** {doc['Last_Modified']}")
            st.markdown(f"**Added By:** {doc['Added_By']}")
        
        # Document preview (placeholder)
        st.markdown("### Document Preview")
        
        # Different preview based on document type
        if doc['File_Format'] in ['PDF', 'DOC', 'DOCX', 'XLS', 'XLSX']:
            st.info("Document preview not available in this view. Please download the document to view.")
        elif doc['File_Format'] in ['JPG', 'PNG', 'GIF']:
            # Image placeholder
            st.image("https://via.placeholder.com/800x400?text=Image+Preview", caption="Document Preview")
        elif doc['File_Format'] in ['DWG', 'RVT', 'DGN']:
            st.info("CAD/BIM file preview not available. Please open in appropriate software.")
        else:
            st.info("Preview not available for this file type.")
        
        # Revision history (simulated)
        st.markdown("### Revision History")
        
        # Get revision letter from "Rev X" format
        current_rev = doc['Revision'].split(' ')[1]
        
        # Create revision history starting from Rev A to current
        revisions = []
        
        for i in range(ord('A'), ord(current_rev) + 1):
            rev_letter = chr(i)
            
            # Earlier dates for earlier revisions
            days_back = (ord(current_rev) - i) * random.randint(10, 30)
            rev_date = datetime.strptime(doc['Last_Modified'], "%Y-%m-%d") - timedelta(days=days_back)
            
            if i == ord(current_rev):  # Current revision
                rev_date = datetime.strptime(doc['Last_Modified'], "%Y-%m-%d")
            
            revisions.append({
                "Revision": f"Rev {rev_letter}",
                "Date": rev_date.strftime("%Y-%m-%d"),
                "Modified By": random.choice(["J. Smith", "L. Johnson", "A. Martinez", "K. Wong", "S. Davis"]),
                "Comments": generate_revision_comment(doc['Type'], rev_letter)
            })
        
        # Sort by revision letter in descending order (newest first)
        revisions.sort(key=lambda x: x["Revision"], reverse=True)
        
        # Create a dataframe for display
        revision_df = pd.DataFrame(revisions)
        
        # Display the revision history
        st.dataframe(revision_df, use_container_width=True)
        
        # Document references (related documents)
        st.markdown("### Related Documents")
        
        # Generate some random related documents
        has_related = random.choice([True, False])
        
        if has_related:
            related_count = random.randint(1, 3)
            related_docs = []
            
            # Get all documents excluding the current one
            all_docs = [d for d in generate_sample_documents() if d['ID'] != doc['ID']]
            
            # Pick random related documents
            for i in range(min(related_count, len(all_docs))):
                related_doc = random.choice(all_docs)
                all_docs.remove(related_doc)  # Remove to avoid duplicates
                
                related_docs.append({
                    "ID": related_doc['ID'],
                    "Title": related_doc['Title'],
                    "Type": related_doc['Type'],
                    "Relationship": random.choice(["Referenced", "Supersedes", "Supplement", "Attachment", "Similar"])
                })
            
            # Create a dataframe for display
            related_df = pd.DataFrame(related_docs)
            
            # Display the related documents
            st.dataframe(related_df, use_container_width=True)
        else:
            st.info("No related documents found.")
        
        # Action buttons at the bottom
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬇️ Download Document", use_container_width=True):
                # This would trigger a download in a real app
                st.toast(f"Downloading {doc['Title']} ({doc['File_Format']})")
        
        with col2:
            if st.button("✏️ Edit Metadata", use_container_width=True):
                st.session_state.edit_document_id = doc['ID']
                st.session_state.edit_document_data = doc
                st.session_state.document_view = "edit"
                st.rerun()
        
        with col3:
            if st.button("🔄 Upload New Revision", use_container_width=True):
                st.session_state.document_view = "add"
                st.session_state.is_revision = True
                st.session_state.revision_document_id = doc['ID']
                st.rerun()

def generate_revision_comment(doc_type, rev_letter):
    """Generate a realistic revision comment based on document type and revision letter"""
    if rev_letter == 'A':
        return "Initial issue"
    
    # Common revision comments by document type
    comments = {
        "Drawing": [
            "Updated dimensions",
            "Revised details",
            "Corrected annotations",
            "Added section views",
            "Updated to reflect site conditions",
            "Coordination with other disciplines",
            "Added construction details"
        ],
        "Specification": [
            "Updated product requirements",
            "Revised execution section",
            "Added quality assurance requirements",
            "Updated references",
            "Clarified material options",
            "Added sustainable requirements"
        ],
        "Manual": [
            "Updated operating procedures",
            "Added troubleshooting section",
            "Revised maintenance schedule",
            "Updated contact information",
            "Added safety warnings"
        ],
        "Report": [
            "Updated findings",
            "Revised conclusions",
            "Added supplemental data",
            "Corrected calculations",
            "Updated recommendations"
        ],
        "Contract": [
            "Updated scope of work",
            "Revised payment terms",
            "Added schedule milestones",
            "Clarified responsibilities",
            "Updated insurance requirements"
        ],
        "Permit": [
            "Updated to address feedback",
            "Corrected application information",
            "Added supporting documentation",
            "Revised calculations"
        ],
        "Certificate": [
            "Updated information",
            "Corrected errors",
            "Renewed certification",
            "Added endorsements"
        ]
    }
    
    # Get comments for this document type or use general comments
    type_comments = comments.get(doc_type, [
        "Updated content",
        "Corrected errors",
        "Added information",
        "Revised per feedback",
        "Modified content"
    ])
    
    return random.choice(type_comments)

def render_document_form(is_edit=False):
    """Render the document creation/edit form"""
    if is_edit:
        st.subheader("Edit Document Metadata")
        # Ensure we have a document to edit
        if not st.session_state.get("edit_document_id"):
            st.error("No document selected for editing. Please select a document from the library.")
            # Return to list view
            st.session_state.document_view = "list"
            st.rerun()
            return
        
        # Get the document data for editing
        doc = st.session_state.get("edit_document_data", {})
    else:
        if st.session_state.get("is_revision", False):
            st.subheader("Upload New Document Revision")
            # Get the original document data for reference
            original_doc_id = st.session_state.get("revision_document_id")
            docs = generate_sample_documents()
            original_doc = next((d for d in docs if d["ID"] == original_doc_id), None)
            
            if original_doc:
                doc = original_doc.copy()
                # Increment the revision letter
                current_rev = doc['Revision'].split(' ')[1]
                next_rev = chr(ord(current_rev) + 1)
                doc['Revision'] = f"Rev {next_rev}"
            else:
                # If original doc not found, create new
                st.warning("Original document not found. Creating new document instead.")
                doc = initialize_new_document()
        else:
            st.subheader("Upload New Document")
            # Initialize empty document for new entries
            doc = initialize_new_document()
    
    # Create the form
    with st.form(key="document_form"):
        # Basic information
        st.subheader("Document Information")
        col1, col2 = st.columns(2)
        
        with col1:
            # For display only in edit mode
            if is_edit:
                st.text_input("Document ID", value=doc.get("ID", ""), disabled=True)
            
            title = st.text_input("Title *", value=doc.get("Title", ""))
            
            # Document type
            doc_types = ["Drawing", "Specification", "Manual", "Report", "Contract", "Permit", "Certificate", "Other"]
            
            # Find index of selected type if editing
            type_index = 0
            if is_edit and doc.get("Type") in doc_types:
                type_index = doc_types.index(doc.get("Type"))
            
            selected_type = st.selectbox(
                "Document Type *",
                doc_types,
                index=type_index
            )
        
        with col2:
            # Categories
            categories = ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "General"]
            
            # Find index of selected category if editing
            category_index = 0
            if is_edit and doc.get("Category") in categories:
                category_index = categories.index(doc.get("Category"))
            
            selected_category = st.selectbox(
                "Category *",
                categories,
                index=category_index
            )
            
            # Status options
            statuses = ["Active", "Superseded", "Pending Review", "Archived"]
            
            # Find index of selected status if editing
            status_index = 0
            if is_edit and doc.get("Status") in statuses:
                status_index = statuses.index(doc.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                statuses,
                index=status_index
            )
        
        # Document details
        st.subheader("Document Details")
        col1, col2 = st.columns(2)
        
        with col1:
            # Revision
            revision = st.text_input(
                "Revision *",
                value=doc.get("Revision", "Rev A"),
                placeholder="e.g., Rev A"
            )
            
            # Added by
            added_by = st.text_input(
                "Added By *",
                value=doc.get("Added_By", ""),
                placeholder="Name of person uploading"
            )
        
        with col2:
            # File format
            file_formats = [
                "PDF", "DOC", "DOCX", "XLS", "XLSX", "DWG", "RVT", "DGN", 
                "JPG", "PNG", "TIF", "ZIP", "Other"
            ]
            
            # Find index of selected format if editing
            format_index = 0
            if is_edit and doc.get("File_Format") in file_formats:
                format_index = file_formats.index(doc.get("File_Format"))
            
            selected_format = st.selectbox(
                "File Format *",
                file_formats,
                index=format_index
            )
            
            # Dates in edit mode
            if is_edit:
                # Format date string for date_input
                last_modified = datetime.strptime(doc.get("Last_Modified", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                
                last_modified_date = st.date_input(
                    "Last Modified *",
                    value=last_modified
                )
            else:
                last_modified_date = datetime.now().date()
        
        # Description (optional)
        description = st.text_area(
            "Description",
            value=doc.get("Description", ""),
            height=100,
            placeholder="Optional description of the document..."
        )
        
        # File upload (only for new documents or new revisions)
        if not is_edit:
            uploaded_file = st.file_uploader(
                "Upload Document *", 
                type=["pdf", "doc", "docx", "xls", "xlsx", "dwg", "jpg", "png", "zip"]
            )
        
        # References (Related Documents)
        st.subheader("Document References")
        
        # Get all documents excluding this one if editing
        all_docs = []
        if is_edit:
            all_docs = [d for d in generate_sample_documents() if d['ID'] != doc['ID']]
        else:
            all_docs = generate_sample_documents()
        
        # Create a list of document IDs and titles for the multiselect
        doc_options = [f"{d['ID']} - {d['Title']}" for d in all_docs]
        
        related_docs = st.multiselect(
            "Related Documents",
            options=doc_options,
            default=[],
            help="Select any documents that are related to this one"
        )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Document" if is_edit else "Upload Document",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not title:
            st.error("Please enter a title.")
            return
        
        if not revision:
            st.error("Please enter a revision.")
            return
        
        if not added_by:
            st.error("Please enter who added this document.")
            return
        
        # Validate file upload for new documents
        if not is_edit and not uploaded_file:
            st.error("Please upload a document file.")
            return
        
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Document {doc['ID']} updated successfully!")
        else:
            st.success(f"Document uploaded successfully!")
        
        # Clear revision flag if set
        if st.session_state.get("is_revision", False):
            st.session_state.is_revision = False
            st.session_state.revision_document_id = None
        
        # Return to list view
        st.session_state.document_view = "list"
        st.rerun()
    
    if cancel_button:
        # Clear revision flag if set
        if st.session_state.get("is_revision", False):
            st.session_state.is_revision = False
            st.session_state.revision_document_id = None
        
        # Return to previous view
        if is_edit and st.session_state.get("selected_document_id") == st.session_state.get("edit_document_id"):
            # If editing from detail view, return to detail view
            st.session_state.document_view = "view"
        else:
            # Otherwise return to list view
            st.session_state.document_view = "list"
        
        st.rerun()

def initialize_new_document():
    """Initialize a new empty document with default values"""
    return {
        "ID": f"DOC-{random.randint(100, 999)}",
        "Title": "",
        "Type": "Drawing",
        "Category": "General",
        "Status": "Active",
        "Revision": "Rev A",
        "Date_Added": datetime.now().strftime("%Y-%m-%d"),
        "Last_Modified": datetime.now().strftime("%Y-%m-%d"),
        "File_Size": "",
        "Added_By": "",
        "File_Format": "PDF",
        "Description": ""
    }

def render_document_analysis():
    """Render the document analysis view with charts and metrics"""
    st.subheader("Document Library Analysis")
    
    # Get sample data
    documents = generate_sample_documents()
    
    # Calculate summary metrics
    total_documents = len(documents)
    active_documents = sum(1 for doc in documents if doc["Status"] == "Active")
    superseded_documents = sum(1 for doc in documents if doc["Status"] == "Superseded")
    pending_documents = sum(1 for doc in documents if doc["Status"] == "Pending Review")
    archived_documents = sum(1 for doc in documents if doc["Status"] == "Archived")
    
    # Calculate average file size
    file_sizes = []
    for doc in documents:
        size_str = doc["File_Size"]
        if "KB" in size_str:
            size_kb = float(size_str.split()[0])
            file_sizes.append(size_kb)
        elif "MB" in size_str:
            size_mb = float(size_str.split()[0])
            size_kb = size_mb * 1000
            file_sizes.append(size_kb)
    
    avg_file_size = sum(file_sizes) / len(file_sizes) if file_sizes else 0
    total_size = sum(file_sizes)
    
    # Format the sizes for display
    if avg_file_size < 1000:
        avg_size_str = f"{avg_file_size:.1f} KB"
    else:
        avg_size_str = f"{avg_file_size/1000:.1f} MB"
        
    if total_size < 1000:
        total_size_str = f"{total_size:.1f} KB"
    else:
        total_size_str = f"{total_size/1000:.1f} MB"
    
    # Summary metrics in a nice grid
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", f"{total_documents}")
    
    with col2:
        st.metric("Active Documents", f"{active_documents}", delta=f"{active_documents/total_documents:.0%}")
    
    with col3:
        st.metric("Average File Size", avg_size_str)
    
    with col4:
        st.metric("Total Storage", total_size_str)
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Document Types", "Status & Activity", "Revisions"])
    
    # Tab 1: Document Types Analysis
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Document type breakdown
            type_counts = {}
            for doc in documents:
                doc_type = doc["Type"]
                type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
            
            type_df = pd.DataFrame({
                'Document Type': list(type_counts.keys()),
                'Count': list(type_counts.values())
            })
            
            # Sort by count
            type_df = type_df.sort_values('Count', ascending=False)
            
            # Create Plotly pie chart
            fig = px.pie(
                type_df, 
                values='Count', 
                names='Document Type',
                title='Document Type Distribution',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown
            category_counts = {}
            for doc in documents:
                category = doc["Category"]
                category_counts[category] = category_counts.get(category, 0) + 1
            
            category_df = pd.DataFrame({
                'Category': list(category_counts.keys()),
                'Count': list(category_counts.values())
            })
            
            # Sort by count
            category_df = category_df.sort_values('Count', ascending=False)
            
            # Create bar chart
            fig = px.bar(
                category_df, 
                x='Category', 
                y='Count',
                title='Document Category Distribution',
                color='Count',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # File format breakdown
        st.subheader("File Format Distribution")
        
        format_counts = {}
        for doc in documents:
            file_format = doc["File_Format"]
            format_counts[file_format] = format_counts.get(file_format, 0) + 1
        
        format_df = pd.DataFrame({
            'File Format': list(format_counts.keys()),
            'Count': list(format_counts.values())
        })
        
        # Sort by count
        format_df = format_df.sort_values('Count', ascending=False)
        
        # Create bar chart with horizontal orientation
        fig = px.bar(
            format_df, 
            y='File Format', 
            x='Count',
            title='File Format Distribution',
            orientation='h',
            color='Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Status & Activity Analysis
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Status breakdown
            status_counts = {
                'Active': active_documents,
                'Superseded': superseded_documents,
                'Pending Review': pending_documents,
                'Archived': archived_documents
            }
            
            status_df = pd.DataFrame({
                'Status': list(status_counts.keys()),
                'Count': list(status_counts.values())
            })
            
            # Create Plotly pie chart
            fig = px.pie(
                status_df, 
                values='Count', 
                names='Status',
                title='Document Status Distribution',
                color='Status',
                color_discrete_map={
                    'Active': '#10B981',       # Green
                    'Superseded': '#F59E0B',   # Amber
                    'Pending Review': '#FBBF24',  # Yellow
                    'Archived': '#9CA3AF'      # Gray
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Document activity over time
            # Prepare data for trend analysis
            activity_data = []
            for doc in documents:
                date_added = datetime.strptime(doc["Date_Added"], "%Y-%m-%d")
                activity_data.append({
                    'Date': date_added,
                    'Type': 'Added',
                    'Document Type': doc['Type']
                })
                
                last_modified = datetime.strptime(doc["Last_Modified"], "%Y-%m-%d")
                if last_modified > date_added:
                    activity_data.append({
                        'Date': last_modified,
                        'Type': 'Modified',
                        'Document Type': doc['Type']
                    })
            
            # Convert to DataFrame
            activity_df = pd.DataFrame(activity_data)
            
            # Group by month and type
            activity_df['Month'] = activity_df['Date'].dt.strftime('%Y-%m')
            activity_by_month = activity_df.groupby(['Month', 'Type']).size().reset_index(name='Count')
            
            # Create stacked bar chart
            fig = px.bar(
                activity_by_month, 
                x='Month', 
                y='Count',
                color='Type',
                title='Document Activity by Month',
                barmode='stack',
                color_discrete_map={
                    'Added': '#3B82F6',    # Blue
                    'Modified': '#8B5CF6'  # Purple
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Status by document type
        st.subheader("Status by Document Type")
        
        # Create a cross-tabulation of status and type
        status_type = []
        for doc in documents:
            status_type.append({
                'Status': doc['Status'],
                'Document Type': doc['Type']
            })
        
        # Create DataFrame
        st_df = pd.DataFrame(status_type)
        
        # Create a pivot table
        pivot_table = pd.crosstab(st_df['Document Type'], st_df['Status'])
        
        # Create stacked bar chart
        fig = px.bar(
            pivot_table, 
            barmode='stack',
            title='Document Status by Type',
            color_discrete_map={
                'Active': '#10B981',       # Green
                'Superseded': '#F59E0B',   # Amber
                'Pending Review': '#FBBF24',  # Yellow
                'Archived': '#9CA3AF'      # Gray
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Revisions Analysis
    with tab3:
        # Count revisions per document
        revision_counts = {}
        for doc in documents:
            revision = doc["Revision"]
            if "Rev " in revision:
                rev_letter = revision.split(' ')[1]
                rev_number = ord(rev_letter) - ord('A') + 1
                
                if rev_number in revision_counts:
                    revision_counts[rev_number] += 1
                else:
                    revision_counts[rev_number] = 1
        
        # Create DataFrame
        rev_df = pd.DataFrame({
            'Revision Count': list(revision_counts.keys()),
            'Number of Documents': list(revision_counts.values())
        })
        
        # Sort by revision count
        rev_df = rev_df.sort_values('Revision Count')
        
        # Calculate statistics
        total_revisions = sum(k * v for k, v in revision_counts.items())
        avg_revisions = total_revisions / total_documents
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Revisions", f"{total_revisions}")
        
        with col2:
            st.metric("Avg. Revisions per Document", f"{avg_revisions:.2f}")
        
        # Create bar chart for revision distribution
        fig = px.bar(
            rev_df, 
            x='Revision Count', 
            y='Number of Documents',
            title='Document Revision Distribution',
            text='Number of Documents',
            color='Number of Documents',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Revisions by document type
        st.subheader("Revisions by Document Type")
        
        # Calculate average revisions by document type
        type_revisions = {}
        type_counts = {}
        
        for doc in documents:
            doc_type = doc["Type"]
            revision = doc["Revision"]
            
            if "Rev " in revision:
                rev_letter = revision.split(' ')[1]
                rev_number = ord(rev_letter) - ord('A') + 1
                
                if doc_type in type_revisions:
                    type_revisions[doc_type] += rev_number
                    type_counts[doc_type] += 1
                else:
                    type_revisions[doc_type] = rev_number
                    type_counts[doc_type] = 1
        
        # Calculate averages
        avg_by_type = []
        for doc_type, rev_sum in type_revisions.items():
            count = type_counts[doc_type]
            avg_revisions = rev_sum / count
            
            avg_by_type.append({
                'Document Type': doc_type,
                'Average Revisions': avg_revisions,
                'Document Count': count
            })
        
        # Create DataFrame
        avg_type_df = pd.DataFrame(avg_by_type)
        
        # Sort by average revisions
        avg_type_df = avg_type_df.sort_values('Average Revisions', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            avg_type_df, 
            x='Document Type', 
            y='Average Revisions',
            title='Average Revisions by Document Type',
            color='Document Count',
            color_continuous_scale=px.colors.sequential.Viridis,
            text_auto='.2f'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)