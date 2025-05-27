"""
Highland Tower Development - Cost Management UI
Enterprise frontend interface for cost tracking and budget management.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from typing import Dict, Any

# Import the backend
from modules.cost_management_backend import (
    cost_manager,
    CostCategory,
    BudgetStatus,
    CostItemStatus,
    CostItem,
    BudgetCategory
)

def render_cost_management_enterprise():
    """Render the enterprise cost management interface"""
    
    st.markdown("""
    <div class="module-header">
        <h1>💰 Cost Management</h1>
        <p>Highland Tower Development - Enterprise budget tracking and financial analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display project totals
    render_project_summary()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Budget Overview",
        "💳 Cost Items", 
        "📈 Analytics",
        "🔄 Change Orders",
        "💹 Cash Flow"
    ])
    
    with tab1:
        render_budget_overview()
    
    with tab2:
        render_cost_items_management()
    
    with tab3:
        render_financial_analytics()
    
    with tab4:
        render_change_orders()
    
    with tab5:
        render_cash_flow_analysis()

def render_project_summary():
    """Display high-level project financial summary"""
    totals = cost_manager.calculate_project_totals()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Budget",
            value=f"${totals['total_budget']:,.0f}",
            delta=f"${totals['total_change_orders']:,.0f} in COs"
        )
    
    with col2:
        st.metric(
            label="💸 Actual Spent",
            value=f"${totals['total_actual']:,.0f}",
            delta=f"{totals['variance_percentage']:.1f}% variance"
        )
    
    with col3:
        st.metric(
            label="📋 Committed",
            value=f"${totals['total_committed']:,.0f}",
            delta="Under contract"
        )
    
    with col4:
        st.metric(
            label="💵 Remaining",
            value=f"${totals['total_remaining']:,.0f}",
            delta=f"{(totals['total_remaining']/totals['total_budget']*100):.1f}% of budget"
        )

