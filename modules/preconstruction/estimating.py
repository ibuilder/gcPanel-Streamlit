"""
Estimating Module for Pre-Construction

This module provides comprehensive cost estimating capabilities:
- Conceptual estimates
- Detailed cost breakdowns
- Cost analysis and comparison
- Historical data analysis
- Export functionality
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def render_estimating():
    """Render the Estimating dashboard"""
    st.header("Cost Estimating")
    
    # Create tabs for different estimating sections
    tabs = st.tabs([
        "Summary", 
        "Detailed Estimate", 
        "Cost Analysis", 
        "Historical Data", 
        "Export"
    ])
    
    # Summary tab
    with tabs[0]:
        render_estimate_summary()
    
    # Detailed Estimate tab
    with tabs[1]:
        render_detailed_estimate()
    
    # Cost Analysis tab
    with tabs[2]:
        render_cost_analysis()
    
    # Historical Data tab
    with tabs[3]:
        render_historical_data()
    
    # Export tab
    with tabs[4]:
        render_export_options()

def render_estimate_summary():
    """Render the estimate summary section"""
    st.subheader("Project Estimate Summary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Project details
        st.markdown("""
        **Project Name:** Highland Tower Development
        **Estimate Type:** Design Development (90%)
        **Prepared By:** Sarah Thompson
        **Date:** May 22, 2025
        **Gross Area:** 168,500 SF
        """)
        
        # Summary metrics
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric(
                label="Total Cost",
                value="$45,520,000",
                delta="-$480,000",
                delta_color="normal",
                help="Compared to previous estimate"
            )
        
        with metrics_col2:
            st.metric(
                label="Cost per SF",
                value="$270.15",
                delta="-$2.85",
                delta_color="normal"
            )
        
        with metrics_col3:
            st.metric(
                label="Contingency",
                value="$2,250,000",
                delta="5%",
                delta_color="off"
            )
        
        # CSI Division Summary Table
        st.markdown("#### CSI Division Summary")
        
        division_data = {
            "Division": [
                "01 General Requirements",
                "02-03 Site & Concrete",
                "04 Masonry",
                "05 Metals",
                "06 Wood & Plastics",
                "07 Thermal & Moisture",
                "08 Openings",
                "09 Finishes",
                "10-14 Specialties & Conveying",
                "21-23 Fire & HVAC",
                "26-28 Electrical",
                "31-33 Sitework & Utilities"
            ],
            "Amount": [
                2715000, 7500000, 1250000, 4800000, 2600000, 3750000, 
                2900000, 4300000, 2580000, 5100000, 4750000, 3275000
            ],
            "$/SF": [
                16.11, 44.51, 7.42, 28.49, 15.43, 22.26, 
                17.21, 25.52, 15.31, 30.27, 28.19, 19.44
            ],
            "% of Total": [
                5.97, 16.48, 2.75, 10.54, 5.71, 8.24, 
                6.37, 9.45, 5.67, 11.20, 10.44, 7.19
            ]
        }
        
        df_division = pd.DataFrame(division_data)
        st.dataframe(df_division, use_container_width=True)
    
    with col2:
        # Visualization of cost breakdown
        st.markdown("#### Cost Distribution by Division")
        
        # Create a DataFrame for the pie chart
        df_pie = pd.DataFrame({
            "Division": division_data["Division"],
            "Cost": division_data["Amount"]
        })
        
        fig = px.pie(
            df_pie, 
            values="Cost", 
            names="Division", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="center",
                x=0.5,
                font=dict(size=8)
            ),
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Estimate versions
        st.markdown("#### Estimate Versions")
        versions = [
            {"version": "Conceptual (June 2024)", "amount": "$47,500,000", "per_sf": "$281.90"},
            {"version": "Schematic (Sept 2024)", "amount": "$46,800,000", "per_sf": "$277.75"},
            {"version": "Design Dev (Jan 2025)", "amount": "$46,000,000", "per_sf": "$273.00"},
            {"version": "Current (May 2025)", "amount": "$45,520,000", "per_sf": "$270.15"}
        ]
        
        for v in versions:
            st.markdown(f"""
            <div style="padding: 8px; border-bottom: 1px solid #eee; font-size: 14px;">
                <div style="font-weight: 500;">{v["version"]}</div>
                <div style="display: flex; justify-content: space-between;">
                    <span>{v["amount"]}</span>
                    <span>{v["per_sf"]}/SF</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_detailed_estimate():
    """Render the detailed estimate section"""
    st.subheader("Detailed Cost Estimate")
    
    # Create a filter for divisions
    divisions = [
        "All Divisions",
        "01 General Requirements",
        "02-03 Site & Concrete",
        "04 Masonry",
        "05 Metals",
        "06 Wood & Plastics",
        "07 Thermal & Moisture",
        "08 Openings",
        "09 Finishes",
        "10-14 Specialties & Conveying",
        "21-23 Fire & HVAC",
        "26-28 Electrical",
        "31-33 Sitework & Utilities"
    ]
    
    selected_division = st.selectbox("Filter by Division", divisions)
    
    # Create a mock detailed estimate for demonstration
    detailed_data = []
    
    # Division 1 items
    if selected_division in ["All Divisions", "01 General Requirements"]:
        detailed_data.extend([
            {"csi": "01 11 00", "description": "Summary of Work", "quantity": 1, "unit": "LS", "unit_cost": 150000, "total": 150000},
            {"csi": "01 31 00", "description": "Project Management", "quantity": 24, "unit": "MO", "unit_cost": 45000, "total": 1080000},
            {"csi": "01 32 00", "description": "Construction Schedule", "quantity": 1, "unit": "LS", "unit_cost": 35000, "total": 35000},
            {"csi": "01 50 00", "description": "Temporary Facilities", "quantity": 24, "unit": "MO", "unit_cost": 25000, "total": 600000},
            {"csi": "01 74 00", "description": "Cleaning", "quantity": 168500, "unit": "SF", "unit_cost": 1.25, "total": 210625},
            {"csi": "01 78 00", "description": "Closeout Submittals", "quantity": 1, "unit": "LS", "unit_cost": 75000, "total": 75000}
        ])
    
    # Division 2-3 items
    if selected_division in ["All Divisions", "02-03 Site & Concrete"]:
        detailed_data.extend([
            {"csi": "02 41 00", "description": "Demolition", "quantity": 1, "unit": "LS", "unit_cost": 650000, "total": 650000},
            {"csi": "03 11 00", "description": "Concrete Forming", "quantity": 168500, "unit": "SF", "unit_cost": 8.5, "total": 1432250},
            {"csi": "03 15 00", "description": "Concrete Accessories", "quantity": 1, "unit": "LS", "unit_cost": 275000, "total": 275000},
            {"csi": "03 20 00", "description": "Concrete Reinforcing", "quantity": 425, "unit": "TON", "unit_cost": 2500, "total": 1062500},
            {"csi": "03 30 00", "description": "Cast-in-Place Concrete", "quantity": 6500, "unit": "CY", "unit_cost": 500, "total": 3250000},
            {"csi": "03 35 00", "description": "Concrete Finishing", "quantity": 168500, "unit": "SF", "unit_cost": 4.75, "total": 800375}
        ])
    
    # Division 4 items
    if selected_division in ["All Divisions", "04 Masonry"]:
        detailed_data.extend([
            {"csi": "04 20 00", "description": "Unit Masonry", "quantity": 12500, "unit": "SF", "unit_cost": 45, "total": 562500},
            {"csi": "04 43 00", "description": "Stone Masonry", "quantity": 8500, "unit": "SF", "unit_cost": 75, "total": 637500},
            {"csi": "04 72 00", "description": "Cast Stone Masonry", "quantity": 250, "unit": "LF", "unit_cost": 200, "total": 50000}
        ])
    
    # Create DataFrame
    if detailed_data:
        df_detailed = pd.DataFrame(detailed_data)
        
        # Add a column for unit cost formatting
        df_detailed["Unit Cost"] = df_detailed["unit_cost"].apply(lambda x: f"${x:,.2f}")
        df_detailed["Total"] = df_detailed["total"].apply(lambda x: f"${x:,.2f}")
        
        # Display the table
        st.dataframe(
            df_detailed[["csi", "description", "quantity", "unit", "Unit Cost", "Total"]], 
            column_config={
                "csi": "CSI Code",
                "description": "Description",
                "quantity": "Quantity",
                "unit": "Unit",
                "Unit Cost": "Unit Cost",
                "Total": "Total Cost"
            },
            use_container_width=True
        )
    else:
        st.info("Select a division to view detailed cost items.")
    
    # Add ability to add new items
    with st.expander("Add New Cost Item"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("CSI Code", placeholder="XX XX XX")
            st.text_input("Description", placeholder="Item description")
            st.number_input("Quantity", min_value=0.0, step=1.0)
        
        with col2:
            st.selectbox("Unit", ["LS", "SF", "SY", "CY", "LF", "EA", "TON", "MO", "DAY"])
            st.number_input("Unit Cost ($)", min_value=0.0, step=10.0)
            st.button("Add Item")

def render_cost_analysis():
    """Render the cost analysis section"""
    st.subheader("Cost Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Cost Metrics")
        
        metrics = [
            {"metric": "Building Structure", "cost_sf": 125.25, "percent": 46.4},
            {"metric": "Building Enclosure", "cost_sf": 45.60, "percent": 16.9},
            {"metric": "Building Interiors", "cost_sf": 40.30, "percent": 14.9},
            {"metric": "Building Services", "cost_sf": 58.50, "percent": 21.7},
            {"metric": "Sitework", "cost_sf": 0.50, "percent": 0.1}
        ]
        
        # Create a DataFrame for the table
        df_metrics = pd.DataFrame(metrics)
        df_metrics["Cost/SF"] = df_metrics["cost_sf"].apply(lambda x: f"${x:.2f}")
        df_metrics["Percent"] = df_metrics["percent"].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            df_metrics[["metric", "Cost/SF", "Percent"]], 
            column_config={
                "metric": "Category",
                "Cost/SF": "Cost per SF",
                "Percent": "% of Total"
            },
            use_container_width=True
        )
        
        # Cost Factors Analysis
        st.markdown("#### Cost Factors Analysis")
        
        factors = [
            {"factor": "Labor Market Conditions", "impact": "High", "adjustment": "+3.5%"},
            {"factor": "Material Price Volatility", "impact": "Medium", "adjustment": "+2.0%"},
            {"factor": "Site Conditions", "impact": "Low", "adjustment": "+0.5%"},
            {"factor": "Schedule Constraints", "impact": "Medium", "adjustment": "+1.5%"},
            {"factor": "COVID-19 Recovery", "impact": "Low", "adjustment": "+0.8%"},
            {"factor": "Market Competition", "impact": "High", "adjustment": "-2.5%"}
        ]
        
        for factor in factors:
            impact_color = "#4a90e2"  # Default blue for medium
            if factor["impact"] == "High":
                impact_color = "#ef4444"  # Red
            elif factor["impact"] == "Low":
                impact_color = "#38d39f"  # Green
                
            st.markdown(f"""
            <div style="margin-bottom: 8px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{factor["factor"]}</strong>
                    <span style="color: {impact_color};">{factor["impact"]} Impact</span>
                </div>
                <div>Adjustment: {factor["adjustment"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Cost Comparison by Building Type
        st.markdown("#### Cost Comparison ($/SF)")
        
        comparison_data = pd.DataFrame({
            "Building Type": ["Economy", "Average", "High-End", "Current Project"],
            "Cost per SF": [230, 255, 290, 270.15]
        })
        
        fig = px.bar(
            comparison_data,
            x="Building Type",
            y="Cost per SF",
            color="Building Type",
            text="Cost per SF",
            color_discrete_sequence=["#4a90e2", "#4a90e2", "#4a90e2", "#ef4444"]
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost breakdown analysis
        st.markdown("#### Trade Package Analysis")
        
        trade_data = pd.DataFrame({
            "Trade Package": ["Structure", "Enclosure", "Mechanical", "Electrical", "Plumbing", "Finishes", "Other"],
            "Benchmark Cost": [12500000, 5800000, 4100000, 4200000, 2800000, 4300000, 3950000],
            "Current Estimate": [12350000, 5750000, 4250000, 4150000, 2900000, 4200000, 3920000]
        })
        
        # Calculate variance
        trade_data["Variance"] = trade_data["Current Estimate"] - trade_data["Benchmark Cost"]
        trade_data["Variance %"] = trade_data["Variance"] / trade_data["Benchmark Cost"] * 100
        
        # Create a new DataFrame for plotting
        df_plot = pd.DataFrame({
            "Trade Package": trade_data["Trade Package"].tolist() + trade_data["Trade Package"].tolist(),
            "Type": ["Benchmark"]*len(trade_data) + ["Current"]*len(trade_data),
            "Cost": trade_data["Benchmark Cost"].tolist() + trade_data["Current Estimate"].tolist()
        })
        
        fig = px.bar(
            df_plot,
            x="Trade Package",
            y="Cost",
            color="Type",
            barmode="group",
            text_auto='.2s',
            color_discrete_sequence=["#4a90e2", "#ff6b6b"]
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def render_historical_data():
    """Render the historical data analysis section"""
    st.subheader("Historical Cost Data Analysis")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Building Type", ["Residential - High Rise", "All Types", "Commercial", "Mixed-Use", "Institutional"])
    
    with col2:
        st.selectbox("Location", ["Highland District", "All Locations", "Downtown", "Midtown", "Suburban"])
    
    with col3:
        st.selectbox("Year", ["2025", "All Years", "2024", "2023", "2022", "2021"])
    
    # Historical projects table
    st.markdown("#### Similar Historical Projects")
    
    historical_data = [
        {"project": "The Madison Tower", "type": "Residential", "year": 2023, "cost": 42500000, "sf": 158000, "cost_sf": 269.00},
        {"project": "Highland Heights", "type": "Mixed-Use", "year": 2023, "cost": 38750000, "sf": 145000, "cost_sf": 267.24},
        {"project": "Park Central", "type": "Residential", "year": 2024, "cost": 51200000, "sf": 188000, "cost_sf": 272.34},
        {"project": "The Meridian", "type": "Residential", "year": 2022, "cost": 39800000, "sf": 152000, "cost_sf": 261.84},
        {"project": "City Center Lofts", "type": "Mixed-Use", "year": 2022, "cost": 44600000, "sf": 172500, "cost_sf": 258.55}
    ]
    
    # Create DataFrame
    df_historical = pd.DataFrame(historical_data)
    
    # Add formatted columns
    df_historical["Total Cost"] = df_historical["cost"].apply(lambda x: f"${x:,.0f}")
    df_historical["Cost/SF"] = df_historical["cost_sf"].apply(lambda x: f"${x:.2f}")
    
    # Display table
    st.dataframe(
        df_historical[["project", "type", "year", "sf", "Total Cost", "Cost/SF"]], 
        column_config={
            "project": "Project Name",
            "type": "Building Type",
            "year": "Year Completed",
            "sf": "Gross SF",
            "Total Cost": "Total Cost",
            "Cost/SF": "Cost per SF"
        },
        use_container_width=True
    )
    
    # Cost trend analysis
    st.markdown("#### Historical Cost Trends")
    
    # Create trend data
    trend_data = pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "Cost Index": [100, 104, 106, 112, 128, 132, 135, 138]
    })
    
    fig = px.line(
        trend_data,
        x="Year",
        y="Cost Index",
        markers=True,
        title="Construction Cost Index (2018 = 100)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost drivers
    st.markdown("#### Historical Cost Drivers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Material cost trends
        material_data = pd.DataFrame({
            "Year": [2020, 2021, 2022, 2023, 2024, 2025],
            "Concrete": [100, 108, 132, 128, 125, 122],
            "Steel": [100, 115, 140, 130, 125, 128],
            "Lumber": [100, 180, 150, 120, 110, 115],
            "Copper": [100, 125, 130, 135, 140, 142]
        })
        
        fig = px.line(
            material_data,
            x="Year",
            y=["Concrete", "Steel", "Lumber", "Copper"],
            title="Material Price Index (2020 = 100)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Labor cost trends
        labor_data = pd.DataFrame({
            "Year": [2020, 2021, 2022, 2023, 2024, 2025],
            "Concrete": [100, 105, 110, 116, 122, 128],
            "Carpentry": [100, 104, 108, 115, 122, 130],
            "Electrical": [100, 106, 112, 118, 125, 132],
            "Plumbing": [100, 105, 111, 117, 124, 131]
        })
        
        fig = px.line(
            labor_data,
            x="Year",
            y=["Concrete", "Carpentry", "Electrical", "Plumbing"],
            title="Labor Cost Index (2020 = 100)"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_export_options():
    """Render the export options section"""
    st.subheader("Export Estimate")
    
    # Export format selection
    st.markdown("#### Select Export Format")
    export_format = st.radio(
        "Format", 
        ["Excel (.xlsx)", "PDF (.pdf)", "CSV (.csv)"],
        horizontal=True
    )
    
    # Export options
    st.markdown("#### Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Include Summary", value=True)
        st.checkbox("Include Detailed Breakdown", value=True)
        st.checkbox("Include Cost Analysis", value=True)
    
    with col2:
        st.checkbox("Include Historical Comparison", value=False)
        st.checkbox("Include Visualizations", value=True)
        st.checkbox("Include Notes & Assumptions", value=True)
    
    # Notes and assumptions
    st.markdown("#### Notes & Assumptions")
    st.text_area(
        "Add notes to include in exported estimate",
        value="1. Estimate based on 90% Design Development drawings dated May 1, 2025.\n2. Escalation included at 3.5% per year.\n3. 5% design contingency included.\n4. Excludes FF&E, land costs, and financing costs.",
        height=150
    )
    
    # Export button
    st.button("Generate Export", type="primary")