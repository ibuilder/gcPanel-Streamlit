"""
Issues & Risks Management Module
Highland Tower Development - Project Risk Management and Issue Tracking
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render():
    """Render the Issues & Risks Management module"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
            ⚠️ Issues & Risks Management
        </h1>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Highland Tower Development - Risk Mitigation & Issue Resolution
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⚠️ Report Issue", type="primary", use_container_width=True):
            st.session_state.show_report_issue = True
    
    with col2:
        if st.button("🎯 Add Risk", use_container_width=True):
            st.session_state.show_add_risk = True
    
    with col3:
        if st.button("📊 Risk Assessment", use_container_width=True):
            st.session_state.show_assessment = True
    
    with col4:
        if st.button("📈 Trend Analysis", use_container_width=True):
            st.session_state.show_trends = True
    
    # Highland Tower Risk Overview
    st.markdown("### 🏗️ Highland Tower Risk Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Issues", "8", "-2 this week")
    
    with col2:
        st.metric("High Priority Risks", "3", "Monitored")
    
    with col3:
        st.metric("Risk Score", "Medium", "Stable")
    
    with col4:
        st.metric("Mitigation Actions", "12", "+3 implemented")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["⚠️ Active Issues", "🎯 Risk Register", "📊 Analytics"])
    
    with tab1:
        render_active_issues()
    
    with tab2:
        render_risk_register()
    
    with tab3:
        render_risk_analytics()