def render_budget_overview():
    """Display budget category performance"""
    st.subheader("📊 Budget Categories Performance")
    
    # Get category performance data
    performance_data = cost_manager.get_category_performance()
    
    if not performance_data:
        st.info("No budget data available.")
        return
    
    # Create performance dataframe with proper formatting
    df_display = []
    for item in performance_data:
        df_display.append({
            "Category": item["Category"],
            "Type": item["Type"],
            "Budgeted": f"${item['Budgeted']:,.0f}",
            "Actual": f"${item['Actual']:,.0f}",
            "Remaining": f"${item['Remaining']:,.0f}",
            "Variance": f"{item['Variance_Pct']:+.1f}%",
            "Status": item["Status"]
        })
    
    df = pd.DataFrame(df_display)
    
    # Color-code status
    def highlight_status(val):
        if val == "Over Budget":
            return 'background-color: #ffebee'
        elif val == "At Risk":
            return 'background-color: #fff3e0'
        elif val == "Under Budget":
            return 'background-color: #e8f5e8'
        return ''
    
    styled_df = df.style.applymap(highlight_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Budget visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Actual chart
        chart_data = []
        for item in performance_data:
            chart_data.append({
                "Category": item["Category"],
                "Amount": item["Budgeted"],
                "Type": "Budgeted"
            })
            chart_data.append({
                "Category": item["Category"],
                "Amount": item["Actual"],
                "Type": "Actual"
            })
        
        chart_df = pd.DataFrame(chart_data)
        fig = px.bar(chart_df, x='Category', y='Amount', color='Type',
                    title="Budget vs Actual by Category", barmode='group')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status distribution pie chart
        status_counts = {}
        for item in performance_data:
            status = item["Status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig_pie = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Budget Status Distribution"
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

def render_cost_items_management():
    """Display and manage individual cost items"""
    st.subheader("💳 Cost Items Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            options=["All"] + [cat.value for cat in CostCategory],
            key="cost_category_filter"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All"] + [status.value for status in CostItemStatus],
            key="cost_status_filter"
        )
    
    with col3:
        if st.button("➕ Add New Cost Item", use_container_width=True):
            st.session_state.show_cost_form = True
    
    # Show add form if requested
    if st.session_state.get('show_cost_form', False):
        render_add_cost_item_form()
    
    # Get and filter cost items
    cost_items = cost_manager.get_all_cost_items()
    
    if category_filter != "All":
        cost_items = [item for item in cost_items if item.category.value == category_filter]
    
    if status_filter != "All":
        cost_items = [item for item in cost_items if item.status.value == status_filter]
    
    # Display cost items
    if not cost_items:
        st.info("No cost items match your filter criteria.")
        return
    
    for item in cost_items:
        render_cost_item_card(item)

def render_add_cost_item_form():
    """Render form to add new cost item"""
    with st.form("add_cost_item_form"):
        st.subheader("➕ Add New Cost Item")
        
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input("Description*")
            category = st.selectbox("Category*", [cat.value for cat in CostCategory])
            status = st.selectbox("Status*", [status.value for status in CostItemStatus])
            budgeted_amount = st.number_input("Budgeted Amount*", min_value=0.0, step=100.0)
        
        with col2:
            work_package = st.text_input("Work Package*")
            location = st.text_input("Location")
            vendor_supplier = st.text_input("Vendor/Supplier")
            planned_date = st.date_input("Planned Date")
        
        col3, col4 = st.columns(2)
        with col3:
            committed_amount = st.number_input("Committed Amount", min_value=0.0, step=100.0)
        with col4:
            actual_amount = st.number_input("Actual Amount", min_value=0.0, step=100.0)
        
        purchase_order = st.text_input("Purchase Order")
        
        submitted = st.form_submit_button("💾 Add Cost Item", use_container_width=True)
        
        if submitted:
            # Validate required fields
            if not all([description, category, status, budgeted_amount, work_package]):
                st.error("Please fill in all required fields marked with *")
            else:
                # Create cost item
                item_data = {
                    "description": description,
                    "category": category,
                    "status": status,
                    "budgeted_amount": budgeted_amount,
                    "committed_amount": committed_amount,
                    "actual_amount": actual_amount,
                    "work_package": work_package,
                    "location": location,
                    "vendor_supplier": vendor_supplier,
                    "planned_date": planned_date.isoformat(),
                    "actual_date": None,
                    "purchase_order": purchase_order or None,
                    "invoice_number": None,
                    "created_by": "Project Manager"
                }
                
                # Validate data
                errors = cost_manager.validate_cost_item_data(item_data)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    item_id = cost_manager.create_cost_item(item_data)
                    st.success(f"✅ Cost item created successfully! ID: {item_id}")
                    st.session_state.show_cost_form = False
                    st.rerun()

def render_cost_item_card(item: CostItem):
    """Render individual cost item card"""
    # Color coding for status
    status_colors = {
        CostItemStatus.PLANNED: "🟡",
        CostItemStatus.COMMITTED: "🔵",
        CostItemStatus.INVOICED: "🟠",
        CostItemStatus.PAID: "🟢"
    }
    
    variance = item.calculate_variance()
    variance_pct = item.calculate_variance_percentage()
    
    with st.expander(
        f"{status_colors.get(item.status, '⚪')} {item.description} | ${item.budgeted_amount:,.0f} | {item.status.value}",
        expanded=False
    ):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.write(f"**📋 Work Package:** {item.work_package}")
            st.write(f"**📍 Location:** {item.location}")
            st.write(f"**🏢 Vendor:** {item.vendor_supplier}")
            st.write(f"**📅 Planned Date:** {item.planned_date}")
            if item.purchase_order:
                st.write(f"**📄 PO:** {item.purchase_order}")
        
        with col2:
            st.write(f"**💰 Budgeted:** ${item.budgeted_amount:,.2f}")
            st.write(f"**📋 Committed:** ${item.committed_amount:,.2f}")
            st.write(f"**💸 Actual:** ${item.actual_amount:,.2f}")
            st.write(f"**💵 Remaining:** ${item.remaining_amount:,.2f}")
            
            if variance != 0:
                variance_color = "🔴" if variance > 0 else "🟢"
                st.write(f"**📊 Variance:** {variance_color} ${variance:,.2f} ({variance_pct:+.1f}%)")
        
        with col3:
            st.write("**Actions:**")
            if st.button(f"✏️ Edit", key=f"edit_cost_{item.item_id}"):
                st.info("Edit functionality would open edit form")
            
            if item.status == CostItemStatus.PLANNED:
                if st.button(f"📋 Commit", key=f"commit_{item.item_id}"):
                    cost_manager.update_cost_item(item.item_id, {"status": CostItemStatus.COMMITTED})
                    st.success("Item committed!")
                    st.rerun()

def render_financial_analytics():
    """Display financial analytics and insights"""
    st.subheader("📈 Financial Analytics")
    
    # Project totals for charts
    totals = cost_manager.calculate_project_totals()
    performance_data = cost_manager.get_category_performance()
    
    if not performance_data:
        st.info("No data available for analytics.")
        return
    
    # Financial summary cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget utilization gauge
        utilization = (totals['total_actual'] / totals['total_budget']) * 100
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = utilization,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Budget Utilization %"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 120]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 80], 'color': "lightgray"},
                    {'range': [80, 100], 'color': "yellow"},
                    {'range': [100, 120], 'color': "red"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100}}))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Cost breakdown by category
        categories = [item["Category"] for item in performance_data]
        amounts = [item["Actual"] for item in performance_data]
        
        fig_breakdown = px.pie(
            values=amounts,
            names=categories,
            title="Cost Distribution by Category"
        )
        fig_breakdown.update_layout(height=300)
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Variance analysis
    st.subheader("📊 Variance Analysis")
    
    variance_data = []
    for item in performance_data:
        if item["Variance"] != 0:
            variance_data.append({
                "Category": item["Category"],
                "Variance": item["Variance"],
                "Variance_Pct": item["Variance_Pct"]
            })
    
    if variance_data:
        df_variance = pd.DataFrame(variance_data)
        fig_variance = px.bar(
            df_variance, 
            x='Category', 
            y='Variance',
            title="Budget Variance by Category",
            color='Variance',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        st.plotly_chart(fig_variance, use_container_width=True)

def render_change_orders():
    """Display change order management"""
    st.subheader("🔄 Change Orders")
    
    change_orders = list(cost_manager.change_orders.values())
    
    if not change_orders:
        st.info("No change orders on record.")
        return
    
    for co in change_orders:
        status_color = {"Pending": "🟡", "Approved": "🟢", "Rejected": "🔴"}.get(co.status, "⚪")
        
        with st.expander(f"{status_color} {co.co_number} | ${co.amount:,.0f} | {co.status}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**📋 Description:** {co.description}")
                st.write(f"**💰 Amount:** ${co.amount:,.2f}")
                st.write(f"**📅 Submitted:** {co.submitted_date}")
                if co.approved_date:
                    st.write(f"**✅ Approved:** {co.approved_date}")
            
            with col2:
                st.write(f"**📝 Reason:** {co.reason}")
                st.write(f"**📊 Impact:** {co.impact_description}")

def render_cash_flow_analysis():
    """Display cash flow analysis"""
    st.subheader("💹 Cash Flow Analysis")
    
    cash_flow_data = cost_manager.get_cash_flow_data()
    
    if not cash_flow_data:
        st.info("No cash flow data available.")
        return
    
    # Create cash flow chart
    df_cash = pd.DataFrame(cash_flow_data)
    
    fig_cash = go.Figure()
    
    fig_cash.add_trace(go.Scatter(
        x=df_cash['Month'],
        y=df_cash['Planned_Cumulative'],
        mode='lines+markers',
        name='Planned',
        line=dict(color='blue')
    ))
    
    fig_cash.add_trace(go.Scatter(
        x=df_cash['Month'],
        y=df_cash['Actual_Cumulative'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='red')
    ))
    
    fig_cash.update_layout(
        title="Cumulative Cash Flow - Planned vs Actual",
        xaxis_title="Month",
        yaxis_title="Cumulative Amount ($)",
        height=400
    )
    
    st.plotly_chart(fig_cash, use_container_width=True)
    
    # Cash flow table
    st.subheader("📊 Monthly Cash Flow Data")
    
    # Format the dataframe for display
    df_display = df_cash.copy()
    df_display['Planned_Cumulative'] = df_display['Planned_Cumulative'].apply(lambda x: f"${x:,.0f}")
    df_display['Actual_Cumulative'] = df_display['Actual_Cumulative'].apply(lambda x: f"${x:,.0f}")
    df_display['Variance'] = df_display['Variance'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)