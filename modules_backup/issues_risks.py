"""
Issues & Risks Management Module for Highland Tower Development
Proactive risk management and issue resolution system
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def render():
    """Render comprehensive issues and risks management system"""
    
    st.title("⚠️ Issues & Risks - Highland Tower Development")
    st.markdown("**Proactive risk management and issue resolution for $45.5M project**")
    
    # Action buttons for CRUD operations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Report Issue/Risk", type="primary", use_container_width=True):
            st.session_state.issues_mode = "add"
            st.rerun()
    
    with col2:
        if st.button("📊 Risk Matrix", use_container_width=True):
            st.session_state.issues_mode = "matrix"
            st.rerun()
    
    with col3:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.issues_mode = "analytics"
            st.rerun()
    
    with col4:
        if st.button("📋 Action Plans", use_container_width=True):
            st.session_state.issues_mode = "actions"
            st.rerun()
    
    st.markdown("---")
    
    # Highland Tower Issues & Risks Database
    issues_risks_data = [
        {
            "id": "HTD-RISK-001",
            "type": "Risk",
            "category": "Schedule",
            "title": "MEP Coordination Delays",
            "description": "Potential delays in MEP rough-in due to structural steel schedule compression affecting coordination time",
            "impact": "High",
            "probability": "Medium",
            "risk_score": 12,
            "status": "Active",
            "owner": "Sarah Johnson - Project Manager",
            "created_date": "2025-05-15",
            "target_date": "2025-06-01",
            "location": "All Levels",
            "cost_impact": "$150,000",
            "schedule_impact": "7 days",
            "mitigation_plan": [
                "Increase MEP coordination meetings to daily",
                "Deploy additional BIM coordination resources",
                "Consider parallel installation where safe"
            ],
            "action_items": [
                "Schedule daily MEP coordination meetings",
                "Hire additional BIM coordinator",
                "Review installation sequence options"
            ],
            "last_updated": "2025-05-20"
        },
        {
            "id": "HTD-ISS-001",
            "type": "Issue",
            "category": "Quality",
            "title": "Curtain Wall Seal Failure",
            "description": "Water infiltration detected at curtain wall connections on south facade units 8-10",
            "impact": "High",
            "probability": "N/A",
            "risk_score": 16,
            "status": "In Progress",
            "owner": "Robert Kim - Architecture Team",
            "created_date": "2025-05-18",
            "target_date": "2025-05-25",
            "location": "South Facade Units 8-10",
            "cost_impact": "$75,000",
            "schedule_impact": "3 days",
            "mitigation_plan": [
                "Immediate temporary waterproofing",
                "Full seal replacement and testing",
                "Enhanced QC for remaining installations"
            ],
            "action_items": [
                "Apply temporary sealant - COMPLETED",
                "Order replacement sealing materials",
                "Schedule water testing post-repair"
            ],
            "last_updated": "2025-05-21"
        },
        {
            "id": "HTD-RISK-002",
            "type": "Risk",
            "category": "Safety",
            "title": "Winter Weather Operations",
            "description": "Approaching winter season may impact exterior work and crane operations",
            "impact": "Medium",
            "probability": "High",
            "risk_score": 9,
            "status": "Monitoring",
            "owner": "John Davis - Safety Manager",
            "created_date": "2025-05-10",
            "target_date": "2025-11-01",
            "location": "Exterior Work Areas",
            "cost_impact": "$50,000",
            "schedule_impact": "10 days",
            "mitigation_plan": [
                "Accelerate exterior work completion",
                "Prepare winter protection protocols",
                "Secure heated workspaces for critical activities"
            ],
            "action_items": [
                "Develop winter work procedures",
                "Order weather protection materials",
                "Train crews on cold weather protocols"
            ],
            "last_updated": "2025-05-16"
        },
        {
            "id": "HTD-ISS-002",
            "type": "Issue",
            "category": "Cost",
            "title": "Steel Price Escalation",
            "description": "Unexpected 8% increase in structural steel pricing affecting change order costs",
            "impact": "Medium",
            "probability": "N/A",
            "risk_score": 8,
            "status": "Resolved",
            "owner": "Mike Chen - Superintendent",
            "created_date": "2025-05-05",
            "target_date": "2025-05-15",
            "location": "Project-wide",
            "cost_impact": "$125,000",
            "schedule_impact": "0 days",
            "mitigation_plan": [
                "Negotiate with steel supplier for locked pricing",
                "Review budget allocation for contingency use",
                "Fast-track remaining steel procurement"
            ],
            "action_items": [
                "Negotiate supplier pricing - COMPLETED",
                "Secure budget approval - COMPLETED",
                "Order remaining steel materials - COMPLETED"
            ],
            "last_updated": "2025-05-15"
        },
        {
            "id": "HTD-RISK-003",
            "type": "Risk",
            "category": "Regulatory",
            "title": "Building Code Updates",
            "description": "Potential mid-project building code changes affecting fire protection systems",
            "impact": "Low",
            "probability": "Low",
            "risk_score": 2,
            "status": "Monitoring",
            "owner": "Lisa Rodriguez - Quality Inspector",
            "created_date": "2025-05-12",
            "target_date": "2025-12-31",
            "location": "Fire Protection Systems",
            "cost_impact": "$25,000",
            "schedule_impact": "2 days",
            "mitigation_plan": [
                "Monitor AHJ communications regularly",
                "Maintain flexibility in fire protection design",
                "Establish contingency budget allocation"
            ],
            "action_items": [
                "Subscribe to building code update alerts",
                "Review current fire protection compliance",
                "Establish AHJ communication protocol"
            ],
            "last_updated": "2025-05-18"
        }
    ]
    
    # Handle different modes
    if st.session_state.get("issues_mode") == "add":
        st.markdown("### ➕ Report New Issue/Risk")
        
        with st.form("add_issue_risk_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                issue_type = st.selectbox("Type", ["Issue", "Risk"])
                category = st.selectbox("Category", [
                    "Schedule", "Quality", "Safety", "Cost", "Regulatory", 
                    "Weather", "Supply Chain", "Labor", "Technical"
                ])
                title = st.text_input("Title*", placeholder="Brief descriptive title")
                location = st.text_input("Location", placeholder="Specific location or area affected")
                owner = st.selectbox("Owner", [
                    "Sarah Johnson - Project Manager",
                    "Mike Chen - Superintendent", 
                    "Robert Kim - Architecture Team",
                    "John Davis - Safety Manager",
                    "Lisa Rodriguez - Quality Inspector"
                ])
            
            with col2:
                impact = st.selectbox("Impact", ["Low", "Medium", "High"])
                if issue_type == "Risk":
                    probability = st.selectbox("Probability", ["Low", "Medium", "High"])
                else:
                    probability = "N/A"
                target_date = st.date_input("Target Resolution Date")
                cost_impact = st.text_input("Cost Impact", placeholder="$50,000")
                schedule_impact = st.text_input("Schedule Impact", placeholder="3 days")
            
            description = st.text_area("Description*", placeholder="Detailed description of the issue or risk...")
            
            st.markdown("**Mitigation Plan / Action Items:**")
            mitigation_plan = st.text_area("Mitigation Strategy", placeholder="Enter mitigation steps, one per line")
            action_items = st.text_area("Immediate Actions", placeholder="Enter action items, one per line")
            
            submitted = st.form_submit_button("📝 Submit Issue/Risk", type="primary")
            
            if submitted and title and description:
                st.success("✅ Issue/Risk reported successfully!")
                st.balloons()
                st.session_state.issues_mode = None
                st.rerun()
    
    elif st.session_state.get("issues_mode") == "matrix":
        st.markdown("### 📊 Risk Assessment Matrix")
        
        # Create risk matrix visualization
        risk_items = [item for item in issues_risks_data if item["type"] == "Risk"]
        
        if risk_items:
            # Convert impact and probability to numeric values
            impact_map = {"Low": 1, "Medium": 2, "High": 3}
            prob_map = {"Low": 1, "Medium": 2, "High": 3}
            
            matrix_data = []
            for risk in risk_items:
                if risk["probability"] != "N/A":
                    matrix_data.append({
                        "title": risk["title"],
                        "impact": impact_map[risk["impact"]],
                        "probability": prob_map[risk["probability"]],
                        "risk_score": risk["risk_score"],
                        "status": risk["status"]
                    })
            
            if matrix_data:
                df_matrix = pd.DataFrame(matrix_data)
                
                # Create scatter plot for risk matrix
                fig_matrix = px.scatter(
                    df_matrix, 
                    x="probability", 
                    y="impact",
                    size="risk_score",
                    color="status",
                    hover_name="title",
                    title="🎯 Highland Tower Risk Matrix",
                    labels={
                        "probability": "Probability", 
                        "impact": "Impact",
                        "risk_score": "Risk Score"
                    }
                )
                
                # Customize axes
                fig_matrix.update_xaxes(
                    tickvals=[1, 2, 3],
                    ticktext=["Low", "Medium", "High"],
                    range=[0.5, 3.5]
                )
                fig_matrix.update_yaxes(
                    tickvals=[1, 2, 3],
                    ticktext=["Low", "Medium", "High"],
                    range=[0.5, 3.5]
                )
                
                # Add background colors for risk zones
                fig_matrix.add_shape(
                    type="rect", x0=0.5, y0=0.5, x1=2.5, y1=2.5,
                    fillcolor="green", opacity=0.2, line_width=0
                )
                fig_matrix.add_shape(
                    type="rect", x0=2.5, y0=2.5, x1=3.5, y1=3.5,
                    fillcolor="red", opacity=0.2, line_width=0
                )
                
                st.plotly_chart(fig_matrix, use_container_width=True)
                
                # Risk summary table
                st.markdown("### 📋 Risk Summary")
                
                summary_df = df_matrix.groupby("status").agg({
                    "risk_score": ["count", "mean", "max"]
                }).round(1)
                
                st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("No risks available for matrix analysis")
    
    elif st.session_state.get("issues_mode") == "analytics":
        st.markdown("### 📈 Issues & Risks Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(issues_risks_data)
            st.metric("Total Items", total_items)
        
        with col2:
            active_items = len([item for item in issues_risks_data if item["status"] in ["Active", "In Progress"]])
            st.metric("Active", active_items, f"{(active_items/total_items)*100:.0f}%")
        
        with col3:
            high_impact = len([item for item in issues_risks_data if item["impact"] == "High"])
            st.metric("High Impact", high_impact, "Priority Focus")
        
        with col4:
            avg_risk_score = sum([item["risk_score"] for item in issues_risks_data]) / len(issues_risks_data)
            st.metric("Avg Risk Score", f"{avg_risk_score:.1f}", "Moderate")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            status_counts = pd.Series([item["status"] for item in issues_risks_data]).value_counts()
            
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="📊 Status Distribution",
                color_discrete_map={
                    'Active': '#dc3545',
                    'In Progress': '#ffc107',
                    'Monitoring': '#17a2b8',
                    'Resolved': '#28a745'
                }
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Category breakdown
            category_counts = pd.Series([item["category"] for item in issues_risks_data]).value_counts()
            
            fig_category = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                title="📈 Issues/Risks by Category"
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        # Impact vs Timeline
        timeline_data = []
        for item in issues_risks_data:
            created = datetime.strptime(item["created_date"], "%Y-%m-%d")
            target = datetime.strptime(item["target_date"], "%Y-%m-%d")
            days_to_resolve = (target - created).days
            
            timeline_data.append({
                "title": item["title"],
                "days_to_resolve": days_to_resolve,
                "impact": item["impact"],
                "risk_score": item["risk_score"],
                "status": item["status"]
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        fig_timeline = px.scatter(
            df_timeline,
            x="days_to_resolve",
            y="risk_score", 
            color="impact",
            size="risk_score",
            hover_name="title",
            title="⏱️ Resolution Timeline vs Risk Score"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    elif st.session_state.get("issues_mode") == "actions":
        st.markdown("### 📋 Action Plans & Mitigation")
        
        # Filter for active items with action plans
        active_items = [item for item in issues_risks_data if item["status"] in ["Active", "In Progress"]]
        
        for item in active_items:
            with st.expander(f"🎯 {item['id']} - {item['title']} | {item['status']}", expanded=True):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **📋 Item Details:**
                    - **Type:** {item['type']}
                    - **Category:** {item['category']}
                    - **Impact:** {item['impact']}
                    - **Risk Score:** {item['risk_score']}
                    - **Owner:** {item['owner']}
                    - **Target Date:** {item['target_date']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **💰 Impact Assessment:**
                    - **Cost Impact:** {item['cost_impact']}
                    - **Schedule Impact:** {item['schedule_impact']}
                    - **Location:** {item['location']}
                    - **Last Updated:** {item['last_updated']}
                    """)
                
                st.markdown(f"**📝 Description:** {item['description']}")
                
                # Mitigation plan
                if item['mitigation_plan']:
                    st.markdown("**🛡️ Mitigation Plan:**")
                    for plan in item['mitigation_plan']:
                        st.markdown(f"• {plan}")
                
                # Action items with checkboxes
                if item['action_items']:
                    st.markdown("**✅ Action Items:**")
                    for i, action in enumerate(item['action_items']):
                        if "COMPLETED" in action:
                            st.markdown(f"✅ ~~{action.replace(' - COMPLETED', '')}~~")
                        else:
                            col_action, col_checkbox = st.columns([4, 1])
                            with col_action:
                                st.markdown(f"• {action}")
                            with col_checkbox:
                                if st.checkbox("Done", key=f"action_{item['id']}_{i}"):
                                    st.success("Action marked complete!")
                
                # Action buttons
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button(f"📝 Update", key=f"update_{item['id']}", use_container_width=True):
                        st.session_state[f"update_{item['id']}"] = True
                        st.rerun()
                
                with action_col2:
                    if st.button(f"➕ Add Action", key=f"add_action_{item['id']}", use_container_width=True):
                        st.session_state[f"add_action_{item['id']}"] = True
                        st.rerun()
                
                with action_col3:
                    if st.button(f"✅ Resolve", key=f"resolve_{item['id']}", use_container_width=True):
                        st.success(f"✅ {item['id']} marked as resolved!")
                
                # Handle update mode
                if st.session_state.get(f"update_{item['id']}", False):
                    st.markdown("---")
                    st.markdown("### 📝 Update Item")
                    
                    with st.form(f"update_form_{item['id']}"):
                        new_status = st.selectbox("Status", 
                            ["Active", "In Progress", "Monitoring", "Resolved"],
                            index=["Active", "In Progress", "Monitoring", "Resolved"].index(item['status']))
                        
                        new_notes = st.text_area("Update Notes", placeholder="Enter progress update...")
                        
                        submitted = st.form_submit_button("💾 Save Update", type="primary")
                        
                        if submitted:
                            st.success(f"✅ {item['id']} updated successfully!")
                            st.session_state[f"update_{item['id']}"] = False
                            st.rerun()
    
    # Default view - Issues & Risks Dashboard
    if not st.session_state.get("issues_mode"):
        st.markdown("### ⚠️ Highland Tower Development - Issues & Risks Dashboard")
        
        # Display items in expandable cards
        for item in issues_risks_data:
            # Status and type color coding
            if item["type"] == "Issue":
                type_color = "🔥"
            else:
                type_color = "⚡"
            
            if item["status"] == "Active":
                status_color = "🔴"
            elif item["status"] == "In Progress":
                status_color = "🟡"
            elif item["status"] == "Monitoring":
                status_color = "🔵"
            elif item["status"] == "Resolved":
                status_color = "🟢"
            else:
                status_color = "⚪"
            
            # Impact indicator
            if item["impact"] == "High":
                impact_indicator = "🚨"
            elif item["impact"] == "Medium":
                impact_indicator = "⚠️"
            else:
                impact_indicator = "ℹ️"
            
            with st.expander(f"{status_color} {type_color} {item['id']} - {item['title']} | {item['status']} {impact_indicator}", expanded=False):
                
                col1, col2, col3 = st.columns([2, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    **📋 Details:**
                    - **ID:** {item['id']}
                    - **Type:** {item['type']}
                    - **Category:** {item['category']}
                    - **Impact:** {item['impact']}
                    - **Owner:** {item['owner']}
                    - **Location:** {item['location']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **📅 Timeline:**
                    - **Created:** {item['created_date']}
                    - **Target:** {item['target_date']}
                    - **Last Updated:** {item['last_updated']}
                    - **Risk Score:** {item['risk_score']}
                    """)
                    
                    if item["type"] == "Risk":
                        st.markdown(f"- **Probability:** {item['probability']}")
                
                with col3:
                    st.markdown(f"""
                    **💰 Impact Assessment:**
                    - **Cost Impact:** {item['cost_impact']}
                    - **Schedule Impact:** {item['schedule_impact']}
                    """)
                    
                    # Risk score gauge
                    risk_color = "red" if item['risk_score'] > 10 else "orange" if item['risk_score'] > 5 else "green"
                    st.markdown(f"**Risk Level:** <span style='color: {risk_color}; font-weight: bold;'>{item['risk_score']}/16</span>", unsafe_allow_html=True)
                
                # Description
                st.markdown(f"**📝 Description:** {item['description']}")
                
                # Action buttons
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button(f"✏️ Edit", key=f"edit_{item['id']}", use_container_width=True):
                        st.session_state[f"edit_{item['id']}"] = True
                        st.rerun()
                
                with action_col2:
                    if st.button(f"📋 Actions", key=f"actions_{item['id']}", use_container_width=True):
                        st.session_state.issues_mode = "actions"
                        st.rerun()
                
                with action_col3:
                    if st.button(f"📊 Analyze", key=f"analyze_{item['id']}", use_container_width=True):
                        st.info(f"Risk analysis for {item['id']}")
                
                with action_col4:
                    if item["status"] != "Resolved":
                        if st.button(f"✅ Resolve", key=f"close_{item['id']}", use_container_width=True):
                            st.success(f"✅ {item['id']} marked as resolved!")
    
    # Reset mode button
    if st.session_state.get("issues_mode"):
        if st.button("← Back to Dashboard"):
            st.session_state.issues_mode = None
            st.rerun()

if __name__ == "__main__":
    render()