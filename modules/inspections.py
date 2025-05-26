"""
Inspections Module for Highland Tower Development
Comprehensive quality control and inspection management system
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def render():
    """Render comprehensive inspection management system"""
    
    st.title("🔍 Inspections - Highland Tower Development")
    st.markdown("**Professional quality control and inspection management for $45.5M project**")
    
    # Action buttons for CRUD operations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Schedule Inspection", type="primary", use_container_width=True):
            st.session_state.inspection_mode = "add"
            st.rerun()
    
    with col2:
        if st.button("📋 Digital Checklists", use_container_width=True):
            st.session_state.inspection_mode = "checklists"
            st.rerun()
    
    with col3:
        if st.button("📊 Compliance Reports", use_container_width=True):
            st.session_state.inspection_mode = "compliance"
            st.rerun()
    
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.inspection_mode = "analytics"
            st.rerun()
    
    st.markdown("---")
    
    # Highland Tower Inspections Database
    inspections_data = [
        {
            "inspection_id": "HTD-INS-001",
            "inspection_type": "Structural Steel",
            "location": "Level 13 - Grid A5-B5",
            "inspector": "John Davis - Certified Structural Inspector",
            "scheduled_date": "2025-05-21",
            "completed_date": "2025-05-21",
            "status": "Passed",
            "priority": "High",
            "checklist_items": 24,
            "passed_items": 24,
            "failed_items": 0,
            "notes": "All welded connections meet AWS D1.1 standards. Bolt torque verified. No deficiencies noted.",
            "photos_count": 8,
            "corrective_actions": [],
            "compliance_codes": ["AWS D1.1", "AISC 360", "IBC 2021"],
            "subcontractor": "Apex Steel Construction",
            "next_inspection": "2025-05-28"
        },
        {
            "inspection_id": "HTD-INS-002",
            "inspection_type": "MEP Rough-in",
            "location": "Level 12 - Mechanical Room North",
            "inspector": "Sarah Wilson - MEP Inspector",
            "scheduled_date": "2025-05-20",
            "completed_date": "2025-05-20",
            "status": "Failed",
            "priority": "High",
            "checklist_items": 18,
            "passed_items": 15,
            "failed_items": 3,
            "notes": "Electrical conduit spacing non-compliant in zones C-D. Corrective action required.",
            "photos_count": 12,
            "corrective_actions": [
                "Relocate electrical conduits per NEC spacing requirements",
                "Submit revised installation drawings",
                "Schedule re-inspection within 5 days"
            ],
            "compliance_codes": ["NEC 2020", "IMC 2021", "IPC 2021"],
            "subcontractor": "Premier MEP Systems",
            "next_inspection": "2025-05-25"
        },
        {
            "inspection_id": "HTD-INS-003",
            "inspection_type": "Curtain Wall Installation",
            "location": "South Facade - Units 8-12",
            "inspector": "Robert Kim - Envelope Specialist",
            "scheduled_date": "2025-05-19",
            "completed_date": "2025-05-19",
            "status": "Passed",
            "priority": "Medium",
            "checklist_items": 16,
            "passed_items": 16,
            "failed_items": 0,
            "notes": "Glazing units properly sealed. Structural glazing meets manufacturer specifications.",
            "photos_count": 6,
            "corrective_actions": [],
            "compliance_codes": ["ASTM E1300", "AAMA 501", "IBC 2021"],
            "subcontractor": "Elite Glass & Glazing",
            "next_inspection": "2025-05-26"
        },
        {
            "inspection_id": "HTD-INS-004",
            "inspection_type": "Fire Safety Systems",
            "location": "All Levels - Fire Protection",
            "inspector": "Maria Rodriguez - Fire Safety Inspector",
            "scheduled_date": "2025-05-18",
            "completed_date": null,
            "status": "Scheduled",
            "priority": "High",
            "checklist_items": 32,
            "passed_items": 0,
            "failed_items": 0,
            "notes": "Pre-inspection documentation review complete. Ready for field inspection.",
            "photos_count": 0,
            "corrective_actions": [],
            "compliance_codes": ["NFPA 13", "NFPA 14", "NFPA 72", "IBC 2021"],
            "subcontractor": "Advanced Fire Protection",
            "next_inspection": "2025-05-18"
        },
        {
            "inspection_id": "HTD-INS-005",
            "inspection_type": "Concrete Finishing",
            "location": "Level 11 - Slab on Deck",
            "inspector": "Lisa Chen - Concrete Specialist",
            "scheduled_date": "2025-05-17",
            "completed_date": "2025-05-17",
            "status": "Conditional Pass",
            "priority": "Medium",
            "checklist_items": 12,
            "passed_items": 10,
            "failed_items": 2,
            "notes": "Surface finish acceptable. Minor patching required in grid zones F-G.",
            "photos_count": 4,
            "corrective_actions": [
                "Patch concrete surface imperfections in grid F-G",
                "Apply protective coating after patching"
            ],
            "compliance_codes": ["ACI 301", "ACI 117", "IBC 2021"],
            "subcontractor": "Precision Concrete Works",
            "next_inspection": "2025-05-24"
        }
    ]
    
    # Handle different modes
    if st.session_state.get("inspection_mode") == "add":
        st.markdown("### ➕ Schedule New Inspection")
        
        with st.form("schedule_inspection_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                inspection_type = st.selectbox("Inspection Type", [
                    "Structural Steel", "MEP Rough-in", "Curtain Wall Installation", 
                    "Fire Safety Systems", "Concrete Finishing", "Roofing Systems",
                    "Elevator Installation", "Final Walk-through", "Occupancy Inspection"
                ])
                location = st.text_input("Location", placeholder="Level 13 - Grid A5-B5")
                inspector = st.selectbox("Inspector", [
                    "John Davis - Certified Structural Inspector",
                    "Sarah Wilson - MEP Inspector", 
                    "Robert Kim - Envelope Specialist",
                    "Maria Rodriguez - Fire Safety Inspector",
                    "Lisa Chen - Concrete Specialist"
                ])
                scheduled_date = st.date_input("Scheduled Date")
            
            with col2:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                subcontractor = st.selectbox("Subcontractor", [
                    "Apex Steel Construction", "Premier MEP Systems", "Elite Glass & Glazing",
                    "Precision Concrete Works", "Highland Interior Finishes", "Advanced Fire Protection"
                ])
                compliance_codes = st.multiselect("Compliance Codes", [
                    "IBC 2021", "AWS D1.1", "AISC 360", "NEC 2020", "IMC 2021", "IPC 2021",
                    "ASTM E1300", "AAMA 501", "NFPA 13", "NFPA 14", "NFPA 72", "ACI 301", "ACI 117"
                ])
                notes = st.text_area("Pre-inspection Notes", placeholder="Special requirements or observations...")
            
            submitted = st.form_submit_button("📅 Schedule Inspection", type="primary")
            
            if submitted and inspection_type and location and inspector:
                st.success("✅ Inspection scheduled successfully!")
                st.balloons()
                st.session_state.inspection_mode = None
                st.rerun()
    
    elif st.session_state.get("inspection_mode") == "checklists":
        st.markdown("### 📋 Digital Inspection Checklists")
        
        checklist_type = st.selectbox("Select Checklist Type", [
            "Structural Steel Inspection", "MEP Systems Check", "Curtain Wall Quality", 
            "Fire Safety Compliance", "Concrete Quality Control"
        ])
        
        if checklist_type == "Structural Steel Inspection":
            st.markdown("#### 🏗️ Structural Steel Inspection Checklist")
            
            checklist_items = [
                "Verify structural steel grade and mill certificates",
                "Check bolt grade and torque specifications", 
                "Inspect welded connections per AWS D1.1",
                "Verify member sizes match approved drawings",
                "Check connection details and clearances",
                "Inspect fireproofing application (if applicable)",
                "Verify anchor bolt installation and alignment",
                "Check beam camber and deflection limits"
            ]
            
            for i, item in enumerate(checklist_items):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"{i+1}. {item}")
                
                with col2:
                    status = st.selectbox("", ["Pass", "Fail", "N/A"], key=f"steel_{i}", label_visibility="collapsed")
                
                with col3:
                    if st.button("📷", key=f"photo_{i}", help="Add Photo"):
                        st.info("Photo capture interface")
            
            if st.button("💾 Save Checklist Results", type="primary"):
                st.success("✅ Checklist results saved successfully!")
    
    elif st.session_state.get("inspection_mode") == "compliance":
        st.markdown("### 📊 Compliance Reports & Analytics")
        
        # Compliance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_inspections = len(inspections_data)
            st.metric("Total Inspections", total_inspections)
        
        with col2:
            passed_inspections = len([i for i in inspections_data if i["status"] == "Passed"])
            pass_rate = (passed_inspections / total_inspections) * 100
            st.metric("Pass Rate", f"{pass_rate:.1f}%", "↗️ +5%")
        
        with col3:
            failed_inspections = len([i for i in inspections_data if i["status"] == "Failed"])
            st.metric("Failed Inspections", failed_inspections, "Requires Action")
        
        with col4:
            pending_inspections = len([i for i in inspections_data if i["status"] == "Scheduled"])
            st.metric("Pending", pending_inspections, "This Week")
        
        # Compliance by inspection type
        inspection_types = [i["inspection_type"] for i in inspections_data]
        type_counts = pd.Series(inspection_types).value_counts()
        
        fig_types = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="📊 Inspections by Type",
            labels={'x': 'Inspection Type', 'y': 'Count'}
        )
        st.plotly_chart(fig_types, use_container_width=True)
    
    elif st.session_state.get("inspection_mode") == "analytics":
        st.markdown("### 📈 Inspection Analytics Dashboard")
        
        # Status distribution
        status_counts = pd.Series([i["status"] for i in inspections_data]).value_counts()
        
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="📊 Inspection Status Distribution",
            color_discrete_map={
                'Passed': '#28a745',
                'Failed': '#dc3545', 
                'Conditional Pass': '#ffc107',
                'Scheduled': '#6c757d'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        # Inspector performance
        col1, col2 = st.columns(2)
        
        with col1:
            inspector_data = {}
            for inspection in inspections_data:
                inspector_name = inspection["inspector"].split(" - ")[0]
                if inspector_name not in inspector_data:
                    inspector_data[inspector_name] = {"total": 0, "passed": 0}
                inspector_data[inspector_name]["total"] += 1
                if inspection["status"] == "Passed":
                    inspector_data[inspector_name]["passed"] += 1
            
            inspector_names = list(inspector_data.keys())
            pass_rates = [(inspector_data[name]["passed"] / inspector_data[name]["total"]) * 100 
                         for name in inspector_names]
            
            fig_inspectors = px.bar(
                x=inspector_names,
                y=pass_rates,
                title="👨‍🔬 Inspector Pass Rates",
                labels={'x': 'Inspector', 'y': 'Pass Rate (%)'}
            )
            st.plotly_chart(fig_inspectors, use_container_width=True)
        
        with col2:
            # Priority distribution
            priority_counts = pd.Series([i["priority"] for i in inspections_data]).value_counts()
            
            fig_priority = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="⚡ Priority Distribution",
                color_discrete_map={
                    'High': '#dc3545',
                    'Medium': '#ffc107',
                    'Low': '#28a745'
                }
            )
            st.plotly_chart(fig_priority, use_container_width=True)
    
    # Default view - Inspections Dashboard
    if not st.session_state.get("inspection_mode"):
        st.markdown("### 🔍 Highland Tower Development - Inspections Dashboard")
        
        # Display inspections in expandable cards
        for inspection in inspections_data:
            # Status color coding
            if inspection["status"] == "Passed":
                status_color = "🟢"
            elif inspection["status"] == "Failed":
                status_color = "🔴"
            elif inspection["status"] == "Conditional Pass":
                status_color = "🟡"
            elif inspection["status"] == "Scheduled":
                status_color = "🔵"
            else:
                status_color = "⚪"
            
            # Priority indicator
            if inspection["priority"] == "High":
                priority_indicator = "🚨"
            elif inspection["priority"] == "Medium":
                priority_indicator = "⚠️"
            else:
                priority_indicator = "ℹ️"
            
            with st.expander(f"{status_color} {inspection['inspection_id']} - {inspection['inspection_type']} | {inspection['status']} {priority_indicator}", expanded=False):
                
                col1, col2, col3 = st.columns([2, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    **📋 Inspection Details:**
                    - **ID:** {inspection['inspection_id']}
                    - **Type:** {inspection['inspection_type']}
                    - **Location:** {inspection['location']}
                    - **Inspector:** {inspection['inspector']}
                    - **Priority:** {inspection['priority']}
                    - **Subcontractor:** {inspection['subcontractor']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **📅 Schedule & Status:**
                    - **Scheduled:** {inspection['scheduled_date']}
                    - **Completed:** {inspection['completed_date'] or 'Pending'}
                    - **Status:** {inspection['status']}
                    - **Next Inspection:** {inspection['next_inspection']}
                    - **Photos:** {inspection['photos_count']} attached
                    """)
                
                with col3:
                    st.markdown("**✅ Checklist Results:**")
                    
                    if inspection['checklist_items'] > 0:
                        pass_rate = (inspection['passed_items'] / inspection['checklist_items']) * 100
                        st.markdown(f"**Items:** {inspection['checklist_items']} total")
                        st.markdown(f"**Passed:** {inspection['passed_items']} ({pass_rate:.0f}%)")
                        st.markdown(f"**Failed:** {inspection['failed_items']}")
                        
                        # Progress bar for pass rate
                        st.progress(pass_rate / 100)
                    else:
                        st.markdown("Checklist pending completion")
                
                # Compliance codes
                if inspection['compliance_codes']:
                    st.markdown("**📜 Compliance Codes:**")
                    codes_html = " ".join([f'<span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{code}</span>' for code in inspection['compliance_codes']])
                    st.markdown(codes_html, unsafe_allow_html=True)
                
                # Notes
                if inspection['notes']:
                    st.markdown(f"**📝 Notes:** {inspection['notes']}")
                
                # Corrective actions
                if inspection['corrective_actions']:
                    st.markdown("**🔧 Corrective Actions Required:**")
                    for action in inspection['corrective_actions']:
                        st.markdown(f"• {action}")
                
                # Action buttons
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button(f"✏️ Edit", key=f"edit_{inspection['inspection_id']}", use_container_width=True):
                        st.session_state[f"edit_inspection_{inspection['inspection_id']}"] = True
                        st.rerun()
                
                with action_col2:
                    if st.button(f"📷 Photos", key=f"photos_{inspection['inspection_id']}", use_container_width=True):
                        st.info(f"Opening {inspection['photos_count']} photos for {inspection['inspection_id']}")
                
                with action_col3:
                    if st.button(f"📄 Report", key=f"report_{inspection['inspection_id']}", use_container_width=True):
                        st.success(f"Generating inspection report for {inspection['inspection_id']}")
                
                with action_col4:
                    if inspection['status'] == 'Failed' or inspection['corrective_actions']:
                        if st.button(f"🔄 Re-inspect", key=f"reinspect_{inspection['inspection_id']}", use_container_width=True):
                            st.success(f"Re-inspection scheduled for {inspection['inspection_id']}")
                
                # Handle edit mode
                if st.session_state.get(f"edit_inspection_{inspection['inspection_id']}", False):
                    st.markdown("---")
                    st.markdown("### ✏️ Edit Inspection Details")
                    
                    with st.form(f"edit_inspection_form_{inspection['inspection_id']}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            new_status = st.selectbox("Status", 
                                ["Scheduled", "Passed", "Failed", "Conditional Pass"],
                                index=["Scheduled", "Passed", "Failed", "Conditional Pass"].index(inspection['status']))
                            new_priority = st.selectbox("Priority",
                                ["High", "Medium", "Low"],
                                index=["High", "Medium", "Low"].index(inspection['priority']))
                        
                        with edit_col2:
                            new_inspector = st.text_input("Inspector", value=inspection['inspector'])
                            new_scheduled_date = st.date_input("Scheduled Date", 
                                value=datetime.strptime(inspection['scheduled_date'], "%Y-%m-%d").date())
                        
                        new_notes = st.text_area("Notes", value=inspection['notes'])
                        
                        submitted = st.form_submit_button("💾 Save Changes", type="primary")
                        
                        if submitted:
                            st.success(f"✅ Inspection {inspection['inspection_id']} updated successfully!")
                            st.session_state[f"edit_inspection_{inspection['inspection_id']}"] = False
                            st.rerun()
    
    # Reset mode button
    if st.session_state.get("inspection_mode"):
        if st.button("← Back to Inspections Dashboard"):
            st.session_state.inspection_mode = None
            st.rerun()

if __name__ == "__main__":
    render()