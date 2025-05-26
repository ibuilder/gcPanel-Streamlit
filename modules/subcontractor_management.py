"""
Subcontractor Management Module for Highland Tower Development
Enterprise-grade subcontractor coordination and performance tracking
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def render():
    """Render comprehensive subcontractor management system"""
    
    st.title("🏗️ Subcontractor Management - Highland Tower Development")
    st.markdown("**Enterprise subcontractor coordination for $45.5M mixed-use project**")
    
    # Action buttons for CRUD operations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add Subcontractor", type="primary", use_container_width=True):
            st.session_state.sub_mode = "add"
            st.rerun()
    
    with col2:
        if st.button("📋 Performance Review", use_container_width=True):
            st.session_state.sub_mode = "performance"
            st.rerun()
    
    with col3:
        if st.button("📄 Insurance Tracking", use_container_width=True):
            st.session_state.sub_mode = "insurance"
            st.rerun()
    
    with col4:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.sub_mode = "analytics"
            st.rerun()
    
    st.markdown("---")
    
    # Highland Tower Subcontractors Database
    subcontractors_data = [
        {
            "sub_id": "HTD-SUB-001",
            "company_name": "Apex Steel Construction",
            "trade": "Structural Steel",
            "contact_person": "Robert Martinez",
            "phone": "(555) 234-5678",
            "email": "rmartinez@apexsteel.com",
            "contract_value": "$8,750,000",
            "start_date": "2024-08-01",
            "end_date": "2025-01-15",
            "status": "Active",
            "performance_rating": 4.8,
            "safety_rating": 4.9,
            "quality_rating": 4.7,
            "schedule_compliance": "95%",
            "location": "Levels 8-13",
            "crew_size": "18 workers",
            "insurance_status": "Current",
            "insurance_expiry": "2025-12-31",
            "payment_status": "Current",
            "current_progress": "87%",
            "recent_activities": ["Steel beam installation Level 13", "Welding inspections passed", "Crew safety training completed"]
        },
        {
            "sub_id": "HTD-SUB-002", 
            "company_name": "Premier MEP Systems",
            "trade": "Mechanical/Electrical/Plumbing",
            "contact_person": "Lisa Thompson",
            "phone": "(555) 345-6789",
            "email": "lthompson@premiermep.com",
            "contract_value": "$6,200,000",
            "start_date": "2024-09-15",
            "end_date": "2025-04-30",
            "status": "Active",
            "performance_rating": 4.6,
            "safety_rating": 4.8,
            "quality_rating": 4.5,
            "schedule_compliance": "92%",
            "location": "All Levels",
            "crew_size": "24 workers",
            "insurance_status": "Current",
            "insurance_expiry": "2025-11-15",
            "payment_status": "Current",
            "current_progress": "78%",
            "recent_activities": ["HVAC ductwork Level 12", "Electrical rough-in progress", "Plumbing inspections scheduled"]
        },
        {
            "sub_id": "HTD-SUB-003",
            "company_name": "Elite Glass & Glazing",
            "trade": "Curtain Wall & Windows",
            "contact_person": "David Kim",
            "phone": "(555) 456-7890", 
            "email": "dkim@eliteglass.com",
            "contract_value": "$4,950,000",
            "start_date": "2024-11-01",
            "end_date": "2025-03-15",
            "status": "Active",
            "performance_rating": 4.9,
            "safety_rating": 4.7,
            "quality_rating": 4.8,
            "schedule_compliance": "98%",
            "location": "Exterior Facades",
            "crew_size": "12 workers",
            "insurance_status": "Current",
            "insurance_expiry": "2025-10-30",
            "payment_status": "Current",
            "current_progress": "65%",
            "recent_activities": ["South facade glazing complete", "North facade in progress", "Quality inspections passed"]
        },
        {
            "sub_id": "HTD-SUB-004",
            "company_name": "Precision Concrete Works",
            "trade": "Concrete & Foundations",
            "contact_person": "Maria Santos",
            "phone": "(555) 567-8901",
            "email": "msantos@precisionconcrete.com", 
            "contract_value": "$5,400,000",
            "start_date": "2024-06-01",
            "end_date": "2024-12-15",
            "status": "Completed",
            "performance_rating": 4.9,
            "safety_rating": 4.8,
            "quality_rating": 4.9,
            "schedule_compliance": "99%",
            "location": "Foundation & Structure",
            "crew_size": "16 workers",
            "insurance_status": "Current",
            "insurance_expiry": "2025-06-01",
            "payment_status": "Final Payment Pending",
            "current_progress": "100%",
            "recent_activities": ["Project completed successfully", "Final inspections passed", "Closeout documentation submitted"]
        },
        {
            "sub_id": "HTD-SUB-005",
            "company_name": "Highland Interior Finishes", 
            "trade": "Interior Finishes",
            "contact_person": "Jennifer Brown",
            "phone": "(555) 678-9012",
            "email": "jbrown@highland-finishes.com",
            "contract_value": "$3,800,000",
            "start_date": "2025-01-15",
            "end_date": "2025-05-30",
            "status": "Starting Soon",
            "performance_rating": 4.7,
            "safety_rating": 4.6,
            "quality_rating": 4.8,
            "schedule_compliance": "N/A",
            "location": "Residential Units",
            "crew_size": "20 workers",
            "insurance_status": "Current",
            "insurance_expiry": "2025-12-31",
            "payment_status": "Contract Signed",
            "current_progress": "0%",
            "recent_activities": ["Contract executed", "Pre-construction meeting scheduled", "Material procurement initiated"]
        }
    ]
    
    # Handle different modes
    if st.session_state.get("sub_mode") == "add":
        st.markdown("### ➕ Add New Subcontractor")
        
        with st.form("add_subcontractor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name*")
                trade = st.selectbox("Trade", [
                    "Structural Steel", "Mechanical/Electrical/Plumbing", "Curtain Wall & Windows",
                    "Concrete & Foundations", "Interior Finishes", "Roofing", "Elevator",
                    "Fire Protection", "Security Systems", "Landscaping"
                ])
                contact_person = st.text_input("Primary Contact*")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email Address")
            
            with col2:
                contract_value = st.text_input("Contract Value", placeholder="$5,000,000")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                location = st.text_input("Work Location", placeholder="Levels 1-5")
                crew_size = st.text_input("Crew Size", placeholder="15 workers")
            
            insurance_expiry = st.date_input("Insurance Expiry Date")
            notes = st.text_area("Additional Notes", placeholder="Special requirements, certifications, etc.")
            
            submitted = st.form_submit_button("➕ Add Subcontractor", type="primary")
            
            if submitted and company_name and contact_person:
                st.success("✅ Subcontractor added successfully!")
                st.balloons()
                st.session_state.sub_mode = None
                st.rerun()
    
    elif st.session_state.get("sub_mode") == "performance":
        st.markdown("### 📋 Performance Review Dashboard")
        
        # Performance metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_performance = sum([sub["performance_rating"] for sub in subcontractors_data]) / len(subcontractors_data)
            st.metric("Avg Performance", f"{avg_performance:.1f}/5.0", "↗️ +0.2")
        
        with col2:
            avg_safety = sum([sub["safety_rating"] for sub in subcontractors_data]) / len(subcontractors_data)
            st.metric("Avg Safety", f"{avg_safety:.1f}/5.0", "↗️ +0.1")
        
        with col3:
            avg_quality = sum([sub["quality_rating"] for sub in subcontractors_data]) / len(subcontractors_data)
            st.metric("Avg Quality", f"{avg_quality:.1f}/5.0", "↗️ +0.3")
        
        with col4:
            active_subs = len([sub for sub in subcontractors_data if sub["status"] == "Active"])
            st.metric("Active Subs", active_subs, f"of {len(subcontractors_data)} total")
        
        # Performance comparison chart
        fig = go.Figure()
        
        for sub in subcontractors_data:
            fig.add_trace(go.Scatter(
                x=['Performance', 'Safety', 'Quality'],
                y=[sub['performance_rating'], sub['safety_rating'], sub['quality_rating']],
                mode='lines+markers',
                name=sub['company_name'],
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="📊 Subcontractor Performance Comparison",
            yaxis_title="Rating (1-5)",
            yaxis=dict(range=[0, 5]),
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.get("sub_mode") == "insurance":
        st.markdown("### 📄 Insurance & Compliance Tracking")
        
        # Insurance status overview
        current_insurance = len([sub for sub in subcontractors_data if sub["insurance_status"] == "Current"])
        st.metric("Current Insurance", f"{current_insurance}/{len(subcontractors_data)}", "100% Compliant")
        
        # Insurance expiry tracking
        st.markdown("#### 📅 Insurance Expiry Dates")
        
        for sub in subcontractors_data:
            expiry_date = datetime.strptime(sub["insurance_expiry"], "%Y-%m-%d")
            days_until_expiry = (expiry_date - datetime.now()).days
            
            if days_until_expiry < 30:
                status_color = "🔴"
                alert = " ⚠️ URGENT"
            elif days_until_expiry < 90:
                status_color = "🟡"
                alert = " ⚠️ Soon"
            else:
                status_color = "🟢"
                alert = ""
            
            st.markdown(f"{status_color} **{sub['company_name']}** - Expires: {sub['insurance_expiry']}{alert}")
    
    elif st.session_state.get("sub_mode") == "analytics":
        st.markdown("### 📊 Subcontractor Analytics")
        
        # Contract value breakdown
        fig_contracts = px.pie(
            values=[float(sub["contract_value"].replace("$", "").replace(",", "")) for sub in subcontractors_data],
            names=[sub["company_name"] for sub in subcontractors_data],
            title="💰 Contract Value Distribution"
        )
        st.plotly_chart(fig_contracts, use_container_width=True)
        
        # Schedule compliance
        col1, col2 = st.columns(2)
        
        with col1:
            compliance_data = [sub["schedule_compliance"] for sub in subcontractors_data if sub["schedule_compliance"] != "N/A"]
            compliance_values = [float(comp.replace("%", "")) for comp in compliance_data]
            
            fig_compliance = px.bar(
                x=[sub["company_name"] for sub in subcontractors_data if sub["schedule_compliance"] != "N/A"],
                y=compliance_values,
                title="📅 Schedule Compliance by Subcontractor"
            )
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        with col2:
            # Progress tracking
            progress_data = [float(sub["current_progress"].replace("%", "")) for sub in subcontractors_data if sub["current_progress"] != "N/A"]
            
            fig_progress = px.bar(
                x=[sub["company_name"] for sub in subcontractors_data if sub["current_progress"] != "N/A"],
                y=progress_data,
                title="📈 Current Progress by Subcontractor"
            )
            st.plotly_chart(fig_progress, use_container_width=True)
    
    # Default view - Subcontractor Directory
    if not st.session_state.get("sub_mode"):
        st.markdown("### 🏗️ Highland Tower Subcontractor Directory")
        
        # Display subcontractors in expandable cards
        for sub in subcontractors_data:
            # Status color coding
            if sub["status"] == "Active":
                status_color = "🟢"
            elif sub["status"] == "Completed":
                status_color = "🔵"
            elif sub["status"] == "Starting Soon":
                status_color = "🟡"
            else:
                status_color = "🔴"
            
            with st.expander(f"{status_color} {sub['company_name']} - {sub['trade']} | {sub['status']}", expanded=False):
                
                col1, col2, col3 = st.columns([2, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    **📋 Contract Details:**
                    - **Sub ID:** {sub['sub_id']}
                    - **Trade:** {sub['trade']}
                    - **Contract Value:** {sub['contract_value']}
                    - **Duration:** {sub['start_date']} to {sub['end_date']}
                    - **Location:** {sub['location']}
                    - **Crew Size:** {sub['crew_size']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **👥 Contact Information:**
                    - **Contact:** {sub['contact_person']}
                    - **Phone:** {sub['phone']}
                    - **Email:** {sub['email']}
                    - **Payment Status:** {sub['payment_status']}
                    - **Insurance:** {sub['insurance_status']} (Exp: {sub['insurance_expiry']})
                    """)
                
                with col3:
                    st.markdown("**📊 Performance Metrics:**")
                    
                    # Performance rating bars
                    performance_pct = (sub['performance_rating'] / 5.0) * 100
                    safety_pct = (sub['safety_rating'] / 5.0) * 100
                    quality_pct = (sub['quality_rating'] / 5.0) * 100
                    
                    st.markdown(f"**Performance:** {sub['performance_rating']}/5.0")
                    st.progress(performance_pct / 100)
                    
                    st.markdown(f"**Safety:** {sub['safety_rating']}/5.0")
                    st.progress(safety_pct / 100)
                    
                    st.markdown(f"**Quality:** {sub['quality_rating']}/5.0")
                    st.progress(quality_pct / 100)
                    
                    st.markdown(f"**Schedule Compliance:** {sub['schedule_compliance']}")
                    if sub['schedule_compliance'] != "N/A":
                        compliance_val = float(sub['schedule_compliance'].replace("%", ""))
                        st.progress(compliance_val / 100)
                
                # Recent activities
                st.markdown("**📝 Recent Activities:**")
                for activity in sub['recent_activities']:
                    st.markdown(f"• {activity}")
                
                # Action buttons
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button(f"✏️ Edit", key=f"edit_{sub['sub_id']}", use_container_width=True):
                        st.session_state[f"edit_sub_{sub['sub_id']}"] = True
                        st.rerun()
                
                with action_col2:
                    if st.button(f"📞 Contact", key=f"contact_{sub['sub_id']}", use_container_width=True):
                        st.info(f"Opening contact for {sub['contact_person']}")
                
                with action_col3:
                    if st.button(f"📋 Review", key=f"review_{sub['sub_id']}", use_container_width=True):
                        st.success(f"Performance review initiated for {sub['company_name']}")
                
                with action_col4:
                    if st.button(f"💰 Payment", key=f"payment_{sub['sub_id']}", use_container_width=True):
                        st.success(f"Payment processing for {sub['company_name']}")
                
                # Handle edit mode
                if st.session_state.get(f"edit_sub_{sub['sub_id']}", False):
                    st.markdown("---")
                    st.markdown("### ✏️ Edit Subcontractor Details")
                    
                    with st.form(f"edit_sub_form_{sub['sub_id']}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            new_contact = st.text_input("Primary Contact", value=sub['contact_person'])
                            new_phone = st.text_input("Phone", value=sub['phone'])
                            new_email = st.text_input("Email", value=sub['email'])
                        
                        with edit_col2:
                            new_status = st.selectbox("Status", 
                                ["Active", "Completed", "Starting Soon", "On Hold", "Terminated"],
                                index=["Active", "Completed", "Starting Soon", "On Hold", "Terminated"].index(sub['status']))
                            new_crew_size = st.text_input("Crew Size", value=sub['crew_size'])
                            new_payment_status = st.text_input("Payment Status", value=sub['payment_status'])
                        
                        # Performance ratings
                        st.markdown("**Performance Ratings:**")
                        rating_col1, rating_col2, rating_col3 = st.columns(3)
                        
                        with rating_col1:
                            new_performance = st.slider("Performance Rating", 1.0, 5.0, sub['performance_rating'], 0.1)
                        with rating_col2:
                            new_safety = st.slider("Safety Rating", 1.0, 5.0, sub['safety_rating'], 0.1)
                        with rating_col3:
                            new_quality = st.slider("Quality Rating", 1.0, 5.0, sub['quality_rating'], 0.1)
                        
                        submitted = st.form_submit_button("💾 Save Changes", type="primary")
                        
                        if submitted:
                            st.success(f"✅ {sub['company_name']} updated successfully!")
                            st.session_state[f"edit_sub_{sub['sub_id']}"] = False
                            st.rerun()
    
    # Reset mode button
    if st.session_state.get("sub_mode"):
        if st.button("← Back to Directory"):
            st.session_state.sub_mode = None
            st.rerun()

if __name__ == "__main__":
    render()