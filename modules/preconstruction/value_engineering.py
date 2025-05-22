"""
Value Engineering Module for Pre-Construction

This module provides tools for value engineering analysis:
- Cost savings opportunities
- Alternative material/system evaluation
- Life cycle cost analysis
- Constructability improvements
- VE proposal tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_value_engineering():
    """Render the Value Engineering dashboard"""
    st.header("Value Engineering")
    
    # Create tabs for different VE sections
    tabs = st.tabs([
        "Dashboard", 
        "VE Proposals", 
        "Life Cycle Analysis", 
        "Materials Alternatives", 
        "Review & Approval"
    ])
    
    # Dashboard tab
    with tabs[0]:
        render_ve_dashboard()
    
    # VE Proposals tab
    with tabs[1]:
        render_ve_proposals()
    
    # Life Cycle Analysis tab
    with tabs[2]:
        render_life_cycle_analysis()
    
    # Materials Alternatives tab
    with tabs[3]:
        render_materials_alternatives()
    
    # Review & Approval tab
    with tabs[4]:
        render_review_approval()

def render_ve_dashboard():
    """Render the Value Engineering dashboard"""
    
    # VE stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total VE Proposals",
            value="32",
            help="Total number of value engineering proposals"
        )
    
    with col2:
        st.metric(
            label="Approved",
            value="18",
            delta="+3",
            help="Approved value engineering proposals"
        )
    
    with col3:
        st.metric(
            label="In Review",
            value="8",
            help="Value engineering proposals under review"
        )
    
    with col4:
        st.metric(
            label="Rejected",
            value="6",
            help="Rejected value engineering proposals"
        )
    
    # VE savings
    col_savings1, col_savings2, col_savings3 = st.columns(3)
    
    with col_savings1:
        st.metric(
            label="Total Potential Savings",
            value="$2,845,000",
            help="Total potential savings from all VE proposals"
        )
    
    with col_savings2:
        st.metric(
            label="Approved Savings",
            value="$1,625,000",
            delta="+$275,000",
            help="Savings from approved VE proposals"
        )
    
    with col_savings3:
        st.metric(
            label="Savings % of Project Cost",
            value="3.6%",
            delta="+0.6%",
            help="Savings as percentage of total project cost"
        )
    
    # Savings by Category - Pie Chart
    st.subheader("Approved Savings by Category")
    
    savings_by_category = pd.DataFrame({
        "Category": ["Structural", "MEP Systems", "Finishes", "Envelope", "Site/Civil", "Other"],
        "Savings": [580000, 450000, 210000, 240000, 125000, 20000]
    })
    
    fig = px.pie(
        savings_by_category,
        values="Savings",
        names="Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=30, b=0, l=0, r=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # VE Proposals by Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent VE Proposals")
        
        recent_proposals = [
            {"id": "VE-28", "title": "Alternate Roof Insulation System", "savings": "$125,000", "status": "Approved", "date": "May 15, 2025"},
            {"id": "VE-29", "title": "Reduced Glass Types", "savings": "$85,000", "status": "In Review", "date": "May 12, 2025"},
            {"id": "VE-30", "title": "Alternative Lobby Flooring Material", "savings": "$65,000", "status": "In Review", "date": "May 10, 2025"},
            {"id": "VE-31", "title": "Simplified MEP Distribution", "savings": "$165,000", "status": "In Review", "date": "May 8, 2025"},
            {"id": "VE-32", "title": "Foundation Design Optimization", "savings": "$210,000", "status": "In Review", "date": "May 5, 2025"}
        ]
        
        for proposal in recent_proposals:
            status_color = "#4a90e2"  # Blue for In Review
            if proposal["status"] == "Approved":
                status_color = "#38d39f"  # Green
            elif proposal["status"] == "Rejected":
                status_color = "#e53935"  # Red
                
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #eee; border-radius: 5px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{proposal["id"]}: {proposal["title"]}</strong>
                    <span style="color: {status_color};">{proposal["status"]}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 14px;">
                    <span>Potential Savings: {proposal["savings"]}</span>
                    <span>Submitted: {proposal["date"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("VE Status by System")
        
        # Create a grouped bar chart for VE status by system
        status_by_system = pd.DataFrame({
            "System": ["Structural", "MEP", "Envelope", "Finishes", "Site", "Other"],
            "Approved": [4, 5, 3, 4, 1, 1],
            "In Review": [1, 2, 2, 1, 1, 1],
            "Rejected": [2, 1, 1, 1, 0, 1]
        })
        
        fig = px.bar(
            status_by_system, 
            x="System", 
            y=["Approved", "In Review", "Rejected"],
            barmode="group",
            color_discrete_sequence=["#38d39f", "#4a90e2", "#e53935"]
        )
        
        fig.update_layout(
            height=400,
            margin=dict(t=30, b=0, l=0, r=0),
            legend_title="Status"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_ve_proposals():
    """Render the VE Proposals section"""
    
    # Filter & Search controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.text_input("Search Proposals", placeholder="Enter keywords...")
    
    with col2:
        st.selectbox("Filter by System", ["All Systems", "Structural", "MEP", "Envelope", "Finishes", "Site/Civil", "Other"])
    
    with col3:
        st.selectbox("Status", ["All Status", "Approved", "In Review", "Rejected"])
    
    with col4:
        st.button("Add New Proposal", type="primary")
    
    # VE Proposals Table
    proposals = [
        {"id": "VE-01", "title": "Alternative Foundation System", "system": "Structural", "savings": "$310,000", "status": "Approved", "date": "Jan 10, 2025", "submitted_by": "John D."},
        {"id": "VE-02", "title": "Steel Section Optimization", "system": "Structural", "savings": "$180,000", "status": "Approved", "date": "Jan 15, 2025", "submitted_by": "Sarah T."},
        {"id": "VE-03", "title": "MEP Shaft Consolidation", "system": "MEP", "savings": "$95,000", "status": "Approved", "date": "Jan 20, 2025", "submitted_by": "Mike R."},
        {"id": "VE-04", "title": "Alternative Cooling System", "system": "MEP", "savings": "$125,000", "status": "Rejected", "date": "Jan 25, 2025", "submitted_by": "Sarah T."},
        {"id": "VE-05", "title": "Curtain Wall System Redesign", "system": "Envelope", "savings": "$150,000", "status": "Approved", "date": "Feb 1, 2025", "submitted_by": "Lisa K."},
        {"id": "VE-06", "title": "Alternative Roofing Material", "system": "Envelope", "savings": "$90,000", "status": "Approved", "date": "Feb 5, 2025", "submitted_by": "John D."},
        {"id": "VE-07", "title": "Parking Layout Optimization", "system": "Site/Civil", "savings": "$85,000", "status": "Approved", "date": "Feb 10, 2025", "submitted_by": "Mike R."},
        {"id": "VE-08", "title": "Common Area Flooring Alternative", "system": "Finishes", "savings": "$75,000", "status": "Approved", "date": "Feb 15, 2025", "submitted_by": "Lisa K."},
        {"id": "VE-28", "title": "Alternate Roof Insulation System", "system": "Envelope", "savings": "$125,000", "status": "Approved", "date": "May 15, 2025", "submitted_by": "John D."},
        {"id": "VE-29", "title": "Reduced Glass Types", "system": "Envelope", "savings": "$85,000", "status": "In Review", "date": "May 12, 2025", "submitted_by": "Sarah T."},
        {"id": "VE-30", "title": "Alternative Lobby Flooring Material", "system": "Finishes", "savings": "$65,000", "status": "In Review", "date": "May 10, 2025", "submitted_by": "Lisa K."},
        {"id": "VE-31", "title": "Simplified MEP Distribution", "system": "MEP", "savings": "$165,000", "status": "In Review", "date": "May 8, 2025", "submitted_by": "Mike R."},
        {"id": "VE-32", "title": "Foundation Design Optimization", "system": "Structural", "savings": "$210,000", "status": "In Review", "date": "May 5, 2025", "submitted_by": "John D."}
    ]
    
    # Create DataFrame
    df_proposals = pd.DataFrame(proposals)
    
    # Display with styling
    st.dataframe(
        df_proposals,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "title": st.column_config.TextColumn("Proposal Title", width="medium"),
            "system": st.column_config.TextColumn("System", width="small"),
            "savings": st.column_config.TextColumn("Potential Savings", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "date": st.column_config.TextColumn("Submission Date", width="small"),
            "submitted_by": st.column_config.TextColumn("Submitted By", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Proposal detail view
    st.subheader("Proposal Detail View")
    
    selected_proposal = st.selectbox(
        "Select Proposal to View", 
        [f"{p['id']}: {p['title']}" for p in proposals]
    )
    
    # Get ID from selection
    selected_id = selected_proposal.split(":")[0].strip()
    
    # Find the proposal
    selected_data = next((p for p in proposals if p["id"] == selected_id), None)
    
    if selected_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {selected_data['id']}: {selected_data['title']}")
            
            st.markdown(f"""
            **System:** {selected_data['system']}  
            **Potential Savings:** {selected_data['savings']}  
            **Status:** {selected_data['status']}  
            **Submitted:** {selected_data['date']}  
            **Submitted By:** {selected_data['submitted_by']}
            """)
            
            st.markdown("##### Description")
            
            # Mock description - in a real app, this would come from the database
            if selected_id == "VE-01":
                st.markdown("""
                Proposal to replace the deep pile foundation system with a mat foundation. Geotechnical analysis shows that soil conditions are suitable for a mat foundation, which would reduce excavation depth, eliminate pile drilling equipment, and reduce schedule by approximately 3 weeks.
                
                **Original Design:** Deep pile foundation with pile caps and grade beams  
                **Proposed Alternative:** Mat foundation with thickened edges under load-bearing elements
                """)
            elif selected_id == "VE-32":
                st.markdown("""
                Foundation design optimization through refined structural analysis and geotechnical parameters. By utilizing advanced 3D modeling and more precise loading calculations, we can reduce foundation thickness by 6" in non-critical areas while maintaining structural integrity and safety factors.
                
                **Original Design:** Uniform 24" mat foundation thickness  
                **Proposed Alternative:** Variable thickness mat foundation (18"-24") based on loading analysis
                """)
            else:
                st.markdown("""
                This value engineering proposal aims to reduce project costs while maintaining functionality, quality, and performance. The proposed alternative meets all code requirements and design criteria.
                
                **Original Design:** As per current drawings and specifications  
                **Proposed Alternative:** Optimized approach to achieve equivalent performance at lower cost
                """)
            
            st.markdown("##### Impact Analysis")
            
            col_impact1, col_impact2, col_impact3 = st.columns(3)
            
            with col_impact1:
                st.markdown("**Cost Impact**")
                st.success(f"Savings: {selected_data['savings']}")
            
            with col_impact2:
                st.markdown("**Schedule Impact**")
                schedule_impact = "Positive (saves 2-3 weeks)" if selected_id in ["VE-01", "VE-07", "VE-31"] else "Neutral (no change)"
                st.info(schedule_impact)
            
            with col_impact3:
                st.markdown("**Quality Impact**")
                quality_impact = "Neutral (maintains quality)" if selected_id not in ["VE-04"] else "Negative (reduced performance)"
                quality_color = "info" if quality_impact.startswith("Neutral") else "error"
                if quality_color == "info":
                    st.info(quality_impact)
                else:
                    st.error(quality_impact)
        
        with col2:
            st.markdown("##### Review Status")
            
            # Mock review data
            review_status = [
                {"reviewer": "Design Team", "status": "Approved", "date": "Feb 10, 2025", "comments": "Feasible option that meets design criteria."},
                {"reviewer": "Owner", "status": "Approved", "date": "Feb 12, 2025", "comments": "Acceptable alternative."},
                {"reviewer": "Construction Manager", "status": "Approved", "date": "Feb 8, 2025", "comments": "Will improve schedule and reduce complexity."}
            ]
            
            if selected_data["status"] == "Rejected":
                review_status = [
                    {"reviewer": "Design Team", "status": "Rejected", "date": "Feb 5, 2025", "comments": "Does not meet performance requirements."},
                    {"reviewer": "Owner", "status": "Rejected", "date": "Feb 6, 2025", "comments": "Unacceptable reduction in system quality."},
                    {"reviewer": "Construction Manager", "status": "In Review", "date": "Feb 4, 2025", "comments": "Checking constructability."}
                ]
            elif selected_data["status"] == "In Review":
                review_status = [
                    {"reviewer": "Design Team", "status": "In Review", "date": "May 18, 2025", "comments": "Checking structural implications."},
                    {"reviewer": "Owner", "status": "Pending", "date": "Pending", "comments": ""},
                    {"reviewer": "Construction Manager", "status": "In Review", "date": "May 16, 2025", "comments": "Evaluating schedule impact."}
                ]
            
            for review in review_status:
                status_color = "#4a90e2"  # Blue for In Review
                if review["status"] == "Approved":
                    status_color = "#38d39f"  # Green
                elif review["status"] == "Rejected":
                    status_color = "#e53935"  # Red
                elif review["status"] == "Pending":
                    status_color = "#9e9e9e"  # Gray
                    
                st.markdown(f"""
                <div style="padding: 10px; border: 1px solid #eee; border-radius: 5px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{review["reviewer"]}</strong>
                        <span style="color: {status_color};">{review["status"]}</span>
                    </div>
                    <div style="font-size: 12px; color: #6c757d;">{review["date"]}</div>
                    <div style="margin-top: 5px; font-size: 14px;">{review["comments"]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Approval actions
            if selected_data["status"] == "In Review":
                st.selectbox("Decision", ["Select Action", "Approve", "Reject", "Request More Information"])
                st.text_area("Comments", placeholder="Enter review comments...")
                st.button("Submit Review")

def render_life_cycle_analysis():
    """Render the Life Cycle Analysis section"""
    
    st.subheader("Life Cycle Cost Analysis")
    
    # Explanation
    st.markdown("""
    Life cycle cost analysis (LCCA) evaluates total cost of ownership over the life of the building,
    including initial construction costs, operation, maintenance, and replacement costs. This analysis
    helps identify options that may have higher upfront costs but provide better long-term value.
    """)
    
    # System selection
    system = st.selectbox(
        "Select System for Life Cycle Analysis", 
        ["HVAC Systems", "Building Envelope", "Lighting Systems", "Flooring Materials", "Roofing Systems"]
    )
    
    # HVAC System Analysis
    if system == "HVAC Systems":
        st.markdown("#### HVAC System Alternatives Life Cycle Analysis")
        
        # System options
        options = ["Variable Refrigerant Flow (VRF)", "Water-source Heat Pump", "Chiller + VAV System", "Rooftop Package Units"]
        
        # Life cycle periods
        periods = [1, 5, 10, 15, 20, 25, 30]
        
        # Create data for each option
        vrf_data = [3200000, 3500000, 4000000, 4700000, 5600000, 6700000, 7900000]
        wshp_data = [3400000, 3650000, 4100000, 4600000, 5300000, 6100000, 7100000]
        chiller_data = [2900000, 3400000, 4100000, 4900000, 6000000, 7300000, 8900000]
        rtu_data = [2200000, 3000000, 4000000, 5200000, 6600000, 8200000, 10000000]
        
        # Create DataFrame for chart
        df_lcc = pd.DataFrame({
            "Year": periods,
            "VRF": vrf_data,
            "Water-source Heat Pump": wshp_data,
            "Chiller + VAV": chiller_data,
            "Rooftop Units": rtu_data
        })
        
        # Plot line chart
        fig = px.line(
            df_lcc, 
            x="Year", 
            y=["VRF", "Water-source Heat Pump", "Chiller + VAV", "Rooftop Units"],
            labels={"value": "Cumulative Cost ($)", "variable": "System Type"},
            title="Cumulative Life Cycle Cost Comparison"
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # System comparison table
        st.markdown("#### System Comparison")
        
        system_comparison = pd.DataFrame({
            "System": options,
            "Initial Cost": ["$3,200,000", "$3,400,000", "$2,900,000", "$2,200,000"],
            "Annual Energy Cost": ["$95,000", "$80,000", "$125,000", "$180,000"],
            "Annual Maintenance": ["$30,000", "$35,000", "$40,000", "$45,000"],
            "Expected Life": ["20 years", "25 years", "25 years", "15 years"],
            "Replacement Cost": ["$2,200,000", "$2,300,000", "$2,100,000", "$1,800,000"],
            "30-Year Cost": ["$7,900,000", "$7,100,000", "$8,900,000", "$10,000,000"]
        })
        
        st.dataframe(system_comparison, hide_index=True, use_container_width=True)
        
        # Recommendation
        st.markdown("#### Recommendation")
        
        st.markdown("""
        Based on life cycle cost analysis, the **Water-source Heat Pump** system provides the best long-term value
        with a 30-year life cycle cost of $7.1M, which is $800,000 less than the VRF option and $1.8M less than
        the Chiller + VAV option.
        
        While the Water-source Heat Pump system has a higher initial cost than the Chiller + VAV option,
        its lower energy costs and maintenance requirements result in a lower total cost of ownership
        over the 30-year analysis period.
        
        **Recommendation:** Proceed with Water-source Heat Pump system design.
        """)
    
    # Simplified versions for other systems
    else:
        st.info(f"Life cycle analysis for {system} is under development. Please select 'HVAC Systems' for a complete demonstration.")

def render_materials_alternatives():
    """Render the Materials Alternatives section"""
    
    st.subheader("Material/System Alternatives Analysis")
    
    # Category selection
    category = st.selectbox(
        "Select Category", 
        ["Structural Systems", "Exterior Envelope", "Interior Finishes", "MEP Systems", "Site Development"]
    )
    
    # For this demo, we'll show exterior envelope alternatives
    if category == "Exterior Envelope":
        st.markdown("#### Exterior Wall System Alternatives")
        
        # Alternatives
        alternatives = [
            {
                "name": "Curtain Wall System (Original Design)",
                "description": "Aluminum curtain wall system with insulated glass units and spandrel panels.",
                "cost": "$85 per SF",
                "schedule": "14 weeks lead time",
                "performance": "U-value: 0.38, SHGC: 0.28",
                "aesthetics": "High visibility, modern appearance",
                "constructability": "Moderate complexity",
                "image": "https://via.placeholder.com/150?text=Curtain+Wall",
                "selected": True
            },
            {
                "name": "Precast Concrete with Punched Windows",
                "description": "Insulated precast concrete panels with punched window openings.",
                "cost": "$65 per SF",
                "schedule": "12 weeks lead time",
                "performance": "U-value: 0.35, SHGC: 0.35",
                "aesthetics": "Institutional appearance",
                "constructability": "Simple installation",
                "image": "https://via.placeholder.com/150?text=Precast",
                "selected": False
            },
            {
                "name": "Metal Panel System",
                "description": "Insulated metal panel system with strip windows.",
                "cost": "$70 per SF",
                "schedule": "10 weeks lead time",
                "performance": "U-value: 0.40, SHGC: 0.30",
                "aesthetics": "Modern industrial appearance",
                "constructability": "Simple installation",
                "image": "https://via.placeholder.com/150?text=Metal+Panel",
                "selected": False
            },
            {
                "name": "EIFS with Storefront Windows",
                "description": "Exterior insulation and finish system with aluminum storefront windows.",
                "cost": "$55 per SF",
                "schedule": "8 weeks lead time",
                "performance": "U-value: 0.32, SHGC: 0.35",
                "aesthetics": "Stucco-like appearance",
                "constructability": "Moderate complexity",
                "image": "https://via.placeholder.com/150?text=EIFS",
                "selected": False
            }
        ]
        
        # Display alternatives as cards
        col1, col2 = st.columns(2)
        
        for i, alt in enumerate(alternatives):
            with col1 if i % 2 == 0 else col2:
                border_style = "border: 2px solid #4CAF50;" if alt["selected"] else "border: 1px solid #e0e0e0;"
                
                st.markdown(f"""
                <div style="padding: 15px; {border_style} border-radius: 5px; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <img src="{alt["image"]}" style="width: 80px; height: 80px; object-fit: cover; margin-right: 15px; border-radius: 4px;">
                        <div>
                            <div style="font-weight: 600; font-size: 16px;">{alt["name"]}</div>
                            <div style="font-size: 14px; color: #666;">{alt["description"]}</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <strong>Cost:</strong>
                            <span>{alt["cost"]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <strong>Lead Time:</strong>
                            <span>{alt["schedule"]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <strong>Performance:</strong>
                            <span>{alt["performance"]}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <strong>Constructability:</strong>
                            <span>{alt["constructability"]}</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 10px;">
                        {f'<span style="background-color: #E8F5E9; color: #4CAF50; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: 500;">SELECTED</span>' if alt["selected"] else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Cost comparison
        st.markdown("#### Cost Comparison")
        
        # Create cost data
        cost_data = pd.DataFrame({
            "Alternative": ["Curtain Wall", "Precast Concrete", "Metal Panel", "EIFS"],
            "Material Cost": [65, 50, 55, 40],
            "Labor Cost": [20, 15, 15, 15]
        })
        
        # Calculate total cost
        cost_data["Total Cost"] = cost_data["Material Cost"] + cost_data["Labor Cost"]
        
        # Create stacked bar chart
        fig = px.bar(
            cost_data, 
            x="Alternative", 
            y=["Material Cost", "Labor Cost"],
            title="Cost per Square Foot",
            labels={"value": "Cost per SF ($)"},
            barmode="stack"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # System performance radar chart
        st.markdown("#### Performance Comparison")
        
        # Create performance data (1-10 scale)
        performance_data = {
            "Category": ["Thermal", "Acoustics", "Durability", "Maintenance", "Aesthetics", "Cost"],
            "Curtain Wall": [7, 6, 8, 7, 9, 5],
            "Precast Concrete": [8, 9, 9, 9, 6, 7],
            "Metal Panel": [7, 7, 7, 8, 8, 6],
            "EIFS": [8, 6, 6, 5, 7, 8]
        }
        
        # Create radar chart
        fig = go.Figure()
        
        for system in ["Curtain Wall", "Precast Concrete", "Metal Panel", "EIFS"]:
            fig.add_trace(go.Scatterpolar(
                r=performance_data[system],
                theta=performance_data["Category"],
                fill='toself',
                name=system
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # VE recommendation
        st.markdown("#### Recommendation")
        
        selected_system = st.radio(
            "Select Recommended Alternative",
            ["Curtain Wall System (Original Design)", "Precast Concrete with Punched Windows", "Metal Panel System", "EIFS with Storefront Windows"]
        )
        
        st.text_area(
            "Recommendation Justification",
            value="The precast concrete system provides a 24% cost savings over the original curtain wall design while meeting all performance requirements. The precast system also offers improved durability, reduced maintenance, and simplified installation that could accelerate the construction schedule. Impact on aesthetics is minimal for the North and East facades.",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("Save Recommendation", type="primary")
        
        with col2:
            st.button("Cancel")
    
    # Simplified version for other categories
    else:
        st.info(f"Materials alternatives analysis for {category} is under development. Please select 'Exterior Envelope' for a complete demonstration.")

def render_review_approval():
    """Render the Review & Approval section"""
    
    st.subheader("VE Review & Approval Process")
    
    # Process explanation
    st.markdown("""
    The Value Engineering review and approval process ensures all stakeholders have input on proposed changes.
    Each VE item follows this workflow from submission to implementation.
    """)
    
    # Process flowchart
    st.image("https://via.placeholder.com/800x200?text=VE+Review+Process+Flowchart", caption="Value Engineering Review Process")
    
    # Pending approvals
    st.markdown("#### Pending Approvals")
    
    # Pending items
    pending_items = [
        {"id": "VE-29", "title": "Reduced Glass Types", "savings": "$85,000", "submitted": "May 12, 2025", "designer": "In Review", "owner": "Pending", "cm": "Approved"},
        {"id": "VE-30", "title": "Alternative Lobby Flooring Material", "savings": "$65,000", "submitted": "May 10, 2025", "designer": "Approved", "owner": "In Review", "cm": "Approved"},
        {"id": "VE-31", "title": "Simplified MEP Distribution", "savings": "$165,000", "submitted": "May 8, 2025", "designer": "In Review", "owner": "Pending", "cm": "In Review"},
        {"id": "VE-32", "title": "Foundation Design Optimization", "savings": "$210,000", "submitted": "May 5, 2025", "designer": "In Review", "owner": "Pending", "cm": "Approved"}
    ]
    
    # Create DataFrame
    df_pending = pd.DataFrame(pending_items)
    
    # Display with styling
    st.dataframe(
        df_pending,
        column_config={
            "id": st.column_config.TextColumn("VE ID", width="small"),
            "title": st.column_config.TextColumn("Title", width="medium"),
            "savings": st.column_config.TextColumn("Savings", width="small"),
            "submitted": st.column_config.TextColumn("Submitted", width="small"),
            "designer": st.column_config.TextColumn("Designer", width="small"),
            "owner": st.column_config.TextColumn("Owner", width="small"),
            "cm": st.column_config.TextColumn("Construction Manager", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # My pending reviews
    st.markdown("#### My Pending Reviews")
    
    my_reviews = [
        {"id": "VE-29", "title": "Reduced Glass Types", "savings": "$85,000", "deadline": "May 25, 2025", "days_left": 3},
        {"id": "VE-31", "title": "Simplified MEP Distribution", "savings": "$165,000", "deadline": "May 22, 2025", "days_left": 0},
        {"id": "VE-32", "title": "Foundation Design Optimization", "savings": "$210,000", "deadline": "May 20, 2025", "days_left": -2}
    ]
    
    for review in my_reviews:
        days_color = "#4a90e2"  # Blue for default
        days_text = f"{review['days_left']} days left"
        
        if review["days_left"] < 0:
            days_color = "#e53935"  # Red for overdue
            days_text = f"{abs(review['days_left'])} days overdue"
        elif review["days_left"] == 0:
            days_color = "#ff9800"  # Orange for due today
            days_text = "Due today"
        
        st.markdown(f"""
        <div style="padding: 12px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>{review["id"]}: {review["title"]}</strong>
                <div style="font-size: 14px;">Potential Savings: {review["savings"]}</div>
            </div>
            <div style="text-align: right;">
                <div>Deadline: {review["deadline"]}</div>
                <div style="color: {days_color}; font-weight: 500;">{days_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Complete review form
    st.markdown("#### Complete Review")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Select VE Item to Review", [f"{r['id']}: {r['title']}" for r in my_reviews])
    
    with col2:
        st.selectbox("Decision", ["Select Decision", "Approve", "Reject", "Request Additional Information"])
    
    st.text_area("Review Comments", placeholder="Enter your comments about this VE proposal...")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.button("Submit Review", type="primary")
    
    with col4:
        st.button("Save Draft")