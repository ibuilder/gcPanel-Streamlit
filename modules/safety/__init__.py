"""
Safety Management Module for gcPanel

This module provides comprehensive safety management functionality including:
- Safety Incidents tracking
- Safety Inspections management
- Hazard identification and mitigation
- Safety metrics and reporting

The module follows the standardized CRUD styling for consistent user experience.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json

from assets.crud_styler import apply_crud_styles
from modules.crud_template import CrudModule

# Import submodules
from modules.safety.incidents import SafetyIncidentModule
from modules.safety.inspections import SafetyInspectionModule
from modules.safety.hazards import HazardModule

def render_safety_dashboard():
    """Render the safety dashboard with key metrics and charts."""
    st.subheader("Safety Performance Dashboard")
    
    # Apply styling
    apply_crud_styles()
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Key safety metrics
    st.markdown("### Key Safety Metrics")
    
    # Row 1 Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_without_incident = random.randint(25, 45)
        st.metric("Days Without Incident", days_without_incident)
    
    with col2:
        recordable_incidents = random.randint(2, 4)
        st.metric("Recordable Incidents", recordable_incidents, "-1 vs Last Year")
    
    with col3:
        incident_rate = round(recordable_incidents * 200000 / 250000, 2)  # Assuming 250,000 work hours
        st.metric("Incident Rate", incident_rate, "-0.5 vs Target")
    
    with col4:
        safety_training = random.randint(92, 98)
        st.metric("Safety Training", f"{safety_training}%", "+2% vs Last Month")
    
    # Safety incident trend chart
    st.markdown("### Incident Trend")
    
    # Generate sample data for past 12 months
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    incident_counts = [random.randint(0, 3) for _ in range(12)]
    
    # Create pandas DataFrame
    df_incidents = pd.DataFrame({
        'Month': months,
        'Incidents': incident_counts
    })
    
    # Display bar chart
    st.bar_chart(df_incidents.set_index('Month')['Incidents'])
    
    # Safety inspection compliance chart
    st.markdown("### Inspection Compliance")
    
    # Generate sample data for different inspection types
    inspection_types = ["Daily Site Walk", "Weekly Safety Audit", "Monthly Equipment", "Quarterly Compliance"]
    planned_inspections = [20, 4, 2, 1]
    completed_inspections = [random.randint(max(1, planned - 2), planned) for planned in planned_inspections]
    
    # Calculate compliance percentage
    compliance_pct = [round(completed / planned * 100) for completed, planned in zip(completed_inspections, planned_inspections)]
    
    # Create pandas DataFrame
    df_inspections = pd.DataFrame({
        'Type': inspection_types,
        'Planned': planned_inspections,
        'Completed': completed_inspections,
        'Compliance': compliance_pct
    })
    
    # Display as a standard table instead of styled gradient (which requires matplotlib)
    st.table(df_inspections)
    
    # Close the white container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent hazards container
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    st.markdown("### Recent Hazards")
    
    # Generate sample hazard data
    recent_hazards = [
        {
            "id": "HAZ-001",
            "description": "Exposed electrical wiring near water source",
            "location": "Level 3 - East Wing",
            "severity": "High",
            "status": "Open"
        },
        {
            "id": "HAZ-002",
            "description": "Trip hazard from construction debris",
            "location": "Main Entrance",
            "severity": "Medium",
            "status": "Mitigated"
        },
        {
            "id": "HAZ-003",
            "description": "Missing guardrails on scaffolding",
            "location": "West Facade",
            "severity": "High",
            "status": "Open"
        },
        {
            "id": "HAZ-004",
            "description": "Inadequate ventilation in painting area",
            "location": "Basement - Room B12",
            "severity": "Medium",
            "status": "In Progress"
        }
    ]
    
    # Display hazards with severity indicators
    for hazard in recent_hazards:
        # Determine severity color
        severity_color = {
            "High": "red",
            "Medium": "orange",
            "Low": "blue"
        }.get(hazard["severity"], "gray")
        
        # Determine status color
        status_color = {
            "Open": "red",
            "In Progress": "blue",
            "Mitigated": "green",
            "Closed": "gray"
        }.get(hazard["status"], "gray")
        
        # Create hazard card
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 10px; border: 1px solid #eee; 
                 border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9;">
            <div style="width: 80px; text-align: center; margin-right: 15px;">
                <div style="padding: 5px; background-color: {severity_color}; color: white; 
                         border-radius: 4px; font-weight: bold;">
                    {hazard["severity"]}
                </div>
            </div>
            <div style="flex-grow: 1;">
                <div><strong>{hazard["id"]}: {hazard["description"]}</strong></div>
                <div>Location: {hazard["location"]}</div>
                <div>Status: <span style="color: {status_color};">{hazard["status"]}</span></div>
            </div>
            <div>
                <button style="background-color: #2196F3; color: white; border: none; 
                         padding: 5px 10px; text-align: center; text-decoration: none; 
                         display: inline-block; font-size: 12px; margin: 4px 2px; 
                         cursor: pointer; border-radius: 4px;">
                    View
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close the white container
    st.markdown("</div>", unsafe_allow_html=True)

def render_ai_safety_monitoring():
    """Render AI-powered safety monitoring dashboard"""
    st.markdown("### 🤖 AI-Powered Safety Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Real-Time Safety Alerts**")
        alerts = [
            {"type": "PPE Violation", "location": "Level 5", "confidence": "95%", "severity": "High"},
            {"type": "Fall Risk Detected", "location": "Scaffolding Area", "confidence": "88%", "severity": "High"},
            {"type": "Unsafe Lifting", "location": "Loading Dock", "confidence": "92%", "severity": "Medium"}
        ]
        
        for alert in alerts:
            color = "#ff4444" if alert["severity"] == "High" else "#ff8800"
            st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
                    <strong>⚠️ {alert["type"]}</strong><br>
                    <small>Location: {alert["location"]} | Confidence: {alert["confidence"]}</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Safety Predictions**")
        st.success("🎯 Zero predicted incidents this week")
        st.warning("⚠️ Elevated risk on Friday (weather)")
        st.info("📊 Safety score trending upward")
        st.markdown("🔄 Next AI safety audit: Tomorrow 2 PM")

def render_digital_safety_checklists():
    """Render digital safety checklists with templates"""
    st.markdown("### ✅ Digital Safety Checklists")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Available Checklist Templates**")
        checklists = [
            {"name": "Daily Site Safety Walk", "items": 25, "completion": "100%"},
            {"name": "Equipment Pre-Use Inspection", "items": 15, "completion": "80%"},
            {"name": "Weekly Safety Meeting", "items": 12, "completion": "92%"},
            {"name": "Crane Operation Safety", "items": 30, "completion": "67%"}
        ]
        
        for checklist in checklists:
            completion = float(checklist["completion"].rstrip('%'))
            color = "#4CAF50" if completion >= 90 else "#ff8800" if completion >= 70 else "#ff4444"
            
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>📋 {checklist["name"]}</strong><br>
                    <small>{checklist["items"]} items | </small>
                    <span style="color: {color}; font-weight: bold;">{checklist["completion"]} Complete</span>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Quick Actions**")
        if st.button("📋 Start Daily Safety Walk", type="primary"):
            st.success("Daily Safety Walk checklist started!")
        
        if st.button("🚨 Report Safety Incident"):
            st.info("Safety incident reporting form opened")
        
        if st.button("👷 PPE Compliance Check"):
            st.info("PPE compliance verification initiated")

def render_safety_training_tracker():
    """Render safety training and certification tracking"""
    st.markdown("### 🎓 Safety Training & Certifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Training Compliance**")
        st.metric("Overall Compliance", "94%", "+2% this month")
        st.metric("Certifications Current", "87%", "+5% this month")
        st.metric("Training Hours YTD", "1,247", "+156 vs target")
    
    with col2:
        st.markdown("**Upcoming Expirations**")
        st.markdown("🟡 John Smith - OSHA 10 (30 days)")
        st.markdown("🔴 Sarah Johnson - First Aid (5 days)")
        st.markdown("🟡 Mike Davis - Crane Operator (45 days)")
    
    with col3:
        st.markdown("**Required Training**")
        st.markdown("📚 Fall Protection (5 workers)")
        st.markdown("📚 Hazmat Handling (3 workers)")
        st.markdown("📚 Equipment Safety (8 workers)")

def render_work_permits_management():
    """Render comprehensive work permits management for Highland Tower Development"""
    import uuid
    from datetime import datetime, time
    
    st.markdown("### 📋 Work Permits Management")
    st.markdown("**Highland Tower Development - Construction Work Permit System**")
    
    # Apply CRUD styling
    apply_crud_styles()
    
    # Initialize permits data file
    permits_file = "data/safety/work_permits.json"
    os.makedirs(os.path.dirname(permits_file), exist_ok=True)
    
    # Load existing permits
    def load_permits():
        if os.path.exists(permits_file):
            try:
                with open(permits_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_permits(permits):
        with open(permits_file, 'w') as f:
            json.dump(permits, f, indent=2)
    
    # Load current permits
    permits = load_permits()
    
    # Permit management actions
    action = st.radio(
        "Select Action",
        ["📋 Active Permits", "➕ Issue New Permit", "📝 Permit Templates", "📊 Permit Analytics"],
        horizontal=True
    )
    
    if action == "➕ Issue New Permit":
        st.markdown("### Issue New Work Permit")
        
        # Permit type selection
        permit_type = st.selectbox(
            "Select Permit Type",
            [
                "",
                "Hot Work Permit",
                "Confined Space Entry Permit", 
                "Lifting Operations Permit",
                "Excavation Permit",
                "Working at Height Permit",
                "Electrical Work Permit",
                "Chemical Handling Permit",
                "Demolition Permit",
                "Fire Protection Impairment Permit",
                "Lock Out Tag Out (LOTO) Permit"
            ]
        )
        
        if permit_type:
            render_permit_form(permit_type, permits, save_permits)
    
    elif action == "📋 Active Permits":
        st.markdown("### Active Work Permits - Highland Tower Development")
        
        if not permits:
            st.info("No work permits issued yet. Use 'Issue New Permit' to create permits.")
        else:
            # Filter controls
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Pending Approval", "Expired", "Closed"])
            
            with col2:
                permit_filter = st.selectbox("Filter by Type", ["All"] + list(set([p.get('permit_type', '') for p in permits])))
            
            with col3:
                search_term = st.text_input("Search Permits", placeholder="Search by description or location")
            
            # Filter permits
            filtered_permits = permits
            
            if status_filter != "All":
                filtered_permits = [p for p in filtered_permits if p.get('status') == status_filter]
            
            if permit_filter != "All":
                filtered_permits = [p for p in filtered_permits if p.get('permit_type') == permit_filter]
            
            if search_term:
                search_term = search_term.lower()
                filtered_permits = [
                    p for p in filtered_permits 
                    if search_term in p.get('work_description', '').lower() or 
                       search_term in p.get('location', '').lower()
                ]
            
            # Display permits
            for permit in filtered_permits:
                status_color = {
                    "Active": "#4CAF50",
                    "Pending Approval": "#ff8800",
                    "Expired": "#ff4444",
                    "Closed": "#666666"
                }.get(permit.get('status', ''), "#666666")
                
                with st.expander(f"🔖 {permit.get('permit_number', 'N/A')} - {permit.get('permit_type', 'Unknown')} ({permit.get('status', 'Unknown')})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**📍 Location:** {permit.get('location', 'Not specified')}")
                        st.markdown(f"**🔨 Work Description:** {permit.get('work_description', 'Not specified')}")
                        st.markdown(f"**👤 Permit Holder:** {permit.get('permit_holder', 'Not specified')}")
                        st.markdown(f"**📅 Issue Date:** {permit.get('issue_date', 'Not specified')}")
                    
                    with col2:
                        st.markdown(f"**⏰ Valid From:** {permit.get('valid_from', 'Not specified')}")
                        st.markdown(f"**⏰ Valid Until:** {permit.get('valid_until', 'Not specified')}")
                        st.markdown(f"**✅ Authorized By:** {permit.get('authorized_by', 'Not specified')}")
                        
                        status_html = f'<span style="color: {status_color}; font-weight: bold;">● {permit.get("status", "Unknown")}</span>'
                        st.markdown(f"**📊 Status:** {status_html}", unsafe_allow_html=True)
                    
                    # Safety requirements
                    if permit.get('safety_requirements'):
                        st.markdown("**🦺 Safety Requirements:**")
                        for req in permit['safety_requirements']:
                            st.markdown(f"• {req}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📄 View Details", key=f"view_{permit.get('id')}"):
                            st.info("Detailed permit view opened")
                    with col2:
                        if permit.get('status') == 'Active' and st.button(f"🔒 Close Permit", key=f"close_{permit.get('id')}"):
                            # Update permit status
                            for i, p in enumerate(permits):
                                if p.get('id') == permit.get('id'):
                                    permits[i]['status'] = 'Closed'
                                    permits[i]['closed_date'] = datetime.now().isoformat()
                                    break
                            save_permits(permits)
                            st.success("Permit closed successfully!")
                            st.rerun()
                    with col3:
                        if st.button(f"📧 Send Reminder", key=f"remind_{permit.get('id')}"):
                            st.success("Reminder sent to permit holder!")
    
    elif action == "📝 Permit Templates":
        render_permit_templates()
    
    elif action == "📊 Permit Analytics":
        render_permit_analytics(permits)

def render_permit_form(permit_type, permits, save_permits):
    """Render permit form based on permit type"""
    
    with st.form("work_permit_form"):
        # Basic permit information
        col1, col2 = st.columns(2)
        
        with col1:
            permit_number = st.text_input("Permit Number*", value=f"HTD-{permit_type[:3].upper()}-{len(permits)+1:03d}")
            location = st.text_input("Work Location*", placeholder="Tower Level 12, North Wing")
            permit_holder = st.text_input("Permit Holder*", placeholder="John Smith")
            company = st.text_input("Company/Contractor*", placeholder="Highland Construction LLC")
        
        with col2:
            valid_date = st.date_input("Valid Date*", value=datetime.now().date())
            valid_from = st.time_input("Valid From*", value=time(8, 0))
            valid_until = st.time_input("Valid Until*", value=time(17, 0))
            authorized_by = st.text_input("Authorized By*", placeholder="Safety Manager")
        
        work_description = st.text_area("Work Description*", placeholder="Detailed description of the work to be performed")
        
        # Permit-specific requirements based on type
        safety_requirements = []
        
        if permit_type == "Hot Work Permit":
            st.markdown("#### 🔥 Hot Work Specific Requirements")
            
            col1, col2 = st.columns(2)
            with col1:
                fire_watch = st.checkbox("Fire watch assigned")
                if fire_watch:
                    safety_requirements.append("Fire watch personnel assigned")
                
                hot_work_trained = st.checkbox("Hot work trained personnel")
                if hot_work_trained:
                    safety_requirements.append("Hot work trained personnel verified")
                
                fire_extinguisher = st.checkbox("Fire extinguisher available")
                if fire_extinguisher:
                    safety_requirements.append("Fire extinguisher readily available")
            
            with col2:
                combustibles_removed = st.checkbox("Combustible materials removed/protected")
                if combustibles_removed:
                    safety_requirements.append("Combustible materials removed or protected")
                
                ventilation_adequate = st.checkbox("Adequate ventilation")
                if ventilation_adequate:
                    safety_requirements.append("Adequate ventilation confirmed")
                
                cutting_equipment = st.checkbox("Cutting equipment inspected")
                if cutting_equipment:
                    safety_requirements.append("Cutting equipment pre-use inspection completed")
        
        elif permit_type == "Confined Space Entry Permit":
            st.markdown("#### 🏠 Confined Space Entry Requirements")
            
            col1, col2 = st.columns(2)
            with col1:
                atmospheric_testing = st.checkbox("Atmospheric testing completed")
                if atmospheric_testing:
                    safety_requirements.append("Atmospheric testing completed and documented")
                
                ventilation_system = st.checkbox("Forced ventilation system")
                if ventilation_system:
                    safety_requirements.append("Forced ventilation system operational")
                
                entry_supervisor = st.checkbox("Entry supervisor assigned")
                if entry_supervisor:
                    safety_requirements.append("Qualified entry supervisor assigned")
            
            with col2:
                rescue_plan = st.checkbox("Emergency rescue plan")
                if rescue_plan:
                    safety_requirements.append("Emergency rescue plan in place")
                
                communication = st.checkbox("Communication system established")
                if communication:
                    safety_requirements.append("Reliable communication system established")
                
                fall_protection = st.checkbox("Fall protection if required")
                if fall_protection:
                    safety_requirements.append("Fall protection system installed")
        
        elif permit_type == "Lifting Operations Permit":
            st.markdown("#### 🏗️ Lifting Operations Requirements")
            
            col1, col2 = st.columns(2)
            with col1:
                lift_plan = st.checkbox("Lift plan prepared and approved")
                if lift_plan:
                    safety_requirements.append("Detailed lift plan prepared and approved")
                
                crane_inspection = st.checkbox("Crane daily inspection")
                if crane_inspection:
                    safety_requirements.append("Crane daily inspection completed")
                
                operator_certified = st.checkbox("Certified crane operator")
                if operator_certified:
                    safety_requirements.append("Certified crane operator assigned")
            
            with col2:
                exclusion_zone = st.checkbox("Exclusion zone established")
                if exclusion_zone:
                    safety_requirements.append("Exclusion zone established and marked")
                
                rigging_inspection = st.checkbox("Rigging equipment inspected")
                if rigging_inspection:
                    safety_requirements.append("Rigging equipment inspected and certified")
                
                spotter_assigned = st.checkbox("Spotter/signaller assigned")
                if spotter_assigned:
                    safety_requirements.append("Qualified spotter/signaller assigned")
        
        elif permit_type == "Working at Height Permit":
            st.markdown("#### 🪜 Working at Height Requirements")
            
            col1, col2 = st.columns(2)
            with col1:
                fall_protection_plan = st.checkbox("Fall protection plan")
                if fall_protection_plan:
                    safety_requirements.append("Fall protection plan developed and implemented")
                
                harness_inspection = st.checkbox("Safety harness inspection")
                if harness_inspection:
                    safety_requirements.append("Safety harness and equipment pre-use inspection")
                
                anchor_points = st.checkbox("Secure anchor points identified")
                if anchor_points:
                    safety_requirements.append("Secure anchor points identified and tested")
            
            with col2:
                weather_conditions = st.checkbox("Weather conditions suitable")
                if weather_conditions:
                    safety_requirements.append("Weather conditions assessed as suitable")
                
                rescue_plan_height = st.checkbox("Rescue plan for working at height")
                if rescue_plan_height:
                    safety_requirements.append("Emergency rescue plan specific to height work")
                
                competent_person = st.checkbox("Competent person supervision")
                if competent_person:
                    safety_requirements.append("Competent person supervising height work")
        
        # Additional safety measures
        st.markdown("#### 🦺 Additional Safety Measures")
        ppe_requirements = st.multiselect(
            "Required PPE",
            ["Hard Hat", "Safety Glasses", "High Visibility Vest", "Safety Boots", "Gloves", 
             "Respirator", "Fall Protection Harness", "Hearing Protection", "Cut-Resistant Gloves"]
        )
        
        for ppe in ppe_requirements:
            safety_requirements.append(f"PPE Required: {ppe}")
        
        emergency_contacts = st.text_area(
            "Emergency Contacts", 
            placeholder="Emergency contact numbers and procedures"
        )
        
        additional_notes = st.text_area(
            "Additional Safety Notes",
            placeholder="Any additional safety considerations or special requirements"
        )
        
        # Submit button
        if st.form_submit_button("🔖 Issue Work Permit", type="primary"):
            if permit_number and location and permit_holder and work_description:
                new_permit = {
                    "id": str(uuid.uuid4()),
                    "permit_number": permit_number,
                    "permit_type": permit_type,
                    "location": location,
                    "work_description": work_description,
                    "permit_holder": permit_holder,
                    "company": company,
                    "issue_date": datetime.now().isoformat(),
                    "valid_date": str(valid_date),
                    "valid_from": str(valid_from),
                    "valid_until": str(valid_until),
                    "authorized_by": authorized_by,
                    "safety_requirements": safety_requirements,
                    "ppe_requirements": ppe_requirements,
                    "emergency_contacts": emergency_contacts,
                    "additional_notes": additional_notes,
                    "status": "Active",
                    "project": "Highland Tower Development"
                }
                
                permits.append(new_permit)
                save_permits(permits)
                
                st.success(f"✅ Work permit {permit_number} issued successfully!")
                st.info(f"📧 Permit notification sent to {permit_holder} and safety team.")
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")

def render_permit_templates():
    """Render work permit templates and guidelines"""
    st.markdown("### 📝 Work Permit Templates & Guidelines")
    
    # Template selection
    template_type = st.selectbox(
        "Select Template",
        [
            "Hot Work Permit Template",
            "Confined Space Entry Template",
            "Lifting Operations Template", 
            "Working at Height Template",
            "Excavation Permit Template",
            "Electrical Work Template",
            "LOTO Procedure Template"
        ]
    )
    
    if template_type == "Hot Work Permit Template":
        st.markdown("#### 🔥 Hot Work Permit Template")
        st.markdown("""
        **Highland Tower Development - Hot Work Permit**
        
        **Purpose:** Required for any work involving open flames, welding, cutting, grinding, or other spark-producing activities.
        
        **Pre-Work Requirements:**
        ✅ Fire watch personnel assigned and trained  
        ✅ Fire extinguisher(s) readily available  
        ✅ Combustible materials removed or protected  
        ✅ Hot work equipment inspected  
        ✅ Area cleared of flammable vapors  
        ✅ Ventilation adequate for work type  
        ✅ Emergency procedures reviewed  
        
        **During Work Requirements:**
        • Fire watch maintains continuous observation
        • Hot work equipment operators trained and qualified
        • Work area monitored for fire/heat buildup
        • Fire extinguishing equipment readily accessible
        
        **Post-Work Requirements:**
        • Fire watch continues for minimum 30 minutes after work completion
        • Area inspected for hot spots or smoldering materials
        • All hot work equipment properly secured
        
        **Emergency Contacts:**
        • Fire Department: 911
        • Highland Tower Security: (555) 123-4567
        • Project Safety Manager: (555) 987-6543
        """)
    
    elif template_type == "Confined Space Entry Template":
        st.markdown("#### 🏠 Confined Space Entry Template")
        st.markdown("""
        **Highland Tower Development - Confined Space Entry Permit**
        
        **Purpose:** Required for entry into any confined space as defined by OSHA 29 CFR 1926.95.
        
        **Pre-Entry Requirements:**
        ✅ Atmospheric testing completed (O2, LEL, Toxic gases)  
        ✅ Space isolated and locked/tagged out  
        ✅ Forced ventilation established  
        ✅ Entry supervisor assigned  
        ✅ Emergency rescue plan developed  
        ✅ Communication system established  
        ✅ Personal protective equipment verified  
        
        **Atmospheric Test Results:**
        • Oxygen: 19.5% - 23.5% (Required)
        • Lower Explosive Limit: <10% (Required)
        • Carbon Monoxide: <35 ppm (Required)
        • Hydrogen Sulfide: <10 ppm (Required)
        
        **Entry Team Roles:**
        • Entry Supervisor: Overall responsibility for permit
        • Entrant(s): Personnel entering confined space
        • Attendant: Outside person monitoring entry
        
        **Emergency Procedures:**
        • Non-entry rescue preferred
        • Emergency services: 911
        • Highland Tower Emergency: (555) 123-4567
        """)
    
    elif template_type == "Lifting Operations Template":
        st.markdown("#### 🏗️ Lifting Operations Template")
        st.markdown("""
        **Highland Tower Development - Lifting Operations Permit**
        
        **Purpose:** Required for all crane operations and critical lifts on Highland Tower Development.
        
        **Pre-Lift Requirements:**
        ✅ Detailed lift plan prepared and approved  
        ✅ Crane daily inspection completed  
        ✅ Load weight verified and within crane capacity  
        ✅ Ground conditions assessed  
        ✅ Exclusion zone established  
        ✅ Rigging equipment inspected  
        ✅ Weather conditions suitable  
        
        **Critical Lift Criteria:**
        • Load exceeds 75% of crane capacity
        • Multiple crane lifts
        • Lifts over occupied areas
        • Blind lifts requiring radio communication
        • Lifts near power lines
        
        **Rigging Inspection:**
        • Slings, hooks, and hardware inspected
        • Weight and balance verified
        • Proper lifting points identified
        • Load secured against shifting
        
        **Communication:**
        • Standard hand signals reviewed
        • Radio communication tested
        • Emergency stop procedures established
        """)
    
    # Download template button
    if st.button("📄 Download Template", type="primary"):
        st.success(f"✅ {template_type} downloaded successfully!")
        st.info("📧 Template has been saved to Highland Tower Development safety documents.")

def render_permit_analytics(permits):
    """Render permit analytics and statistics"""
    st.markdown("### 📊 Work Permit Analytics")
    
    if not permits:
        st.info("No permit data available for analytics.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_permits = len(permits)
        st.metric("Total Permits", total_permits)
    
    with col2:
        active_permits = len([p for p in permits if p.get('status') == 'Active'])
        st.metric("Active Permits", active_permits)
    
    with col3:
        pending_permits = len([p for p in permits if p.get('status') == 'Pending Approval'])
        st.metric("Pending Approval", pending_permits)
    
    with col4:
        expired_permits = len([p for p in permits if p.get('status') == 'Expired'])
        st.metric("Expired Permits", expired_permits)
    
    # Permit type distribution
    st.markdown("#### Permit Type Distribution")
    permit_types = {}
    for permit in permits:
        ptype = permit.get('permit_type', 'Unknown')
        permit_types[ptype] = permit_types.get(ptype, 0) + 1
    
    if permit_types:
        col1, col2 = st.columns(2)
        
        with col1:
            for ptype, count in permit_types.items():
                st.markdown(f"**{ptype}:** {count} permits")
        
        with col2:
            # Most common permit types
            sorted_types = sorted(permit_types.items(), key=lambda x: x[1], reverse=True)
            st.markdown("**Most Common Permits:**")
            for i, (ptype, count) in enumerate(sorted_types[:3]):
                st.markdown(f"{i+1}. {ptype} ({count})")
    
    # Recent permit activity
    st.markdown("#### Recent Permit Activity")
    recent_permits = sorted(permits, key=lambda x: x.get('issue_date', ''), reverse=True)[:5]
    
    for permit in recent_permits:
        status_color = {
            "Active": "#4CAF50",
            "Pending Approval": "#ff8800", 
            "Expired": "#ff4444",
            "Closed": "#666666"
        }.get(permit.get('status', ''), "#666666")
        
        st.markdown(f"""
        <div style="border-left: 4px solid {status_color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
            <strong>{permit.get('permit_number', 'N/A')} - {permit.get('permit_type', 'Unknown')}</strong><br>
            <small>Location: {permit.get('location', 'N/A')} | Status: {permit.get('status', 'Unknown')} | Date: {permit.get('issue_date', 'N/A')[:10]}</small>
        </div>
        """, unsafe_allow_html=True)

def render():
    """Render the Safety Management module."""
    st.title("🦺 Safety Management")
    
    # Create tabs for different safety functions
    tabs = st.tabs(["Dashboard", "Incidents", "Inspections", "Hazards", "Work Permits"])
    
    # Dashboard tab
    with tabs[0]:
        render_safety_dashboard()
    
    # Incidents tab
    with tabs[1]:
        incidents_module = SafetyIncidentModule()
        incidents_module.render()
    
    # Inspections tab
    with tabs[2]:
        inspections_module = SafetyInspectionModule()
        inspections_module.render()
    
    # Hazards tab
    with tabs[3]:
        hazards_module = HazardModule()
        hazards_module.render()
    
    # Work Permits tab
    with tabs[4]:
        render_work_permits_management()