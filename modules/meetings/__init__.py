"""
Meeting Management Module for gcPanel Construction Management Platform

This module provides comprehensive meeting management capabilities including:
- Professional meeting agenda templates
- Meeting scheduling and coordination
- Action item tracking
- Meeting minutes and documentation
- Follow-up and accountability systems

Based on authentic industry standards and best practices for construction project meetings.
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from assets.crud_styler import apply_crud_styles
import io

def render():
    """Main render function for the Meeting Management module"""
    st.title("🤝 Meeting Management Center")
    st.markdown("### Highland Tower Development - Professional Meeting Coordination")
    
    # Apply CRUD styling
    apply_crud_styles()
    
    # Create main tabs for meeting management
    tabs = st.tabs([
        "📋 Meeting Agendas",
        "📅 Schedule Meetings", 
        "✅ Action Items",
        "📝 Meeting Minutes",
        "📊 Meeting Analytics"
    ])
    
    with tabs[0]:  # Meeting Agendas
        render_meeting_agendas()
    
    with tabs[1]:  # Schedule Meetings
        render_meeting_scheduling()
    
    with tabs[2]:  # Action Items
        render_action_items()
    
    with tabs[3]:  # Meeting Minutes
        render_meeting_minutes()
    
    with tabs[4]:  # Meeting Analytics
        render_meeting_analytics()

def render_meeting_agendas():
    """Render meeting agenda templates and management"""
    st.markdown("### 📋 Professional Meeting Agenda Templates")
    st.markdown("**Industry-standard agenda templates for Highland Tower Development**")
    
    # Meeting type selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        meeting_type = st.selectbox(
            "Select Meeting Type",
            [
                "Project Planning Kick-Off Meeting",
                "Weekly Project Coordination",
                "Weekly Subcontractor Foreman Meeting",
                "Weekly Owner Architect Contractor (OAC) Meeting",
                "Design Review Meeting",
                "Contractor Pre-Qualification",
                "Safety Planning Meeting",
                "Progress Review Meeting",
                "Closeout Planning Meeting"
            ],
            key="meeting_type_selector"
        )
    
    with col2:
        if st.button("📄 Download Template", key="download_template"):
            agenda_content = generate_meeting_agenda(meeting_type)
            st.download_button(
                label="💾 Save Agenda",
                data=agenda_content,
                file_name=f"{meeting_type.replace(' ', '_').lower()}_agenda.txt",
                mime="text/plain"
            )
    
    # Display selected agenda template
    st.markdown("---")
    
    if meeting_type == "Project Planning Kick-Off Meeting":
        render_kickoff_meeting_agenda()
    elif meeting_type == "Weekly Project Coordination":
        render_weekly_coordination_agenda()
    elif meeting_type == "Weekly Subcontractor Foreman Meeting":
        render_subcontractor_foreman_agenda()
    elif meeting_type == "Weekly Owner Architect Contractor (OAC) Meeting":
        render_oac_meeting_agenda()
    elif meeting_type == "Design Review Meeting":
        render_design_review_agenda()
    elif meeting_type == "Contractor Pre-Qualification":
        render_contractor_prequalification_agenda()
    elif meeting_type == "Safety Planning Meeting":
        render_safety_planning_agenda()
    elif meeting_type == "Progress Review Meeting":
        render_progress_review_agenda()
    elif meeting_type == "Closeout Planning Meeting":
        render_closeout_planning_agenda()

def render_kickoff_meeting_agenda():
    """Render the Project Planning Kick-Off Meeting agenda based on authentic industry standards"""
    st.markdown("### 🚀 Project Planning Kick-Off Meeting")
    st.markdown("**Highland Tower Development - Initial Project Coordination**")
    
    # Meeting details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📅 Date:** TBD")
        st.markdown("**🕐 Time:** 9:00 AM - 11:00 AM")
    with col2:
        st.markdown("**📍 Location:** Project Office")
        st.markdown("**👥 Attendees:** 8-12 participants")
    with col3:
        st.markdown("**📋 Meeting Lead:** Project Manager")
        st.markdown("**⏱️ Duration:** 2 hours")
    
    st.markdown("---")
    
    # Agenda items with authentic structure from archtoolbox.com
    agenda_items = [
        {
            "time": "9:00 - 9:15",
            "topic": "1. Introductions and Role Definitions",
            "details": [
                "Team member introductions",
                "Role and responsibility clarification",
                "Contact information exchange",
                "Authority levels and decision-making hierarchy"
            ]
        },
        {
            "time": "9:15 - 9:45",
            "topic": "2. Project Overview and Goals",
            "details": [
                "Highland Tower Development scope review",
                "Project objectives and success criteria",
                "Timeline and milestone overview",
                "Budget parameters and constraints"
            ]
        },
        {
            "time": "9:45 - 10:15",
            "topic": "3. Design Process and Schedule",
            "details": [
                "Design phases and deliverables",
                "Review and approval processes",
                "Design development timeline",
                "Coordination requirements"
            ]
        },
        {
            "time": "10:15 - 10:30",
            "topic": "4. Communication Protocols",
            "details": [
                "Meeting schedules and formats",
                "Document sharing procedures",
                "Progress reporting requirements",
                "Issue escalation procedures"
            ]
        },
        {
            "time": "10:30 - 10:45",
            "topic": "5. Project Requirements Review",
            "details": [
                "Building program confirmation",
                "Code and regulatory requirements",
                "Site constraints and opportunities",
                "Sustainability and performance goals"
            ]
        },
        {
            "time": "10:45 - 11:00",
            "topic": "6. Next Steps and Action Items",
            "details": [
                "Immediate action items assignment",
                "Next meeting scheduling",
                "Document distribution plan",
                "Follow-up responsibilities"
            ]
        }
    ]
    
    # Display agenda items
    for item in agenda_items:
        with st.container():
            st.markdown(f"#### {item['time']} - {item['topic']}")
            
            for detail in item['details']:
                st.markdown(f"• {detail}")
            
            st.markdown("")
    
    # Pre-meeting preparation
    st.markdown("---")
    st.markdown("### 📋 Pre-Meeting Preparation")
    
    preparation_items = [
        "Review project contract and scope documents",
        "Prepare team contact information sheets",
        "Gather relevant site surveys and reports",
        "Compile regulatory and code requirements",
        "Prepare project schedule templates",
        "Set up document sharing platforms"
    ]
    
    for item in preparation_items:
        st.markdown(f"• {item}")

def render_weekly_coordination_agenda():
    """Render weekly project coordination meeting agenda"""
    st.markdown("### 📅 Weekly Project Coordination Meeting")
    st.markdown("**Highland Tower Development - Regular Progress Review**")
    
    agenda_items = [
        ("5 min", "1. Safety Moment", ["Recent safety incidents", "Safety reminders", "New safety procedures"]),
        ("10 min", "2. Progress Review", ["Work completed this week", "Current activities", "Upcoming milestones"]),
        ("15 min", "3. Schedule Updates", ["Schedule adherence", "Delays and impacts", "Recovery plans"]),
        ("10 min", "4. Issues and Concerns", ["Current problems", "Resource needs", "Coordination requirements"]),
        ("10 min", "5. Next Week Planning", ["Upcoming activities", "Resource allocation", "Critical path items"]),
        ("5 min", "6. Action Items", ["Review previous actions", "Assign new actions", "Set deadlines"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_subcontractor_foreman_agenda():
    """Render weekly subcontractor foreman meeting agenda"""
    st.markdown("### 👷 Weekly Subcontractor Foreman Meeting")
    st.markdown("**Highland Tower Development - Trade Coordination & Field Operations**")
    
    # Meeting details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📅 Day:** Every Tuesday")
        st.markdown("**🕐 Time:** 7:00 AM - 8:00 AM")
    with col2:
        st.markdown("**📍 Location:** Job Site Trailer")
        st.markdown("**👥 Attendees:** All Trade Foremen")
    with col3:
        st.markdown("**📋 Meeting Lead:** Site Superintendent")
        st.markdown("**⏱️ Duration:** 60 minutes")
    
    st.markdown("---")
    
    agenda_items = [
        ("5 min", "1. Safety First - Jobsite Safety Review", 
         ["Previous week safety incidents or near misses",
          "Current week safety focus areas",
          "New safety requirements or procedures",
          "Safety equipment and PPE updates"]),
        
        ("10 min", "2. Weather & Site Conditions", 
         ["Weekly weather forecast impact",
          "Site access and logistics updates",
          "Material delivery schedules",
          "Temporary facilities status"]),
        
        ("15 min", "3. Trade Progress Reports", 
         ["Each foreman reports on previous week progress",
          "Current phase completion status",
          "Labor productivity and crew status",
          "Material delivery confirmations"]),
        
        ("15 min", "4. Coordination & Sequencing", 
         ["Trade interface coordination",
          "Work area assignments and conflicts",
          "Equipment sharing and scheduling",
          "Utility shutdowns and connections"]),
        
        ("10 min", "5. Quality Control & Inspections", 
         ["Required inspections for current week",
          "Quality issues from previous week",
          "Mock-up approvals and samples",
          "Submittal status updates"]),
        
        ("5 min", "6. Action Items & Next Week Preview", 
         ["Critical tasks for upcoming week",
          "Resource requirements and requests",
          "Milestone deadlines approaching",
          "Follow-up actions assignment"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")
    
    # Trade participation section
    st.markdown("---")
    st.markdown("### 🔧 Required Trade Representation")
    
    trades = [
        "General Contractor Superintendent",
        "Site Safety Manager", 
        "Concrete/Foundation Foreman",
        "Structural Steel Foreman",
        "Framing Foreman",
        "MEP Foremen (Electrical, Plumbing, HVAC)",
        "Drywall/Finishing Foreman",
        "Roofing Foreman",
        "Exterior/Glazing Foreman"
    ]
    
    for trade in trades:
        st.markdown(f"• {trade}")

def render_oac_meeting_agenda():
    """Render weekly Owner Architect Contractor (OAC) meeting agenda"""
    st.markdown("### 🏢 Weekly Owner Architect Contractor (OAC) Meeting")
    st.markdown("**Highland Tower Development - Executive Project Coordination**")
    
    # Meeting details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📅 Day:** Every Thursday")
        st.markdown("**🕐 Time:** 10:00 AM - 11:30 AM")
    with col2:
        st.markdown("**📍 Location:** Highland Properties Office")
        st.markdown("**👥 Attendees:** Senior Project Team")
    with col3:
        st.markdown("**📋 Meeting Lead:** Project Manager")
        st.markdown("**⏱️ Duration:** 90 minutes")
    
    st.markdown("---")
    
    agenda_items = [
        ("10 min", "1. Executive Summary & Project Dashboard", 
         ["Overall project health status",
          "Key performance indicators review",
          "Budget variance summary",
          "Schedule milestone status"]),
        
        ("15 min", "2. Design & Documentation Status", 
         ["Design development progress",
          "Submittal review and approval status",
          "RFI resolution and pending items",
          "Change order proposals and approvals"]),
        
        ("15 min", "3. Construction Progress Review", 
         ["Major milestone completions",
          "Current construction activities",
          "Quality control and inspection results",
          "Substantial completion timeline"]),
        
        ("15 min", "4. Financial & Commercial Items", 
         ["Progress billing and payment status",
          "Change order financial impact",
          "Budget forecast and projections",
          "Cash flow planning"]),
        
        ("10 min", "5. Risk Management & Issues", 
         ["Project risks and mitigation strategies",
          "Regulatory and permitting updates",
          "Weather delays and recovery plans",
          "Long-lead item procurement status"]),
        
        ("10 min", "6. Owner Requirements & Tenant Coordination", 
         ["Tenant improvement coordination",
          "Marketing and leasing schedule alignment",
          "Owner furnished equipment status",
          "Warranty and maintenance planning"]),
        
        ("10 min", "7. Stakeholder Communications", 
         ["Public relations and community impact",
          "City/municipality coordination",
          "Utility company coordination",
          "Marketing milestone achievements"]),
        
        ("5 min", "8. Action Items & Next Steps", 
         ["Decision items requiring owner input",
          "Follow-up actions and accountability",
          "Next meeting agenda items",
          "Executive escalation needs"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")
    
    # Key participants section
    st.markdown("---")
    st.markdown("### 👥 Required OAC Participants")
    
    participants = [
        "Owner Representative - Highland Properties",
        "Project Manager - Construction Team",
        "Principal Architect - Design Team",
        "General Contractor Project Executive",
        "Construction Manager",
        "Owner's Financial Representative",
        "Project Development Manager",
        "Legal Counsel (as needed for major decisions)"
    ]
    
    for participant in participants:
        st.markdown(f"• {participant}")

def render_design_review_agenda():
    """Render design review meeting agenda"""
    st.markdown("### 🎨 Design Review Meeting")
    st.markdown("**Highland Tower Development - Design Phase Coordination**")
    
    agenda_items = [
        ("10 min", "1. Design Presentation", ["Current design status", "Key design decisions", "Design rationale"]),
        ("20 min", "2. Technical Review", ["Code compliance check", "Engineering coordination", "Systems integration"]),
        ("15 min", "3. Stakeholder Feedback", ["Owner comments", "User requirements", "Aesthetic considerations"]),
        ("10 min", "4. Budget Impact", ["Cost implications", "Value engineering opportunities", "Budget alignment"]),
        ("5 min", "5. Next Steps", ["Design revisions needed", "Additional studies required", "Next review date"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_contractor_prequalification_agenda():
    """Render contractor pre-qualification meeting agenda"""
    st.markdown("### 🏗️ Contractor Pre-Qualification Meeting")
    st.markdown("**Highland Tower Development - Contractor Evaluation**")
    
    agenda_items = [
        ("10 min", "1. Company Overview", ["Company history", "Project experience", "Team qualifications"]),
        ("15 min", "2. Project Approach", ["Construction methodology", "Schedule approach", "Quality control"]),
        ("10 min", "3. Safety Program", ["Safety record", "Safety procedures", "Training programs"]),
        ("10 min", "4. Financial Capacity", ["Bonding capacity", "Financial stability", "Insurance coverage"]),
        ("10 min", "5. References", ["Similar projects", "Client references", "Performance history"]),
        ("5 min", "6. Questions & Clarifications", ["Project-specific questions", "Scope clarifications", "Next steps"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_safety_planning_agenda():
    """Render safety planning meeting agenda"""
    st.markdown("### 🦺 Safety Planning Meeting")
    st.markdown("**Highland Tower Development - Safety Program Development**")
    
    agenda_items = [
        ("10 min", "1. Safety Program Overview", ["Site safety plan", "Safety requirements", "Compliance standards"]),
        ("15 min", "2. Hazard Identification", ["Site hazards", "Activity-specific risks", "Environmental concerns"]),
        ("15 min", "3. Safety Procedures", ["Safety protocols", "Emergency procedures", "Training requirements"]),
        ("10 min", "4. Safety Resources", ["Safety equipment", "Personnel requirements", "Inspection schedules"]),
        ("5 min", "5. Implementation Plan", ["Rollout schedule", "Training plan", "Monitoring procedures"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_progress_review_agenda():
    """Render progress review meeting agenda"""
    st.markdown("### 📈 Progress Review Meeting")
    st.markdown("**Highland Tower Development - Monthly Progress Assessment**")
    
    agenda_items = [
        ("15 min", "1. Schedule Performance", ["Progress vs. baseline", "Critical path analysis", "Recovery strategies"]),
        ("15 min", "2. Budget Performance", ["Cost vs. budget", "Change orders", "Financial projections"]),
        ("10 min", "3. Quality Metrics", ["Quality inspections", "Deficiency tracking", "Quality improvements"]),
        ("10 min", "4. Risk Assessment", ["Current risks", "Risk mitigation", "New risk identification"]),
        ("10 min", "5. Stakeholder Updates", ["Owner communication", "Regulatory updates", "Community relations"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_closeout_planning_agenda():
    """Render closeout planning meeting agenda"""
    st.markdown("### 🎯 Closeout Planning Meeting")
    st.markdown("**Highland Tower Development - Project Completion Planning**")
    
    agenda_items = [
        ("15 min", "1. Completion Status", ["Remaining work", "Punch list items", "Completion timeline"]),
        ("15 min", "2. Documentation Requirements", ["As-built drawings", "O&M manuals", "Warranty documents"]),
        ("10 min", "3. Testing and Commissioning", ["System testing", "Performance verification", "Training requirements"]),
        ("10 min", "4. Handover Process", ["Owner training", "Key transfers", "Warranty activation"]),
        ("10 min", "5. Final Deliverables", ["Final documentation", "Project records", "Lessons learned"])
    ]
    
    for time, topic, details in agenda_items:
        st.markdown(f"#### {time} - {topic}")
        for detail in details:
            st.markdown(f"• {detail}")
        st.markdown("")

def render_meeting_scheduling():
    """Render meeting scheduling interface"""
    st.markdown("### 📅 Schedule Project Meetings")
    st.markdown("**Highland Tower Development - Meeting Coordination**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Meeting Details")
        meeting_title = st.text_input("Meeting Title", value="Weekly Project Coordination")
        meeting_date = st.date_input("Meeting Date", value=datetime.now().date() + timedelta(days=1))
        meeting_time = st.time_input("Meeting Time", value=datetime.strptime("09:00", "%H:%M").time())
        duration = st.selectbox("Duration", ["30 minutes", "1 hour", "1.5 hours", "2 hours", "3 hours"])
        location = st.text_input("Location", value="Project Office Conference Room")
    
    with col2:
        st.markdown("#### Attendees")
        attendees = st.multiselect(
            "Select Attendees",
            [
                "Project Manager - Sarah Chen",
                "Architect - Michael Rodriguez", 
                "General Contractor - BuildTech Construction",
                "Owner Representative - Highland Properties",
                "Structural Engineer - Davis Engineering",
                "MEP Engineer - Systems Plus",
                "Safety Manager - John Thompson",
                "Site Superintendent - Mark Wilson"
            ]
        )
        
        meeting_type = st.selectbox(
            "Meeting Type",
            [
                "Project Planning Kick-Off Meeting",
                "Weekly Project Coordination",
                "Weekly Subcontractor Foreman Meeting",
                "Weekly Owner Architect Contractor (OAC) Meeting",
                "Design Review Meeting",
                "Safety Planning Meeting",
                "Progress Review Meeting"
            ]
        )
    
    if st.button("📅 Schedule Meeting"):
        st.success(f"✅ Meeting '{meeting_title}' scheduled for {meeting_date} at {meeting_time}")
        st.info(f"📧 Meeting invitations sent to {len(attendees)} attendees")

def render_action_items():
    """Render action items tracking"""
    st.markdown("### ✅ Action Items Tracking")
    st.markdown("**Highland Tower Development - Meeting Follow-up**")
    
    # Sample action items
    action_items = [
        {
            "id": "AI-001",
            "description": "Submit architectural drawings for city review",
            "assigned_to": "Michael Rodriguez",
            "due_date": "2024-02-15",
            "status": "In Progress",
            "priority": "High",
            "meeting": "Design Review - Jan 30"
        },
        {
            "id": "AI-002", 
            "description": "Finalize geotechnical report recommendations",
            "assigned_to": "Davis Engineering",
            "due_date": "2024-02-10",
            "status": "Completed",
            "priority": "High",
            "meeting": "Project Kick-off - Jan 15"
        },
        {
            "id": "AI-003",
            "description": "Update project schedule with permit timeline",
            "assigned_to": "Sarah Chen",
            "due_date": "2024-02-12",
            "status": "Pending",
            "priority": "Medium",
            "meeting": "Weekly Coordination - Feb 5"
        }
    ]
    
    # Action items table
    df = pd.DataFrame(action_items)
    
    # Status filter
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "In Progress", "Completed", "Overdue"]
    )
    
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    
    st.dataframe(
        df,
        column_config={
            "id": "Action ID",
            "description": "Description",
            "assigned_to": "Assigned To",
            "due_date": "Due Date",
            "status": "Status",
            "priority": "Priority",
            "meeting": "Source Meeting"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Add new action item
    st.markdown("---")
    st.markdown("#### ➕ Add New Action Item")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        new_description = st.text_input("Description")
        new_assigned = st.text_input("Assigned To")
    with col2:
        new_due_date = st.date_input("Due Date")
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    with col3:
        new_meeting = st.text_input("Source Meeting")
        if st.button("➕ Add Action Item"):
            st.success("✅ Action item added successfully!")

def render_meeting_minutes():
    """Render meeting minutes management"""
    st.markdown("### 📝 Meeting Minutes")
    st.markdown("**Highland Tower Development - Meeting Documentation**")
    
    # Recent meetings
    meetings = [
        {
            "date": "2024-02-05",
            "type": "Weekly Coordination",
            "attendees": 8,
            "action_items": 3,
            "status": "Published"
        },
        {
            "date": "2024-01-30", 
            "type": "Design Review",
            "attendees": 6,
            "action_items": 5,
            "status": "Draft"
        },
        {
            "date": "2024-01-15",
            "type": "Project Kick-off",
            "attendees": 12,
            "action_items": 8,
            "status": "Published"
        }
    ]
    
    st.markdown("#### Recent Meeting Minutes")
    
    for meeting in meetings:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{meeting['type']}**")
                st.markdown(f"📅 {meeting['date']}")
            with col2:
                st.markdown(f"👥 {meeting['attendees']} attendees")
            with col3:
                st.markdown(f"✅ {meeting['action_items']} actions")
            with col4:
                if meeting['status'] == 'Published':
                    st.success(f"📄 {meeting['status']}")
                else:
                    st.warning(f"📝 {meeting['status']}")
            
            st.markdown("---")

def render_meeting_analytics():
    """Render meeting analytics and metrics"""
    st.markdown("### 📊 Meeting Analytics")
    st.markdown("**Highland Tower Development - Meeting Performance Metrics**")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Meetings", "24", "3")
    with col2:
        st.metric("Avg Attendance", "87%", "5%")
    with col3:
        st.metric("Action Items", "47", "8")
    with col4:
        st.metric("Completion Rate", "89%", "7%")
    
    # Charts would go here in a real implementation
    st.markdown("#### Meeting Frequency by Type")
    st.info("📈 Weekly Coordination: 12 meetings | Design Reviews: 6 meetings | Safety Meetings: 4 meetings")
    
    st.markdown("#### Action Item Completion Trends")
    st.info("📈 Average completion time: 5.2 days | On-time completion: 89%")

def generate_meeting_agenda(meeting_type):
    """Generate downloadable meeting agenda content"""
    
    agenda_templates = {
        "Project Planning Kick-Off Meeting": """
