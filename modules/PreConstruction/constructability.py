"""
Constructability Review Module

This module provides tools for constructability review, including:
- Design review for construction efficiency
- Sequencing and phasing analysis
- Construction risk assessment
- Logistics planning
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_constructability():
    """Render the Constructability Review dashboard"""
    st.header("Constructability Review")
    
    # Introduction
    st.markdown("""
    Constructability Review ensures that designs can be efficiently and safely built
    within the project constraints. It identifies issues early to prevent costly changes
    during construction.
    """)
    
    # Create tabs for different constructability sections
    tabs = st.tabs([
        "Review Summary", 
        "Issues Log", 
        "Design Recommendations", 
        "Sequencing", 
        "Site Logistics"
    ])
    
    # Review summary tab
    with tabs[0]:
        render_review_summary()
    
    # Issues log tab
    with tabs[1]:
        render_issues_log()
    
    # Design recommendations tab
    with tabs[2]:
        render_design_recommendations()
    
    # Sequencing tab
    with tabs[3]:
        render_sequencing()
    
    # Site logistics tab
    with tabs[4]:
        render_site_logistics()

def render_review_summary():
    """Render the constructability review summary section"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Constructability Review Summary")
        
        # Project info
        st.info("""
        **Highland Tower Development**
        
        Constructability review conducted at 90% CD phase.
        Review team: John Davis (PM), Michael Chen (Superintendent), Sarah Wilson (MEP Coordinator),
        Robert Johnson (Structural Engineer), Lisa Martinez (Architect)
        """)
        
        # Summary metrics
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric(
                label="Total Issues",
                value="45",
                help="Total number of constructability issues identified"
            )
        
        with metrics_col2:
            st.metric(
                label="Critical Issues",
                value="8",
                delta="-3",
                delta_color="inverse",
                help="Number of critical issues requiring immediate attention"
            )
        
        with metrics_col3:
            st.metric(
                label="Resolved",
                value="32",
                delta="71%",
                help="Number of issues resolved"
            )
        
        with metrics_col4:
            st.metric(
                label="Cost Impact",
                value="$350K",
                delta="-$150K",
                delta_color="inverse",
                help="Estimated cost impact of identified issues"
            )
        
        # Review progress
        st.subheader("Review Progress by Discipline")
        
        disciplines = [
            {"name": "Architectural", "completion": 95, "issues": 12, "resolved": 10},
            {"name": "Structural", "completion": 100, "issues": 8, "resolved": 7},
            {"name": "Mechanical", "completion": 90, "issues": 10, "resolved": 6},
            {"name": "Electrical", "completion": 85, "issues": 7, "resolved": 4},
            {"name": "Plumbing", "completion": 90, "issues": 5, "resolved": 3},
            {"name": "Civil/Site", "completion": 75, "issues": 3, "resolved": 2}
        ]
        
        for discipline in disciplines:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.progress(discipline["completion"] / 100)
            
            with col2:
                st.markdown(f"**{discipline['name']}:** {discipline['completion']}%")
            
            with col3:
                st.markdown(f"{discipline['resolved']}/{discipline['issues']} issues")
    
    with col2:
        st.subheader("Issue Status")
        
        # Issue status breakdown
        status_data = pd.DataFrame({
            "Status": ["Resolved", "In Progress", "Open", "Critical"],
            "Count": [32, 3, 2, 8]
        })
        
        fig = px.pie(
            status_data,
            values="Count",
            names="Status",
            color="Status",
            color_discrete_map={
                "Resolved": "#38d39f",
                "In Progress": "#4a90e2",
                "Open": "#f59e0b",
                "Critical": "#ef4444"
            },
            hole=0.4
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Issues by discipline
        st.markdown("#### Issues by Discipline")
        
        discipline_data = pd.DataFrame({
            "Discipline": [d["name"] for d in disciplines],
            "Issues": [d["issues"] for d in disciplines]
        })
        
        fig = px.bar(
            discipline_data,
            x="Issues",
            y="Discipline",
            orientation="h",
            labels={"Issues": "Number of Issues"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Review comment
        st.info("""
        **Review Note:**
        The majority of critical issues are related to MEP coordination
        in mechanical rooms and ceiling spaces. Additional coordination
        meetings are scheduled to resolve these issues.
        """)

def render_issues_log():
    """Render the constructability issues log section"""
    st.subheader("Constructability Issues Log")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
    
    with filter_col1:
        discipline_filter = st.multiselect(
            "Discipline",
            options=["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil/Site"],
            default=[]
        )
    
    with filter_col2:
        status_filter = st.multiselect(
            "Status",
            options=["Resolved", "In Progress", "Open", "Critical"],
            default=["Open", "Critical", "In Progress"]
        )
    
    with filter_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All", value=False, key="constructability_show_all")
    
    # Create issues data
    issues = [
        {
            "id": "CR-001",
            "description": "Inadequate clearance for mechanical equipment in Mechanical Room 1",
            "discipline": "Mechanical",
            "impact": "May require relocation of equipment or structural modifications",
            "status": "Critical",
            "assigned_to": "Sarah W.",
            "due_date": "May 25, 2025"
        },
        {
            "id": "CR-002",
            "description": "Conflict between structural beams and HVAC main ducts in north wing",
            "discipline": "Structural",
            "impact": "Will require beam penetrations or duct rerouting",
            "status": "Critical",
            "assigned_to": "Robert J.",
            "due_date": "May 26, 2025"
        },
        {
            "id": "CR-003",
            "description": "Fire rating of shaft walls does not match code requirements",
            "discipline": "Architectural",
            "impact": "Will require revision to wall types",
            "status": "Resolved",
            "assigned_to": "Lisa M.",
            "due_date": "May 15, 2025"
        },
        {
            "id": "CR-004",
            "description": "Electrical room size insufficient for required equipment",
            "discipline": "Electrical",
            "impact": "May require layout changes or additional electrical rooms",
            "status": "Critical",
            "assigned_to": "David P.",
            "due_date": "May 25, 2025"
        },
        {
            "id": "CR-005",
            "description": "Insufficient ceiling space for plumbing and HVAC in corridors",
            "discipline": "Mechanical",
            "impact": "May require ceiling height adjustment or rerouting",
            "status": "In Progress",
            "assigned_to": "Sarah W.",
            "due_date": "May 28, 2025"
        },
        {
            "id": "CR-006",
            "description": "No adequate access panels for VAV boxes above hard ceilings",
            "discipline": "Architectural",
            "impact": "Will require additional access panels in ceiling plan",
            "status": "Resolved",
            "assigned_to": "Lisa M.",
            "due_date": "May 15, 2025"
        },
        {
            "id": "CR-007",
            "description": "Storm drainage pipe sizing inconsistent with rainfall data",
            "discipline": "Plumbing",
            "impact": "Requires recalculation and possible upsizing",
            "status": "Open",
            "assigned_to": "James T.",
            "due_date": "May 29, 2025"
        },
        {
            "id": "CR-008",
            "description": "Insufficient space for trash collection area per code",
            "discipline": "Civil/Site",
            "impact": "Will require site layout modification",
            "status": "Resolved",
            "assigned_to": "Thomas R.",
            "due_date": "May 10, 2025"
        }
    ]
    
    # Apply filters
    filtered_issues = issues
    if not show_all:
        if discipline_filter:
            filtered_issues = [i for i in filtered_issues if i["discipline"] in discipline_filter]
        if status_filter:
            filtered_issues = [i for i in filtered_issues if i["status"] in status_filter]
    
    # Display issues
    for issue in filtered_issues:
        status_color = "#6c757d"  # Default gray
        if issue["status"] == "Resolved":
            status_color = "#38d39f"  # Green
        elif issue["status"] == "Critical":
            status_color = "#ef4444"  # Red
        elif issue["status"] == "In Progress":
            status_color = "#4a90e2"  # Blue
        elif issue["status"] == "Open":
            status_color = "#f59e0b"  # Yellow/Orange
            
        with st.expander(f"{issue['id']} - {issue['description']} ({issue['discipline']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Discipline:** {issue['discipline']}
                
                **Impact:** {issue['impact']}
                
                **Status:** <span style="color: {status_color};">{issue['status']}</span>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Assigned To:** {issue['assigned_to']}
                
                **Due Date:** {issue['due_date']}
                """)
            
            # Action buttons
            if issue["status"] not in ["Resolved"]:
                resolve_col, progress_col = st.columns(2)
                with resolve_col:
                    st.button(f"Mark Resolved {issue['id']}", key=f"resolve_{issue['id']}")
                with progress_col:
                    st.button(f"Update Status {issue['id']}", key=f"update_{issue['id']}")
    
    # Add new issue button
    st.button("Add New Issue", key="add_new_issue")

def render_design_recommendations():
    """Render the design recommendations section"""
    st.subheader("Design Recommendations")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### Key Design Recommendations")
        
        recommendations = [
            {
                "id": "REC-001",
                "description": "Increase mechanical room sizes by 15% to accommodate equipment and maintenance access",
                "benefit": "Prevents equipment conflicts and ensures proper maintenance clearances",
                "cost_impact": "+$75,000",
                "schedule_impact": "None",
                "status": "Accepted"
            },
            {
                "id": "REC-002",
                "description": "Revise ceiling heights in corridors from 9' to 10' to accommodate ductwork and piping",
                "benefit": "Resolves MEP conflicts and reduces coordination issues during construction",
                "cost_impact": "+$120,000",
                "schedule_impact": "None",
                "status": "Accepted"
            },
            {
                "id": "REC-003",
                "description": "Add additional electrical rooms on floors 5 and 10 to reduce feeder lengths",
                "benefit": "Reduces materials cost and voltage drop issues",
                "cost_impact": "+$90,000",
                "schedule_impact": "None",
                "status": "Under Review"
            },
            {
                "id": "REC-004",
                "description": "Standardize bathroom layouts across residential units",
                "benefit": "Improves construction efficiency and reduces plumbing complexity",
                "cost_impact": "-$65,000",
                "schedule_impact": "-2 weeks",
                "status": "Accepted"
            },
            {
                "id": "REC-005",
                "description": "Relocate main electrical switchgear from basement to first floor",
                "benefit": "Eliminates need for waterproofing and simplifies installation",
                "cost_impact": "+$40,000",
                "schedule_impact": "None",
                "status": "Rejected"
            }
        ]
        
        for recommendation in recommendations:
            status_color = "#6c757d"  # Default gray
            if recommendation["status"] == "Accepted":
                status_color = "#38d39f"  # Green
            elif recommendation["status"] == "Rejected":
                status_color = "#ef4444"  # Red
            elif recommendation["status"] == "Under Review":
                status_color = "#4a90e2"  # Blue
                
            cost_color = "#38d39f" if "-$" in recommendation["cost_impact"] else "#ef4444"
            schedule_color = "#38d39f" if "-" in recommendation["schedule_impact"] else "#6c757d"
                
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <div style="font-weight: 500;">{recommendation['id']} - {recommendation['description']}</div>
                <div style="font-size: 14px; margin-top: 8px;">
                    <strong>Benefit:</strong> {recommendation['benefit']}
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 8px;">
                    <span><strong>Cost Impact:</strong> <span style="color: {cost_color};">{recommendation['cost_impact']}</span></span>
                    <span><strong>Schedule Impact:</strong> <span style="color: {schedule_color};">{recommendation['schedule_impact']}</span></span>
                    <span><strong>Status:</strong> <span style="color: {status_color};">{recommendation['status']}</span></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Recommendations Summary")
        
        # Count by status
        status_counts = {"Accepted": 0, "Under Review": 0, "Rejected": 0}
        for rec in recommendations:
            if rec["status"] in status_counts:
                status_counts[rec["status"]] += 1
        
        status_df = pd.DataFrame({
            "Status": list(status_counts.keys()),
            "Count": list(status_counts.values())
        })
        
        fig = px.pie(
            status_df,
            values="Count",
            names="Status",
            color="Status",
            color_discrete_map={
                "Accepted": "#38d39f",
                "Under Review": "#4a90e2",
                "Rejected": "#ef4444"
            },
            hole=0.4
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost impact
        st.markdown("#### Cost Impact of Recommendations")
        
        # Calculate net cost impact of accepted recommendations
        net_cost = 0
        for rec in recommendations:
            if rec["status"] == "Accepted":
                cost_str = rec["cost_impact"]
                if "+" in cost_str:
                    net_cost += int(cost_str.replace("+$", "").replace(",", ""))
                elif "-" in cost_str:
                    net_cost -= int(cost_str.replace("-$", "").replace(",", ""))
        
        cost_color = "#ef4444" if net_cost > 0 else "#38d39f"
        cost_sign = "+" if net_cost > 0 else ""
        
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px;">
            <div style="font-size: 16px; color: #6c757d; margin-bottom: 5px;">Net Cost Impact (Accepted)</div>
            <div style="font-size: 24px; font-weight: 500; color: {cost_color};">{cost_sign}${net_cost:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Trade impact
        st.markdown("#### Trade Impact Analysis")
        
        trade_impact = {
            "Mechanical": "High - Significant coordination changes",
            "Electrical": "Medium - Room layout changes",
            "Plumbing": "Low - Minor rerouting required",
            "Structural": "Low - Minimal changes",
            "Architectural": "Medium - Ceiling height changes"
        }
        
        for trade, impact in trade_impact.items():
            impact_color = "#6c757d"
            if "High" in impact:
                impact_color = "#ef4444"
            elif "Medium" in impact:
                impact_color = "#f59e0b"
            elif "Low" in impact:
                impact_color = "#38d39f"
                
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <span>{trade}</span>
                <span style="color: {impact_color};">{impact}</span>
            </div>
            """, unsafe_allow_html=True)

def render_sequencing():
    """Render the construction sequencing section"""
    st.subheader("Construction Sequencing Analysis")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### Phasing & Sequencing Plan")
        
        phases = [
            {
                "phase": "Phase 1: Site Preparation",
                "description": "Demolition, excavation, shoring, and utilities relocation",
                "duration": "3 months",
                "challenges": "Limited site access, adjacent building protection",
                "recommendations": "Use top-down construction method for garage levels"
            },
            {
                "phase": "Phase 2: Foundation & Structure",
                "description": "Foundation systems, basement levels, structural frame to level 15",
                "duration": "9 months",
                "challenges": "Limited crane positions, tight urban site",
                "recommendations": "Use two tower cranes with coordinated swing zones"
            },
            {
                "phase": "Phase 3: Envelope & MEP Rough-in",
                "description": "Building envelope, core & shell MEP systems",
                "duration": "6 months",
                "challenges": "Multiple trades in limited space, material delivery",
                "recommendations": "Just-in-time delivery system, dedicated material hoists"
            },
            {
                "phase": "Phase 4: Interior Fit-Out",
                "description": "Interior partitions, finishes, MEP final install",
                "duration": "8 months",
                "challenges": "Vertical transportation, sequence of finishes",
                "recommendations": "Bottom-up approach for residential, top-down for amenities"
            },
            {
                "phase": "Phase 5: Site Work & Commissioning",
                "description": "Exterior hardscaping, landscaping, commissioning, closeout",
                "duration": "2 months",
                "challenges": "Weather dependency, system integration",
                "recommendations": "Early start on commissioning, weather contingency plan"
            }
        ]
        
        for phase in phases:
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
                <div style="font-weight: 500; color: #2c3e50;">{phase['phase']}</div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <span>{phase['description']}</span>
                </div>
                <div style="display: flex; font-size: 14px; margin-top: 5px;">
                    <span><strong>Duration:</strong> {phase['duration']}</span>
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Challenges:</strong> {phase['challenges']}
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Recommendations:</strong> {phase['recommendations']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Sequencing Considerations")
        
        # Critical sequencing items
        critical_items = [
            "Tower crane positioning and reach",
            "Material handling and hoisting",
            "MEP coordination and installation sequence",
            "Trade stacking in limited spaces",
            "Weather-sensitive activities",
            "Just-in-time material delivery",
            "Commissioning schedule"
        ]
        
        st.markdown("**Critical Sequencing Considerations:**")
        for item in critical_items:
            st.markdown(f"- {item}")
        
        # Schedule risk areas
        st.markdown("#### Schedule Risk Areas")
        
        risk_areas = [
            {"area": "Foundation work", "risk_level": "Medium", "mitigation": "Early procurement, additional crews"},
            {"area": "Curtain wall installation", "risk_level": "High", "mitigation": "Pre-fabrication, mock-ups, dedicated team"},
            {"area": "MEP coordination", "risk_level": "High", "mitigation": "3D modeling, prefabrication, clash detection"},
            {"area": "Elevator installation", "risk_level": "Medium", "mitigation": "Early release, dedicated hoist"},
            {"area": "Weather delays", "risk_level": "Medium", "mitigation": "Temporary enclosures, schedule buffer"}
        ]
        
        for risk in risk_areas:
            risk_color = "#6c757d"
            if risk["risk_level"] == "High":
                risk_color = "#ef4444"
            elif risk["risk_level"] == "Medium":
                risk_color = "#f59e0b"
            elif risk["risk_level"] == "Low":
                risk_color = "#38d39f"
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border-left: 3px solid {risk_color}; background-color: #f8f9fa;">
                <div style="font-weight: 500; display: flex; justify-content: space-between;">
                    <span>{risk['area']}</span>
                    <span style="color: {risk_color};">{risk['risk_level']} Risk</span>
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Mitigation:</strong> {risk['mitigation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Trade stacking analysis
        st.markdown("#### Trade Stacking Analysis")
        
        st.markdown("""
        The project schedule shows potential trade stacking issues:
        
        - Months 8-10: MEP rough-in with fireproofing work
        - Months 12-14: Interior framing with MEP rough-in
        - Months 15-18: Finishes installation overlapping across floors
        
        **Recommendation:** Implement pull planning sessions with trade partners
        to develop detailed 3-week look-ahead schedules and resolve stacking issues.
        """)

def render_site_logistics():
    """Render the site logistics section"""
    st.subheader("Site Logistics Plan")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### Site Logistics Considerations")
        
        # Image placeholder for site logistics plan
        st.image("https://via.placeholder.com/800x600?text=Site+Logistics+Plan", 
                caption="Site Logistics Plan (Preliminary)")
        
        # Site logistics elements
        logistics_elements = [
            {
                "element": "Site Access",
                "description": "Primary access via North Ave, secondary access via 4th Street",
                "challenges": "Limited street frontage, busy urban streets",
                "recommendations": "Dedicated flaggers, scheduled deliveries outside peak hours"
            },
            {
                "element": "Crane Locations",
                "description": "Two tower cranes positioned at NE and SW corners",
                "challenges": "Overlapping swing zones, adjacent buildings",
                "recommendations": "Anti-collision systems, coordinated lifting schedules"
            },
            {
                "element": "Material Laydown",
                "description": "Limited on-site laydown area on west side",
                "challenges": "Extremely limited space for material storage",
                "recommendations": "Off-site staging area with just-in-time delivery system"
            },
            {
                "element": "Vertical Transportation",
                "description": "Two construction hoists on east facade",
                "challenges": "Limited hoist capacity for peak manpower",
                "recommendations": "Staggered work shifts, dedicated material hoist"
            },
            {
                "element": "Field Offices",
                "description": "Trailers positioned along south boundary",
                "challenges": "Limited space for all subcontractor offices",
                "recommendations": "Multi-level office trailers, shared spaces for subs"
            }
        ]
        
        for element in logistics_elements:
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <div style="font-weight: 500; color: #2c3e50;">{element['element']}</div>
                <div style="font-size: 14px; margin-top: 5px;">
                    {element['description']}
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Challenges:</strong> {element['challenges']}
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Recommendations:</strong> {element['recommendations']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Logistics Challenges")
        
        # Traffic management
        st.markdown("**Traffic Management Plan**")
        st.markdown("""
        - Street closure permit for North Ave (partial) during foundation work
        - Police detail for concrete pours and major deliveries
        - Dedicated loading/unloading zone on 4th Street
        - Pedestrian protection canopies on all street frontages
        - Real-time delivery scheduling system to prevent street congestion
        """)
        
        # Neighbor considerations
        st.markdown("**Neighbor Considerations**")
        st.markdown("""
        - Adjacent building protection and monitoring
        - Noise restrictions: 7am-6pm weekdays, 9am-5pm Saturday
        - Vibration monitoring for sensitive equipment in medical office
        - Dust control plan with monitoring stations
        - Regular community updates and point of contact for issues
        """)
        
        # Material handling
        st.markdown("**Material Handling Strategy**")
        st.markdown("""
        - Off-site consolidation center for materials
        - Just-in-time delivery system with 48-hour advanced scheduling
        - Prefabrication of MEP systems to reduce on-site storage
        - Floor-by-floor material distribution plan
        - RFID tracking system for critical materials and equipment
        """)
        
        # Temporary facilities
        st.markdown("**Temporary Facilities**")
        
        facilities = [
            {"name": "Power", "description": "Temporary 1200A service, generator backup"},
            {"name": "Water", "description": "Temporary meters at North Ave and 4th St"},
            {"name": "Sanitation", "description": "Portable facilities plus temporary connections"},
            {"name": "Security", "description": "Fencing, cameras, 24-hour security guard"},
            {"name": "Dewatering", "description": "Well-point system during basement construction"}
        ]
        
        for facility in facilities:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <span><strong>{facility['name']}:</strong></span>
                <span>{facility['description']}</span>
            </div>
            """, unsafe_allow_html=True)