"""
Site Analysis Module

This module provides tools for analyzing construction sites, including:
- Site surveys
- Environmental assessments
- Utilities analysis
- Topography and soil conditions
- Zoning and regulatory compliance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_site_analysis():
    """Render the Site Analysis dashboard"""
    st.header("Site Analysis")
    
    # Create tabs for different site analysis sections
    tabs = st.tabs([
        "Overview", 
        "Environmental", 
        "Utilities", 
        "Topography & Soil", 
        "Zoning & Compliance"
    ])
    
    # Overview tab
    with tabs[0]:
        render_site_overview()
    
    # Environmental tab
    with tabs[1]:
        render_environmental()
    
    # Utilities tab
    with tabs[2]:
        render_utilities()
    
    # Topography & Soil tab
    with tabs[3]:
        render_topography_soil()
    
    # Zoning & Compliance tab
    with tabs[4]:
        render_zoning_compliance()

def render_site_overview():
    """Render the site overview section"""
    # Site overview statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Site Information")
        st.write("**Location:** Downtown Highland District")
        st.write("**Site Area:** 1.2 acres (52,272 sq ft)")
        st.write("**Elevation Range:** 245-258 ft above sea level")
        st.write("**Soil Type:** Urban fill over clay")
        st.write("**Current Zoning:** Mixed-use commercial/residential")
        
        # Site survey status
        st.markdown("#### Site Survey Status")
        survey_status = {
            "Boundary Survey": "Complete",
            "Topographic Survey": "Complete",
            "Tree Survey": "Complete",
            "Utility Location": "Complete",
            "Environmental Assessment": "Complete",
            "Geotechnical Investigation": "Complete"
        }
        
        for item, status in survey_status.items():
            status_color = "#38d39f" if status == "Complete" else "#f59e0b"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 3px 0;">
                <span>{item}</span>
                <span style="color: {status_color};">{status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Site image placeholder
        st.image("https://via.placeholder.com/800x600?text=Site+Plan", caption="Site Plan")
        
        # Upload functionality for site documents
        with st.expander("Site Documents"):
            st.file_uploader("Upload Site Documents", type=["pdf", "jpg", "png"], accept_multiple_files=True)
            
            # Mock documents already uploaded
            st.markdown("#### Available Documents")
            site_docs = [
                "Site Survey.pdf",
                "Property Deed.pdf",
                "Environmental Report.pdf",
                "Traffic Study.pdf",
                "Preliminary Geotech Report.pdf"
            ]
            
            for doc in site_docs:
                st.markdown(f"📄 {doc}")

def render_environmental():
    """Render the environmental assessment section"""
    st.subheader("Environmental Assessment")
    
    # Environmental summary
    st.markdown("""
    #### Environmental Summary
    The site has been assessed for environmental concerns and is suitable for residential
    and commercial development with appropriate mitigation measures.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Environmental findings
        st.markdown("#### Environmental Findings")
        
        findings = [
            {"category": "Soil Contamination", "level": "Low", "status": "Remediated"},
            {"category": "Groundwater Quality", "level": "Acceptable", "status": "Monitoring"},
            {"category": "Air Quality", "level": "Good", "status": "Compliant"},
            {"category": "Noise Levels", "level": "Moderate", "status": "Mitigation Required"},
            {"category": "Protected Species", "level": "None Detected", "status": "Compliant"},
            {"category": "Wetlands", "level": "None Present", "status": "Compliant"},
            {"category": "Historical Significance", "level": "Low", "status": "Documented"}
        ]
        
        for finding in findings:
            level_color = "#38d39f"  # Default green
            if finding["level"] in ["Moderate", "Medium"]:
                level_color = "#f59e0b"  # Orange/yellow
            elif finding["level"] in ["High", "Severe"]:
                level_color = "#ef4444"  # Red
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border-left: 3px solid {level_color}; background-color: #f8f9fa;">
                <strong>{finding["category"]}</strong>
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>Level: <span style="color: {level_color};">{finding["level"]}</span></span>
                    <span>Status: {finding["status"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Required actions
        st.markdown("#### Required Mitigation Actions")
        
        actions = [
            {"action": "Noise barrier installation", "deadline": "Prior to construction", "status": "Planned"},
            {"action": "Soil remediation documentation", "deadline": "Complete", "status": "Submitted"},
            {"action": "Groundwater monitoring wells", "deadline": "Phase 1 construction", "status": "Designed"},
            {"action": "Dust control plan", "deadline": "Prior to excavation", "status": "Draft Complete"}
        ]
        
        for action in actions:
            status_color = "#4a90e2"  # Blue
            if action["status"] == "Complete":
                status_color = "#38d39f"  # Green
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <strong>{action["action"]}</strong>
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 5px;">
                    <span>Deadline: {action["deadline"]}</span>
                    <span style="color: {status_color};">{action["status"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Environmental risk chart
        st.markdown("#### Environmental Risk Assessment")
        
        risk_data = pd.DataFrame({
            "Category": ["Soil", "Water", "Air", "Noise", "Hazmat", "Ecological"],
            "Risk Score": [2, 1, 1, 3, 1, 0],
            "Max Risk": [5, 5, 5, 5, 5, 5]
        })
        
        fig = px.bar(
            risk_data, 
            x="Category", 
            y="Risk Score",
            color="Risk Score",
            color_continuous_scale=["green", "yellow", "red"],
            range_color=[0, 5],
            labels={"Risk Score": "Risk Level (0-5)"}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def render_utilities():
    """Render the utilities analysis section"""
    st.subheader("Utilities Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Existing Utilities")
        
        utilities = [
            {"type": "Water", "provider": "Highland Water Authority", "capacity": "Adequate", "connection": "6\" main on North Ave"},
            {"type": "Sewer", "provider": "Highland Water Authority", "capacity": "Adequate", "connection": "8\" main on North Ave"},
            {"type": "Electricity", "provider": "Highland Energy", "capacity": "Adequate", "connection": "Underground on East Side"},
            {"type": "Natural Gas", "provider": "Highland Gas", "capacity": "Adequate", "connection": "4\" line on West Side"},
            {"type": "Telecom", "provider": "Multiple Providers", "capacity": "Fiber Available", "connection": "Underground conduit"}
        ]
        
        for utility in utilities:
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <strong>{utility["type"]}</strong>
                <div style="font-size: 14px; margin-top: 5px;">
                    <div><strong>Provider:</strong> {utility["provider"]}</div>
                    <div><strong>Capacity:</strong> {utility["capacity"]}</div>
                    <div><strong>Connection Point:</strong> {utility["connection"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Utility Relocation Requirements")
        
        relocations = [
            {"utility": "Power line", "scope": "Relocate overhead lines to underground", "cost": "$120,000", "timeline": "6-8 weeks", "status": "Approved"},
            {"utility": "Water main", "scope": "Replace aging 4\" main with 6\" main", "cost": "$85,000", "timeline": "3-4 weeks", "status": "Pending Approval"},
            {"utility": "Telecom", "scope": "Relocate junction box outside building footprint", "cost": "$35,000", "timeline": "2 weeks", "status": "Scheduled"}
        ]
        
        for relocation in relocations:
            status_color = "#4a90e2"  # Blue 
            if relocation["status"] == "Approved":
                status_color = "#38d39f"  # Green
            elif relocation["status"] == "Rejected":
                status_color = "#ef4444"  # Red
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <strong>{relocation["utility"]}</strong>
                <div style="font-size: 14px; margin-top: 5px;">
                    <div><strong>Scope:</strong> {relocation["scope"]}</div>
                    <div><strong>Est. Cost:</strong> {relocation["cost"]}</div>
                    <div><strong>Timeline:</strong> {relocation["timeline"]}</div>
                    <div><strong>Status:</strong> <span style="color: {status_color};">{relocation["status"]}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Utility cost summary
        st.markdown("#### Utility Connection Costs")
        
        connection_costs = pd.DataFrame({
            "Utility": ["Water", "Sewer", "Electricity", "Gas", "Telecom"],
            "Cost": [150000, 125000, 200000, 75000, 50000]
        })
        
        fig = px.pie(
            connection_costs, 
            values="Cost", 
            names="Utility",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def render_topography_soil():
    """Render the topography and soil analysis section"""
    st.subheader("Topography & Soil Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Elevation Profile")
        
        # Mock elevation data
        elevation_data = pd.DataFrame({
            "Position": [f"P{i}" for i in range(1, 11)],
            "Elevation (ft)": [245, 247, 249, 252, 253, 255, 257, 258, 256, 254]
        })
        
        fig = px.line(
            elevation_data, 
            x="Position", 
            y="Elevation (ft)",
            markers=True
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Soil boring results
        st.markdown("#### Soil Boring Test Results")
        
        boring_data = pd.DataFrame({
            "Depth (ft)": [5, 10, 15, 20, 25, 30],
            "Soil Type": ["Fill", "Sandy Clay", "Clay", "Clay", "Weathered Rock", "Bedrock"],
            "SPT (N-value)": [8, 15, 25, 30, 50, "Refusal"],
            "Moisture (%)": [18, 22, 25, 20, 12, 5]
        })
        
        st.dataframe(boring_data, use_container_width=True)
    
    with col2:
        st.markdown("#### Geotechnical Recommendations")
        
        recommendations = [
            "Deep foundations (piles) extending to bedrock at 30' depth",
            "Waterproofing system for below-grade construction",
            "Dewatering system during excavation",
            "Engineered fill for utility trenches",
            "Subsurface drainage system around foundation"
        ]
        
        for i, rec in enumerate(recommendations):
            st.markdown(f"**{i+1}.** {rec}")
        
        # Foundation options
        st.markdown("#### Foundation Options Analysis")
        
        foundation_options = [
            {"type": "Drilled Piers", "cost": "High", "time": "Long", "risk": "Low", "recommended": True},
            {"type": "Driven Piles", "cost": "High", "time": "Medium", "risk": "Low", "recommended": False},
            {"type": "Spread Footings", "cost": "Medium", "time": "Short", "risk": "High", "recommended": False},
            {"type": "Mat Foundation", "cost": "High", "time": "Medium", "risk": "Medium", "recommended": False}
        ]
        
        for option in foundation_options:
            highlight = "background-color: #edf7ed; border-left: 3px solid #38d39f;" if option["recommended"] else ""
            
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; {highlight}">
                <strong>{option["type"]}</strong>
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 5px;">
                    <span>Cost: {option["cost"]}</span>
                    <span>Time: {option["time"]}</span>
                    <span>Risk: {option["risk"]}</span>
                </div>
                {f'<div style="color: #38d39f; margin-top: 5px;"><strong>✓ RECOMMENDED</strong></div>' if option["recommended"] else ''}
            </div>
            """, unsafe_allow_html=True)

def render_zoning_compliance():
    """Render the zoning and compliance section"""
    st.subheader("Zoning & Regulatory Compliance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Zoning Information")
        
        st.markdown("""
        **Current Zoning:** MXU-3 (Mixed-Use Urban)
        
        **Allowed Uses:**
        - Multi-family residential
        - Retail (ground floor)
        - Office
        - Restaurant
        - Hotel
        
        **Building Requirements:**
        - Maximum height: 180 feet
        - Setbacks: 10 ft (front), 5 ft (sides), 15 ft (rear)
        - FAR (Floor Area Ratio): 6.0
        - Minimum open space: 15%
        - Parking requirement: 0.75 spaces per residential unit, 1 per 500 SF commercial
        """)
        
        # Compliance status
        st.markdown("#### Compliance Status")
        
        compliance_items = [
            {"item": "Height Limitation", "requirement": "Max 180 ft", "proposed": "165 ft", "status": "Compliant"},
            {"item": "Setbacks", "requirement": "10'/5'/15'", "proposed": "15'/10'/20'", "status": "Compliant"},
            {"item": "FAR", "requirement": "Max 6.0", "proposed": "5.8", "status": "Compliant"},
            {"item": "Open Space", "requirement": "Min 15%", "proposed": "18%", "status": "Compliant"},
            {"item": "Parking", "requirement": "110 spaces", "proposed": "120 spaces", "status": "Compliant"}
        ]
        
        for item in compliance_items:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <span><strong>{item["item"]}</strong></span>
                <span>Req: {item["requirement"]}</span>
                <span>Proposed: {item["proposed"]}</span>
                <span style="color: #38d39f;">{item["status"]}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Required Permits & Approvals")
        
        permits = [
            {"name": "Site Plan Approval", "agency": "City Planning Commission", "status": "Approved", "date": "Jan 15, 2025"},
            {"name": "Building Permit", "agency": "Building Department", "status": "Pending", "date": "Est. Jun 2025"},
            {"name": "Demolition Permit", "agency": "Building Department", "status": "Approved", "date": "Feb 28, 2025"},
            {"name": "Environmental Clearance", "agency": "DEP", "status": "Approved", "date": "Dec 10, 2024"},
            {"name": "Curb Cut Permit", "agency": "DOT", "status": "Pending", "date": "Est. May 2025"},
            {"name": "Water/Sewer Connection", "agency": "Water Authority", "status": "Not Submitted", "date": "Est. Jul 2025"}
        ]
        
        for permit in permits:
            status_color = "#4a90e2"  # Blue for Pending
            if permit["status"] == "Approved":
                status_color = "#38d39f"  # Green
            elif permit["status"] == "Rejected":
                status_color = "#ef4444"  # Red
            elif permit["status"] == "Not Submitted":
                status_color = "#6c757d"  # Grey
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <strong>{permit["name"]}</strong>
                <div style="font-size: 14px; margin-top: 5px;">
                    <div><strong>Agency:</strong> {permit["agency"]}</div>
                    <div><strong>Status:</strong> <span style="color: {status_color};">{permit["status"]}</span></div>
                    <div><strong>Date:</strong> {permit["date"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Variance requests
        st.markdown("#### Variance Requests")
        st.markdown("*No variances required for current design*")