HIGHLAND TOWER DEVELOPMENT
PROJECT PLANNING KICK-OFF MEETING AGENDA

Date: [TBD]
Time: 9:00 AM - 11:00 AM
Location: Project Office
Meeting Lead: Project Manager

AGENDA ITEMS:

9:00 - 9:15   1. INTRODUCTIONS AND ROLE DEFINITIONS
              • Team member introductions
              • Role and responsibility clarification
              • Contact information exchange
              • Authority levels and decision-making hierarchy

9:15 - 9:45   2. PROJECT OVERVIEW AND GOALS
              • Highland Tower Development scope review
              • Project objectives and success criteria
              • Timeline and milestone overview
              • Budget parameters and constraints

9:45 - 10:15  3. DESIGN PROCESS AND SCHEDULE
              • Design phases and deliverables
              • Review and approval processes
              • Design development timeline
              • Coordination requirements

10:15 - 10:30 4. COMMUNICATION PROTOCOLS
              • Meeting schedules and formats
              • Document sharing procedures
              • Progress reporting requirements
              • Issue escalation procedures

10:30 - 10:45 5. PROJECT REQUIREMENTS REVIEW
              • Building program confirmation
              • Code and regulatory requirements
              • Site constraints and opportunities
              • Sustainability and performance goals

