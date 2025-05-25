"""
Subcontractor Management Module
Highland Tower Development - Managing Sub Trades
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render():
    """Render the Subcontractor Management module"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
            👥 Subcontractor Management
        </h1>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Highland Tower Development - Sub Trade Coordination
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add Subcontractor", type="primary", use_container_width=True):
            st.session_state.show_add_sub = True
    
    with col2:
        if st.button("📋 Performance Review", use_container_width=True):
            st.session_state.show_performance = True
    
    with col3:
        if st.button("💰 Payment Status", use_container_width=True):
            st.session_state.show_payments = True
    
    with col4:
        if st.button("📊 Sub Reports", use_container_width=True):
            st.session_state.show_reports = True
    
    # Highland Tower Active Subcontractors
    st.markdown("### 🏗️ Highland Tower Active Subcontractors")
    
    subcontractors_data = pd.DataFrame([
        {
            "Company": "Steel Fabricators Inc",
            "Trade": "Structural Steel",
            "Contract Value": "$2,850,000",
            "Progress": "85%",
            "Performance": "Excellent",
            "Payment Status": "Current",
            "Contact": "Mike Johnson"
        },
        {
            "Company": "Premier Concrete",
            "Trade": "Concrete & Foundation",
            "Contract Value": "$1,950,000", 
            "Progress": "95%",
            "Performance": "Good",
            "Payment Status": "Current",
            "Contact": "Sarah Davis"
        },
        {
            "Company": "Elite MEP Solutions",
            "Trade": "HVAC & Plumbing",
            "Contract Value": "$3,200,000",
            "Progress": "65%",
            "Performance": "Excellent",
            "Payment Status": "Pending",
            "Contact": "Alex Rodriguez"
        },
        {
            "Company": "Precision Electrical",
            "Trade": "Electrical Systems",
            "Contract Value": "$2,100,000",
            "Progress": "70%",
            "Performance": "Good", 
            "Payment Status": "Current",
            "Contact": "Lisa Chen"
        },
        {
            "Company": "Glazing Specialists",
            "Trade": "Windows & Curtain Wall",
            "Contract Value": "$1,650,000",
            "Progress": "45%",
            "Performance": "Good",
            "Payment Status": "Current",
            "Contact": "Tom Wilson"
        }
    ])
    
    # Display subcontractors with performance indicators
    for idx, sub in subcontractors_data.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{sub['Company']}**")
                st.caption(f"{sub['Trade']} • Contact: {sub['Contact']}")
            
            with col2:
                st.metric("Contract Value", sub['Contract Value'])
            
            with col3:
                progress = int(sub['Progress'].replace('%', ''))
                st.progress(progress / 100)
                st.caption(f"{sub['Progress']} Complete")
            
            with col4:
                if sub['Performance'] == "Excellent":
                    st.success(f"⭐ {sub['Performance']}")
                else:
                    st.info(f"👍 {sub['Performance']}")
            
            with col5:
                if sub['Payment Status'] == "Current":
                    st.success("💚 Current")
                else:
                    st.warning("⏳ Pending")
        
        st.markdown("---")
    
    # Sub trade performance metrics
    tab1, tab2, tab3 = st.tabs(["📊 Performance Metrics", "💰 Financial Summary", "📋 Issues Tracking"])
    
    with tab1:
        render_performance_metrics()
    
    with tab2:
        render_financial_summary(subcontractors_data)
    
    with tab3:
        render_issues_tracking()

def render_performance_metrics():
    """Render subcontractor performance metrics"""
    
    st.markdown("### 📈 Highland Tower Subcontractor Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Progress", "72%", "+5% this month")
    
    with col2:
        st.metric("On-Time Performance", "88%", "+2%")
    
    with col3:
        st.metric("Quality Score", "4.2/5", "Excellent")
    
    with col4:
        st.metric("Safety Compliance", "96%", "Above target")
    
    # Performance tracking chart
    st.markdown("#### 📊 Monthly Performance Trends")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    performance_data = pd.DataFrame({
        "Month": months,
        "Schedule Performance": [85, 87, 89, 88, 92],
        "Quality Score": [4.1, 4.0, 4.2, 4.3, 4.2],
        "Safety Score": [94, 95, 96, 97, 96]
    })
    
    st.line_chart(performance_data.set_index("Month"))

def render_financial_summary(subcontractors_data):
    """Render financial summary for subcontractors"""
    
    st.markdown("### 💰 Highland Tower Financial Summary")
    
    # Calculate totals
    total_contracts = subcontractors_data['Contract Value'].str.replace('$', '').str.replace(',', '').astype(float).sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Subcontract Value", f"${total_contracts:,.0f}")
    
    with col2:
        st.metric("Payments Made", f"${total_contracts * 0.68:,.0f}")
    
    with col3:
        st.metric("Remaining Balance", f"${total_contracts * 0.32:,.0f}")
    
    # Payment status breakdown
    st.markdown("#### 💳 Payment Status Breakdown")
    
    payment_data = pd.DataFrame([
        {"Status": "Current", "Count": 4, "Value": "$8,750,000"},
        {"Status": "Pending", "Count": 1, "Value": "$3,200,000"},
        {"Status": "Overdue", "Count": 0, "Value": "$0"}
    ])
    
    st.dataframe(payment_data, use_container_width=True, hide_index=True)

def render_issues_tracking():
    """Render subcontractor issues tracking"""
    
    st.markdown("### ⚠️ Highland Tower Sub Trade Issues")
    
    issues_data = pd.DataFrame([
        {
            "Date": "2025-01-20",
            "Subcontractor": "Elite MEP Solutions", 
            "Issue": "HVAC equipment delivery delayed",
            "Priority": "High",
            "Status": "In Progress",
            "Assigned To": "Project Manager"
        },
        {
            "Date": "2025-01-18",
            "Subcontractor": "Glazing Specialists",
            "Issue": "Window frame specification clarification needed",
            "Priority": "Medium", 
            "Status": "Resolved",
            "Assigned To": "Site Engineer"
        },
        {
            "Date": "2025-01-15",
            "Subcontractor": "Precision Electrical",
            "Issue": "Coordination with MEP trades required",
            "Priority": "Medium",
            "Status": "Open",
            "Assigned To": "MEP Coordinator"
        }
    ])
    
    for idx, issue in issues_data.iterrows():
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        status_color = {"Open": "⚪", "In Progress": "🟡", "Resolved": "🟢"}
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.markdown(f"**{issue['Issue']}**")
            st.caption(f"{issue['Subcontractor']} • {issue['Date']}")
        
        with col2:
            st.write(f"Assigned: {issue['Assigned To']}")
        
        with col3:
            st.write(f"{priority_color[issue['Priority']]} {issue['Priority']}")
        
        with col4:
            st.write(f"{status_color[issue['Status']]} {issue['Status']}")
        
        st.markdown("---")

if __name__ == "__main__":
    render()