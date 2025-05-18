"""
Closeout module for the gcPanel Construction Management Dashboard.

This module provides project closeout features including punch lists,
warranties, O&M manuals, and final documentation.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

def render_occupancy_permits():
    """Render the occupancy permits section"""
    
    st.header("Occupancy Permits & Final Inspections")
    
    # Add button for creating new permit/inspection record
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("Add New Permit/Inspection", type="primary", key="add_permit_btn"):
            st.session_state.show_permit_form = True
    
    # Add progress visualization
    progress_col1, progress_col2 = st.columns([1, 3])
    with progress_col1:
        st.markdown("### Overall Progress")
    with progress_col2:
        # Calculate progress percentage based on permit statuses
        approved_count = 2  # From our sample data
        total_count = 5     # From our sample data
        progress_pct = (approved_count / total_count) * 100
        
        # Display progress bar
        st.progress(progress_pct)
        st.markdown(f"**{progress_pct:.1f}% Complete** ({approved_count}/{total_count} permits approved)")
    
    # Add status visualization
    st.markdown("### Permit Status Overview")
    
    # Create sample data for the status chart
    status_data = {
        "Status": ["Approved", "Approved with Conditions", "Pending", "Scheduled", "Pending Corrections"],
        "Count": [1, 1, 1, 1, 1]
    }
    status_df = pd.DataFrame(status_data)
    
    # Define colors for the status chart
    status_colors = {
        "Approved": "#28a745",
        "Approved with Conditions": "#20c997",
        "Pending": "#6c757d",
        "Scheduled": "#17a2b8",
        "Pending Corrections": "#ffc107",
        "Rejected": "#dc3545"
    }
    
    # Create status chart
    fig = px.bar(
        status_df, 
        x="Status", 
        y="Count",
        color="Status",
        color_discrete_map=status_colors,
        title="Permit Status Distribution"
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Number of Permits",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sample permit data
    permits = [
        {
            "id": "PER-2025-001",
            "type": "Building Permit",
            "authority": "City of Seattle Building Department",
            "submission_date": datetime.now() - timedelta(days=90),
            "inspection_date": datetime.now() - timedelta(days=15),
            "status": "Approved",
            "inspector": "John Wilson",
            "conditions": "None",
            "expiration_date": datetime.now() + timedelta(days=365),
            "documents": ["Building_Permit.pdf", "Approval_Letter.pdf"],
            "notes": "Final approval received"
        },
        {
            "id": "PER-2025-002",
            "type": "Electrical Inspection",
            "authority": "Seattle Electrical Inspector",
            "submission_date": datetime.now() - timedelta(days=60),
            "inspection_date": datetime.now() - timedelta(days=10),
            "status": "Approved with Conditions",
            "inspector": "Sarah Johnson",
            "conditions": "Emergency lighting needs to be recertified in 30 days",
            "expiration_date": datetime.now() + timedelta(days=30),
            "documents": ["Electrical_Inspection_Report.pdf"],
            "notes": "Follow-up inspection scheduled"
        },
        {
            "id": "PER-2025-003",
            "type": "Fire Safety Inspection",
            "authority": "Seattle Fire Department",
            "submission_date": datetime.now() - timedelta(days=45),
            "inspection_date": datetime.now() - timedelta(days=5),
            "status": "Pending Corrections",
            "inspector": "Robert Chen",
            "conditions": "Sprinkler coverage in east stairwell needs adjustment",
            "expiration_date": None,
            "documents": ["Fire_Safety_Inspection_Report.pdf", "Correction_Notice.pdf"],
            "notes": "Reinspection scheduled for next week"
        },
        {
            "id": "PER-2025-004",
            "type": "Elevator Certification",
            "authority": "WA State Elevator Inspector",
            "submission_date": datetime.now() - timedelta(days=30),
            "inspection_date": datetime.now() - timedelta(days=2),
            "status": "Scheduled",
            "inspector": "Pending Assignment",
            "conditions": "N/A",
            "expiration_date": None,
            "documents": ["Elevator_Permit_Application.pdf"],
            "notes": "Initial inspection scheduled"
        },
        {
            "id": "PER-2025-005",
            "type": "Certificate of Occupancy",
            "authority": "City of Seattle Building Department",
            "submission_date": datetime.now() - timedelta(days=20),
            "inspection_date": None,
            "status": "Pending",
            "inspector": "Pending Assignment",
            "conditions": "All other inspections must be approved",
            "expiration_date": None,
            "documents": ["CO_Application.pdf"],
            "notes": "Awaiting final inspections completion"
        }
    ]
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Pending", "Scheduled", "Approved", "Approved with Conditions", "Pending Corrections", "Rejected"],
            default=["Pending", "Scheduled", "Pending Corrections"],
            key="permit_status_filter"
        )
    
    with col2:
        type_filter = st.multiselect(
            "Permit Type",
            list(set(permit["type"] for permit in permits)),
            default=[],
            key="permit_type_filter"
        )
    
    with col3:
        authority_filter = st.multiselect(
            "Authority",
            list(set(permit["authority"] for permit in permits)),
            default=[],
            key="permit_authority_filter"
        )
    
    # Apply filters
    filtered_permits = [permit for permit in permits if permit["status"] in status_filter]
    
    if type_filter:
        filtered_permits = [permit for permit in filtered_permits if permit["type"] in type_filter]
    
    if authority_filter:
        filtered_permits = [permit for permit in filtered_permits if permit["authority"] in authority_filter]
    
    # Permit metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_permits = len(permits)
        st.metric("Total Permits", total_permits)
    
    with metrics_col2:
        approved_permits = len([permit for permit in permits if permit["status"] in ["Approved", "Approved with Conditions"]])
        approved_pct = (approved_permits / total_permits) * 100 if total_permits > 0 else 0
        st.metric("Approved", f"{approved_permits} ({approved_pct:.1f}%)")
    
    with metrics_col3:
        pending_permits = len([permit for permit in permits if permit["status"] in ["Pending", "Scheduled", "Pending Corrections"]])
        st.metric("Pending", pending_permits)
    
    with metrics_col4:
        co_status = next((permit["status"] for permit in permits if permit["type"] == "Certificate of Occupancy"), "Not Started")
        st.metric("CO Status", co_status)
    
    # Permit list
    st.subheader("Permits and Inspections")
    
    # Show permit list as cards
    for permit in filtered_permits:
        # Determine status color
        if permit["status"] == "Approved":
            status_color = "#28a745"  # Green
        elif permit["status"] == "Approved with Conditions":
            status_color = "#20c997"  # Teal
        elif permit["status"] == "Pending":
            status_color = "#6c757d"  # Gray
        elif permit["status"] == "Scheduled":
            status_color = "#17a2b8"  # Cyan
        elif permit["status"] == "Pending Corrections":
            status_color = "#ffc107"  # Yellow
        else:  # Rejected
            status_color = "#dc3545"  # Red
        
        # Create card
        with st.expander(f"{permit['id']} - {permit['type']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Authority:** {permit['authority']}")
                st.markdown(f"**Submission Date:** {permit['submission_date'].strftime('%Y-%m-%d')}")
                
                if permit["inspection_date"]:
                    st.markdown(f"**Inspection Date:** {permit['inspection_date'].strftime('%Y-%m-%d')}")
                else:
                    st.markdown("**Inspection Date:** Not scheduled")
                
                st.markdown(f"**Inspector:** {permit['inspector']}")
            
            with col2:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{permit['status']}</span>", unsafe_allow_html=True)
                
                if permit["conditions"] and permit["conditions"] != "N/A" and permit["conditions"] != "None":
                    st.markdown(f"**Conditions:** {permit['conditions']}")
                
                if permit["expiration_date"]:
                    st.markdown(f"**Expiration Date:** {permit['expiration_date'].strftime('%Y-%m-%d')}")
            
            # Documents
            if permit["documents"]:
                st.markdown("**Documents:**")
                for doc in permit["documents"]:
                    st.markdown(f"- {doc}")
            
            # Notes
            if permit["notes"]:
                st.markdown(f"**Notes:** {permit['notes']}")
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if permit["status"] in ["Pending", "Pending Corrections"]:
                    st.button("Schedule Inspection", key=f"schedule_{permit['id']}")
                elif permit["status"] == "Scheduled":
                    st.button("Record Results", key=f"record_{permit['id']}")
            
            with buttons_col2:
                st.button("Edit", key=f"edit_{permit['id']}")
            
            with buttons_col3:
                st.button("Upload Document", key=f"upload_{permit['id']}")
    
    # Add permit form
    if st.session_state.get("show_permit_form", False):
        with st.form("permit_form"):
            st.subheader("Add Permit/Inspection")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                permit_type = st.selectbox(
                    "Permit Type", 
                    ["Building Permit", "Electrical Inspection", "Plumbing Inspection", 
                     "Fire Safety Inspection", "Elevator Certification", "Certificate of Occupancy",
                     "Mechanical Inspection", "Health Department Inspection", "Other"],
                    key="new_permit_type"
                )
                
                permit_authority = st.text_input("Authority", key="new_permit_authority")
                permit_submission = st.date_input("Submission Date", datetime.now(), key="new_permit_submission")
                
                permit_inspection = st.date_input(
                    "Inspection Date (if scheduled)", 
                    None,
                    key="new_permit_inspection"
                )
            
            with form_col2:
                permit_status = st.selectbox(
                    "Status", 
                    ["Pending", "Scheduled", "Approved", "Approved with Conditions", "Pending Corrections", "Rejected"],
                    key="new_permit_status"
                )
                
                permit_inspector = st.text_input("Inspector", key="new_permit_inspector")
                permit_conditions = st.text_area("Conditions", key="new_permit_conditions")
                
                if permit_status in ["Approved", "Approved with Conditions"]:
                    permit_expiration = st.date_input(
                        "Expiration Date (if applicable)", 
                        datetime.now() + timedelta(days=365),
                        key="new_permit_expiration"
                    )
            
            permit_notes = st.text_area("Notes", key="new_permit_notes")
            
            # Permit document upload
            st.file_uploader("Upload Documents", accept_multiple_files=True, key="new_permit_docs")
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_permit = st.form_submit_button("Save")
            with submit_col2:
                cancel_permit = st.form_submit_button("Cancel")
            
            if submit_permit:
                st.success("Permit added successfully")
                st.session_state.show_permit_form = False
                st.rerun()
            
            if cancel_permit:
                st.session_state.show_permit_form = False
                st.rerun()

def render_owner_training():
    """Render the owner training section"""
    
    st.header("Owner Training Documentation")
    
    # Add button for creating new training session
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("Add Training Session", type="primary", key="add_training_btn"):
            st.session_state.show_training_form = True
    
    # Sample training sessions
    training_sessions = [
        {
            "id": "TRN-2025-001",
            "system": "HVAC Systems",
            "trainer": "Johnson Controls",
            "date": datetime.now() - timedelta(days=15),
            "attendees": ["John Smith (Owner)", "Sarah Johnson (Building Manager)", "Technical Staff (3)"],
            "location": "Mechanical Room & Conference Room A",
            "duration": "4 hours",
            "materials": ["HVAC_User_Manual.pdf", "Maintenance_Schedule.pdf"],
            "videos": ["HVAC_Training_Session.mp4"],
            "signed_off": True,
            "notes": "Complete training provided on all HVAC systems"
        },
        {
            "id": "TRN-2025-002",
            "system": "Building Management System",
            "trainer": "SmartBuild Technologies",
            "date": datetime.now() - timedelta(days=10),
            "attendees": ["Sarah Johnson (Building Manager)", "IT Staff (2)"],
            "location": "Control Room & Online Session",
            "duration": "8 hours",
            "materials": ["BMS_Manual.pdf", "User_Guide.pdf", "Emergency_Procedures.pdf"],
            "videos": ["BMS_Training_Part1.mp4", "BMS_Training_Part2.mp4"],
            "signed_off": True,
            "notes": "Follow-up session scheduled for advanced features"
        },
        {
            "id": "TRN-2025-003",
            "system": "Fire Alarm & Sprinkler Systems",
            "trainer": "FireSafe Inc.",
            "date": datetime.now() - timedelta(days=5),
            "attendees": ["Sarah Johnson (Building Manager)", "Security Team (4)", "Maintenance Staff (2)"],
            "location": "Throughout Building",
            "duration": "6 hours",
            "materials": ["Fire_Safety_Manual.pdf", "Evacuation_Procedures.pdf"],
            "videos": ["Fire_System_Training.mp4"],
            "signed_off": True,
            "notes": "Complete training on all fire safety systems and procedures"
        },
        {
            "id": "TRN-2025-004",
            "system": "Elevator Systems",
            "trainer": "Otis Elevator Co.",
            "date": datetime.now() - timedelta(days=2),
            "attendees": ["Maintenance Staff (3)"],
            "location": "Elevator Machine Room",
            "duration": "3 hours",
            "materials": ["Elevator_Maintenance_Guide.pdf"],
            "videos": [],
            "signed_off": False,
            "notes": "Basic maintenance training provided, sign-off pending documentation review"
        },
        {
            "id": "TRN-2025-005",
            "system": "Security Systems",
            "trainer": "SecureView Systems",
            "date": datetime.now() + timedelta(days=7),
            "attendees": ["Security Team (4)", "Building Manager"],
            "location": "Security Office",
            "duration": "4 hours",
            "materials": ["Security_System_Manual.pdf"],
            "videos": [],
            "signed_off": False,
            "notes": "Session scheduled"
        }
    ]
    
    # Metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_sessions = len(training_sessions)
        st.metric("Total Sessions", total_sessions)
    
    with metrics_col2:
        completed_sessions = len([session for session in training_sessions if session["date"] < datetime.now()])
        st.metric("Completed", completed_sessions)
    
    with metrics_col3:
        signoff_sessions = len([session for session in training_sessions if session["signed_off"]])
        signoff_pct = (signoff_sessions / completed_sessions) * 100 if completed_sessions > 0 else 0
        st.metric("Signed Off", f"{signoff_sessions} ({signoff_pct:.1f}%)")
    
    with metrics_col4:
        scheduled_sessions = len([session for session in training_sessions if session["date"] > datetime.now()])
        st.metric("Scheduled", scheduled_sessions)
    
    # Training sessions list
    st.subheader("Training Sessions")
    
    # Sort by date
    training_sessions.sort(key=lambda x: x["date"], reverse=True)
    
    # Display sessions
    for session in training_sessions:
        # Determine status
        if session["date"] > datetime.now():
            status = "Scheduled"
            status_color = "#17a2b8"  # Cyan
        elif session["signed_off"]:
            status = "Completed & Signed Off"
            status_color = "#28a745"  # Green
        else:
            status = "Pending Sign-off"
            status_color = "#ffc107"  # Yellow
        
        # Create card
        with st.expander(f"{session['id']} - {session['system']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Trainer:** {session['trainer']}")
                st.markdown(f"**Date:** {session['date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Location:** {session['location']}")
                st.markdown(f"**Duration:** {session['duration']}")
            
            with col2:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{status}</span>", unsafe_allow_html=True)
                
                attendees_str = ", ".join(session["attendees"])
                st.markdown(f"**Attendees:** {attendees_str}")
            
            # Materials
            if session["materials"]:
                st.markdown("**Materials:**")
                for material in session["materials"]:
                    st.markdown(f"- {material}")
            
            # Videos
            if session["videos"]:
                st.markdown("**Video Recordings:**")
                for video in session["videos"]:
                    st.markdown(f"- {video}")
            
            # Notes
            if session["notes"]:
                st.markdown(f"**Notes:** {session['notes']}")
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if session["date"] < datetime.now() and not session["signed_off"]:
                    st.button("Sign Off Training", key=f"signoff_{session['id']}")
            
            with buttons_col2:
                st.button("Edit", key=f"edit_training_{session['id']}")
            
            with buttons_col3:
                if session["date"] < datetime.now():
                    st.button("Upload Materials/Videos", key=f"upload_training_{session['id']}")
    
    # Add training form
    if st.session_state.get("show_training_form", False):
        with st.form("training_form"):
            st.subheader("Add Training Session")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                training_system = st.text_input("System/Equipment", key="new_training_system")
                training_trainer = st.text_input("Trainer/Company", key="new_training_trainer")
                training_date = st.date_input("Training Date", key="new_training_date")
                training_duration = st.text_input("Duration", key="new_training_duration", placeholder="e.g., 4 hours")
                training_location = st.text_input("Location", key="new_training_location")
            
            with form_col2:
                training_attendees = st.text_area(
                    "Attendees", 
                    key="new_training_attendees",
                    placeholder="Enter one attendee per line\nInclude role in parentheses"
                )
                training_notes = st.text_area("Notes", key="new_training_notes")
                training_signoff = st.checkbox("Signed Off", key="new_training_signoff")
            
            # Upload materials
            st.subheader("Upload Training Materials")
            training_materials = st.file_uploader("Documents", accept_multiple_files=True, key="new_training_materials")
            
            st.subheader("Upload Training Videos")
            training_videos = st.file_uploader("Videos", accept_multiple_files=True, key="new_training_videos", type=["mp4", "mov", "avi"])
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_training = st.form_submit_button("Save")
            with submit_col2:
                cancel_training = st.form_submit_button("Cancel")
            
            if submit_training:
                st.success("Training session added successfully")
                st.session_state.show_training_form = False
                st.rerun()
            
            if cancel_training:
                st.session_state.show_training_form = False
                st.rerun()

def render_financial_closeout():
    """Render the financial closeout section"""
    
    st.header("Financial Close-out")
    
    # Add button for creating new financial document
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("Add Financial Document", type="primary", key="add_financial_btn"):
            st.session_state.show_financial_form = True
    
    # Sample financial closeout data
    financial_docs = [
        {
            "id": "FIN-2025-001",
            "type": "Final Payment Application",
            "amount": 2450000.0,
            "date_submitted": datetime.now() - timedelta(days=30),
            "status": "Approved",
            "approved_by": "John Smith",
            "approval_date": datetime.now() - timedelta(days=15),
            "payment_date": datetime.now() - timedelta(days=7),
            "documents": ["Final_Pay_App.pdf", "Supporting_Documentation.pdf"],
            "notes": "Final payment approved by owner"
        },
        {
            "id": "FIN-2025-002",
            "type": "Retainage Release",
            "amount": 912500.0,
            "date_submitted": datetime.now() - timedelta(days=20),
            "status": "Pending Approval",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": ["Retainage_Release_Request.pdf"],
            "notes": "Awaiting owner review"
        },
        {
            "id": "FIN-2025-003",
            "type": "Final Lien Waiver - General Contractor",
            "amount": None,
            "date_submitted": datetime.now() - timedelta(days=15),
            "status": "Submitted",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": ["GC_Final_Lien_Waiver.pdf"],
            "notes": "Submitted with final payment application"
        },
        {
            "id": "FIN-2025-004",
            "type": "Final Lien Waiver - Electrical Sub",
            "amount": None,
            "date_submitted": datetime.now() - timedelta(days=14),
            "status": "Submitted",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": ["Electrical_Final_Lien_Waiver.pdf"],
            "notes": "Submitted with final payment application"
        },
        {
            "id": "FIN-2025-005",
            "type": "Final Lien Waiver - Mechanical Sub",
            "amount": None,
            "date_submitted": datetime.now() - timedelta(days=14),
            "status": "Submitted",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": ["Mechanical_Final_Lien_Waiver.pdf"],
            "notes": "Submitted with final payment application"
        },
        {
            "id": "FIN-2025-006",
            "type": "Final Lien Waiver - Plumbing Sub",
            "amount": None,
            "date_submitted": datetime.now() - timedelta(days=13),
            "status": "Missing",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": [],
            "notes": "Follow-up requested from subcontractor"
        },
        {
            "id": "FIN-2025-007",
            "type": "Consent of Surety",
            "amount": None,
            "date_submitted": datetime.now() - timedelta(days=10),
            "status": "Submitted",
            "approved_by": None,
            "approval_date": None,
            "payment_date": None,
            "documents": ["Consent_of_Surety.pdf"],
            "notes": "Bond release documentation"
        }
    ]
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Pending", "Submitted", "Pending Approval", "Approved", "Rejected", "Missing"],
            default=["Pending", "Submitted", "Pending Approval", "Missing"],
            key="financial_status_filter"
        )
    
    with col2:
        type_filter = st.multiselect(
            "Document Type",
            list(set(doc["type"] for doc in financial_docs)),
            default=[],
            key="financial_type_filter"
        )
    
    # Apply filters
    filtered_docs = [doc for doc in financial_docs if doc["status"] in status_filter]
    
    if type_filter:
        filtered_docs = [doc for doc in filtered_docs if doc["type"] in type_filter]
    
    # Financial metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_docs = len(financial_docs)
        st.metric("Total Documents", total_docs)
    
    with metrics_col2:
        total_payment = sum(doc["amount"] or 0 for doc in financial_docs if doc["status"] == "Approved")
        st.metric("Total Approved", f"${total_payment:,.2f}")
    
    with metrics_col3:
        lien_waivers = [doc for doc in financial_docs if "Lien Waiver" in doc["type"]]
        missing_waivers = len([doc for doc in lien_waivers if doc["status"] == "Missing"])
        waiver_count = f"{len(lien_waivers) - missing_waivers}/{len(lien_waivers)}"
        st.metric("Lien Waivers Received", waiver_count)
    
    with metrics_col4:
        retainage_status = next((doc["status"] for doc in financial_docs if doc["type"] == "Retainage Release"), "Not Started")
        st.metric("Retainage Status", retainage_status)
    
    # Document list
    st.subheader("Financial Documents")
    
    # Sort by date submitted
    filtered_docs.sort(key=lambda x: x["date_submitted"], reverse=True)
    
    # Show document list
    for doc in filtered_docs:
        # Determine status color
        if doc["status"] == "Approved":
            status_color = "#28a745"  # Green
        elif doc["status"] == "Submitted" or doc["status"] == "Pending Approval":
            status_color = "#17a2b8"  # Cyan
        elif doc["status"] == "Pending":
            status_color = "#6c757d"  # Gray
        elif doc["status"] == "Missing":
            status_color = "#dc3545"  # Red
        else:  # Rejected
            status_color = "#dc3545"  # Red
        
        # Create card
        with st.expander(f"{doc['id']} - {doc['type']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Submitted Date:** {doc['date_submitted'].strftime('%Y-%m-%d')}")
                
                if doc["amount"] is not None:
                    st.markdown(f"**Amount:** ${doc['amount']:,.2f}")
                
                if doc["approved_by"]:
                    st.markdown(f"**Approved By:** {doc['approved_by']}")
                
                if doc["approval_date"]:
                    st.markdown(f"**Approval Date:** {doc['approval_date'].strftime('%Y-%m-%d')}")
                
                if doc["payment_date"]:
                    st.markdown(f"**Payment Date:** {doc['payment_date'].strftime('%Y-%m-%d')}")
            
            with col2:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{doc['status']}</span>", unsafe_allow_html=True)
                
                # Documents
                if doc["documents"]:
                    st.markdown("**Documents:**")
                    for document in doc["documents"]:
                        st.markdown(f"- {document}")
                else:
                    st.markdown("**Documents:** None uploaded")
                
                # Notes
                if doc["notes"]:
                    st.markdown(f"**Notes:** {doc['notes']}")
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if doc["status"] in ["Submitted", "Pending Approval"]:
                    st.button("Approve", key=f"approve_{doc['id']}")
                elif doc["status"] == "Missing":
                    st.button("Upload", key=f"upload_missing_{doc['id']}")
            
            with buttons_col2:
                st.button("Edit", key=f"edit_financial_{doc['id']}")
            
            with buttons_col3:
                st.button("View Details", key=f"details_financial_{doc['id']}")
    
    # Add financial document form
    if st.session_state.get("show_financial_form", False):
        with st.form("financial_form"):
            st.subheader("Add Financial Document")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                doc_type = st.selectbox(
                    "Document Type", 
                    ["Final Payment Application", "Retainage Release", "Final Lien Waiver", 
                     "Consent of Surety", "Release of Bonds", "Other"],
                    key="new_doc_type"
                )
                
                if doc_type in ["Final Payment Application", "Retainage Release"]:
                    doc_amount = st.number_input("Amount ($)", min_value=0.0, value=0.0, key="new_doc_amount")
                
                doc_date = st.date_input("Submission Date", datetime.now(), key="new_doc_date")
                doc_status = st.selectbox(
                    "Status", 
                    ["Pending", "Submitted", "Pending Approval", "Approved", "Rejected", "Missing"],
                    key="new_doc_status"
                )
            
            with form_col2:
                if doc_status == "Approved":
                    doc_approved_by = st.text_input("Approved By", key="new_doc_approved_by")
                    doc_approval_date = st.date_input("Approval Date", datetime.now(), key="new_doc_approval_date")
                    doc_payment_date = st.date_input("Payment Date", datetime.now(), key="new_doc_payment_date")
                
                doc_notes = st.text_area("Notes", key="new_doc_notes")
            
            # Document upload
            st.file_uploader("Upload Documents", accept_multiple_files=True, key="new_doc_files")
            
            # Form submission
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_doc = st.form_submit_button("Save")
            with submit_col2:
                cancel_doc = st.form_submit_button("Cancel")
            
            if submit_doc:
                st.success("Financial document added successfully")
                st.session_state.show_financial_form = False
                st.rerun()
            
            if cancel_doc:
                st.session_state.show_financial_form = False
                st.rerun()

def render_closeout():
    """Render the closeout module"""
    
    # Header
    st.title("Project Closeout")
    
    # Tab navigation for closeout sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Punch List", 
        "Occupancy Permits", 
        "Owner Training",
        "Financial Close-out",
        "Warranties", 
        "O&M Manuals", 
        "Final Documentation"
    ])
    
    # Punch List Tab
    with tab1:
        render_punch_list()
    
    # Occupancy Permits Tab
    with tab2:
        render_occupancy_permits()
    
    # Owner Training Tab
    with tab3:
        render_owner_training()
    
    # Financial Close-out Tab
    with tab4:
        render_financial_closeout()
    
    # Warranties Tab
    with tab5:
        render_warranties()
    
    # O&M Manuals Tab
    with tab6:
        render_om_manuals()
    
    # Final Documentation Tab
    with tab7:
        render_final_documentation()

def render_punch_list():
    """Render the punch list section"""
    
    st.header("Punch List")
    
    # Sample data for punch list items
    locations = [
        "Building A - Floor 1", "Building A - Floor 2", "Building A - Floor 3", 
        "Building B - Floor 1", "Building B - Floor 2", 
        "Exterior - North", "Exterior - South", "Exterior - East", "Exterior - West",
        "Roof", "Parking Garage", "Mechanical Room", "Electrical Room"
    ]
    
    categories = [
        "Architectural", "Mechanical", "Electrical", "Plumbing", 
        "Structural", "Civil", "Landscape", "Finishes", "Safety"
    ]
    
    responsible_parties = [
        "General Contractor", "Electrical Subcontractor", "Mechanical Subcontractor",
        "Plumbing Subcontractor", "Finishes Subcontractor", "Concrete Subcontractor",
        "Steel Subcontractor", "Landscape Subcontractor", "Owner"
    ]
    
    # Create sample punch list items
    punch_items = []
    for i in range(1, 51):
        # Generate realistic item
        location = random.choice(locations)
        category = random.choice(categories)
        responsible = random.choice(responsible_parties)
        
        # Create some common issues based on category
        if category == "Architectural":
            description = random.choice([
                "Door not closing properly", "Missing door stop", "Window seal damaged",
                "Ceiling tile damaged", "Wall finish incomplete", "Baseboard misaligned",
                "Door hardware missing", "Flooring damaged"
            ])
        elif category == "Mechanical":
            description = random.choice([
                "Diffuser misaligned", "Thermostat not functioning", "Duct leakage",
                "HVAC unit noisy", "Damper not operating", "Fan not balanced",
                "Inadequate cooling", "Inadequate ventilation"
            ])
        elif category == "Electrical":
            description = random.choice([
                "Missing outlet cover", "Light fixture not functioning", "Switch not working",
                "Exposed wiring", "Panel not labeled", "Emergency light not functioning",
                "Incorrect fixture installed", "Outlet not powered"
            ])
        elif category == "Plumbing":
            description = random.choice([
                "Sink leaking", "Toilet running", "Faucet dripping", "Drain slow",
                "Water pressure low", "Hot water not available", "Pipe insulation missing",
                "Backflow preventer not tested"
            ])
        else:
            description = f"{category} issue #{i}"
        
        # Generate dates and other metadata
        identified_date = datetime.now() - timedelta(days=random.randint(1, 60))
        
        # Status and completion info
        status = random.choices(
            ["Open", "In Progress", "Complete", "Verified"], 
            weights=[0.2, 0.3, 0.4, 0.1], 
            k=1
        )[0]
        
        completion_date = None
        verification_date = None
        
        if status in ["Complete", "Verified"]:
            completion_date = identified_date + timedelta(days=random.randint(1, 14))
            
            if status == "Verified":
                verification_date = completion_date + timedelta(days=random.randint(1, 7))
        
        # Create the item
        punch_items.append({
            "id": f"PL-{2025}-{i:03d}",
            "location": location,
            "category": category,
            "description": description,
            "responsible_party": responsible,
            "identified_date": identified_date,
            "status": status,
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "completion_date": completion_date,
            "verification_date": verification_date,
            "photo": random.choice([True, False]),
            "cost_impact": random.uniform(0, 5000) if random.random() > 0.7 else 0,
            "schedule_impact": random.randint(0, 5) if random.random() > 0.8 else 0,
            "notes": random.choice([
                "Contractor notified", "Materials ordered", "Requires coordination with owner",
                "Second occurrence", "Owner requested change", "Warranty issue", None
            ])
        })
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Open", "In Progress", "Complete", "Verified"],
            default=["Open", "In Progress"],
            key="punch_status_filter"
        )
    
    with col2:
        category_filter = st.multiselect(
            "Category",
            categories,
            default=[],
            key="punch_category_filter"
        )
    
    with col3:
        responsible_filter = st.multiselect(
            "Responsible Party",
            responsible_parties,
            default=[],
            key="punch_responsible_filter"
        )
    
    # Apply filters
    filtered_items = [item for item in punch_items if item["status"] in status_filter]
    
    if category_filter:
        filtered_items = [item for item in filtered_items if item["category"] in category_filter]
    
    if responsible_filter:
        filtered_items = [item for item in filtered_items if item["responsible_party"] in responsible_filter]
    
    # Punch list metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_items = len(punch_items)
        filtered_count = len(filtered_items)
        st.metric("Total Items", total_items)
    
    with metrics_col2:
        open_items = len([item for item in punch_items if item["status"] in ["Open", "In Progress"]])
        open_pct = (open_items / total_items) * 100 if total_items > 0 else 0
        st.metric("Open Items", f"{open_items} ({open_pct:.1f}%)")
    
    with metrics_col3:
        complete_items = len([item for item in punch_items if item["status"] in ["Complete", "Verified"]])
        complete_pct = (complete_items / total_items) * 100 if total_items > 0 else 0
        st.metric("Completed", f"{complete_items} ({complete_pct:.1f}%)")
    
    with metrics_col4:
        high_priority = len([item for item in punch_items if item["priority"] in ["High", "Critical"] and item["status"] in ["Open", "In Progress"]])
        st.metric("High Priority Open", high_priority)
    
    # Punch list visualizations
    st.subheader("Punch List Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Punch list by category
        category_counts = {}
        for item in punch_items:
            cat = item["category"]
            if cat not in category_counts:
                category_counts[cat] = {"total": 0, "open": 0}
            
            category_counts[cat]["total"] += 1
            if item["status"] in ["Open", "In Progress"]:
                category_counts[cat]["open"] += 1
        
        # Create data for chart
        categories_for_chart = list(category_counts.keys())
        total_counts = [category_counts[cat]["total"] for cat in categories_for_chart]
        open_counts = [category_counts[cat]["open"] for cat in categories_for_chart]
        
        # Sort by total count
        sorted_indices = sorted(range(len(total_counts)), key=lambda k: total_counts[k], reverse=True)
        categories_sorted = [categories_for_chart[i] for i in sorted_indices]
        total_sorted = [total_counts[i] for i in sorted_indices]
        open_sorted = [open_counts[i] for i in sorted_indices]
        
        # Create DataFrame for chart
        category_df = pd.DataFrame({
            "Category": categories_sorted,
            "Total": total_sorted,
            "Open": open_sorted
        })
        
        # Create bar chart
        fig = px.bar(
            category_df,
            x="Category",
            y=["Total", "Open"],
            title="Punch List Items by Category",
            barmode="group"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Punch list by location
        location_counts = {}
        for item in punch_items:
            loc = item["location"]
            if loc not in location_counts:
                location_counts[loc] = 0
            
            if item["status"] in ["Open", "In Progress"]:
                location_counts[loc] += 1
        
        # Create data for chart
        locations_for_chart = list(location_counts.keys())
        location_open_counts = [location_counts[loc] for loc in locations_for_chart]
        
        # Sort by count
        sorted_indices = sorted(range(len(location_open_counts)), key=lambda k: location_open_counts[k], reverse=True)
        locations_sorted = [locations_for_chart[i] for i in sorted_indices]
        open_counts_sorted = [location_open_counts[i] for i in sorted_indices]
        
        # Create DataFrame for chart
        location_df = pd.DataFrame({
            "Location": locations_sorted,
            "Open Items": open_counts_sorted
        })
        
        # Create bar chart
        fig = px.bar(
            location_df.head(10),  # Show top 10 locations
            x="Location",
            y="Open Items",
            title="Open Punch List Items by Location (Top 10)",
            color="Open Items",
            color_continuous_scale="Reds"
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Punch list item list
    st.subheader("Punch List Items")
    
    # Sort by status and priority
    def get_status_priority(item):
        status_order = {"Open": 0, "In Progress": 1, "Complete": 2, "Verified": 3}
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        return (status_order[item["status"]], priority_order[item["priority"]])
    
    filtered_items.sort(key=get_status_priority)
    
    for item in filtered_items:
        # Status color
        if item["status"] == "Open":
            status_color = "#dc3545"  # Red
        elif item["status"] == "In Progress":
            status_color = "#fd7e14"  # Orange
        elif item["status"] == "Complete":
            status_color = "#28a745"  # Green
        else:  # Verified
            status_color = "#20c997"  # Teal
        
        # Priority color
        if item["priority"] == "Critical":
            priority_color = "#dc3545"  # Red
            priority_icon = "🔴"
        elif item["priority"] == "High":
            priority_color = "#fd7e14"  # Orange
            priority_icon = "🟠"
        elif item["priority"] == "Medium":
            priority_color = "#ffc107"  # Yellow
            priority_icon = "🟡"
        else:  # Low
            priority_color = "#28a745"  # Green
            priority_icon = "🟢"
        
        # Item card
        with st.expander(f"{priority_icon} {item['id']} - {item['category']} - {item['description']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Location:** {item['location']}")
                st.markdown(f"**Category:** {item['category']}")
                st.markdown(f"**Responsible:** {item['responsible_party']}")
                st.markdown(f"**Priority:** <span style='color: {priority_color}; font-weight: bold;'>{item['priority']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Identified Date:** {item['identified_date'].strftime('%Y-%m-%d')}")
            
            with col2:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{item['status']}</span>", unsafe_allow_html=True)
                
                if item["completion_date"]:
                    st.markdown(f"**Completion Date:** {item['completion_date'].strftime('%Y-%m-%d')}")
                
                if item["verification_date"]:
                    st.markdown(f"**Verification Date:** {item['verification_date'].strftime('%Y-%m-%d')}")
                
                if item["cost_impact"] > 0:
                    st.markdown(f"**Cost Impact:** ${item['cost_impact']:,.2f}")
                
                if item["schedule_impact"] > 0:
                    st.markdown(f"**Schedule Impact:** {item['schedule_impact']} days")
            
            st.markdown(f"**Description:** {item['description']}")
            
            if item["notes"]:
                st.markdown(f"**Notes:** {item['notes']}")
            
            if item["photo"]:
                st.markdown("**Photo:** 📷 *Photo available*")
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if item["status"] == "Open":
                    st.button("Start Work", key=f"start_{item['id']}")
                elif item["status"] == "In Progress":
                    st.button("Mark Complete", key=f"complete_{item['id']}")
                elif item["status"] == "Complete":
                    st.button("Verify", key=f"verify_{item['id']}")
            
            with buttons_col2:
                st.button("Edit", key=f"edit_{item['id']}")
            
            with buttons_col3:
                st.button("View Details", key=f"details_{item['id']}")
    
    # Add punch list item button
    st.divider()
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("Add Punch List Item", type="primary", key="add_punch_btn"):
            st.session_state.show_punch_form = True
    
    # Punch list item form
    if st.session_state.get("show_punch_form", False):
        with st.form("punch_form"):
            st.subheader("Add Punch List Item")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                punch_location = st.selectbox("Location", locations, key="new_punch_location")
                punch_category = st.selectbox("Category", categories, key="new_punch_category")
                punch_responsible = st.selectbox("Responsible Party", responsible_parties, key="new_punch_responsible")
                punch_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="new_punch_priority")
            
            with form_col2:
                punch_status = st.selectbox("Status", ["Open", "In Progress", "Complete"], key="new_punch_status")
                punch_date = st.date_input("Identified Date", datetime.now(), key="new_punch_date")
                punch_cost = st.number_input("Cost Impact ($)", min_value=0.0, value=0.0, step=100.0, key="new_punch_cost")
                punch_schedule = st.number_input("Schedule Impact (days)", min_value=0, value=0, key="new_punch_schedule")
            
            punch_description = st.text_area("Description", key="new_punch_description")
            punch_notes = st.text_area("Notes (optional)", key="new_punch_notes")
            
            # Photo upload
            punch_photos = st.file_uploader("Upload Photos", accept_multiple_files=True, key="new_punch_photos")
            
            submitted = st.form_submit_button("Save Punch List Item")
            
            if submitted:
                st.success("Punch list item added successfully!")
                st.session_state.show_punch_form = False
                st.rerun()
    
    # Export options
    st.divider()
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        st.button("Export to Excel", key="export_punch_excel")
    
    with export_col2:
        st.button("Generate Punch List Report", key="gen_punch_report")
    
    with export_col3:
        st.button("Print Punch List", key="print_punch")

def render_warranties():
    """Render the warranties section"""
    
    st.header("Warranties & Guarantees")
    
    # Sample data for warranty items
    warranty_types = [
        "General Contractor Warranty", "Subcontractor Warranty", "Manufacturer Warranty",
        "Extended Warranty", "Special Warranty", "Equipment Warranty"
    ]
    
    categories = [
        "General", "Structural", "HVAC", "Electrical", "Plumbing", "Roofing", 
        "Flooring", "Windows", "Doors", "Equipment", "Elevators", "Fire Protection"
    ]
    
    # Create sample warranty items
    warranties = []
    for i in range(1, 31):
        category = random.choice(categories)
        
        # Create description based on category
        if category == "General":
            description = "General Contractor Workmanship"
        elif category == "Structural":
            description = random.choice(["Concrete Structure", "Steel Structure", "Foundation", "Structural Framing"])
        elif category == "HVAC":
            description = random.choice(["Air Handling Units", "Chillers", "Boilers", "VAV Boxes", "Ductwork", "BAS Controls"])
        elif category == "Electrical":
            description = random.choice(["Electrical Distribution", "Lighting", "Generators", "UPS Systems", "Switchgear"])
        elif category == "Plumbing":
            description = random.choice(["Plumbing Fixtures", "Piping", "Water Heaters", "Pumps", "Backflow Preventers"])
        elif category == "Roofing":
            description = random.choice(["Membrane Roofing", "Metal Roofing", "Roof Accessories", "Flashing and Trim"])
        elif category == "Flooring":
            description = random.choice(["Carpet", "Ceramic Tile", "Vinyl Flooring", "Wood Flooring", "Concrete Flooring"])
        elif category == "Equipment":
            description = random.choice(["Kitchen Equipment", "Laboratory Equipment", "Audiovisual Equipment", "Fitness Equipment"])
        else:
            description = f"{category} Systems and Components"
        
        # Generate date information
        start_date = datetime.now() - timedelta(days=random.randint(30, 180))
        duration_years = random.choices([1, 2, 5, 10, 20], weights=[0.2, 0.3, 0.3, 0.15, 0.05], k=1)[0]
        expiration_date = start_date + timedelta(days=365 * duration_years)
        
        # Calculate days remaining
        days_remaining = (expiration_date - datetime.now()).days
        
        # Create a warranty item
        warranties.append({
            "id": f"W-{2025}-{i:03d}",
            "type": random.choice(warranty_types),
            "category": category,
            "description": description,
            "provider": random.choice([
                "General Contractor", "Mechanical Subcontractor", "Electrical Subcontractor",
                "ABC Manufacturer", "XYZ Corporation", "Acme Systems", "Best Warranty Inc."
            ]),
            "start_date": start_date,
            "duration_years": duration_years,
            "expiration_date": expiration_date,
            "days_remaining": days_remaining,
            "renewable": random.choice([True, False]),
            "documentation": random.choice([True, False]),
            "certificate_number": f"CERT-{random.randint(10000, 99999)}",
            "contact_name": random.choice(["John Smith", "Mary Jones", "Robert Johnson", "Alice Brown"]),
            "contact_email": f"contact{random.randint(1, 99)}@example.com",
            "contact_phone": f"({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "notes": random.choice([
                "Requires annual inspection", "Extended warranty available", "Transferable to new owner",
                "Limited coverage", "Full replacement warranty", "Labor only", "Parts only", None
            ])
        })
    
    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        category_filter = st.multiselect(
            "Category",
            list(set(w["category"] for w in warranties)),
            default=[],
            key="warranty_category_filter"
        )
    
    with filter_col2:
        status_filter = st.multiselect(
            "Status",
            ["Active", "Expired", "Expiring Soon (< 90 days)"],
            default=["Active"],
            key="warranty_status_filter"
        )
    
    with filter_col3:
        duration_filter = st.multiselect(
            "Duration",
            [1, 2, 5, 10, 20],
            default=[],
            key="warranty_duration_filter"
        )
    
    # Apply filters
    filtered_warranties = warranties.copy()
    
    if category_filter:
        filtered_warranties = [w for w in filtered_warranties if w["category"] in category_filter]
    
    if "Active" in status_filter and "Expired" in status_filter and "Expiring Soon (< 90 days)" in status_filter:
        # All statuses selected, no filtering needed
        pass
    else:
        temp_warranties = []
        if "Active" in status_filter:
            temp_warranties.extend([w for w in filtered_warranties if w["days_remaining"] > 90])
        if "Expiring Soon (< 90 days)" in status_filter:
            temp_warranties.extend([w for w in filtered_warranties if 0 < w["days_remaining"] <= 90])
        if "Expired" in status_filter:
            temp_warranties.extend([w for w in filtered_warranties if w["days_remaining"] <= 0])
        filtered_warranties = temp_warranties
    
    if duration_filter:
        filtered_warranties = [w for w in filtered_warranties if w["duration_years"] in duration_filter]
    
    # Warranty metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_warranties = len(warranties)
        st.metric("Total Warranties", total_warranties)
    
    with metrics_col2:
        active_warranties = len([w for w in warranties if w["days_remaining"] > 0])
        active_pct = (active_warranties / total_warranties) * 100 if total_warranties > 0 else 0
        st.metric("Active Warranties", f"{active_warranties} ({active_pct:.1f}%)")
    
    with metrics_col3:
        expiring_soon = len([w for w in warranties if 0 < w["days_remaining"] <= 90])
        st.metric("Expiring Soon", expiring_soon)
    
    with metrics_col4:
        expired = len([w for w in warranties if w["days_remaining"] <= 0])
        st.metric("Expired", expired)
    
    # Warranty visualizations
    st.subheader("Warranty Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Warranty by category
        category_counts = {}
        for warranty in warranties:
            cat = warranty["category"]
            if cat not in category_counts:
                category_counts[cat] = 0
            category_counts[cat] += 1
        
        # Create data for chart
        category_df = pd.DataFrame({
            "Category": list(category_counts.keys()),
            "Count": list(category_counts.values())
        }).sort_values("Count", ascending=False)
        
        # Create bar chart
        fig = px.bar(
            category_df,
            x="Category",
            y="Count",
            title="Warranties by Category",
            color="Count",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Warranty expiration timeline
        expirations = []
        for warranty in warranties:
            if warranty["days_remaining"] > 0:  # Only include non-expired warranties
                expirations.append({
                    "Category": warranty["category"],
                    "Days Remaining": warranty["days_remaining"],
                    "Expiration Date": warranty["expiration_date"],
                    "Description": warranty["description"]
                })
        
        # Convert to DataFrame and sort
        if expirations:
            expiration_df = pd.DataFrame(expirations).sort_values("Days Remaining")
            
            # Create the timeline chart
            timeline_data = []
            for i, row in expiration_df.iterrows():
                timeline_data.append({
                    "Task": row["Description"],
                    "Start": datetime.now().strftime("%Y-%m-%d"),
                    "Finish": row["Expiration Date"].strftime("%Y-%m-%d"),
                    "Category": row["Category"]
                })
            
            # Create a Gantt chart
            timeline_df = pd.DataFrame(timeline_data)
            
            fig = px.timeline(
                timeline_df,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Category",
                title="Warranty Expiration Timeline"
            )
            
            fig.update_yaxes(autorange="reversed")  # Reverse the y-axis to put the earliest expiring at the top
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No active warranties to display in the timeline.")
    
    # Warranty list
    st.subheader("Warranty List")
    
    # Sort by days remaining (ascending)
    filtered_warranties.sort(key=lambda w: w["days_remaining"])
    
    for warranty in filtered_warranties:
        # Status determination
        if warranty["days_remaining"] <= 0:
            status = "Expired"
            status_color = "#dc3545"  # Red
        elif warranty["days_remaining"] <= 90:
            status = "Expiring Soon"
            status_color = "#fd7e14"  # Orange
        else:
            status = "Active"
            status_color = "#28a745"  # Green
        
        # Calculate expiry display
        if warranty["days_remaining"] <= 0:
            expiry_display = f"Expired {abs(warranty['days_remaining'])} days ago"
        else:
            expiry_display = f"Expires in {warranty['days_remaining']} days"
        
        # Warranty card
        with st.expander(f"{warranty['category']} - {warranty['description']} ({expiry_display})", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**ID:** {warranty['id']}")
                st.markdown(f"**Type:** {warranty['type']}")
                st.markdown(f"**Category:** {warranty['category']}")
                st.markdown(f"**Provider:** {warranty['provider']}")
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{status}</span>", unsafe_allow_html=True)
                st.markdown(f"**Certificate Number:** {warranty['certificate_number']}")
            
            with col2:
                st.markdown(f"**Start Date:** {warranty['start_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Duration:** {warranty['duration_years']} {'years' if warranty['duration_years'] > 1 else 'year'}")
                st.markdown(f"**Expiration Date:** {warranty['expiration_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Renewable:** {'Yes' if warranty['renewable'] else 'No'}")
                st.markdown(f"**Documentation:** {'Available' if warranty['documentation'] else 'Not Available'}")
            
            st.markdown("### Contact Information")
            st.markdown(f"**Name:** {warranty['contact_name']}")
            st.markdown(f"**Email:** {warranty['contact_email']}")
            st.markdown(f"**Phone:** {warranty['contact_phone']}")
            
            if warranty["notes"]:
                st.markdown(f"**Notes:** {warranty['notes']}")
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if warranty["documentation"]:
                    st.button("View Documentation", key=f"view_doc_{warranty['id']}")
            
            with buttons_col2:
                st.button("Edit Warranty", key=f"edit_warranty_{warranty['id']}")
            
            with buttons_col3:
                if warranty["renewable"] and warranty["days_remaining"] <= 90 and warranty["days_remaining"] > 0:
                    st.button("Renew Warranty", key=f"renew_{warranty['id']}")
    
    # Add warranty button
    st.divider()
    if st.button("Add Warranty", type="primary", key="add_warranty_btn"):
        st.session_state.show_warranty_form = True
    
    # Warranty form
    if st.session_state.get("show_warranty_form", False):
        with st.form("warranty_form"):
            st.subheader("Add Warranty")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                warranty_type = st.selectbox("Type", warranty_types, key="new_warranty_type")
                warranty_category = st.selectbox("Category", categories, key="new_warranty_category")
                warranty_description = st.text_input("Description", key="new_warranty_description")
                warranty_provider = st.text_input("Provider", key="new_warranty_provider")
                warranty_cert = st.text_input("Certificate Number", key="new_warranty_cert")
            
            with form_col2:
                warranty_start = st.date_input("Start Date", datetime.now(), key="new_warranty_start")
                warranty_duration = st.selectbox("Duration (years)", [1, 2, 5, 10, 20], key="new_warranty_duration")
                warranty_renewable = st.checkbox("Renewable", value=False, key="new_warranty_renewable")
                warranty_contact_name = st.text_input("Contact Name", key="new_warranty_contact_name")
                warranty_contact_email = st.text_input("Contact Email", key="new_warranty_contact_email")
                warranty_contact_phone = st.text_input("Contact Phone", key="new_warranty_contact_phone")
            
            warranty_notes = st.text_area("Notes (optional)", key="new_warranty_notes")
            warranty_docs = st.file_uploader("Upload Documentation", key="new_warranty_docs")
            
            submitted = st.form_submit_button("Save Warranty")
            
            if submitted:
                st.success("Warranty added successfully!")
                st.session_state.show_warranty_form = False
                st.rerun()

def render_om_manuals():
    """Render the O&M manuals section"""
    
    st.header("Operation & Maintenance Manuals")
    
    # Sample data for O&M manual categories
    categories = [
        "General Information", "Architectural", "Structural", "Mechanical", "Electrical", 
        "Plumbing", "Fire Protection", "Building Automation", "Elevators", "Security",
        "Audio/Visual", "Telecommunication", "Landscaping", "Building Envelope"
    ]
    
    manuals = []
    for i, category in enumerate(categories):
        manuals.append({
            "id": f"OM-{2025}-{i+1:03d}",
            "category": category,
            "title": f"{category} O&M Manual",
            "description": f"Operation and maintenance documentation for {category.lower()} systems.",
            "version": f"1.{random.randint(0, 9)}",
            "last_updated": datetime.now() - timedelta(days=random.randint(1, 180)),
            "format": random.choice(["PDF", "Paper", "PDF & Paper"]),
            "location": random.choice(["Document Repository", "Project Files", "Online System"]),
            "reviewed": random.choice([True, False]),
            "review_date": (datetime.now() - timedelta(days=random.randint(1, 90))) if random.random() > 0.3 else None,
            "approved": random.choice([True, False]),
            "approval_date": (datetime.now() - timedelta(days=random.randint(1, 60))) if random.random() > 0.4 else None,
            "training_required": random.choice([True, False]),
            "training_completed": random.choice([True, False]) if random.random() > 0.5 else False,
            "file_size_mb": round(random.uniform(1.0, 50.0), 1),
            "page_count": random.randint(10, 500),
            "attachments": random.randint(0, 20),
            "special_instructions": random.choice([
                "Requires annual updates", "Contains proprietary information", 
                "Includes warranty registration", "Includes service contacts", None
            ])
        })
    
    # Display options selection
    view_mode = st.radio(
        "View Mode",
        ["Card View", "Table View"],
        horizontal=True,
        key="om_view_mode"
    )
    
    # Filter options
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        category_filter = st.multiselect(
            "Category",
            list(set(m["category"] for m in manuals)),
            default=[],
            key="om_category_filter"
        )
    
    with filter_col2:
        format_filter = st.multiselect(
            "Format",
            ["PDF", "Paper", "PDF & Paper"],
            default=[],
            key="om_format_filter"
        )
    
    with filter_col3:
        status_filter = st.multiselect(
            "Status",
            ["Approved", "Not Approved", "Reviewed", "Not Reviewed"],
            default=[],
            key="om_status_filter"
        )
    
    # Apply filters
    filtered_manuals = manuals.copy()
    
    if category_filter:
        filtered_manuals = [m for m in filtered_manuals if m["category"] in category_filter]
    
    if format_filter:
        filtered_manuals = [m for m in filtered_manuals if m["format"] in format_filter]
    
    if status_filter:
        temp_manuals = []
        if "Approved" in status_filter:
            temp_manuals.extend([m for m in filtered_manuals if m["approved"]])
        if "Not Approved" in status_filter:
            temp_manuals.extend([m for m in filtered_manuals if not m["approved"]])
        if "Reviewed" in status_filter:
            temp_manuals.extend([m for m in filtered_manuals if m["reviewed"]])
        if "Not Reviewed" in status_filter:
            temp_manuals.extend([m for m in filtered_manuals if not m["reviewed"]])
        
        # Remove duplicates (a manual might match multiple filters)
        seen_ids = set()
        unique_manuals = []
        for m in temp_manuals:
            if m["id"] not in seen_ids:
                seen_ids.add(m["id"])
                unique_manuals.append(m)
        
        filtered_manuals = unique_manuals
    
    # O&M manual metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_manuals = len(manuals)
        st.metric("Total Manuals", total_manuals)
    
    with metrics_col2:
        approved_manuals = len([m for m in manuals if m["approved"]])
        approved_pct = (approved_manuals / total_manuals) * 100 if total_manuals > 0 else 0
        st.metric("Approved", f"{approved_manuals} ({approved_pct:.1f}%)")
    
    with metrics_col3:
        reviewed_manuals = len([m for m in manuals if m["reviewed"]])
        reviewed_pct = (reviewed_manuals / total_manuals) * 100 if total_manuals > 0 else 0
        st.metric("Reviewed", f"{reviewed_manuals} ({reviewed_pct:.1f}%)")
    
    with metrics_col4:
        training_required = len([m for m in manuals if m["training_required"]])
        training_completed = len([m for m in manuals if m["training_required"] and m["training_completed"]])
        if training_required > 0:
            training_pct = (training_completed / training_required) * 100
            st.metric("Training Completed", f"{training_completed}/{training_required} ({training_pct:.1f}%)")
        else:
            st.metric("Training Completed", "N/A")
    
    # Display manuals based on view mode
    st.subheader("O&M Manuals")
    
    if view_mode == "Card View":
        # Sort by category
        filtered_manuals.sort(key=lambda m: m["category"])
        
        # Group by category
        category_groups = {}
        for manual in filtered_manuals:
            category = manual["category"]
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(manual)
        
        # Display by category
        for category, category_manuals in category_groups.items():
            st.markdown(f"### {category}")
            
            # Create a grid of cards
            cols = st.columns(3)
            for i, manual in enumerate(category_manuals):
                with cols[i % 3]:
                    # Status indicators
                    status_markers = []
                    if manual["approved"]:
                        status_markers.append("✅ Approved")
                    if manual["reviewed"]:
                        status_markers.append("📝 Reviewed")
                    if manual["training_required"]:
                        if manual["training_completed"]:
                            status_markers.append("🎓 Training Completed")
                        else:
                            status_markers.append("⚠️ Training Required")
                    
                    status_display = " | ".join(status_markers) if status_markers else "📄 Draft"
                    
                    # Create card
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 20px; height: 180px; overflow: hidden;">
                            <h4 style="margin-top: 0;">{manual["title"]}</h4>
                            <p style="margin-bottom: 5px;">{manual["description"][:80]}...</p>
                            <p style="color: #666; font-size: 0.8em;">Version: {manual["version"]} | Format: {manual["format"]}</p>
                            <p style="color: #666; font-size: 0.8em;">Updated: {manual["last_updated"].strftime('%Y-%m-%d')}</p>
                            <p style="font-size: 0.8em;">{status_display}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Add view button
                    st.button("View Details", key=f"view_om_{manual['id']}")
    
    else:  # Table View
        # Create DataFrame for display
        table_data = []
        for manual in filtered_manuals:
            status = []
            if manual["approved"]:
                status.append("Approved")
            if manual["reviewed"]:
                status.append("Reviewed")
            if manual["training_required"] and not manual["training_completed"]:
                status.append("Training Needed")
            
            table_data.append({
                "Title": manual["title"],
                "Category": manual["category"],
                "Format": manual["format"],
                "Version": manual["version"],
                "Last Updated": manual["last_updated"].strftime("%Y-%m-%d"),
                "Status": ", ".join(status) if status else "Draft",
                "ID": manual["id"]
            })
        
        # Convert to DataFrame
        table_df = pd.DataFrame(table_data)
        
        # Display the table
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.Column(
                    "Action",
                    help="View manual details",
                    disabled=True,
                    width="small"
                )
            }
        )
    
    # Add manual button
    st.divider()
    if st.button("Add O&M Manual", type="primary", key="add_om_btn"):
        st.session_state.show_om_form = True
    
    # O&M manual form
    if st.session_state.get("show_om_form", False):
        with st.form("om_form"):
            st.subheader("Add O&M Manual")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                om_category = st.selectbox("Category", categories, key="new_om_category")
                om_title = st.text_input("Title", key="new_om_title")
                om_description = st.text_area("Description", key="new_om_description", height=100)
                om_version = st.text_input("Version", "1.0", key="new_om_version")
            
            with form_col2:
                om_format = st.selectbox("Format", ["PDF", "Paper", "PDF & Paper"], key="new_om_format")
                om_location = st.text_input("File Location", key="new_om_location")
                om_training = st.checkbox("Training Required", value=False, key="new_om_training")
                om_special = st.text_area("Special Instructions (optional)", key="new_om_special", height=100)
            
            # File upload
            om_files = st.file_uploader("Upload O&M Manual Files", accept_multiple_files=True, key="new_om_files")
            
            submitted = st.form_submit_button("Save O&M Manual")
            
            if submitted:
                st.success("O&M Manual added successfully!")
                st.session_state.show_om_form = False
                st.rerun()

def render_final_documentation():
    """Render the final documentation section"""
    
    st.header("Final Documentation")
    
    # Define document categories and statuses
    document_categories = [
        "As-Built Drawings", "Record Drawings", "Permits & Certificates", 
        "Testing Reports", "Commissioning Reports", "Inspection Reports",
        "Owner Training Materials", "Project Photographs", "BIM Model",
        "Closeout Letters", "Substantial Completion", "Final Completion",
        "Lien Waivers", "Occupancy Certificates", "Utility Connections"
    ]
    
    document_statuses = ["Not Started", "In Progress", "Received", "Reviewed", "Approved", "Final"]
    
    # Create sample closeout documents
    documents = []
    for i, category in enumerate(document_categories):
        # Generate a more realistic status based on progress
        if i < 3:
            # Early items should be further along
            status = random.choices(document_statuses[2:], weights=[0.1, 0.2, 0.4, 0.3], k=1)[0]
        elif i >= len(document_categories) - 3:
            # Later items might not be as far along
            status = random.choices(document_statuses, weights=[0.2, 0.3, 0.3, 0.1, 0.05, 0.05], k=1)[0]
        else:
            # Middle items have a more even distribution
            status = random.choices(document_statuses, weights=[0.05, 0.15, 0.3, 0.2, 0.2, 0.1], k=1)[0]
        
        # Dates based on status
        due_date = datetime.now() + timedelta(days=random.randint(-30, 90))
        received_date = None
        reviewed_date = None
        approved_date = None
        
        if status in ["Received", "Reviewed", "Approved", "Final"]:
            received_date = due_date - timedelta(days=random.randint(1, 30))
            
            if status in ["Reviewed", "Approved", "Final"]:
                reviewed_date = received_date + timedelta(days=random.randint(1, 14))
                
                if status in ["Approved", "Final"]:
                    approved_date = reviewed_date + timedelta(days=random.randint(1, 7))
        
        # Generate document metadata
        documents.append({
            "id": f"DOC-{2025}-{i+1:03d}",
            "category": category,
            "description": f"{category} documentation for project completion",
            "responsibility": random.choice([
                "General Contractor", "Architect", "Engineer", "Subcontractor", "Owner"
            ]),
            "status": status,
            "due_date": due_date,
            "received_date": received_date,
            "reviewed_date": reviewed_date,
            "approved_date": approved_date,
            "format": random.choice(["PDF", "Paper", "Digital", "Multiple"]),
            "location": random.choice([
                "Project Files", "Document Repository", "Drawing Set", "Owner Files"
            ]),
            "notes": random.choice([
                "Requires architect sign-off", "Missing some details", "Final revision needed",
                "Pending owner review", "Includes third-party certificates", None
            ])
        })
    
    # Calculate overall completion percentage
    status_weights = {
        "Not Started": 0.0,
        "In Progress": 0.3,
        "Received": 0.6,
        "Reviewed": 0.8,
        "Approved": 0.9,
        "Final": 1.0
    }
    
    completion_score = sum(status_weights[doc["status"]] for doc in documents)
    total_possible = len(documents)
    completion_percentage = (completion_score / total_possible) * 100
    
    # Closeout metrics
    st.subheader("Closeout Progress")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Overall Completion", f"{completion_percentage:.1f}%")
    
    with metrics_col2:
        not_started = len([d for d in documents if d["status"] == "Not Started"])
        st.metric("Not Started", not_started)
    
    with metrics_col3:
        in_progress = len([d for d in documents if d["status"] == "In Progress"])
        st.metric("In Progress", in_progress)
    
    with metrics_col4:
        completed = len([d for d in documents if d["status"] in ["Approved", "Final"]])
        st.metric("Completed", completed)
    
    # Visualizations
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Status distribution chart
        status_counts = {}
        for doc in documents:
            status = doc["status"]
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        # Create data for pie chart
        status_df = pd.DataFrame({
            "Status": list(status_counts.keys()),
            "Count": list(status_counts.values())
        })
        
        # Color map
        color_map = {
            "Not Started": "#dc3545",  # Red
            "In Progress": "#fd7e14",  # Orange
            "Received": "#ffc107",    # Yellow
            "Reviewed": "#17a2b8",    # Cyan
            "Approved": "#28a745",    # Green
            "Final": "#20c997"        # Teal
        }
        
        # Create pie chart
        fig = px.pie(
            status_df,
            values="Count",
            names="Status",
            title="Document Status Distribution",
            color="Status",
            color_discrete_map=color_map
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Progress by category chart
        progress_data = []
        for doc in documents:
            progress_data.append({
                "Category": doc["category"],
                "Progress": status_weights[doc["status"]] * 100
            })
        
        # Create DataFrame
        progress_df = pd.DataFrame(progress_data)
        
        # Create horizontal bar chart
        fig = px.bar(
            progress_df,
            y="Category",
            x="Progress",
            title="Completion Progress by Category",
            color="Progress",
            color_continuous_scale="Viridis",
            labels={"Progress": "Completion (%)"},
            orientation="h"
        )
        
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Document tracker
    st.subheader("Document Tracker")
    
    # Sorting and filtering options
    sort_col, filter_col = st.columns([1, 3])
    
    with sort_col:
        sort_by = st.selectbox(
            "Sort By",
            ["Status", "Category", "Due Date", "Responsibility"],
            key="doc_sort_by"
        )
    
    with filter_col:
        status_filter = st.multiselect(
            "Status Filter",
            document_statuses,
            default=[],
            key="doc_status_filter"
        )
    
    # Apply filters
    filtered_docs = documents.copy()
    if status_filter:
        filtered_docs = [d for d in filtered_docs if d["status"] in status_filter]
    
    # Apply sorting
    if sort_by == "Status":
        # Custom sort order for status
        status_order = {status: i for i, status in enumerate(document_statuses)}
        filtered_docs.sort(key=lambda d: status_order[d["status"]])
    elif sort_by == "Category":
        filtered_docs.sort(key=lambda d: d["category"])
    elif sort_by == "Due Date":
        filtered_docs.sort(key=lambda d: d["due_date"])
    elif sort_by == "Responsibility":
        filtered_docs.sort(key=lambda d: d["responsibility"])
    
    # Display document list
    for doc in filtered_docs:
        # Set status color
        if doc["status"] == "Not Started":
            status_color = "#dc3545"  # Red
        elif doc["status"] == "In Progress":
            status_color = "#fd7e14"  # Orange
        elif doc["status"] == "Received":
            status_color = "#ffc107"  # Yellow
        elif doc["status"] == "Reviewed":
            status_color = "#17a2b8"  # Cyan
        elif doc["status"] == "Approved":
            status_color = "#28a745"  # Green
        else:  # Final
            status_color = "#20c997"  # Teal
        
        # Document card
        with st.expander(f"{doc['category']} - {doc['status']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**ID:** {doc['id']}")
                st.markdown(f"**Category:** {doc['category']}")
                st.markdown(f"**Description:** {doc['description']}")
                st.markdown(f"**Responsibility:** {doc['responsibility']}")
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{doc['status']}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Due Date:** {doc['due_date'].strftime('%Y-%m-%d')}")
                
                if doc["received_date"]:
                    st.markdown(f"**Received Date:** {doc['received_date'].strftime('%Y-%m-%d')}")
                
                if doc["reviewed_date"]:
                    st.markdown(f"**Reviewed Date:** {doc['reviewed_date'].strftime('%Y-%m-%d')}")
                
                if doc["approved_date"]:
                    st.markdown(f"**Approved Date:** {doc['approved_date'].strftime('%Y-%m-%d')}")
                
                st.markdown(f"**Format:** {doc['format']}")
                st.markdown(f"**Location:** {doc['location']}")
            
            if doc["notes"]:
                st.markdown(f"**Notes:** {doc['notes']}")
            
            # Progress bar
            status_index = document_statuses.index(doc["status"])
            progress_pct = (status_index + 1) / len(document_statuses)
            
            st.progress(progress_pct)
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3, buttons_col4 = st.columns(4)
            
            with buttons_col1:
                if doc["status"] in ["Not Started", "In Progress"]:
                    st.button("Mark Received", key=f"receive_{doc['id']}")
                elif doc["status"] == "Received":
                    st.button("Mark Reviewed", key=f"review_{doc['id']}")
                elif doc["status"] == "Reviewed":
                    st.button("Mark Approved", key=f"approve_{doc['id']}")
                elif doc["status"] == "Approved":
                    st.button("Mark Final", key=f"finalize_{doc['id']}")
            
            with buttons_col2:
                st.button("View Document", key=f"view_{doc['id']}")
            
            with buttons_col3:
                st.button("Edit", key=f"edit_{doc['id']}")
            
            with buttons_col4:
                st.button("Upload New Version", key=f"upload_{doc['id']}")
    
    # Add document button
    st.divider()
    if st.button("Add Document", type="primary", key="add_doc_btn"):
        st.session_state.show_doc_form = True
    
    # Document form
    if st.session_state.get("show_doc_form", False):
        with st.form("doc_form"):
            st.subheader("Add Closeout Document")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                doc_category = st.selectbox("Category", document_categories, key="new_doc_category")
                doc_description = st.text_area("Description", key="new_doc_description")
                doc_responsibility = st.selectbox(
                    "Responsibility", 
                    ["General Contractor", "Architect", "Engineer", "Subcontractor", "Owner"],
                    key="new_doc_responsibility"
                )
                doc_status = st.selectbox("Status", document_statuses, key="new_doc_status")
            
            with form_col2:
                doc_due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30), key="new_doc_due_date")
                doc_format = st.selectbox("Format", ["PDF", "Paper", "Digital", "Multiple"], key="new_doc_format")
                doc_location = st.text_input("Location", key="new_doc_location")
                doc_notes = st.text_area("Notes (optional)", key="new_doc_notes")
            
            # File upload
            doc_files = st.file_uploader("Upload Document Files", accept_multiple_files=True, key="new_doc_files")
            
            submitted = st.form_submit_button("Save Document")
            
            if submitted:
                st.success("Document added successfully!")
                st.session_state.show_doc_form = False
                st.rerun()
    
    # Final closeout checklist
    st.subheader("Final Closeout Checklist")
    
    checklist_items = [
        {"item": "All punch list items completed", "complete": random.choice([True, False])},
        {"item": "All warranties collected and organized", "complete": random.choice([True, False])},
        {"item": "All O&M manuals received and approved", "complete": random.choice([True, False])},
        {"item": "All as-built drawings received and approved", "complete": random.choice([True, False])},
        {"item": "Final inspections passed", "complete": random.choice([True, False])},
        {"item": "Certificate of Occupancy received", "complete": random.choice([True, False])},
        {"item": "Final lien waivers collected", "complete": random.choice([True, False])},
        {"item": "Final payment application approved", "complete": random.choice([True, False])},
        {"item": "Owner training completed", "complete": random.choice([True, False])},
        {"item": "Keys and access credentials transferred", "complete": random.choice([True, False])},
        {"item": "Utility transfers completed", "complete": random.choice([True, False])},
        {"item": "Final cleaning completed", "complete": random.choice([True, False])}
    ]
    
    # Calculate progress
    completed_items = sum(1 for item in checklist_items if item["complete"])
    total_items = len(checklist_items)
    checklist_progress = (completed_items / total_items) * 100
    
    st.progress(checklist_progress / 100, text=f"Closeout Progress: {checklist_progress:.1f}%")
    
    # Display checklist
    for i, item in enumerate(checklist_items):
        checked = item["complete"]
        # Create a checkbox with the current state
        if st.checkbox(item["item"], value=checked, key=f"checklist_{i}"):
            # This would update the database in a real application
            pass
    
    # Final export options
    st.divider()
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        st.button("Export Closeout Binder", key="export_binder")
    
    with export_col2:
        st.button("Generate Closeout Report", key="gen_closeout_report")
    
    with export_col3:
        st.button("Create Final Turnover Package", key="create_turnover_pkg")