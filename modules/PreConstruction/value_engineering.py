"""
Value Engineering Module

This module provides tools for value engineering analysis, including:
- Cost saving opportunities
- Alternative material analysis
- Life cycle cost analysis
- Value proposition evaluation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_value_engineering():
    """Render the Value Engineering dashboard"""
    st.header("Value Engineering")
    
    # Introduction
    st.markdown("""
    Value Engineering identifies opportunities to reduce costs while maintaining
    or improving performance, reliability, quality, and safety.
    """)
    
    # Create layout columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_ve_proposals()
    
    with col2:
        render_ve_summary()
    
    # Create tabs for detailed sections
    tabs = st.tabs([
        "Material Alternatives", 
        "Systems Analysis", 
        "Life Cycle Analysis"
    ])
    
    # Material alternatives tab
    with tabs[0]:
        render_material_alternatives()
    
    # Systems analysis tab
    with tabs[1]:
        render_systems_analysis()
    
    # Life cycle analysis tab
    with tabs[2]:
        render_lifecycle_analysis()

def render_ve_proposals():
    """Render the VE proposals section"""
    st.subheader("Value Engineering Proposals")
    
    # Controls
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
    
    with filter_col1:
        status_filter = st.multiselect(
            "Status",
            options=["Under Review", "Approved", "Rejected", "Implemented"],
            default=["Under Review", "Approved"]
        )
    
    with filter_col2:
        category_filter = st.multiselect(
            "Category",
            options=["Structure", "Envelope", "MEP", "Finishes", "Site"],
            default=[]
        )
    
    with filter_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All", value=False)
    
    # Create VE proposal data
    ve_proposals = [
        {
            "id": "VE-001",
            "description": "Substitute cast-in-place concrete with precast panels for exterior walls",
            "category": "Structure",
            "savings": 350000,
            "implementation_cost": 75000,
            "net_savings": 275000,
            "status": "Approved",
            "impact": "Schedule improvement of 3 weeks, no aesthetic change"
        },
        {
            "id": "VE-002",
            "description": "Change curtain wall system from custom to standard system",
            "category": "Envelope",
            "savings": 425000,
            "implementation_cost": 25000,
            "net_savings": 400000,
            "status": "Under Review",
            "impact": "Minor aesthetic change, improved lead time"
        },
        {
            "id": "VE-003",
            "description": "Reduce parking garage ceiling height from 10' to 9'",
            "category": "Structure",
            "savings": 180000,
            "implementation_cost": 15000,
            "net_savings": 165000,
            "status": "Approved",
            "impact": "No functional impact"
        },
        {
            "id": "VE-004",
            "description": "Substitute high-end fixture package with mid-range in apartments",
            "category": "Finishes",
            "savings": 225000,
            "implementation_cost": 0,
            "net_savings": 225000,
            "status": "Rejected",
            "impact": "Reduced marketability of units"
        },
        {
            "id": "VE-005",
            "description": "Change roofing system from built-up to single-ply TPO",
            "category": "Envelope",
            "savings": 120000,
            "implementation_cost": 10000,
            "net_savings": 110000,
            "status": "Approved",
            "impact": "Reduced warranty period from 30 to 20 years"
        },
        {
            "id": "VE-006",
            "description": "Optimize HVAC zoning throughout building",
            "category": "MEP",
            "savings": 275000,
            "implementation_cost": 45000,
            "net_savings": 230000,
            "status": "Under Review",
            "impact": "No impact on comfort, improved energy efficiency"
        },
        {
            "id": "VE-007",
            "description": "Eliminate decorative canopy at secondary entrance",
            "category": "Site",
            "savings": 95000,
            "implementation_cost": 0,
            "net_savings": 95000,
            "status": "Rejected",
            "impact": "Negative aesthetic impact, reduced weather protection"
        },
        {
            "id": "VE-008",
            "description": "Substitute granite countertops with quartz in apartments",
            "category": "Finishes",
            "savings": 85000,
            "implementation_cost": 0,
            "net_savings": 85000,
            "status": "Approved",
            "impact": "Improved durability, no aesthetic impact"
        },
    ]
    
    # Apply filters
    filtered_proposals = ve_proposals
    if not show_all:
        if status_filter:
            filtered_proposals = [p for p in filtered_proposals if p["status"] in status_filter]
        if category_filter:
            filtered_proposals = [p for p in filtered_proposals if p["category"] in category_filter]
    
    # Display proposals
    for proposal in filtered_proposals:
        status_color = "#6c757d"  # Default gray
        if proposal["status"] == "Approved":
            status_color = "#38d39f"  # Green
        elif proposal["status"] == "Rejected":
            status_color = "#ef4444"  # Red
        elif proposal["status"] == "Under Review":
            status_color = "#4a90e2"  # Blue
            
        with st.expander(f"{proposal['id']} - {proposal['description']} (${proposal['net_savings']:,} savings)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Category:** {proposal['category']}
                
                **Impact Assessment:** {proposal['impact']}
                
                **Status:** <span style="color: {status_color};">{proposal['status']}</span>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Cost Savings:** ${proposal['savings']:,}
                
                **Implementation Cost:** ${proposal['implementation_cost']:,}
                
                **Net Savings:** ${proposal['net_savings']:,}
                """)
            
            # Action buttons
            if proposal["status"] == "Under Review":
                approve_col, reject_col = st.columns(2)
                with approve_col:
                    st.button(f"Approve {proposal['id']}", key=f"approve_{proposal['id']}")
                with reject_col:
                    st.button(f"Reject {proposal['id']}", key=f"reject_{proposal['id']}")

