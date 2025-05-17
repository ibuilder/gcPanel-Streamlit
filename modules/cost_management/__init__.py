"""
Cost Management module for the gcPanel Construction Management Dashboard.

This module provides cost management features including budgeting,
cost tracking, forecasting, and cost reports.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

def render_cost_management():
    """Render the cost management module"""
    
    # Header
    st.title("Cost Management")
    
    # Tab navigation for cost management sections
    tab1, tab2, tab3, tab4 = st.tabs(["Budget", "Cost Tracking", "Forecasting", "Cost Reports"])
    
    # Budget Tab
    with tab1:
        render_budget()
    
    # Cost Tracking Tab
    with tab2:
        render_cost_tracking()
    
    # Forecasting Tab
    with tab3:
        render_forecasting()
    
    # Cost Reports Tab
    with tab4:
        render_cost_reports()

def render_budget():
    """Render the budget section"""
    
    st.header("Project Budget")
    
    # Sample data for budget
    budget_categories = [
        # Division 00 & 01 - General Requirements
        {"division": "00-01", "category": "General Requirements", "description": "Project management, supervision, temporary facilities, etc."},
        
        # Division 02 - Existing Conditions & Site Work
        {"division": "02", "category": "Site Work", "description": "Demolition, excavation, grading, etc."},
        
        # Division 03 - Concrete
        {"division": "03", "category": "Concrete", "description": "Foundations, slabs, concrete structures, etc."},
        
        # Division 04 - Masonry
        {"division": "04", "category": "Masonry", "description": "Brick, block, stone masonry, etc."},
        
        # Division 05 - Metals
        {"division": "05", "category": "Metals", "description": "Structural steel, metal fabrications, etc."},
        
        # Division 06 - Wood & Plastics
        {"division": "06", "category": "Wood & Plastics", "description": "Rough carpentry, finish carpentry, etc."},
        
        # Division 07 - Thermal & Moisture Protection
        {"division": "07", "category": "Thermal & Moisture", "description": "Waterproofing, roofing, insulation, etc."},
        
        # Division 08 - Openings
        {"division": "08", "category": "Doors & Windows", "description": "Doors, windows, hardware, etc."},
        
        # Division 09 - Finishes
        {"division": "09", "category": "Finishes", "description": "Drywall, ceilings, flooring, painting, etc."},
        
        # Division 10-14 - Specialties
        {"division": "10-14", "category": "Specialties", "description": "Signage, toilet accessories, equipment, etc."},
        
        # Division 21-23 - Mechanical
        {"division": "21-23", "category": "Mechanical", "description": "Fire protection, plumbing, HVAC, etc."},
        
        # Division 26-28 - Electrical
        {"division": "26-28", "category": "Electrical", "description": "Power, lighting, low voltage, etc."},
        
        # Division 31-33 - Site & Infrastructure
        {"division": "31-33", "category": "Site & Infrastructure", "description": "Utilities, paving, landscaping, etc."},
        
        # Other costs
        {"division": "Other", "category": "General Conditions", "description": "Insurance, bonds, general conditions, etc."},
        {"division": "Other", "category": "Contingency", "description": "Project contingency"},
        {"division": "Other", "category": "Overhead & Profit", "description": "Contractor's overhead and profit"}
    ]
    
    # Generate realistic budget data
    project_size = random.uniform(5_000_000, 50_000_000)  # Project size between $5M and $50M
    
    budget_data = []
    for category in budget_categories:
        # Set appropriate percentages for each division
        if category["division"] == "00-01":
            pct = random.uniform(0.05, 0.08)
        elif category["division"] == "02":
            pct = random.uniform(0.05, 0.1)
        elif category["division"] == "03":
            pct = random.uniform(0.08, 0.15)
        elif category["division"] == "04":
            pct = random.uniform(0.03, 0.06)
        elif category["division"] == "05":
            pct = random.uniform(0.08, 0.12)
        elif category["division"] == "06":
            pct = random.uniform(0.04, 0.07)
        elif category["division"] == "07":
            pct = random.uniform(0.05, 0.08)
        elif category["division"] == "08":
            pct = random.uniform(0.04, 0.06)
        elif category["division"] == "09":
            pct = random.uniform(0.07, 0.1)
        elif category["division"] == "10-14":
            pct = random.uniform(0.03, 0.05)
        elif category["division"] == "21-23":
            pct = random.uniform(0.1, 0.15)
        elif category["division"] == "26-28":
            pct = random.uniform(0.08, 0.12)
        elif category["division"] == "31-33":
            pct = random.uniform(0.04, 0.08)
        elif category["category"] == "General Conditions":
            pct = random.uniform(0.03, 0.05)
        elif category["category"] == "Contingency":
            pct = random.uniform(0.05, 0.07)
        elif category["category"] == "Overhead & Profit":
            pct = random.uniform(0.03, 0.06)
        else:
            pct = random.uniform(0.01, 0.03)
        
        # Calculate budget amount
        budget_amount = project_size * pct
        
        # Generate committed, actual, and forecast data
        committed_pct = random.uniform(0.7, 1.0)
        committed_amount = budget_amount * committed_pct
        
        actual_pct = random.uniform(0.5, 0.9)
        actual_amount = committed_amount * actual_pct
        
        forecast_variance_pct = random.uniform(-0.1, 0.15)  # -10% to +15% variance
        forecast_amount = budget_amount * (1 + forecast_variance_pct)
        
        variance_amount = budget_amount - forecast_amount
        variance_pct = variance_amount / budget_amount * 100
        
        budget_data.append({
            "division": category["division"],
            "category": category["category"],
            "description": category["description"],
            "budget": budget_amount,
            "committed": committed_amount,
            "actual": actual_amount,
            "forecast": forecast_amount,
            "variance": variance_amount,
            "variance_pct": variance_pct
        })
    
    # Calculate totals
    total_budget = sum(item["budget"] for item in budget_data)
    total_committed = sum(item["committed"] for item in budget_data)
    total_actual = sum(item["actual"] for item in budget_data)
    total_forecast = sum(item["forecast"] for item in budget_data)
    total_variance = total_budget - total_forecast
    total_variance_pct = total_variance / total_budget * 100 if total_budget > 0 else 0
    
    # Budget summary metrics
    st.subheader("Budget Summary")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Total Budget", f"${total_budget:,.0f}")
    
    with metrics_col2:
        st.metric("Total Committed", f"${total_committed:,.0f}")
    
    with metrics_col3:
        st.metric("Total Actual Cost", f"${total_actual:,.0f}")
    
    with metrics_col4:
        variance_color = "red" if total_variance < 0 else "green"
        st.metric(
            "Budget Variance", 
            f"${abs(total_variance):,.0f} ({abs(total_variance_pct):.1f}%)",
            delta=f"{'Under' if total_variance > 0 else 'Over'} Budget"
        )
    
    # Budget distribution chart
    st.subheader("Budget Distribution")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Create data for pie chart
        budget_pie_data = pd.DataFrame({
            "Category": [item["category"] for item in budget_data],
            "Budget": [item["budget"] for item in budget_data]
        })
        
        budget_pie_fig = px.pie(
            budget_pie_data,
            values="Budget",
            names="Category",
            title="Budget by Category",
            hole=0.4
        )
        
        st.plotly_chart(budget_pie_fig, use_container_width=True)
    
    with chart_col2:
        # Create data for bar chart comparing budget vs. forecast
        compare_df = pd.DataFrame({
            "Division": [f"{item['division']} - {item['category']}" for item in budget_data],
            "Budget": [item["budget"] for item in budget_data],
            "Forecast": [item["forecast"] for item in budget_data]
        })
        
        # Sort by budget amount descending
        compare_df = compare_df.sort_values("Budget", ascending=False)
        
        compare_fig = px.bar(
            compare_df,
            x="Division",
            y=["Budget", "Forecast"],
            title="Budget vs. Forecast by Division",
            barmode="group"
        )
        
        compare_fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(compare_fig, use_container_width=True)
    
    # Budget detail table
    st.subheader("Budget Detail")
    
    # Create a DataFrame for better display
    budget_df = pd.DataFrame(budget_data)
    
    # Format currency and percentage columns
    for col in ["budget", "committed", "actual", "forecast", "variance"]:
        budget_df[col + "_fmt"] = budget_df[col].apply(lambda x: f"${x:,.0f}")
    
    budget_df["variance_pct_fmt"] = budget_df["variance_pct"].apply(lambda x: f"{x:.1f}%")
    budget_df["committed_pct"] = budget_df["committed"] / budget_df["budget"] * 100
    budget_df["committed_pct_fmt"] = budget_df["committed_pct"].apply(lambda x: f"{x:.1f}%")
    
    # Select and rename columns for display
    display_cols = [
        "division", "category", "description", 
        "budget_fmt", "committed_fmt", "committed_pct_fmt", 
        "actual_fmt", "forecast_fmt", "variance_fmt", "variance_pct_fmt"
    ]
    
    display_df = budget_df[display_cols].rename(columns={
        "division": "Division",
        "category": "Category",
        "description": "Description",
        "budget_fmt": "Budget",
        "committed_fmt": "Committed",
        "committed_pct_fmt": "Committed %",
        "actual_fmt": "Actual",
        "forecast_fmt": "Forecast",
        "variance_fmt": "Variance",
        "variance_pct_fmt": "Variance %"
    })
    
    # Add totals row
    totals_row = pd.DataFrame({
        "Division": ["TOTAL"],
        "Category": [""],
        "Description": [""],
        "Budget": [f"${total_budget:,.0f}"],
        "Committed": [f"${total_committed:,.0f}"],
        "Committed %": [f"{total_committed / total_budget * 100:.1f}%" if total_budget > 0 else "0.0%"],
        "Actual": [f"${total_actual:,.0f}"],
        "Forecast": [f"${total_forecast:,.0f}"],
        "Variance": [f"${total_variance:,.0f}"],
        "Variance %": [f"{total_variance_pct:.1f}%"]
    })
    
    display_df = pd.concat([display_df, totals_row], ignore_index=True)
    
    # Apply conditional formatting
    def highlight_variance(val):
        if "%" not in str(val):
            return ""
        
        try:
            v = float(val.strip("%"))
            if v < -5:
                return "background-color: rgba(255, 0, 0, 0.2)"
            elif v > 5:
                return "background-color: rgba(0, 255, 0, 0.2)"
            else:
                return ""
        except:
            return ""
    
    # Display the table with formatting
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Budget actions
    st.divider()
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        st.button("Edit Budget", key="edit_budget_btn")
    
    with action_col2:
        st.button("Export to Excel", key="export_budget_btn")
    
    with action_col3:
        st.button("Print Budget Report", key="print_budget_btn")

def render_cost_tracking():
    """Render the cost tracking section"""
    
    st.header("Cost Tracking")
    
    # Create sample data for cost items
    cost_types = ["Labor", "Materials", "Equipment", "Subcontractors", "Other"]
    divisions = ["00-01", "02", "03", "04", "05", "06", "07", "08", "09", "10-14", "21-23", "26-28", "31-33"]
    categories = ["General Requirements", "Site Work", "Concrete", "Masonry", "Metals", 
                 "Wood & Plastics", "Thermal & Moisture", "Doors & Windows", "Finishes", 
                 "Specialties", "Mechanical", "Electrical", "Site & Infrastructure", 
                 "General Conditions", "Contingency", "Overhead & Profit"]
    
    cost_items = []
    for i in range(1, 101):
        # Generate a cost item with realistic attributes
        cost_type = random.choice(cost_types)
        division = random.choice(divisions)
        category = random.choice(categories)
        
        # Dates and amounts
        transaction_date = datetime.now() - timedelta(days=random.randint(1, 180))
        
        # Different amount ranges based on cost type
        if cost_type == "Labor":
            amount = random.uniform(1000, 10000)
        elif cost_type == "Materials":
            amount = random.uniform(5000, 50000)
        elif cost_type == "Equipment":
            amount = random.uniform(2000, 20000)
        elif cost_type == "Subcontractors":
            amount = random.uniform(10000, 100000)
        else:
            amount = random.uniform(500, 5000)
        
        # Create the cost item
        cost_items.append({
            "id": f"COST-{2025}-{i:03d}",
            "description": f"{cost_type} - {category} - Item {i}",
            "type": cost_type,
            "division": division,
            "category": category,
            "transaction_date": transaction_date,
            "amount": amount,
            "status": random.choice(["Pending", "Approved", "Paid"]),
            "po_number": f"PO-{2025}-{random.randint(1000, 9999)}" if random.random() > 0.3 else None,
            "invoice_number": f"INV-{random.randint(10000, 99999)}" if random.random() > 0.4 else None,
            "vendor": random.choice([
                "Reliable Construction Inc.", "Elite Electrical Services", "Supreme Plumbing Co.", 
                "Advanced HVAC Systems", "Quality Roofing Ltd.", "Green Landscaping", 
                "Structural Masters", "Concrete Solutions", "Premium Finishes", "Global Services"
            ]),
            "notes": random.choice([
                "Regular monthly billing",
                "Phase 1 completion",
                "Materials for east wing",
                "Equipment rental",
                "Change order work",
                "Overtime hours",
                "Additional scope",
                "Repair work",
                None
            ])
        })
    
    # Filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        date_range = st.selectbox(
            "Date Range",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "All Time"],
            key="cost_date_range"
        )
    
    with filter_col2:
        cost_type_filter = st.multiselect(
            "Cost Type",
            cost_types,
            default=cost_types,
            key="cost_type_filter"
        )
    
    with filter_col3:
        category_filter = st.multiselect(
            "Category",
            categories,
            default=[],
            key="cost_category_filter"
        )
    
    with filter_col4:
        status_filter = st.multiselect(
            "Status",
            ["Pending", "Approved", "Paid"],
            default=["Pending", "Approved", "Paid"],
            key="cost_status_filter"
        )
    
    # Apply filters
    filtered_costs = [cost for cost in cost_items if cost["type"] in cost_type_filter and cost["status"] in status_filter]
    
    # Apply date filter
    today = datetime.now()
    if date_range == "Last 30 Days":
        filtered_costs = [cost for cost in filtered_costs if (today - cost["transaction_date"]).days <= 30]
    elif date_range == "Last 90 Days":
        filtered_costs = [cost for cost in filtered_costs if (today - cost["transaction_date"]).days <= 90]
    elif date_range == "Last 6 Months":
        filtered_costs = [cost for cost in filtered_costs if (today - cost["transaction_date"]).days <= 180]
    
    # Apply category filter if selected
    if category_filter:
        filtered_costs = [cost for cost in filtered_costs if cost["category"] in category_filter]
    
    # Cost metrics
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        total_costs = sum(cost["amount"] for cost in filtered_costs)
        st.metric("Total Costs", f"${total_costs:,.2f}")
    
    with metrics_col2:
        paid_costs = sum(cost["amount"] for cost in filtered_costs if cost["status"] == "Paid")
        st.metric("Paid", f"${paid_costs:,.2f}")
    
    with metrics_col3:
        pending_costs = sum(cost["amount"] for cost in filtered_costs if cost["status"] in ["Pending", "Approved"])
        st.metric("Pending", f"${pending_costs:,.2f}")
    
    # Cost analysis charts
    st.subheader("Cost Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Cost distribution by type
        cost_by_type = {}
        for cost in filtered_costs:
            cost_type = cost["type"]
            if cost_type not in cost_by_type:
                cost_by_type[cost_type] = 0
            cost_by_type[cost_type] += cost["amount"]
        
        type_df = pd.DataFrame({
            "Type": list(cost_by_type.keys()),
            "Amount": list(cost_by_type.values())
        })
        
        type_fig = px.pie(
            type_df,
            values="Amount",
            names="Type",
            title="Cost Distribution by Type",
            hole=0.4
        )
        
        st.plotly_chart(type_fig, use_container_width=True)
    
    with chart_col2:
        # Cost trend over time
        # Group costs by month
        cost_by_month = {}
        for cost in filtered_costs:
            month = cost["transaction_date"].strftime("%Y-%m")
            if month not in cost_by_month:
                cost_by_month[month] = 0
            cost_by_month[month] += cost["amount"]
        
        # Sort months
        sorted_months = sorted(cost_by_month.keys())
        
        trend_df = pd.DataFrame({
            "Month": sorted_months,
            "Amount": [cost_by_month[month] for month in sorted_months]
        })
        
        trend_fig = px.line(
            trend_df,
            x="Month",
            y="Amount",
            title="Cost Trend by Month",
            markers=True
        )
        
        trend_fig.update_layout(yaxis_title="Cost Amount ($)")
        
        st.plotly_chart(trend_fig, use_container_width=True)
    
    # Cost breakdown by category
    st.subheader("Cost Breakdown")
    
    # Group costs by category
    cost_by_category = {}
    for cost in filtered_costs:
        category = cost["category"]
        if category not in cost_by_category:
            cost_by_category[category] = 0
        cost_by_category[category] += cost["amount"]
    
    # Create DataFrame and sort by amount
    category_df = pd.DataFrame({
        "Category": list(cost_by_category.keys()),
        "Amount": list(cost_by_category.values())
    })
    
    category_df = category_df.sort_values("Amount", ascending=False)
    
    # Create bar chart
    category_fig = px.bar(
        category_df,
        x="Category",
        y="Amount",
        title="Costs by Category",
        color="Amount",
        color_continuous_scale="Viridis"
    )
    
    category_fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Cost Amount ($)"
    )
    
    st.plotly_chart(category_fig, use_container_width=True)
    
    # Cost items table
    st.subheader("Cost Items")
    
    # Sort by transaction date (newest first)
    filtered_costs.sort(key=lambda x: x["transaction_date"], reverse=True)
    
    # Create a DataFrame for display
    costs_df = pd.DataFrame(filtered_costs)
    
    # Format columns
    costs_df["transaction_date_fmt"] = costs_df["transaction_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    costs_df["amount_fmt"] = costs_df["amount"].apply(lambda x: f"${x:,.2f}")
    
    # Select and rename columns for display
    display_cols = [
        "id", "transaction_date_fmt", "description", "type", "category", 
        "amount_fmt", "status", "vendor", "po_number", "invoice_number"
    ]
    
    display_df = costs_df[display_cols].rename(columns={
        "id": "ID",
        "transaction_date_fmt": "Date",
        "description": "Description",
        "type": "Type",
        "category": "Category",
        "amount_fmt": "Amount",
        "status": "Status",
        "vendor": "Vendor",
        "po_number": "PO #",
        "invoice_number": "Invoice #"
    })
    
    # Display the table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Cost entry form toggle
    st.divider()
    if st.button("Add Cost Item", type="primary", key="add_cost_btn"):
        st.session_state.show_cost_form = True
    
    # Cost entry form
    if st.session_state.get("show_cost_form", False):
        with st.form("cost_form"):
            st.subheader("Add Cost Item")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                cost_description = st.text_input("Description", key="cost_description")
                cost_type = st.selectbox("Cost Type", cost_types, key="cost_type")
                cost_category = st.selectbox("Category", categories, key="cost_category")
                cost_date = st.date_input("Transaction Date", datetime.now(), key="cost_date")
            
            with form_col2:
                cost_amount = st.number_input("Amount ($)", min_value=0.0, value=0.0, step=100.0, key="cost_amount")
                cost_status = st.selectbox("Status", ["Pending", "Approved", "Paid"], key="cost_status")
                cost_vendor = st.text_input("Vendor", key="cost_vendor")
                cost_po = st.text_input("PO Number (optional)", key="cost_po")
                cost_invoice = st.text_input("Invoice Number (optional)", key="cost_invoice")
            
            cost_notes = st.text_area("Notes (optional)", key="cost_notes")
            
            submitted = st.form_submit_button("Save Cost Item")
            
            if submitted:
                st.success("Cost item added successfully!")
                st.session_state.show_cost_form = False
                st.rerun()

def render_forecasting():
    """Render the cost forecasting section"""
    
    st.header("Cost Forecasting")
    
    # Sample data for project
    project_start_date = datetime(2024, 1, 1)
    project_end_date = datetime(2025, 12, 31)
    total_duration_months = (project_end_date.year - project_start_date.year) * 12 + (project_end_date.month - project_start_date.month)
    current_month = min((datetime.now().year - project_start_date.year) * 12 + (datetime.now().month - project_start_date.month), total_duration_months)
    
    total_budget = random.uniform(5_000_000, 50_000_000)  # Project size between $5M and $50M
    
    # Create monthly budget/actual/forecast data
    monthly_data = []
    cumulative_budget = 0
    cumulative_actual = 0
    cumulative_forecast = 0
    
    for i in range(total_duration_months + 1):
        month_date = project_start_date + pd.DateOffset(months=i)
        
        # S-curve distribution for budget
        # Higher spending in the middle months, lower at start and end
        if i == 0:
            month_budget_pct = 0.01
        else:
            progress = i / total_duration_months
            # S-curve formula (approximation)
            month_budget_pct = 6 * (progress * (1 - progress))
            # Adjust to ensure it sums to 100%
            month_budget_pct = month_budget_pct / 0.96
        
        month_budget = total_budget * month_budget_pct
        cumulative_budget += month_budget
        
        # Actual costs (only for past and current months)
        if i <= current_month:
            # Randomize actual vs budget (random variance)
            actual_variance = random.uniform(-0.1, 0.2)  # -10% to +20% variance
            month_actual = month_budget * (1 + actual_variance)
            cumulative_actual += month_actual
        else:
            month_actual = 0
        
        # Forecast costs
        if i < current_month:
            # Past months, forecast equals actual
            month_forecast = month_actual
        else:
            # Current and future months
            forecast_variance = random.uniform(-0.05, 0.15)  # -5% to +15% variance
            month_forecast = month_budget * (1 + forecast_variance)
        
        cumulative_forecast += month_forecast if i >= current_month else month_actual
        
        # Add to monthly data
        monthly_data.append({
            "month": month_date,
            "month_name": month_date.strftime("%b %Y"),
            "month_budget": month_budget,
            "month_actual": month_actual,
            "month_forecast": month_forecast,
            "cumulative_budget": cumulative_budget,
            "cumulative_actual": cumulative_actual if i <= current_month else None,
            "cumulative_forecast": cumulative_forecast
        })
    
    # Projected final cost
    final_forecast = monthly_data[-1]["cumulative_forecast"]
    budget_variance = total_budget - final_forecast
    variance_pct = (budget_variance / total_budget) * 100
    
    # Forecast metrics
    st.subheader("Cost Forecast Summary")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Total Budget", f"${total_budget:,.0f}")
    
    with metrics_col2:
        st.metric("Actual Cost to Date", f"${cumulative_actual:,.0f}")
    
    with metrics_col3:
        st.metric("Projected Final Cost", f"${final_forecast:,.0f}")
    
    with metrics_col4:
        variance_color = "green" if budget_variance > 0 else "red"
        variance_label = "Under Budget" if budget_variance > 0 else "Over Budget"
        st.metric(
            "Budget Variance", 
            f"${abs(budget_variance):,.0f} ({abs(variance_pct):.1f}%)",
            delta=variance_label
        )
    
    # Cost S-Curve
    st.subheader("Cost S-Curve")
    
    # Create DataFrame for charts
    df = pd.DataFrame(monthly_data)
    
    # Create S-curve chart
    fig = go.Figure()
    
    # Add budget line
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["cumulative_budget"],
        mode='lines',
        name='Budget',
        line=dict(color='blue', width=2)
    ))
    
    # Add actual cost line (only for past months)
    actual_df = df[df["cumulative_actual"].notnull()]
    fig.add_trace(go.Scatter(
        x=actual_df["month"],
        y=actual_df["cumulative_actual"],
        mode='lines+markers',
        name='Actual',
        line=dict(color='green', width=2)
    ))
    
    # Add forecast line
    forecast_df = df[df["month"] >= df.loc[current_month, "month"]]
    fig.add_trace(go.Scatter(
        x=forecast_df["month"],
        y=forecast_df["cumulative_forecast"],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Add vertical line for current date
    if current_month < total_duration_months:
        # Convert timestamp to string to avoid arithmetic issues
        current_date_str = df.loc[current_month, "month"].strftime('%Y-%m-%d')
        fig.add_vline(
            x=current_date_str,
            line_dash="dash",
            line_color="gray",
            annotation_text="Current Date",
            annotation_position="top right"
        )
    
    fig.update_layout(
        title="Project Cost S-Curve",
        xaxis_title="Date",
        yaxis_title="Cumulative Cost ($)",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix="$", tickformat=",")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Cost Breakdown
    st.subheader("Monthly Cost Breakdown")
    
    # Create monthly bar chart
    monthly_fig = go.Figure()
    
    # Add budget bars
    monthly_fig.add_trace(go.Bar(
        x=df["month_name"],
        y=df["month_budget"],
        name='Budget',
        marker_color='blue'
    ))
    
    # Add actual bars (only for past months)
    actual_months = df[df["month_actual"] > 0]["month_name"].tolist()
    actual_values = df[df["month_actual"] > 0]["month_actual"].tolist()
    
    monthly_fig.add_trace(go.Bar(
        x=actual_months,
        y=actual_values,
        name='Actual',
        marker_color='green'
    ))
    
    # Add forecast bars (for future months)
    forecast_months = df[df["month"] >= df.loc[current_month, "month"]]["month_name"].tolist()
    forecast_values = df[df["month"] >= df.loc[current_month, "month"]]["month_forecast"].tolist()
    
    monthly_fig.add_trace(go.Bar(
        x=forecast_months,
        y=forecast_values,
        name='Forecast',
        marker_color='red'
    ))
    
    monthly_fig.update_layout(
        title="Monthly Cost Distribution",
        xaxis_title="Month",
        yaxis_title="Monthly Cost ($)",
        barmode='group',
        xaxis=dict(tickangle=-45),
        legend=dict(x=0.01, y=0.99)
    )
    
    # Format y-axis as currency
    monthly_fig.update_yaxes(tickprefix="$", tickformat=",")
    
    st.plotly_chart(monthly_fig, use_container_width=True)
    
    # Cost Performance Indices
    st.subheader("Cost Performance Analysis")
    
    # Calculate Earned Value metrics
    if current_month > 0:
        # Calculate percent complete (based on budget)
        percent_complete = cumulative_actual / total_budget * 100
        
        # Planned Value (PV) - what should have been accomplished
        planned_value = monthly_data[current_month]["cumulative_budget"]
        
        # Actual Cost (AC)
        actual_cost = cumulative_actual
        
        # Earned Value (EV) - value of work completed
        earned_value = total_budget * (percent_complete / 100)
        
        # Cost Performance Index (CPI)
        cpi = earned_value / actual_cost if actual_cost > 0 else 1.0
        
        # Schedule Performance Index (SPI)
        spi = earned_value / planned_value if planned_value > 0 else 1.0
        
        # Estimate at Completion (EAC)
        eac = total_budget / cpi
        
        # Variance at Completion (VAC)
        vac = total_budget - eac
        
        # To Complete Performance Index (TCPI)
        budget_remaining = total_budget - earned_value
        cost_remaining = total_budget - actual_cost
        tcpi = budget_remaining / cost_remaining if cost_remaining > 0 else 1.0
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            cpi_color = "green" if cpi >= 1.0 else "red"
            st.markdown(f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <h4>Cost Performance Index (CPI)</h4>
                    <p style="font-size:24px; font-weight:bold; color:{cpi_color};">{cpi:.2f}</p>
                    <p>CPI > 1.0: Under budget</p>
                    <p>CPI < 1.0: Over budget</p>
                </div>
            """, unsafe_allow_html=True)
        
        with metrics_col2:
            spi_color = "green" if spi >= 1.0 else "red"
            st.markdown(f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <h4>Schedule Performance Index (SPI)</h4>
                    <p style="font-size:24px; font-weight:bold; color:{spi_color};">{spi:.2f}</p>
                    <p>SPI > 1.0: Ahead of schedule</p>
                    <p>SPI < 1.0: Behind schedule</p>
                </div>
            """, unsafe_allow_html=True)
        
        with metrics_col3:
            tcpi_color = "green" if tcpi <= 1.0 else "red"
            st.markdown(f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <h4>To Complete Performance Index (TCPI)</h4>
                    <p style="font-size:24px; font-weight:bold; color:{tcpi_color};">{tcpi:.2f}</p>
                    <p>TCPI < 1.0: Easy to complete within budget</p>
                    <p>TCPI > 1.0: Difficult to complete within budget</p>
                </div>
            """, unsafe_allow_html=True)
        
        # EAC and VAC
        eac_col1, eac_col2 = st.columns(2)
        
        with eac_col1:
            st.metric("Estimate at Completion (EAC)", f"${eac:,.0f}")
        
        with eac_col2:
            vac_color = "green" if vac > 0 else "red"
            vac_label = "Under Budget" if vac > 0 else "Over Budget"
            st.metric("Variance at Completion (VAC)", f"${abs(vac):,.0f}", delta=vac_label)
    
    else:
        st.info("Cost performance metrics will be available once the project starts tracking actual costs.")
    
    # Forecast scenarios
    st.subheader("Forecast Scenarios")
    
    # Create scenario options
    scenario_options = {
        "Current Forecast": 0.0,
        "Optimistic (10% saving)": -0.1,
        "Pessimistic (10% overrun)": 0.1,
        "Worst Case (20% overrun)": 0.2
    }
    
    scenario_col1, scenario_col2 = st.columns(2)
    
    with scenario_col1:
        selected_scenarios = st.multiselect(
            "Select Scenarios to Compare",
            list(scenario_options.keys()),
            default=["Current Forecast", "Optimistic (10% saving)", "Pessimistic (10% overrun)"],
            key="forecast_scenarios"
        )
    
    with scenario_col2:
        custom_scenario = st.slider(
            "Custom Scenario (% change)",
            min_value=-20,
            max_value=30,
            value=0,
            step=5,
            key="custom_scenario"
        )
        
        if custom_scenario != 0:
            scenario_options["Custom Scenario"] = custom_scenario / 100
            if "Custom Scenario" not in selected_scenarios:
                selected_scenarios.append("Custom Scenario")
    
    # Create scenario forecast lines
    scenario_fig = go.Figure()
    
    # Add budget line
    scenario_fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["cumulative_budget"],
        mode='lines',
        name='Budget',
        line=dict(color='blue', width=2)
    ))
    
    # Add actual cost line (only for past months)
    scenario_fig.add_trace(go.Scatter(
        x=actual_df["month"],
        y=actual_df["cumulative_actual"],
        mode='lines+markers',
        name='Actual',
        line=dict(color='green', width=2)
    ))
    
    # Add selected scenario lines
    colors = ['red', 'orange', 'purple', 'brown', 'pink']
    
    for i, scenario in enumerate(selected_scenarios):
        if scenario in scenario_options:
            adjustment = scenario_options[scenario]
            
            # Calculate adjusted forecast
            adjusted_forecast = []
            for j, row in forecast_df.iterrows():
                base_forecast = row["cumulative_forecast"]
                adjusted_value = base_forecast * (1 + adjustment)
                adjusted_forecast.append(adjusted_value)
            
            scenario_fig.add_trace(go.Scatter(
                x=forecast_df["month"],
                y=adjusted_forecast,
                mode='lines',
                name=scenario,
                line=dict(color=colors[i % len(colors)], width=2, dash='dash')
            ))
    
    # Add vertical line for current date
    if current_month < total_duration_months:
        # Get current date from the dataframe 
        current_date_str = df.loc[current_month, "month"].strftime('%Y-%m-%d')
        scenario_fig.add_vline(
            x=current_date_str,
            line_dash="dash",
            line_color="gray",
            annotation_text="Current Date",
            annotation_position="top right"
        )
    
    scenario_fig.update_layout(
        title="Forecast Scenarios Comparison",
        xaxis_title="Date",
        yaxis_title="Cumulative Cost ($)",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )
    
    # Format y-axis as currency
    scenario_fig.update_yaxes(tickprefix="$", tickformat=",")
    
    st.plotly_chart(scenario_fig, use_container_width=True)
    
    # Scenario outcomes table
    st.subheader("Scenario Outcomes")
    
    scenario_outcomes = []
    for scenario in scenario_options.keys():
        adjustment = scenario_options[scenario]
        final_cost = final_forecast * (1 + adjustment)
        budget_variance = total_budget - final_cost
        variance_pct = (budget_variance / total_budget) * 100
        
        scenario_outcomes.append({
            "Scenario": scenario,
            "Final Cost": final_cost,
            "Variance": budget_variance,
            "Variance %": variance_pct
        })
    
    outcome_df = pd.DataFrame(scenario_outcomes)
    
    # Format columns
    outcome_df["Final Cost Fmt"] = outcome_df["Final Cost"].apply(lambda x: f"${x:,.0f}")
    outcome_df["Variance Fmt"] = outcome_df["Variance"].apply(lambda x: f"${x:,.0f}")
    outcome_df["Variance % Fmt"] = outcome_df["Variance %"].apply(lambda x: f"{x:.1f}%")
    outcome_df["Status"] = outcome_df["Variance"].apply(lambda x: "Under Budget" if x > 0 else "Over Budget")
    
    # Display columns
    display_cols = ["Scenario", "Final Cost Fmt", "Variance Fmt", "Variance % Fmt", "Status"]
    display_outcome_df = outcome_df[display_cols].rename(columns={
        "Final Cost Fmt": "Final Cost",
        "Variance Fmt": "Variance",
        "Variance % Fmt": "Variance %"
    })
    
    st.dataframe(
        display_outcome_df,
        use_container_width=True,
        hide_index=True
    )