10:45 - 11:00 6. NEXT STEPS AND ACTION ITEMS
              • Immediate action items assignment
              • Next meeting scheduling
              • Document distribution plan
              • Follow-up responsibilities

PRE-MEETING PREPARATION:
• Review project contract and scope documents
• Prepare team contact information sheets
• Gather relevant site surveys and reports
• Compile regulatory and code requirements
• Prepare project schedule templates
• Set up document sharing platforms
""",
        "Weekly Project Coordination": """
HIGHLAND TOWER DEVELOPMENT
WEEKLY PROJECT COORDINATION MEETING AGENDA

Date: [TBD]
Time: [TBD]
Location: Project Office
Duration: 45 minutes

AGENDA ITEMS:

5 min    1. SAFETY MOMENT
         • Recent safety incidents
         • Safety reminders
         • New safety procedures

10 min   2. PROGRESS REVIEW
         • Work completed this week
         • Current activities
         • Upcoming milestones

15 min   3. SCHEDULE UPDATES
         • Schedule adherence
         • Delays and impacts
         • Recovery plans

10 min   4. ISSUES AND CONCERNS
         • Current problems
         • Resource needs
         • Coordination requirements

10 min   5. NEXT WEEK PLANNING
         • Upcoming activities
         • Resource allocation
         • Critical path items