def render_ve_summary():
    """Render the VE summary section"""
    st.subheader("Value Engineering Summary")
    
    # VE statistics
    total_proposals = 8
    approved = 4
    under_review = 2
    rejected = 2
    
    # Total potential savings
    total_savings = 1350000
    approved_savings = 635000
    
    # Create metric cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Total VE Proposals",
            value=str(total_proposals),
            help="Total number of value engineering proposals"
        )
    
    with col2:
        st.metric(
            label="Approved Proposals",
            value=str(approved),
            delta=f"{approved/total_proposals*100:.0f}%",
            help="Number of approved value engineering proposals"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.metric(
            label="Potential Savings",
            value=f"${total_savings:,}",
            help="Total potential savings from all VE proposals"
        )
    
    with col4:
        st.metric(
            label="Approved Savings",
            value=f"${approved_savings:,}",
            delta=f"{approved_savings/total_savings*100:.0f}%",
            help="Total savings from approved VE proposals"
        )
    
    # VE status breakdown
    st.markdown("#### Proposal Status")
    
    status_data = pd.DataFrame({
        "Status": ["Approved", "Under Review", "Rejected"],
        "Count": [approved, under_review, rejected]
    })
    
    fig = px.pie(
        status_data,
        values="Count",
        names="Status",
        color="Status",
        color_discrete_map={
            "Approved": "#38d39f",
            "Under Review": "#4a90e2",
            "Rejected": "#ef4444"
        },
        hole=0.4
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)
    
    # VE savings by category
    st.markdown("#### Savings by Category")
    
    category_data = pd.DataFrame({
        "Category": ["Structure", "Envelope", "MEP", "Finishes", "Site"],
        "Savings": [440000, 510000, 230000, 310000, 95000]
    })
    
    fig = px.bar(
        category_data,
        x="Category",
        y="Savings",
        text_auto=True,
        labels={"Savings": "Potential Savings ($)"}
    )
    st.plotly_chart(fig, use_container_width=True)

def render_material_alternatives():
    """Render the material alternatives section"""
    st.subheader("Material Alternatives Analysis")
    
    # Create tabs for different material categories
    material_tabs = st.tabs([
        "Structural", 
        "Envelope", 
        "Finishes"
    ])
    
    # Structural materials tab
    with material_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Concrete Alternatives")
            
            concrete_options = [
                {
                    "option": "Cast-in-place concrete",
                    "cost_per_sf": 28.50,
                    "schedule": "Long",
                    "pros": "Flexibility in design, high quality",
                    "cons": "Labor intensive, weather dependent",
                    "recommendation": False
                },
                {
                    "option": "Precast concrete panels",
                    "cost_per_sf": 24.75,
                    "schedule": "Medium",
                    "pros": "Faster installation, factory QC",
                    "cons": "Limited design flexibility, joints",
                    "recommendation": True
                },
                {
                    "option": "Tilt-up concrete",
                    "cost_per_sf": 22.00,
                    "schedule": "Medium",
                    "pros": "Cost-effective, faster than CIP",
                    "cons": "Site limitations, design constraints",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(concrete_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: ${option["cost_per_sf"]}/SF</span>
                        <span>Schedule: {option["schedule"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Structural Steel Alternatives")
            
            steel_options = [
                {
                    "option": "Wide flange beams (standard)",
                    "cost_per_ton": 3200,
                    "schedule": "Medium",
                    "pros": "Readily available, standard details",
                    "cons": "May oversupply capacity",
                    "recommendation": True
                },
                {
                    "option": "Castellated beams",
                    "cost_per_ton": 3600,
                    "schedule": "Long",
                    "pros": "Lighter weight, services through webs",
                    "cons": "Higher cost, longer lead time",
                    "recommendation": False
                },
                {
                    "option": "Composite steel deck",
                    "cost_per_sf": 9.50,
                    "schedule": "Short",
                    "pros": "Fast installation, lighter building",
                    "cons": "Additional fireproofing required",
                    "recommendation": True
                }
            ]
            
            for i, option in enumerate(steel_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                # Show cost per ton or SF depending on what's available
                cost_display = f"${option['cost_per_ton']}/ton" if "cost_per_ton" in option else f"${option['cost_per_sf']}/SF"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: {cost_display}</span>
                        <span>Schedule: {option["schedule"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
    
    # Envelope materials tab
    with material_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Exterior Wall Systems")
            
            wall_options = [
                {
                    "option": "Custom curtain wall",
                    "cost_per_sf": 95.00,
                    "r_value": "R-8",
                    "lead_time": "16-20 weeks",
                    "pros": "Premium aesthetic, custom appearance",
                    "cons": "High cost, long lead time",
                    "recommendation": False
                },
                {
                    "option": "Standard curtain wall",
                    "cost_per_sf": 75.00,
                    "r_value": "R-7",
                    "lead_time": "12-14 weeks",
                    "pros": "Good quality, faster lead time",
                    "cons": "Limited customization",
                    "recommendation": True
                },
                {
                    "option": "Metal panel rainscreen",
                    "cost_per_sf": 65.00,
                    "r_value": "R-19",
                    "lead_time": "8-10 weeks",
                    "pros": "Better insulation, cost-effective",
                    "cons": "Different aesthetic",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(wall_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: ${option["cost_per_sf"]}/SF</span>
                        <span>R-Value: {option["r_value"]}</span>
                        <span>Lead: {option["lead_time"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Roofing Systems")
            
            roofing_options = [
                {
                    "option": "Built-up roofing (BUR)",
                    "cost_per_sf": 22.50,
                    "warranty": "30 years",
                    "lead_time": "4-6 weeks",
                    "pros": "Excellent durability, longer warranty",
                    "cons": "Higher cost, labor intensive",
                    "recommendation": False
                },
                {
                    "option": "Single-ply TPO membrane",
                    "cost_per_sf": 18.00,
                    "warranty": "20 years",
                    "lead_time": "2-3 weeks",
                    "pros": "Cost-effective, faster installation",
                    "cons": "Reduced warranty period",
                    "recommendation": True
                },
                {
                    "option": "Modified bitumen",
                    "cost_per_sf": 20.00,
                    "warranty": "25 years",
                    "lead_time": "3-4 weeks",
                    "pros": "Good durability, easier to repair",
                    "cons": "More labor than TPO",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(roofing_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: ${option["cost_per_sf"]}/SF</span>
                        <span>Warranty: {option["warranty"]}</span>
                        <span>Lead: {option["lead_time"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
    
    # Finishes tab
    with material_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Flooring Options")
            
            flooring_options = [
                {
                    "option": "Luxury vinyl tile (LVT)",
                    "cost_per_sf": 7.50,
                    "lifecycle": "10-15 years",
                    "pros": "Durable, waterproof, easy maintenance",
                    "cons": "Less premium than wood or stone",
                    "recommendation": True
                },
                {
                    "option": "Porcelain tile",
                    "cost_per_sf": 12.00,
                    "lifecycle": "30+ years",
                    "pros": "Extremely durable, premium look",
                    "cons": "Higher cost, harder underfoot",
                    "recommendation": False
                },
                {
                    "option": "Engineered hardwood",
                    "cost_per_sf": 9.50,
                    "lifecycle": "15-20 years",
                    "pros": "Natural look, warm feel",
                    "cons": "Not ideal for wet areas, scratches",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(flooring_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: ${option["cost_per_sf"]}/SF</span>
                        <span>Lifecycle: {option["lifecycle"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Countertop Options")
            
            countertop_options = [
                {
                    "option": "Granite",
                    "cost_per_sf": 75.00,
                    "lifecycle": "20+ years",
                    "pros": "Natural material, unique patterns",
                    "cons": "Requires sealing, more porous",
                    "recommendation": False
                },
                {
                    "option": "Quartz",
                    "cost_per_sf": 65.00,
                    "lifecycle": "20+ years",
                    "pros": "More consistent, better durability",
                    "cons": "Less unique than natural stone",
                    "recommendation": True
                },
                {
                    "option": "Solid surface",
                    "cost_per_sf": 45.00,
                    "lifecycle": "15+ years",
                    "pros": "Seamless, repairable, lower cost",
                    "cons": "Less heat resistant, scratches",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(countertop_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Cost: ${option["cost_per_sf"]}/SF</span>
                        <span>Lifecycle: {option["lifecycle"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)

def render_systems_analysis():
    """Render the systems analysis section"""
    st.subheader("Building Systems Analysis")
    
    # Create tabs for different system categories
    system_tabs = st.tabs([
        "HVAC", 
        "Electrical", 
        "Plumbing"
    ])
    
    # HVAC tab
    with system_tabs[0]:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("#### HVAC System Options")
            
            hvac_options = [
                {
                    "option": "Variable Refrigerant Flow (VRF)",
                    "initial_cost": "$$$$",
                    "energy_efficiency": "Excellent",
                    "maintenance": "Moderate",
                    "savings": "$45,000/year",
                    "pros": "Zone control, energy efficiency, quiet operation",
                    "cons": "Higher initial cost, specialized maintenance",
                    "recommendation": True
                },
                {
                    "option": "Water-source heat pumps",
                    "initial_cost": "$$$",
                    "energy_efficiency": "Good",
                    "maintenance": "Moderate",
                    "savings": "$35,000/year",
                    "pros": "Zone control, reasonable efficiency",
                    "cons": "More mechanical rooms, more maintenance points",
                    "recommendation": False
                },
                {
                    "option": "Rooftop package units",
                    "initial_cost": "$$",
                    "energy_efficiency": "Fair",
                    "maintenance": "Low",
                    "savings": "$25,000/year",
                    "pros": "Lower initial cost, simple maintenance",
                    "cons": "Less zone control, higher energy costs",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(hvac_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Initial Cost: {option["initial_cost"]}</span>
                        <span>Efficiency: {option["energy_efficiency"]}</span>
                        <span>Maintenance: {option["maintenance"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span>Est. Energy Savings: {option["savings"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### HVAC Cost Analysis")
            
            # Cost comparison
            system_costs = pd.DataFrame({
                "System": ["VRF", "Water-source HP", "Rooftop Units"],
                "Initial Cost": [1250000, 975000, 725000],
                "Annual Energy": [175000, 215000, 255000],
                "Annual Maintenance": [35000, 40000, 30000]
            })
            
            # Create a 15-year cost analysis
            years = list(range(0, 16, 5))
            vrf_costs = [system_costs.iloc[0]["Initial Cost"]]
            for _ in range(len(years)-1):
                annual_cost = system_costs.iloc[0]["Annual Energy"] + system_costs.iloc[0]["Annual Maintenance"]
                vrf_costs.append(vrf_costs[-1] + annual_cost * 5)
                
            wshp_costs = [system_costs.iloc[1]["Initial Cost"]]
            for _ in range(len(years)-1):
                annual_cost = system_costs.iloc[1]["Annual Energy"] + system_costs.iloc[1]["Annual Maintenance"]
                wshp_costs.append(wshp_costs[-1] + annual_cost * 5)
                
            rtu_costs = [system_costs.iloc[2]["Initial Cost"]]
            for _ in range(len(years)-1):
                annual_cost = system_costs.iloc[2]["Annual Energy"] + system_costs.iloc[2]["Annual Maintenance"]
                rtu_costs.append(rtu_costs[-1] + annual_cost * 5)
            
            # Create the data frame for plotting
            cost_df = pd.DataFrame({
                "Year": years * 3,
                "Cost": vrf_costs + wshp_costs + rtu_costs,
                "System": ["VRF"] * len(years) + ["Water-source HP"] * len(years) + ["Rooftop Units"] * len(years)
            })
            
            fig = px.line(
                cost_df,
                x="Year",
                y="Cost",
                color="System",
                labels={"Cost": "Cumulative Cost ($)"},
                markers=True
            )
            
            # Add breakeven annotation
            breakeven_year = 8  # Approximate from the data
            fig.add_annotation(
                x=breakeven_year,
                y=3250000,
                text="VRF Breakeven Point",
                showarrow=True,
                arrowhead=1
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key findings
            st.markdown("""
            **Key Findings:**
            
            * VRF has highest initial cost but lowest operating costs
            * Breakeven point is approximately 8 years
            * 15-year lifecycle cost is lowest for VRF
            * VRF provides better zone control and comfort
            """)
    
    # Electrical tab
    with system_tabs[1]:
        st.markdown("#### Electrical Systems Value Engineering")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Lighting Systems")
            
            lighting_options = [
                {
                    "option": "All LED fixtures",
                    "initial_cost": "$$$",
                    "energy_efficiency": "Excellent",
                    "lifecycle": "50,000+ hours",
                    "savings": "$28,000/year",
                    "pros": "Lowest energy use, long life, less heat",
                    "cons": "Higher initial cost",
                    "recommendation": True
                },
                {
                    "option": "LED in public areas, fluorescent in back-of-house",
                    "initial_cost": "$$",
                    "energy_efficiency": "Good",
                    "lifecycle": "Mixed",
                    "savings": "$18,000/year",
                    "pros": "Lower initial cost, still efficient",
                    "cons": "Mixed maintenance schedule",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(lighting_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Initial Cost: {option["initial_cost"]}</span>
                        <span>Efficiency: {option["energy_efficiency"]}</span>
                        <span>Lifecycle: {option["lifecycle"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span>Est. Energy Savings: {option["savings"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Power Distribution")
            
            power_options = [
                {
                    "option": "Standard aluminum feeders",
                    "initial_cost": "$$$",
                    "flexibility": "Good",
                    "pros": "Lower cost than copper, standard approach",
                    "cons": "Larger conduit sizes required",
                    "recommendation": True
                },
                {
                    "option": "Copper feeders",
                    "initial_cost": "$$$$",
                    "flexibility": "Good",
                    "pros": "Smaller conduit sizes, better conductivity",
                    "cons": "Significantly higher cost",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(power_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Initial Cost: {option["initial_cost"]}</span>
                        <span>Flexibility: {option["flexibility"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        # Electrical VE proposals
        st.markdown("#### Electrical VE Proposals")
        
        electrical_ve = [
            {
                "proposal": "Reduce lighting power density by 10%",
                "savings": "$120,000",
                "impact": "Minimal impact on light levels, still exceeds code requirements",
                "status": "Approved"
            },
            {
                "proposal": "Consolidate electrical rooms",
                "savings": "$85,000",
                "impact": "Longer circuit runs but within voltage drop limits",
                "status": "Under Review"
            },
            {
                "proposal": "Substitute standard transformers for premium efficiency",
                "savings": "$45,000",
                "impact": "Slightly higher energy costs over time",
                "status": "Rejected"
            }
        ]
        
        for proposal in electrical_ve:
            status_color = "#6c757d"  # Default gray
            if proposal["status"] == "Approved":
                status_color = "#38d39f"  # Green
            elif proposal["status"] == "Rejected":
                status_color = "#ef4444"  # Red
            elif proposal["status"] == "Under Review":
                status_color = "#4a90e2"  # Blue
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <div style="font-weight: 500;">{proposal["proposal"]}</div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                    <span>Savings: {proposal["savings"]}</span>
                    <span>Status: <span style="color: {status_color};">{proposal["status"]}</span></span>
                </div>
                <div style="font-size: 13px; margin-top: 5px; color: #6c757d;">
                    Impact: {proposal["impact"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Plumbing tab
    with system_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Plumbing Systems")
            
            plumbing_options = [
                {
                    "option": "PEX piping for domestic water",
                    "initial_cost": "$$",
                    "maintenance": "Low",
                    "lifecycle": "50+ years",
                    "pros": "Faster installation, fewer fittings, flexible",
                    "cons": "Less rigid, requires more supports",
                    "recommendation": True
                },
                {
                    "option": "Copper piping",
                    "initial_cost": "$$$",
                    "maintenance": "Low",
                    "lifecycle": "70+ years",
                    "pros": "Traditional, durable, well-known",
                    "cons": "Higher material and labor costs",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(plumbing_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Initial Cost: {option["initial_cost"]}</span>
                        <span>Maintenance: {option["maintenance"]}</span>
                        <span>Lifecycle: {option["lifecycle"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### Fixture Options")
            
            fixture_options = [
                {
                    "option": "Standard water-efficient fixtures",
                    "initial_cost": "$$",
                    "water_savings": "Good",
                    "pros": "Lower cost, still water-efficient",
                    "cons": "Less premium appearance",
                    "recommendation": True
                },
                {
                    "option": "Premium low-flow fixtures",
                    "initial_cost": "$$$",
                    "water_savings": "Excellent",
                    "pros": "Better appearance, slightly more water savings",
                    "cons": "Higher cost, marginal additional savings",
                    "recommendation": False
                }
            ]
            
            for i, option in enumerate(fixture_options):
                bg_color = "#e7f5ff" if option["recommendation"] else "white"
                border = "2px solid #4a90e2" if option["recommendation"] else "1px solid #eee"
                
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                    <div style="font-weight: 500;">{option["option"]}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 5px;">
                        <span>Initial Cost: {option["initial_cost"]}</span>
                        <span>Water Savings: {option["water_savings"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 5px;">
                        <span style="color: #38d39f;">✓ {option["pros"]}</span>
                    </div>
                    <div style="font-size: 13px; margin-top: 3px;">
                        <span style="color: #ef4444;">✗ {option["cons"]}</span>
                    </div>
                    {f'<div style="margin-top: 5px; font-weight: 500; color: #4a90e2;">RECOMMENDED</div>' if option["recommendation"] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Water Savings Analysis")
            
            # Create example water usage data
            standard_usage = 3650000  # gallons per year
            efficient_fixtures = standard_usage * 0.8  # 20% reduction
            premium_fixtures = standard_usage * 0.75  # 25% reduction
            
            # Create a data frame for comparison
            water_df = pd.DataFrame({
                "Fixture Type": ["Standard", "Water-Efficient", "Premium Low-Flow"],
                "Annual Usage (gallons)": [standard_usage, efficient_fixtures, premium_fixtures],
                "Savings (%)": [0, 20, 25]
            })
            
            fig = px.bar(
                water_df,
                x="Fixture Type",
                y="Annual Usage (gallons)",
                text=water_df["Savings (%)"].apply(lambda x: f"{x}% saved" if x > 0 else "Baseline"),
                color="Fixture Type",
                labels={"Annual Usage (gallons)": "Annual Water Usage (gallons)"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost analysis
            st.markdown("#### Cost-Benefit Analysis")
            
            water_cost = 0.01  # dollars per gallon (approximate)
            standard_cost = 120000  # fixture cost
            efficient_cost = 150000
            premium_cost = 195000
            
            standard_annual = standard_usage * water_cost
            efficient_annual = efficient_fixtures * water_cost
            premium_annual = premium_fixtures * water_cost
            
            efficient_savings = standard_annual - efficient_annual
            premium_savings = standard_annual - premium_annual
            
            efficient_payback = (efficient_cost - standard_cost) / efficient_savings
            premium_payback = (premium_cost - standard_cost) / premium_savings
            
            st.markdown(f"""
            **Standard Fixtures:**
            - Initial cost: ${standard_cost:,}
            - Annual water cost: ${standard_annual:,.0f}
            
            **Water-Efficient Fixtures:**
            - Initial cost: ${efficient_cost:,} (${efficient_cost-standard_cost:,} premium)
            - Annual water cost: ${efficient_annual:,.0f}
            - Annual savings: ${efficient_savings:,.0f}
            - Payback period: {efficient_payback:.1f} years
            
            **Premium Low-Flow Fixtures:**
            - Initial cost: ${premium_cost:,} (${premium_cost-standard_cost:,} premium)
            - Annual water cost: ${premium_annual:,.0f}
            - Annual savings: ${premium_savings:,.0f}
            - Payback period: {premium_payback:.1f} years
            
            **Recommendation:**
            Water-efficient fixtures provide the best balance of upfront cost and
            long-term savings with a reasonable payback period.
            """)

def render_lifecycle_analysis():
    """Render the lifecycle analysis section"""
    st.subheader("Life Cycle Cost Analysis")
    
    # Disclaimer
    st.info("""
    This analysis considers the total cost of ownership over the life of the building,
    including initial capital costs, maintenance, energy usage, replacement, and end-of-life
    considerations.
    """)
    
    # Create tabs for different lifecycle analyses
    lifecycle_tabs = st.tabs([
        "Systems Comparison", 
        "Materials Longevity", 
        "Energy Analysis"
    ])
    
    # Systems comparison tab
    with lifecycle_tabs[0]:
        st.markdown("#### Building Systems Life Cycle Comparison")
        
        # Create systems lifecycle data
        systems = [
            {
                "system": "HVAC - VRF",
                "initial_cost": 1250000,
                "annual_energy": 175000,
                "annual_maintenance": 35000,
                "replacement_year": 20,
                "replacement_cost": 1000000
            },
            {
                "system": "HVAC - Rooftop Units",
                "initial_cost": 850000,
                "annual_energy": 255000,
                "annual_maintenance": 30000,
                "replacement_year": 15,
                "replacement_cost": 680000
            },
            {
                "system": "Curtain Wall - Custom",
                "initial_cost": 3800000,
                "annual_energy": 0,
                "annual_maintenance": 15000,
                "replacement_year": 40,
                "replacement_cost": 3800000
            },
            {
                "system": "Curtain Wall - Standard",
                "initial_cost": 3000000,
                "annual_energy": 0,
                "annual_maintenance": 15000,
                "replacement_year": 40,
                "replacement_cost": 3000000
            }
        ]
        
        # Calculate lifecycle costs for a 30-year period
        lifecycle_period = 30
        
        for system in systems:
            total_cost = system["initial_cost"]
            
            # Add annual costs
            annual_costs = system["annual_energy"] + system["annual_maintenance"]
            total_cost += annual_costs * lifecycle_period
            
            # Add replacement costs if needed
            if system["replacement_year"] < lifecycle_period:
                replacements = lifecycle_period // system["replacement_year"]
                total_cost += system["replacement_cost"] * replacements
            
            system["lifecycle_cost"] = total_cost
            system["annual_equivalent"] = total_cost / lifecycle_period
        
        # Create dataframe for visualization
        lifecycle_df = pd.DataFrame(systems)
        
        # Group by system type
        hvac_df = lifecycle_df[lifecycle_df["system"].str.contains("HVAC")]
        envelope_df = lifecycle_df[lifecycle_df["system"].str.contains("Curtain")]
        
        # Create layout columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### HVAC Systems Lifecycle Comparison")
            
            # Create stacked bar chart for HVAC
            hvac_comparison = pd.DataFrame({
                "System": hvac_df["system"],
                "Initial Cost": hvac_df["initial_cost"],
                "Energy (30 years)": hvac_df["annual_energy"] * lifecycle_period,
                "Maintenance (30 years)": hvac_df["annual_maintenance"] * lifecycle_period,
                "Replacement": [1000000, 680000 * 2]  # VRF once, RTU twice
            })
            
            hvac_comparison_melted = pd.melt(
                hvac_comparison,
                id_vars=["System"],
                value_vars=["Initial Cost", "Energy (30 years)", "Maintenance (30 years)", "Replacement"],
                var_name="Cost Type",
                value_name="Cost"
            )
            
            fig = px.bar(
                hvac_comparison_melted,
                x="System",
                y="Cost",
                color="Cost Type",
                barmode="stack",
                labels={"Cost": "Cost ($)"},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Add totals
            for i, system in hvac_df.iterrows():
                st.markdown(f"""
                **{system['system']}**
                - 30-year lifecycle cost: ${system['lifecycle_cost']:,.0f}
                - Annual equivalent cost: ${system['annual_equivalent']:,.0f}
                """)
        
        with col2:
            st.markdown("#### Envelope Systems Lifecycle Comparison")
            
            # Create stacked bar chart for Envelope
            envelope_comparison = pd.DataFrame({
                "System": envelope_df["system"],
                "Initial Cost": envelope_df["initial_cost"],
                "Maintenance (30 years)": envelope_df["annual_maintenance"] * lifecycle_period,
                "Replacement": [0, 0]  # No replacements in 30-year window
            })
            
            envelope_comparison_melted = pd.melt(
                envelope_comparison,
                id_vars=["System"],
                value_vars=["Initial Cost", "Maintenance (30 years)", "Replacement"],
                var_name="Cost Type",
                value_name="Cost"
            )
            
            fig = px.bar(
                envelope_comparison_melted,
                x="System",
                y="Cost",
                color="Cost Type",
                barmode="stack",
                labels={"Cost": "Cost ($)"},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Add totals
            for i, system in envelope_df.iterrows():
                st.markdown(f"""
                **{system['system']}**
                - 30-year lifecycle cost: ${system['lifecycle_cost']:,.0f}
                - Annual equivalent cost: ${system['annual_equivalent']:,.0f}
                """)
        
        # Lifecycle cost recommendations
        st.markdown("#### Life Cycle Cost Recommendations")
        
        recommendations = [
            {
                "system": "HVAC",
                "recommendation": "VRF System",
                "rationale": "Despite higher initial cost, the VRF system has significantly lower energy costs and requires fewer replacements over 30 years, resulting in a 12% lower lifecycle cost."
            },
            {
                "system": "Building Envelope",
                "recommendation": "Standard Curtain Wall",
                "rationale": "The standard curtain wall system has equivalent maintenance costs and longevity but a 21% lower initial cost, making it the clear lifecycle cost winner."
            }
        ]
        
        for rec in recommendations:
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; background-color: #e7f5ff; border-left: 3px solid #4a90e2; border-radius: 4px;">
                <div style="font-weight: 500;">{rec['system']} Recommendation: {rec['recommendation']}</div>
                <div style="font-size: 14px; margin-top: 8px;">
                    {rec['rationale']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Materials longevity tab
    with lifecycle_tabs[1]:
        st.markdown("#### Building Materials Longevity Analysis")
        
        # Create materials longevity data
        materials = [
            {"category": "Roofing", "material": "Built-up Roof", "lifespan": 30, "notes": "Higher initial cost, longer lifespan"},
            {"category": "Roofing", "material": "TPO Single-ply", "lifespan": 20, "notes": "Lower cost, shorter lifespan"},
            {"category": "Exterior Wall", "material": "Brick", "lifespan": 100, "notes": "Very long lifespan, minimal maintenance"},
            {"category": "Exterior Wall", "material": "EIFS", "lifespan": 30, "notes": "Requires more maintenance, shorter life"},
            {"category": "Exterior Wall", "material": "Metal Panel", "lifespan": 40, "notes": "Good longevity, moderate maintenance"},
            {"category": "Flooring", "material": "Porcelain Tile", "lifespan": 50, "notes": "Excellent durability, higher cost"},
            {"category": "Flooring", "material": "Luxury Vinyl Tile", "lifespan": 15, "notes": "Lower cost, shorter replacement cycle"},
            {"category": "Flooring", "material": "Carpet", "lifespan": 7, "notes": "Shortest life, frequent replacement"},
            {"category": "Windows", "material": "Aluminum Frames", "lifespan": 40, "notes": "Durable, low maintenance"},
            {"category": "Windows", "material": "Vinyl Frames", "lifespan": 30, "notes": "Lower cost, shorter lifespan"}
        ]
        
        # Create dataframe
        materials_df = pd.DataFrame(materials)
        
        # Create horizontal bar chart
        fig = px.bar(
            materials_df.sort_values("lifespan"),
            y="material",
            x="lifespan",
            color="category",
            orientation="h",
            labels={"lifespan": "Expected Lifespan (years)", "material": "Material"},
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Materials with replacement cycles
        st.markdown("#### Material Replacement Analysis (50-year building lifecycle)")
        
        # Calculate number of replacements over 50 years
        replacement_data = []
        for material in materials:
            replacements = max(0, (50 // material["lifespan"]) - 1)  # -1 because initial installation isn't a replacement
            replacement_data.append({
                "Material": material["material"],
                "Lifespan": material["lifespan"],
                "Replacements": replacements,
                "Total Installations": replacements + 1  # Initial + replacements
            })
        
        replacement_df = pd.DataFrame(replacement_data)
        
        # Create table with replacement data
        st.dataframe(replacement_df, use_container_width=True)
        
        # Material replacement recommendations
        st.markdown("#### Material Selection Recommendations")
        
        st.markdown("""
        When selecting materials, consider the following:
        
        1. **High-traffic public areas** - Select materials with longer lifespans even at higher initial costs:
           - Porcelain tile for flooring
           - Brick or metal panel for exterior walls
           - Aluminum window frames
        
        2. **Residential units** - Balance initial cost with reasonable lifespan:
           - Luxury vinyl tile for flooring (replacement during unit turnover)
           - Standard curtain wall system
           - TPO roofing with 20-year warranty
        
        3. **Cost-effective approach for shorter-term ownership**:
           - Focus on materials with 15-20 year lifespans if building will be sold within that timeframe
           - Prioritize materials with good warranty coverage
           - Consider market expectations for material quality
        """)
    
    # Energy analysis tab
    with lifecycle_tabs[2]:
        st.markdown("#### Energy Usage and Cost Analysis")
        
        # Create example energy usage data
        energy_systems = [
            {
                "system": "Standard Envelope + RTU HVAC",
                "eui": 75,  # kBtu/sf/year
                "annual_cost": 325000,
                "carbon": 1850  # metric tons CO2/year
            },
            {
                "system": "Standard Envelope + VRF HVAC",
                "eui": 65, 
                "annual_cost": 280000,
                "carbon": 1600
            },
            {
                "system": "High-Performance Envelope + RTU HVAC",
                "eui": 68,
                "annual_cost": 295000,
                "carbon": 1680
            },
            {
                "system": "High-Performance Envelope + VRF HVAC",
                "eui": 58,
                "annual_cost": 250000,
                "carbon": 1430
            }
        ]
        
        energy_df = pd.DataFrame(energy_systems)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Energy Use Intensity (EUI)")
            
            fig = px.bar(
                energy_df,
                x="system",
                y="eui",
                labels={"eui": "EUI (kBtu/sf/year)", "system": "System Combination"},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Annual Energy Cost")
            
            fig = px.bar(
                energy_df,
                x="system",
                y="annual_cost",
                labels={"annual_cost": "Annual Energy Cost ($)", "system": "System Combination"},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Carbon emissions
        st.markdown("#### Carbon Emissions")
        
        fig = px.bar(
            energy_df,
            x="system",
            y="carbon",
            labels={"carbon": "Annual Carbon Emissions (metric tons CO2)", "system": "System Combination"},
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Energy cost over time
        st.markdown("#### Energy Cost Over Time (30 years)")
        
        # Calculate cumulative costs with 3% annual energy inflation
        years = list(range(0, 31, 5))
        cumulative_costs = {}
        
        for system in energy_systems:
            costs = [0]  # Start at 0
            annual = system["annual_cost"]
            
            for year in range(1, 31):
                if year % 5 == 0:  # Only store every 5 years
                    annual_inflated = annual * (1.03) ** year  # 3% annual inflation
                    cumulative = costs[-1] + annual_inflated
                    costs.append(cumulative)
            
            cumulative_costs[system["system"]] = costs
        
        # Create dataframe for plotting
        energy_over_time = pd.DataFrame({
            "Year": years * len(energy_systems),
            "Cumulative Cost": [cost for system_costs in cumulative_costs.values() for cost in system_costs],
            "System": [system for system in cumulative_costs.keys() for _ in years]
        })
        
        fig = px.line(
            energy_over_time,
            x="Year",
            y="Cumulative Cost",
            color="System",
            labels={"Cumulative Cost": "Cumulative Energy Cost ($)"},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Energy recommendations
        st.markdown("#### Energy Analysis Recommendations")
        
        st.markdown("""
        Based on 30-year energy cost analysis:
        
        1. The high-performance envelope with VRF HVAC system provides:
           - 23% lower energy use compared to standard building
           - $2.25M in energy cost savings over 30 years
           - 11,400 metric tons of CO2 emissions reduction
        
        2. The VRF system provides greater energy savings than envelope improvements alone
        
        3. The standard envelope with VRF is more cost-effective than high-performance envelope with RTU
           when considering both initial and lifecycle energy costs
        """)