def render_cost_reports():
    """Render the cost reports section"""
    
    st.header("Cost Reports")
    
    # Report types selection
    report_types = [
        "Budget vs. Actual Summary",
        "Cost Breakdown by Division",
        "Cost Breakdown by Category",
        "Monthly Cost Report",
        "Cash Flow Projection",
        "Contract Summary",
        "Change Order Summary",
        "Cost Forecast Report",
        "Cost Performance Indices",
        "Vendor Payment Summary"
    ]
    
    report_type = st.selectbox(
        "Select Report Type",
        report_types,
        key="cost_report_type"
    )
    
    # Date range for report
    date_col1, date_col2 = st.columns(2)
    
    with date_col1:
        start_date = st.date_input("From Date", datetime.now() - timedelta(days=90), key="report_start_date")
    
    with date_col2:
        end_date = st.date_input("To Date", datetime.now(), key="report_end_date")
    
    # Generate sample report based on selection
    st.subheader(report_type)
    
    if report_type == "Budget vs. Actual Summary":
        # Create a sample budget vs. actual summary
        categories = [
            "General Requirements", "Site Work", "Concrete", "Masonry", "Metals", 
            "Wood & Plastics", "Thermal & Moisture", "Doors & Windows", "Finishes", 
            "Specialties", "Mechanical", "Electrical", "Site & Infrastructure", 
            "General Conditions", "Contingency", "Overhead & Profit"
        ]
        
        report_data = []
        total_budget = 0
        total_committed = 0
        total_actual = 0
        total_remaining = 0
        
        for category in categories:
            budget = random.uniform(100000, 1000000)
            committed_pct = random.uniform(0.7, 1.0)
            committed = budget * committed_pct
            actual_pct = random.uniform(0.5, 0.9) if committed_pct > 0.5 else random.uniform(0, 0.5)
            actual = committed * actual_pct
            remaining = budget - actual
            
            report_data.append({
                "Category": category,
                "Budget": budget,
                "Committed": committed,
                "Actual": actual,
                "Remaining": remaining,
                "Percent Complete": (actual / budget * 100) if budget > 0 else 0
            })
            
            total_budget += budget
            total_committed += committed
            total_actual += actual
            total_remaining += remaining
        
        # Add total row
        report_data.append({
            "Category": "TOTAL",
            "Budget": total_budget,
            "Committed": total_committed,
            "Actual": total_actual,
            "Remaining": total_remaining,
            "Percent Complete": (total_actual / total_budget * 100) if total_budget > 0 else 0
        })
        
        # Create DataFrame
        report_df = pd.DataFrame(report_data)
        
        # Format columns
        for col in ["Budget", "Committed", "Actual", "Remaining"]:
            report_df[col + "_fmt"] = report_df[col].apply(lambda x: f"${x:,.0f}")
        
        report_df["Percent Complete_fmt"] = report_df["Percent Complete"].apply(lambda x: f"{x:.1f}%")
        
        # Display columns
        display_cols = ["Category", "Budget_fmt", "Committed_fmt", "Actual_fmt", "Remaining_fmt", "Percent Complete_fmt"]
        display_report_df = report_df[display_cols].rename(columns={
            "Budget_fmt": "Budget",
            "Committed_fmt": "Committed",
            "Actual_fmt": "Actual",
            "Remaining_fmt": "Remaining",
            "Percent Complete_fmt": "Percent Complete"
        })
        
        st.dataframe(
            display_report_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Create a chart
        fig = px.bar(
            report_df[:-1],  # Exclude the total row
            x="Category",
            y=["Budget", "Committed", "Actual"],
            title="Budget vs. Committed vs. Actual by Category",
            barmode="group"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Amount ($)",
            legend_title="Cost Type"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Cost Breakdown by Division":
        # Create a sample cost breakdown by division
        divisions = [
            "00-01 - General Requirements",
            "02 - Site Work",
            "03 - Concrete",
            "04 - Masonry",
            "05 - Metals",
            "06 - Wood & Plastics",
            "07 - Thermal & Moisture",
            "08 - Doors & Windows",
            "09 - Finishes",
            "10-14 - Specialties",
            "21-23 - Mechanical",
            "26-28 - Electrical",
            "31-33 - Site & Infrastructure"
        ]
        
        report_data = []
        total_budget = 0
        total_actual = 0
        total_variance = 0
        
        for division in divisions:
            budget = random.uniform(100000, 2000000)
            actual = budget * random.uniform(0.8, 1.2)  # -20% to +20% variance
            variance = budget - actual
            variance_pct = (variance / budget * 100) if budget > 0 else 0
            
            report_data.append({
                "Division": division,
                "Budget": budget,
                "Actual": actual,
                "Variance": variance,
                "Variance %": variance_pct
            })
            
            total_budget += budget
            total_actual += actual
            total_variance += variance
        
        # Add total row
        total_variance_pct = (total_variance / total_budget * 100) if total_budget > 0 else 0
        report_data.append({
            "Division": "TOTAL",
            "Budget": total_budget,
            "Actual": total_actual,
            "Variance": total_variance,
            "Variance %": total_variance_pct
        })
        
        # Create DataFrame
        report_df = pd.DataFrame(report_data)
        
        # Format columns
        for col in ["Budget", "Actual", "Variance"]:
            report_df[col + "_fmt"] = report_df[col].apply(lambda x: f"${x:,.0f}")
        
        report_df["Variance %_fmt"] = report_df["Variance %"].apply(lambda x: f"{x:.1f}%")
        
        # Display columns
        display_cols = ["Division", "Budget_fmt", "Actual_fmt", "Variance_fmt", "Variance %_fmt"]
        display_report_df = report_df[display_cols].rename(columns={
            "Budget_fmt": "Budget",
            "Actual_fmt": "Actual",
            "Variance_fmt": "Variance",
            "Variance %_fmt": "Variance %"
        })
        
        st.dataframe(
            display_report_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Create a chart
        fig = px.bar(
            report_df[:-1],  # Exclude the total row
            x="Division",
            y=["Budget", "Actual"],
            title="Budget vs. Actual by Division",
            barmode="group"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Amount ($)",
            legend_title="Cost Type"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Monthly Cost Report":
        # Create a sample monthly cost report
        months = pd.date_range(start=start_date, end=end_date, freq='MS')
        month_names = [month.strftime("%b %Y") for month in months]
        
        # Categories for cost breakdown
        categories = ["Labor", "Materials", "Equipment", "Subcontractors", "Other"]
        
        # Generate monthly cost data
        monthly_costs = {}
        monthly_totals = {month: 0 for month in month_names}
        
        for category in categories:
            category_costs = []
            for month in month_names:
                cost = random.uniform(10000, 100000)
                category_costs.append(cost)
                monthly_totals[month] += cost
            
            monthly_costs[category] = category_costs
        
        # Create DataFrame for display
        report_data = []
        for i, category in enumerate(categories):
            row_data = {"Category": category}
            for j, month in enumerate(month_names):
                row_data[month] = monthly_costs[category][j]
            report_data.append(row_data)
        
        # Add total row
        total_row = {"Category": "TOTAL"}
        for month in month_names:
            total_row[month] = monthly_totals[month]
        report_data.append(total_row)
        
        report_df = pd.DataFrame(report_data)
        
        # Format columns
        for month in month_names:
            report_df[month + "_fmt"] = report_df[month].apply(lambda x: f"${x:,.0f}")
        
        # Display columns
        display_cols = ["Category"] + [month + "_fmt" for month in month_names]
        display_report_df = report_df[display_cols].rename(columns={
            month + "_fmt": month for month in month_names
        })
        
        st.dataframe(
            display_report_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Create a stacked bar chart
        chart_data = []
        for category in categories:
            for i, month in enumerate(month_names):
                chart_data.append({
                    "Month": month,
                    "Category": category,
                    "Cost": monthly_costs[category][i]
                })
        
        chart_df = pd.DataFrame(chart_data)
        
        fig = px.bar(
            chart_df,
            x="Month",
            y="Cost",
            color="Category",
            title="Monthly Cost Breakdown by Category",
            barmode="stack"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Cost ($)",
            legend_title="Cost Category"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Cash Flow Projection":
        # Create a sample cash flow projection
        months = pd.date_range(start=datetime.now(), periods=12, freq='MS')
        month_names = [month.strftime("%b %Y") for month in months]
        
        # Generate cash flow data
        inflows = [random.uniform(100000, 500000) for _ in range(12)]
        outflows = [random.uniform(100000, 400000) for _ in range(12)]
        
        # Calculate cumulative cash flow
        net_cash_flow = [inflows[i] - outflows[i] for i in range(12)]
        cumulative_cash_flow = []
        running_total = 0
        for flow in net_cash_flow:
            running_total += flow
            cumulative_cash_flow.append(running_total)
        
        # Create DataFrame for display
        report_data = []
        for i, month in enumerate(month_names):
            report_data.append({
                "Month": month,
                "Cash Inflows": inflows[i],
                "Cash Outflows": outflows[i],
                "Net Cash Flow": net_cash_flow[i],
                "Cumulative Cash Flow": cumulative_cash_flow[i]
            })
        
        report_df = pd.DataFrame(report_data)
        
        # Format columns
        for col in ["Cash Inflows", "Cash Outflows", "Net Cash Flow", "Cumulative Cash Flow"]:
            report_df[col + "_fmt"] = report_df[col].apply(lambda x: f"${x:,.0f}")
        
        # Display columns
        display_cols = ["Month", "Cash Inflows_fmt", "Cash Outflows_fmt", "Net Cash Flow_fmt", "Cumulative Cash Flow_fmt"]
        display_report_df = report_df[display_cols].rename(columns={
            "Cash Inflows_fmt": "Cash Inflows",
            "Cash Outflows_fmt": "Cash Outflows",
            "Net Cash Flow_fmt": "Net Cash Flow",
            "Cumulative Cash Flow_fmt": "Cumulative Cash Flow"
        })
        
        st.dataframe(
            display_report_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Create a cash flow chart
        fig = go.Figure()
        
        # Add bar chart for inflows and outflows
        fig.add_trace(go.Bar(
            x=month_names,
            y=inflows,
            name='Cash Inflows',
            marker_color='green'
        ))
        
        fig.add_trace(go.Bar(
            x=month_names,
            y=[-outflow for outflow in outflows],  # Negative values for outflows
            name='Cash Outflows',
            marker_color='red'
        ))
        
        # Add line for cumulative cash flow
        fig.add_trace(go.Scatter(
            x=month_names,
            y=cumulative_cash_flow,
            name='Cumulative Cash Flow',
            line=dict(color='blue', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Cash Flow Projection",
            xaxis_tickangle=-45,
            yaxis=dict(
                title="Monthly Cash Flow ($)",
                showgrid=False
            ),
            yaxis2=dict(
                title="Cumulative Cash Flow ($)",
                overlaying='y',
                side='right',
                showgrid=False
            ),
            barmode='relative',
            legend=dict(x=0.01, y=0.99)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add report export options
    st.divider()
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        st.download_button(
            label="Export to Excel",
            data="Sample Excel Export",
            file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel",
            key="export_excel_btn"
        )
    
    with export_col2:
        st.download_button(
            label="Export to PDF",
            data="Sample PDF Export",
            file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            key="export_pdf_btn"
        )
    
    with export_col3:
        st.button("Print Report", key="print_report_btn")