5 min    6. ACTION ITEMS
         • Review previous actions
         • Assign new actions
         • Set deadlines
""",
        "Weekly Subcontractor Foreman Meeting": """
HIGHLAND TOWER DEVELOPMENT
WEEKLY SUBCONTRACTOR FOREMAN MEETING AGENDA

Day: Every Tuesday
Time: 7:00 AM - 8:00 AM
Location: Job Site Trailer
Meeting Lead: Site Superintendent
Duration: 60 minutes

AGENDA ITEMS:

5 min    1. SAFETY FIRST - JOBSITE SAFETY REVIEW
         • Previous week safety incidents or near misses
         • Current week safety focus areas
         • New safety requirements or procedures
         • Safety equipment and PPE updates

10 min   2. WEATHER & SITE CONDITIONS
         • Weekly weather forecast impact
         • Site access and logistics updates
         • Material delivery schedules
         • Temporary facilities status

15 min   3. TRADE PROGRESS REPORTS
         • Each foreman reports on previous week progress
         • Current phase completion status
         • Labor productivity and crew status
         • Material delivery confirmations

15 min   4. COORDINATION & SEQUENCING
         • Trade interface coordination
         • Work area assignments and conflicts
         • Equipment sharing and scheduling
         • Utility shutdowns and connections