def render_active_issues():
    """Render active issues tracking"""
    
    st.markdown("### ⚠️ Highland Tower Active Issues")
    
    issues_data = pd.DataFrame([
        {
            "ID": "ISS-001",
            "Title": "MEP Coordination Conflict - Level 12",
            "Category": "Technical",
            "Priority": "High",
            "Status": "In Progress",
            "Assigned To": "MEP Coordinator",
            "Date Reported": "2025-01-20",
            "Target Resolution": "2025-01-28"
        },
        {
            "ID": "ISS-002", 
            "Title": "Material Delivery Delay - Steel Beams",
            "Category": "Supply Chain",
            "Priority": "Medium",
            "Status": "Open",
            "Assigned To": "Procurement Manager",
            "Date Reported": "2025-01-22",
            "Target Resolution": "2025-01-30"
        },
        {
            "ID": "ISS-003",
            "Title": "Permit Approval Pending - Elevator Installation",
            "Category": "Regulatory",
            "Priority": "High", 
            "Status": "Waiting",
            "Assigned To": "Project Manager",
            "Date Reported": "2025-01-18",
            "Target Resolution": "2025-02-05"
        },
        {
            "ID": "ISS-004",
            "Title": "Weather Impact - Exterior Work Delayed",
            "Category": "Environmental",
            "Priority": "Medium",
            "Status": "Monitoring",
            "Assigned To": "Site Supervisor",
            "Date Reported": "2025-01-24",
            "Target Resolution": "2025-02-01"
        }
    ])
    
    for idx, issue in issues_data.iterrows():
        # Priority color coding
        priority_colors = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
        status_colors = {"Open": "#6c757d", "In Progress": "#0066cc", "Waiting": "#ff8c00", "Monitoring": "#17a2b8"}
        
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
            
            with col1:
                st.markdown(f"**{issue['ID']}: {issue['Title']}**")
                st.caption(f"Category: {issue['Category']} • Reported: {issue['Date Reported']}")
            
            with col2:
                st.write(f"Assigned: {issue['Assigned To']}")
                st.caption(f"Target: {issue['Target Resolution']}")
            
            with col3:
                st.markdown(f"""
                <div style="color: {priority_colors[issue['Priority']]}; font-weight: bold; text-align: center;">
                    {issue['Priority']}<br>Priority
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="color: {status_colors[issue['Status']]}; font-weight: bold;">
                    Status: {issue['Status']}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("📝 Update", key=f"update_issue_{idx}", help="Update issue status"):
                    st.info(f"Updating issue {issue['ID']}")
        
        st.markdown("---")

def render_risk_register():
    """Render risk register and mitigation plans"""
    
    st.markdown("### 🎯 Highland Tower Risk Register")
    
    risks_data = pd.DataFrame([
        {
            "Risk ID": "RSK-001",
            "Risk Description": "Cost escalation due to material price increases",
            "Category": "Financial",
            "Probability": "Medium",
            "Impact": "High", 
            "Risk Score": "High",
            "Mitigation Strategy": "Fixed price contracts, bulk purchasing",
            "Owner": "Project Manager"
        },
        {
            "Risk ID": "RSK-002",
            "Risk Description": "Schedule delays from permit approval processes", 
            "Category": "Regulatory",
            "Probability": "High",
            "Impact": "Medium",
            "Risk Score": "High", 
            "Mitigation Strategy": "Early submission, follow-up protocols",
            "Owner": "Permits Coordinator"
        },
        {
            "Risk ID": "RSK-003",
            "Risk Description": "Weather-related construction delays",
            "Category": "Environmental", 
            "Probability": "Medium",
            "Impact": "Medium",
            "Risk Score": "Medium",
            "Mitigation Strategy": "Weather monitoring, flexible scheduling",
            "Owner": "Site Supervisor"
        },
        {
            "Risk ID": "RSK-004", 
            "Risk Description": "Skilled labor shortage in specialized trades",
            "Category": "Resource",
            "Probability": "Medium",
            "Impact": "High",
            "Risk Score": "High",
            "Mitigation Strategy": "Early contractor engagement, training programs",
            "Owner": "HR Manager"
        }
    ])
    
    for idx, risk in risks_data.iterrows():
        # Risk score color coding
        score_colors = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
        
        with st.expander(f"{risk['Risk ID']}: {risk['Risk Description']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Category:** {risk['Category']}")
                st.markdown(f"**Probability:** {risk['Probability']}")
                st.markdown(f"**Impact:** {risk['Impact']}")
            
            with col2:
                st.markdown(f"""
                **Risk Score:** <span style="color: {score_colors[risk['Risk Score']]}; font-weight: bold;">
                {risk['Risk Score']}</span>
                """, unsafe_allow_html=True)
                st.markdown(f"**Owner:** {risk['Owner']}")
            
            with col3:
                st.markdown(f"**Mitigation Strategy:**")
                st.info(risk['Mitigation Strategy'])
            
            # Action buttons for each risk
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Update Risk", key=f"update_risk_{idx}"):
                    st.success(f"Updating {risk['Risk ID']}")
            with col2:
                if st.button("✅ Close Risk", key=f"close_risk_{idx}"):
                    st.success(f"Risk {risk['Risk ID']} marked for closure")
            with col3:
                if st.button("📊 Assessment", key=f"assess_risk_{idx}"):
                    st.info(f"Opening assessment for {risk['Risk ID']}")

def render_risk_analytics():
    """Render risk analytics and trends"""
    
    st.markdown("### 📊 Highland Tower Risk Analytics")
    
    # Risk distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Risk Distribution by Category")
        risk_categories = pd.DataFrame({
            "Category": ["Financial", "Regulatory", "Environmental", "Resource", "Technical"],
            "Count": [3, 2, 2, 2, 1]
        })
        st.bar_chart(risk_categories.set_index("Category"))
    
    with col2:
        st.markdown("#### ⚠️ Risk Score Distribution")
        risk_scores = pd.DataFrame({
            "Score": ["High", "Medium", "Low"],
            "Count": [4, 5, 1]
        })
        st.bar_chart(risk_scores.set_index("Score"))
    
    # Monthly risk trends
    st.markdown("#### 📈 Monthly Risk & Issue Trends")
    
    months = ["Sep", "Oct", "Nov", "Dec", "Jan"]
    trend_data = pd.DataFrame({
        "Month": months,
        "New Issues": [12, 8, 10, 6, 8],
        "Resolved Issues": [10, 9, 8, 7, 6],
        "Active Risks": [8, 9, 10, 9, 10]
    })
    
    st.line_chart(trend_data.set_index("Month"))
    
    # Risk mitigation effectiveness
    st.markdown("#### ✅ Mitigation Action Status")
    
    mitigation_data = pd.DataFrame([
        {"Action": "Fixed price material contracts", "Status": "Implemented", "Effectiveness": "High"},
        {"Action": "Weather monitoring system", "Status": "Active", "Effectiveness": "Medium"},
        {"Action": "Early permit submissions", "Status": "Ongoing", "Effectiveness": "High"},
        {"Action": "Skilled labor training program", "Status": "Planning", "Effectiveness": "TBD"}
    ])
    
    for idx, action in mitigation_data.iterrows():
        status_colors = {"Implemented": "#28a745", "Active": "#0066cc", "Ongoing": "#ffc107", "Planning": "#6c757d"}
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{action['Action']}**")
        
        with col2:
            st.markdown(f"""
            <span style="color: {status_colors[action['Status']]}; font-weight: bold;">
                {action['Status']}
            </span>
            """, unsafe_allow_html=True)
        
        with col3:
            if action['Effectiveness'] == "High":
                st.success(f"⭐ {action['Effectiveness']}")
            elif action['Effectiveness'] == "Medium":
                st.info(f"👍 {action['Effectiveness']}")
            else:
                st.write(action['Effectiveness'])
        
        st.markdown("---")

if __name__ == "__main__":
    render()