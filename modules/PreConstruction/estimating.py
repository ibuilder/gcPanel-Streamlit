"""
Estimating Module

This module provides tools for cost estimating, including:
- Conceptual estimating
- Detailed estimating
- Value engineering
- Cost analysis
- Bid package preparation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from assets.crud_styler import (
    render_crud_list_container, end_crud_list_container,
    render_crud_detail_container, end_crud_detail_container,
    render_form_actions, render_crud_table, apply_crud_formatter
)

def render_estimating():
    """Render the Estimating dashboard"""
    st.header("Cost Estimating")
    
    # Create tabs for different estimating sections
    tabs = st.tabs([
        "Summary", 
        "Detailed Estimate", 
        "Historical Analysis", 
        "Cost Breakdown"
    ])
    
    # Summary tab
    with tabs[0]:
        render_estimating_summary()
    
    # Detailed estimate tab
    with tabs[1]:
        render_detailed_estimate()
    
    # Historical analysis tab
    with tabs[2]:
        render_historical_analysis()
    
    # Cost breakdown tab
    with tabs[3]:
        render_cost_breakdown()

def render_estimating_summary():
    """Render the estimating summary section"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Project Cost Summary")
        
        # Project info
        st.info("""
        **Highland Tower Development**
        
        This estimate represents the 90% Construction Documents phase estimate.
        Target budget: $45,500,000
        """)
        
        # Estimate summary
        summary_data = {
            "Hard Costs": 38500000,
            "Soft Costs": 5200000,
            "Contingency": 1800000,
            "Total": 45500000,
            "Target Budget": 45500000,
            "Variance": 0
        }
        
        # Format as millions with 1 decimal
        formatted_data = {k: f"${v/1000000:.1f}M" for k, v in summary_data.items()}
        formatted_data["Variance"] = f"${summary_data['Variance']/1000000:.1f}M"
        
        # Create a custom summary display
        st.markdown("""
        <style>
        .cost-summary {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .cost-summary-total {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 2px solid #333;
            font-weight: bold;
        }
        .cost-summary-target {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px dashed #aaa;
        }
        .cost-summary-variance {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-weight: bold;
            color: #4CAF50;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cost-summary">
            <span>Hard Costs</span>
            <span>{formatted_data['Hard Costs']}</span>
        </div>
        <div class="cost-summary">
            <span>Soft Costs</span>
            <span>{formatted_data['Soft Costs']}</span>
        </div>
        <div class="cost-summary">
            <span>Contingency</span>
            <span>{formatted_data['Contingency']}</span>
        </div>
        <div class="cost-summary-total">
            <span>Total Estimated Cost</span>
            <span>{formatted_data['Total']}</span>
        </div>
        <div class="cost-summary-target">
            <span>Target Budget</span>
            <span>{formatted_data['Target Budget']}</span>
        </div>
        <div class="cost-summary-variance">
            <span>Variance</span>
            <span>{formatted_data['Variance']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Cost per square foot analysis
        st.subheader("Cost Metrics")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric(
                label="Cost per SF",
                value="$270",
                delta="-$5",
                delta_color="normal",
                help="Cost per gross square foot"
            )
        
        with metrics_col2:
            st.metric(
                label="Cost per Unit",
                value="$379,167",
                delta="-$4,167",
                delta_color="normal",
                help="Average cost per residential unit"
            )
        
        with metrics_col3:
            st.metric(
                label="Hard Cost %",
                value="84.6%",
                delta="+0.5%",
                delta_color="normal",
                help="Hard costs as percentage of total"
            )
    
    with col2:
        st.subheader("Estimate Versions")
        
        versions = [
            {"version": "90% CD", "date": "May 15, 2025", "amount": "$45.5M", "active": True},
            {"version": "50% CD", "date": "Mar 22, 2025", "amount": "$46.2M", "active": False},
            {"version": "100% DD", "date": "Jan 10, 2025", "amount": "$47.8M", "active": False},
            {"version": "50% DD", "date": "Nov 5, 2024", "amount": "$48.5M", "active": False},
            {"version": "Schematic", "date": "Sep 12, 2024", "amount": "$51.0M", "active": False},
            {"version": "Conceptual", "date": "Jul 3, 2024", "amount": "$55.0M", "active": False}
        ]
        
        for version in versions:
            bg_color = "#f8f9fa" if not version["active"] else "#e7f5ff"
            border = "none" if not version["active"] else "2px solid #4a90e2"
            
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; background-color: {bg_color}; border-left: {border}; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 500;">{version["version"]} Estimate</span>
                    <span>{version["amount"]}</span>
                </div>
                <div style="font-size: 12px; color: #6c757d; margin-top: 4px;">
                    {version["date"]} {" • CURRENT" if version["active"] else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Cost trend chart
        st.markdown("#### Cost Trend")
        
        trend_data = pd.DataFrame({
            "Phase": ["Conceptual", "Schematic", "50% DD", "100% DD", "50% CD", "90% CD"],
            "Cost (millions)": [55.0, 51.0, 48.5, 47.8, 46.2, 45.5]
        })
        
        fig = px.line(
            trend_data, 
            x="Phase", 
            y="Cost (millions)",
            markers=True,
            line_shape="linear",
            labels={"Cost (millions)": "Cost ($ millions)"}
        )
        
        fig.update_layout(height=220)
        st.plotly_chart(fig, use_container_width=True)

def render_detailed_estimate():
    """Render the detailed estimate section"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Detailed Estimate by Division")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            view_type = st.radio(
                "View By",
                options=["Division", "Trade Package", "Building Area"],
                horizontal=True
            )
        
        with filter_col2:
            level = st.select_slider(
                "Detail Level", 
                options=["Summary", "Level 1", "Level 2", "Level 3"]
            )
        
        # Create division data
        division_data = [
            {"div": "01", "name": "General Requirements", "amount": 2250000},
            {"div": "02", "name": "Existing Conditions", "amount": 950000},
            {"div": "03", "name": "Concrete", "amount": 5600000},
            {"div": "04", "name": "Masonry", "amount": 1250000},
            {"div": "05", "name": "Metals", "amount": 4500000},
            {"div": "06", "name": "Wood & Plastics", "amount": 2100000},
            {"div": "07", "name": "Thermal & Moisture", "amount": 3750000},
            {"div": "08", "name": "Openings", "amount": 3250000},
            {"div": "09", "name": "Finishes", "amount": 4850000},
            {"div": "10", "name": "Specialties", "amount": 750000},
            {"div": "11", "name": "Equipment", "amount": 550000},
            {"div": "12", "name": "Furnishings", "amount": 350000},
            {"div": "13", "name": "Special Construction", "amount": 250000},
            {"div": "14", "name": "Conveying Systems", "amount": 1200000},
            {"div": "21", "name": "Fire Suppression", "amount": 850000},
            {"div": "22", "name": "Plumbing", "amount": 1850000},
            {"div": "23", "name": "HVAC", "amount": 2350000},
            {"div": "26", "name": "Electrical", "amount": 2950000},
            {"div": "27", "name": "Communications", "amount": 850000},
            {"div": "31", "name": "Earthwork", "amount": 1100000},
            {"div": "32", "name": "Exterior Improvements", "amount": 850000},
            {"div": "33", "name": "Utilities", "amount": 650000}
        ]
        
        df = pd.DataFrame(division_data)
        df["percent"] = df["amount"] / df["amount"].sum() * 100
        
        if view_type == "Division":
            df["category"] = df["div"] + " " + df["name"]
            fig = px.bar(
                df.sort_values("amount", ascending=False),
                y="category",
                x="amount",
                text_auto='.2s',
                labels={"amount": "Amount ($)", "category": "Division"},
                height=600
            )
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Display division detail
        if st.checkbox("Show Division Details"):
            df_display = df.copy()
            df_display["amount"] = df_display["amount"].apply(lambda x: f"${x:,.0f}")
            df_display["percent"] = df_display["percent"].apply(lambda x: f"{x:.1f}%")
            df_display.columns = ["Division", "Name", "Amount", "Percent"]
            st.dataframe(df_display, use_container_width=True)
        
    with col2:
        st.subheader("Cost Distribution")
        
        # Create cost category data
        categories = {
            "Superstructure": 10100000,
            "Exterior Enclosure": 7000000,
            "Interior Construction": 7200000,
            "Services": 10050000,
            "Equipment & Furnishings": 900000,
            "Site Construction": 3250000
        }
        
        # Create a pie chart
        fig = px.pie(
            values=list(categories.values()),
            names=list(categories.keys()),
            hole=0.4,
            labels={"label": "Category", "value": "Amount"}
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost metrics
        st.subheader("Building Component Metrics")
        
        metrics = [
            {"label": "Structure", "value": "$60 / SF"},
            {"label": "Enclosure", "value": "$42 / SF"},
            {"label": "Interior", "value": "$43 / SF"},
            {"label": "MEP", "value": "$60 / SF"}
        ]
        
        for metric in metrics:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <span>{metric["label"]}</span>
                <span><strong>{metric["value"]}</strong></span>
            </div>
            """, unsafe_allow_html=True)
        
        # Budget allocation
        st.subheader("Budget Allocation")
        
        allocation = pd.DataFrame({
            "Category": ["Hard Costs", "Soft Costs", "Contingency"],
            "Percentage": [84.6, 11.4, 4.0]
        })
        
        fig = px.bar(
            allocation,
            x="Percentage",
            y="Category",
            orientation="h",
            text_auto=True,
            labels={"Percentage": "Percentage of Total Budget"}
        )
        fig.update_traces(marker_color=["#4a90e2", "#f59e0b", "#ef4444"])
        st.plotly_chart(fig, use_container_width=True)

def render_historical_analysis():
    """Render the historical analysis section"""
    st.subheader("Historical Cost Analysis")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Project comparison chart
        st.markdown("#### Comparison to Similar Projects")
        
        comparison = pd.DataFrame({
            "Project": ["Highland Tower", "Skyline Residences", "Urban Centre", "Parkview Heights", "Metro Lofts"],
            "SF Cost": [270, 285, 261, 279, 298],
            "Year": [2025, 2024, 2023, 2023, 2022]
        })
        
        fig = px.bar(
            comparison,
            x="Project",
            y="SF Cost",
            color="Year",
            text_auto=True,
            labels={"SF Cost": "Cost per SF ($)", "Project": "Project Name"},
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost escalation analysis
        st.markdown("#### Cost Escalation Analysis")
        
        # Historical escalation data
        years = list(range(2020, 2026))
        annual_escalation = [2.1, 4.8, 6.2, 3.5, 2.8, 2.3]  # Percentages
        
        # Calculate cumulative escalation (2020 = 100)
        cumulative = [100]
        for rate in annual_escalation:
            cumulative.append(cumulative[-1] * (1 + rate/100))
        
        escalation_df = pd.DataFrame({
            "Year": years,
            "Annual": annual_escalation,
            "Index": cumulative[:-1]
        })
        
        fig = go.Figure()
        
        # Add annual escalation bars
        fig.add_trace(go.Bar(
            x=escalation_df["Year"],
            y=escalation_df["Annual"],
            name="Annual Escalation %",
            marker_color="#4a90e2",
            yaxis="y"
        ))
        
        # Add cumulative index line
        fig.add_trace(go.Scatter(
            x=escalation_df["Year"],
            y=escalation_df["Index"],
            name="Cost Index (2020=100)",
            marker_color="#ef4444",
            mode="lines+markers",
            yaxis="y2"
        ))
        
        # Set up dual axis
        fig.update_layout(
            yaxis=dict(title="Annual Escalation (%)"),
            yaxis2=dict(
                title="Cost Index (2020=100)",
                overlaying="y",
                side="right"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost factors
        st.markdown("#### Cost Factors by Building Type")
        
        building_types = {
            "High-rise residential": 1.00,
            "Mid-rise residential": 0.92,
            "Office": 1.05,
            "Retail": 0.85,
            "Hotel": 1.10,
            "Healthcare": 1.25,
            "Education": 0.95
        }
        
        for building, factor in building_types.items():
            if building == "High-rise residential":
                color = "#4a90e2"
                weight = "bold"
            else:
                color = "#333333"
                weight = "normal"
                
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <span style="color: {color}; font-weight: {weight};">{building}</span>
                <span style="color: {color}; font-weight: {weight};">{factor:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Market trend analysis
        st.markdown("#### Market Trend Analysis")
        
        trends = [
            {"category": "Labor", "change": +3.5, "impact": "Medium", "notes": "Skilled labor shortages in MEP trades"},
            {"category": "Concrete", "change": +2.8, "impact": "High", "notes": "High demand from infrastructure projects"},
            {"category": "Steel", "change": -1.2, "impact": "Medium", "notes": "Recent price reductions due to global supply"},
            {"category": "Lumber", "change": +0.5, "impact": "Low", "notes": "Stabilizing after recent volatility"},
            {"category": "MEP Equipment", "change": +4.2, "impact": "High", "notes": "Supply chain issues affecting lead times"}
        ]
        
        for trend in trends:
            change_color = "#38d39f" if trend["change"] <= 0 else "#ef4444"
            impact_color = "#38d39f" 
            if trend["impact"] == "Medium":
                impact_color = "#f59e0b"
            elif trend["impact"] == "High":
                impact_color = "#ef4444"
                
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 500;">{trend["category"]}</span>
                    <span style="color: {change_color};">{'+' if trend["change"] > 0 else ''}{trend["change"]}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 4px;">
                    <span>Impact: <span style="color: {impact_color};">{trend["impact"]}</span></span>
                </div>
                <div style="font-size: 12px; color: #6c757d; margin-top: 4px;">
                    {trend["notes"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_cost_breakdown():
    """Render the cost breakdown section"""
    st.subheader("Cost Breakdown Analysis")
    
    # Create tabs for different breakdown views
    tabs = st.tabs([
        "By Building Area", 
        "By Floor", 
        "By Unit Type",
        "By Systems"
    ])
    
    # By building area tab
    with tabs[0]:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("#### Cost by Building Area")
            
            areas = [
                {"area": "Residential", "sf": 142000, "cost": 27500000, "cost_per_sf": 193.7},
                {"area": "Retail", "sf": 12500, "cost": 3250000, "cost_per_sf": 260.0},
                {"area": "Amenities", "sf": 6000, "cost": 1800000, "cost_per_sf": 300.0},
                {"area": "Parking", "sf": 28000, "cost": 5950000, "cost_per_sf": 212.5},
                {"area": "Common Areas", "sf": 8000, "cost": 2000000, "cost_per_sf": 250.0}
            ]
            
            df = pd.DataFrame(areas)
            
            # Stacked bar chart showing total cost and cost per SF
            fig = px.bar(
                df,
                x="area",
                y="cost",
                color="cost_per_sf",
                text_auto='.2s',
                labels={"area": "Building Area", "cost": "Total Cost ($)", "cost_per_sf": "Cost per SF ($)"},
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Area Distribution")
            
            # Create pie chart of area distribution
            fig = px.pie(
                df,
                values="sf",
                names="area",
                hole=0.4,
                labels={"area": "Building Area", "sf": "Square Footage"}
            )
            fig.update_traces(textposition="outside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost per SF comparison
            st.markdown("#### Cost per SF by Area")
            
            fig = px.bar(
                df,
                x="area",
                y="cost_per_sf",
                text_auto=True,
                labels={"area": "Building Area", "cost_per_sf": "Cost per SF ($)"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # By floor tab
    with tabs[1]:
        st.markdown("#### Cost Distribution by Floor")
        
        # Create mock data for floors
        floors = []
        
        # Basement levels
        floors.append({"floor": "B2", "use": "Parking", "sf": 14000, "cost": 2800000})
        floors.append({"floor": "B1", "use": "Parking", "sf": 14000, "cost": 3150000})
        
        # Ground + retail
        floors.append({"floor": "1", "use": "Retail/Lobby", "sf": 14500, "cost": 4350000})
        
        # Residential floors (groups of 3 for simplicity)
        for i in range(2, 14, 3):
            floor_group = f"{i}-{i+2}"
            floors.append({"floor": floor_group, "use": "Residential", "sf": 30000, "cost": 6000000})
        
        # Penthouse + mechanical
        floors.append({"floor": "14-15", "use": "Penthouse", "sf": 16000, "cost": 4200000})
        
        df = pd.DataFrame(floors)
        df["cost_per_sf"] = df["cost"] / df["sf"]
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create horizontal bar chart for cost by floor
            df_sorted = df.sort_values("floor", key=lambda x: [
                -1 if f.startswith("B") else 1 for f in x
            ])
            
            fig = px.bar(
                df_sorted,
                y="floor",
                x="cost",
                text_auto='.2s',
                color="use",
                labels={"floor": "Floor", "cost": "Total Cost ($)", "use": "Usage Type"},
                height=400,
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create a table with detailed breakdown
            df_display = df_sorted.copy()
            df_display["cost"] = df_display["cost"].apply(lambda x: f"${x:,.0f}")
            df_display["sf"] = df_display["sf"].apply(lambda x: f"{x:,.0f}")
            df_display["cost_per_sf"] = df_display["cost_per_sf"].apply(lambda x: f"${x:.2f}")
            
            df_display.columns = ["Floor", "Usage", "Area (SF)", "Total Cost", "Cost/SF"]
            st.dataframe(df_display, use_container_width=True)
            
            # Show Floor distribution summary
            st.markdown("#### Floor Type Distribution")
            
            usage_summary = df.groupby("use").agg({"cost": "sum", "sf": "sum"})
            usage_summary["percent"] = usage_summary["cost"] / usage_summary["cost"].sum() * 100
            
            for idx, row in usage_summary.iterrows():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                    <span>{idx}</span>
                    <span>${row['cost']:,.0f} ({row['percent']:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
    
    # By unit type tab
    with tabs[2]:
        st.markdown("#### Cost Distribution by Unit Type")
        
        # Create mock data for unit types
        unit_types = [
            {"type": "Studio", "count": 25, "avg_sf": 550, "total_sf": 13750, "cost": 3575000},
            {"type": "1 Bedroom", "count": 40, "avg_sf": 750, "total_sf": 30000, "cost": 7800000},
            {"type": "2 Bedroom", "count": 35, "avg_sf": 1100, "total_sf": 38500, "cost": 10010000},
            {"type": "3 Bedroom", "count": 15, "avg_sf": 1500, "total_sf": 22500, "cost": 6075000},
            {"type": "Penthouse", "count": 5, "avg_sf": 2250, "total_sf": 11250, "cost": 3375000}
        ]
        
        df = pd.DataFrame(unit_types)
        df["cost_per_sf"] = df["cost"] / df["total_sf"]
        df["cost_per_unit"] = df["cost"] / df["count"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create stacked bar chart
            fig = px.bar(
                df,
                x="type",
                y="cost",
                text_auto='.2s',
                color="count",
                labels={"type": "Unit Type", "cost": "Total Cost ($)", "count": "Number of Units"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create unit cost comparison
            fig = px.bar(
                df,
                x="type",
                y="cost_per_unit",
                text_auto='.2s',
                labels={"type": "Unit Type", "cost_per_unit": "Cost per Unit ($)"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown("#### Unit Type Details")
        
        df_display = df.copy()
        df_display["cost"] = df_display["cost"].apply(lambda x: f"${x:,.0f}")
        df_display["cost_per_sf"] = df_display["cost_per_sf"].apply(lambda x: f"${x:.2f}")
        df_display["cost_per_unit"] = df_display["cost_per_unit"].apply(lambda x: f"${x:,.0f}")
        
        df_display.columns = ["Unit Type", "Count", "Avg SF", "Total SF", "Total Cost", "Cost/SF", "Cost/Unit"]
        st.dataframe(df_display, use_container_width=True)
        
        # Unit Mix Visualization
        st.markdown("#### Unit Mix")
        
        fig = px.pie(
            df,
            values="count",
            names="type",
            hole=0.4,
            labels={"type": "Unit Type", "count": "Number of Units"}
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
    
    # By systems tab
    with tabs[3]:
        st.markdown("#### Cost Distribution by Building Systems")
        
        # Create mock data for systems
        systems = [
            {"system": "Structure", "cost": 10100000, "percent": 22.2},
            {"system": "Enclosure", "cost": 6250000, "percent": 13.7},
            {"system": "Interiors", "cost": 7250000, "percent": 15.9},
            {"system": "HVAC", "cost": 3200000, "percent": 7.0},
            {"system": "Plumbing", "cost": 2750000, "percent": 6.0},
            {"system": "Fire Protection", "cost": 850000, "percent": 1.9},
            {"system": "Electrical", "cost": 3250000, "percent": 7.1},
            {"system": "Elevators", "cost": 1250000, "percent": 2.7},
            {"system": "Site & Foundations", "cost": 3600000, "percent": 7.9},
            {"system": "General Requirements", "cost": 3500000, "percent": 7.7},
            {"system": "Other", "cost": 3500000, "percent": 7.9}
        ]
        
        df = pd.DataFrame(systems)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create horizontal bar chart
            df_sorted = df.sort_values("cost", ascending=True)
            
            fig = px.bar(
                df_sorted,
                y="system",
                x="cost",
                text_auto='.2s',
                labels={"system": "Building System", "cost": "Cost ($)"},
                orientation="h",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create pie chart
            fig = px.pie(
                df,
                values="cost",
                names="system",
                labels={"system": "Building System", "cost": "Cost ($)"}
            )
            fig.update_traces(textposition="inside", textinfo="percent")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # System comparison
        st.markdown("#### System Cost Distribution")
        
        # Create a treemap visualization
        fig = px.treemap(
            df,
            values="cost",
            names="system",
            color="cost",
            color_continuous_scale="Viridis",
            labels={"system": "Building System", "cost": "Cost ($)"}
        )
        fig.update_traces(textinfo="label+value+percent parent")
        st.plotly_chart(fig, use_container_width=True)