10 min   5. QUALITY CONTROL & INSPECTIONS
         • Required inspections for current week
         • Quality issues from previous week
         • Mock-up approvals and samples
         • Submittal status updates

5 min    6. ACTION ITEMS & NEXT WEEK PREVIEW
         • Critical tasks for upcoming week
         • Resource requirements and requests
         • Milestone deadlines approaching
         • Follow-up actions assignment

REQUIRED TRADE REPRESENTATION:
• General Contractor Superintendent
• Site Safety Manager
• Concrete/Foundation Foreman
• Structural Steel Foreman
• Framing Foreman
• MEP Foremen (Electrical, Plumbing, HVAC)
• Drywall/Finishing Foreman
• Roofing Foreman
• Exterior/Glazing Foreman
""",
        "Weekly Owner Architect Contractor (OAC) Meeting": """
HIGHLAND TOWER DEVELOPMENT
WEEKLY OWNER ARCHITECT CONTRACTOR (OAC) MEETING AGENDA

Day: Every Thursday
Time: 10:00 AM - 11:30 AM
Location: Highland Properties Office
Meeting Lead: Project Manager
Duration: 90 minutes

AGENDA ITEMS:

10 min   1. EXECUTIVE SUMMARY & PROJECT DASHBOARD
         • Overall project health status
         • Key performance indicators review
         • Budget variance summary
         • Schedule milestone status

15 min   2. DESIGN & DOCUMENTATION STATUS
         • Design development progress
         • Submittal review and approval status
         • RFI resolution and pending items
         • Change order proposals and approvals

15 min   3. CONSTRUCTION PROGRESS REVIEW
         • Major milestone completions
         • Current construction activities
         • Quality control and inspection results
         • Substantial completion timeline

15 min   4. FINANCIAL & COMMERCIAL ITEMS
         • Progress billing and payment status
         • Change order financial impact
         • Budget forecast and projections
         • Cash flow planning

10 min   5. RISK MANAGEMENT & ISSUES
         • Project risks and mitigation strategies
         • Regulatory and permitting updates
         • Weather delays and recovery plans
         • Long-lead item procurement status

10 min   6. OWNER REQUIREMENTS & TENANT COORDINATION
         • Tenant improvement coordination
         • Marketing and leasing schedule alignment
         • Owner furnished equipment status
         • Warranty and maintenance planning

10 min   7. STAKEHOLDER COMMUNICATIONS
         • Public relations and community impact
         • City/municipality coordination
         • Utility company coordination
         • Marketing milestone achievements

5 min    8. ACTION ITEMS & NEXT STEPS
         • Decision items requiring owner input
         • Follow-up actions and accountability
         • Next meeting agenda items
         • Executive escalation needs

REQUIRED OAC PARTICIPANTS:
• Owner Representative - Highland Properties
• Project Manager - Construction Team
• Principal Architect - Design Team
• General Contractor Project Executive
• Construction Manager
• Owner's Financial Representative
• Project Development Manager
• Legal Counsel (as needed for major decisions)
"""
    }
    
    return agenda_templates.get(meeting_type, "Agenda template not available for this meeting type.")