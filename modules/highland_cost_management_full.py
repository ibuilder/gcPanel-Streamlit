"""
Highland Tower Development - Complete Cost Management with Full CRUD
SOV updates, change orders, and relational ties between modules.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from typing import Dict, List, Any

def render_highland_cost_management():
    """Highland Tower Development - Complete Cost Management with CRUD and Relations"""
    
    st.markdown("""
    <div class="module-header">
        <h1>💰 Highland Tower Cost Management</h1>
        <p>$45.5M Project - SOV Updates, Change Orders, and Budget Control</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Highland Tower cost data
    initialize_highland_cost_data()
    
    # Cost performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_budget = 45500000
    spent_to_date = 30247800
    change_orders_total = sum(co['amount'] for co in st.session_state.highland_change_orders)
    adjusted_budget = total_budget + change_orders_total
    
    with col1:
        st.metric("Contract Value", f"${total_budget:,.0f}", "Original contract")
    with col2:
        st.metric("Spent to Date", f"${spent_to_date:,.0f}", f"{(spent_to_date/total_budget)*100:.1f}%")
    with col3:
        st.metric("Change Orders", f"${change_orders_total:,.0f}", f"{len(st.session_state.highland_change_orders)} total")
    with col4:
        st.metric("Revised Budget", f"${adjusted_budget:,.0f}", f"${change_orders_total:+,.0f}")
    
    # Main tabs for cost management
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 SOV Management", 
        "🔄 Change Orders", 
        "💰 Budget Items", 
        "📈 Cost Analysis", 
        "🔗 Module Relations"
    ])
    
    with tab1:
        render_sov_management()
    
    with tab2:
        render_change_orders_management()
    
    with tab3:
        render_budget_items_management()
    
    with tab4:
        render_cost_analysis()
    
    with tab5:
        render_module_relations()

def initialize_highland_cost_data():
    """Initialize Highland Tower Development cost management data"""
    
    # Schedule of Values (SOV)
    if "highland_sov" not in st.session_state:
        st.session_state.highland_sov = [
            {
                "item_number": "001",
                "description": "General Requirements",
                "scheduled_value": 2280000.0,
                "work_completed_previous": 1950000.0,
                "work_completed_current": 150000.0,
                "materials_stored": 0.0,
                "total_completed": 2100000.0,
                "percent_complete": 92.1,
                "retainage": 105000.0,
                "balance_to_finish": 180000.0
            },
            {
                "item_number": "002", 
                "description": "Concrete Work",
                "scheduled_value": 8750000.0,
                "work_completed_previous": 7200000.0,
                "work_completed_current": 875000.0,
                "materials_stored": 175000.0,
                "total_completed": 8250000.0,
                "percent_complete": 94.3,
                "retainage": 412500.0,
                "balance_to_finish": 500000.0
            },
            {
                "item_number": "003",
                "description": "Structural Steel",
                "scheduled_value": 12400000.0,
                "work_completed_previous": 8680000.0,
                "work_completed_current": 1240000.0,
                "materials_stored": 310000.0,
                "total_completed": 10230000.0,
                "percent_complete": 82.5,
                "retainage": 511500.0,
                "balance_to_finish": 2170000.0
            },
            {
                "item_number": "004",
                "description": "MEP Systems",
                "scheduled_value": 15200000.0,
                "work_completed_previous": 6840000.0,
                "work_completed_current": 1520000.0,
                "materials_stored": 380000.0,
                "total_completed": 8740000.0,
                "percent_complete": 57.5,
                "retainage": 437000.0,
                "balance_to_finish": 6460000.0
            },
            {
                "item_number": "005",
                "description": "Exterior Envelope",
                "scheduled_value": 6870000.0,
                "work_completed_previous": 2748000.0,
                "work_completed_current": 687000.0,
                "materials_stored": 137400.0,
                "total_completed": 3572400.0,
                "percent_complete": 52.0,
                "retainage": 178620.0,
                "balance_to_finish": 3297600.0
            }
        ]
    
    # Change Orders
    if "highland_change_orders" not in st.session_state:
        st.session_state.highland_change_orders = [
            {
                "co_number": "CO-001",
                "description": "Additional Elevator Fireproofing",
                "amount": 125000.0,
                "type": "Addition",
                "status": "Approved",
                "sov_items_affected": ["001", "003"],
                "submitted_date": "2024-03-15",
                "approved_date": "2024-03-22",
                "reason": "Code Compliance",
                "cost_impact_analysis": "Required by updated fire code"
            },
            {
                "co_number": "CO-002", 
                "description": "HVAC Controls Upgrade",
                "amount": 275000.0,
                "type": "Addition",
                "status": "Approved",
                "sov_items_affected": ["004"],
                "submitted_date": "2024-04-08",
                "approved_date": "2024-04-15",
                "reason": "Owner Enhancement",
                "cost_impact_analysis": "Owner requested smart building automation"
            },
            {
                "co_number": "CO-003",
                "description": "Premium Lobby Finishes",
                "amount": 185000.0,
                "type": "Addition", 
                "status": "Pending",
                "sov_items_affected": ["001"],
                "submitted_date": "2024-05-10",
                "approved_date": None,
                "reason": "Owner Request",
                "cost_impact_analysis": "Upgrade from standard to premium materials"
            }
        ]
    
    # Budget line items
    if "highland_budget_items" not in st.session_state:
        st.session_state.highland_budget_items = [
            {
                "cost_code": "01-0000",
                "description": "General Requirements",
                "budgeted_amount": 2280000.0,
                "committed_amount": 2100000.0,
                "actual_amount": 2100000.0,
                "remaining_budget": 180000.0,
                "variance_percent": -7.9
            },
            {
                "cost_code": "03-0000",
                "description": "Concrete",
                "budgeted_amount": 8750000.0,
                "committed_amount": 8500000.0,
                "actual_amount": 8250000.0,
                "remaining_budget": 500000.0,
                "variance_percent": -5.7
            },
            {
                "cost_code": "05-0000",
                "description": "Metals",
                "budgeted_amount": 12400000.0,
                "committed_amount": 11800000.0,
                "actual_amount": 10230000.0,
                "remaining_budget": 2170000.0,
                "variance_percent": -17.5
            }
        ]

def render_sov_management():
    """Schedule of Values Management with full CRUD"""
    st.subheader("📊 Highland Tower Development - Schedule of Values")
    
    # SOV summary
    col1, col2, col3 = st.columns(3)
    
    total_scheduled = sum(item['scheduled_value'] for item in st.session_state.highland_sov)
    total_completed = sum(item['total_completed'] for item in st.session_state.highland_sov)
    overall_percent = (total_completed / total_scheduled * 100) if total_scheduled > 0 else 0
    
    with col1:
        st.metric("Total Contract", f"${total_scheduled:,.0f}")
    with col2:
        st.metric("Work Completed", f"${total_completed:,.0f}")
    with col3:
        st.metric("Overall Progress", f"{overall_percent:.1f}%")
    
    # SOV Actions
    st.write("**📋 SOV Actions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Update SOV Item", key="update_sov"):
            st.session_state.show_sov_update = True
    with col2:
        if st.button("➕ Add SOV Line", key="add_sov"):
            st.session_state.show_sov_add = True
    with col3:
        if st.button("🔄 Apply Change Orders", key="apply_co_to_sov"):
            apply_change_orders_to_sov()
            st.success("Change orders applied to SOV!")
            st.rerun()
    with col4:
        if st.button("📊 Generate Bill", key="generate_bill"):
            st.session_state.show_bill_generation = True
    
    # SOV Update Form
    if st.session_state.get("show_sov_update", False):
        with st.form("sov_update_form"):
            st.write("**📝 Update SOV Item Progress**")
            
            sov_item_options = [f"{item['item_number']} - {item['description']}" for item in st.session_state.highland_sov]
            selected_item = st.selectbox("Select SOV Item", sov_item_options)
            
            if selected_item:
                item_number = selected_item.split(" - ")[0]
                current_item = next(item for item in st.session_state.highland_sov if item['item_number'] == item_number)
                
                col1, col2 = st.columns(2)
                with col1:
                    work_this_period = st.number_input("Work Completed This Period ($)", 
                                                     value=current_item['work_completed_current'], 
                                                     format="%.2f")
                    materials_stored = st.number_input("Materials Presently Stored ($)", 
                                                     value=current_item['materials_stored'], 
                                                     format="%.2f")
                with col2:
                    st.write(f"**Current Progress:** {current_item['percent_complete']:.1f}%")
                    st.write(f"**Scheduled Value:** ${current_item['scheduled_value']:,.0f}")
            
            if st.form_submit_button("💾 Update SOV Item"):
                if selected_item:
                    update_sov_item(item_number, work_this_period, materials_stored)
                    st.success(f"SOV item {item_number} updated!")
                    st.session_state.show_sov_update = False
                    st.rerun()
    
    # Display SOV table
    st.write("**📊 Current Schedule of Values:**")
    sov_df = pd.DataFrame(st.session_state.highland_sov)
    
    # Format for display
    display_sov = sov_df.copy()
    for col in ['scheduled_value', 'work_completed_previous', 'work_completed_current', 
                'materials_stored', 'total_completed', 'retainage', 'balance_to_finish']:
        display_sov[col] = display_sov[col].apply(lambda x: f"${x:,.0f}")
    display_sov['percent_complete'] = display_sov['percent_complete'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_sov, use_container_width=True, hide_index=True)

def render_change_orders_management():
    """Change Orders Management with full CRUD"""
    st.subheader("🔄 Highland Tower Development - Change Orders Management")
    
    # Change Orders summary
    approved_cos = [co for co in st.session_state.highland_change_orders if co['status'] == 'Approved']
    pending_cos = [co for co in st.session_state.highland_change_orders if co['status'] == 'Pending']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total COs", len(st.session_state.highland_change_orders))
    with col2:
        st.metric("Approved", len(approved_cos))
    with col3:
        st.metric("Pending", len(pending_cos))
    with col4:
        approved_total = sum(co['amount'] for co in approved_cos)
        st.metric("Approved Value", f"${approved_total:,.0f}")
    
    # Change Order Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Create Change Order", key="create_co"):
            st.session_state.show_co_creation = True
    with col2:
        if st.button("✅ Approve Pending COs", key="approve_cos"):
            approve_pending_change_orders()
            st.success("Pending change orders approved!")
            st.rerun()
    with col3:
        if st.button("📊 CO Impact Analysis", key="co_analysis"):
            st.session_state.show_co_analysis = True
    
    # Create Change Order Form
    if st.session_state.get("show_co_creation", False):
        with st.form("create_change_order"):
            st.write("**➕ Create New Change Order**")
            
            col1, col2 = st.columns(2)
            with col1:
                co_description = st.text_area("Description*", placeholder="Detailed description of the change")
                co_amount = st.number_input("Amount ($)*", value=0.0, format="%.2f")
                co_type = st.selectbox("Type*", ["Addition", "Deduction", "Credit"])
            with col2:
                reason = st.selectbox("Reason*", ["Owner Request", "Design Change", "Code Compliance", "Field Condition"])
                sov_items = st.multiselect("Affected SOV Items", 
                                         [f"{item['item_number']} - {item['description']}" for item in st.session_state.highland_sov])
                cost_impact = st.text_area("Cost Impact Analysis", placeholder="Analysis of cost and schedule impact")
            
            if st.form_submit_button("🔄 Create Change Order"):
                if co_description and co_amount != 0:
                    create_change_order(co_description, co_amount, co_type, reason, sov_items, cost_impact)
                    st.success("Change order created successfully!")
                    st.session_state.show_co_creation = False
                    st.rerun()
                else:
                    st.error("Please fill in all required fields!")
    
    # Display Change Orders
    st.write("**🔄 Current Change Orders:**")
    for co in st.session_state.highland_change_orders:
        status_color = {"Approved": "🟢", "Pending": "🟡", "Rejected": "🔴"}.get(co['status'], "⚪")
        
        with st.expander(f"{status_color} {co['co_number']} | ${co['amount']:,.0f} | {co['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Description:** {co['description']}")
                st.write(f"**Amount:** ${co['amount']:,.2f}")
                st.write(f"**Type:** {co['type']}")
                st.write(f"**Reason:** {co['reason']}")
            with col2:
                st.write(f"**Status:** {co['status']}")
                st.write(f"**Submitted:** {co['submitted_date']}")
                if co['approved_date']:
                    st.write(f"**Approved:** {co['approved_date']}")
                st.write(f"**SOV Items:** {', '.join(co['sov_items_affected'])}")
            
            st.write(f"**Cost Impact Analysis:** {co['cost_impact_analysis']}")
            
            if co['status'] == 'Pending':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{co['co_number']}"):
                        approve_change_order(co['co_number'])
                        st.rerun()
                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{co['co_number']}"):
                        reject_change_order(co['co_number'])
                        st.rerun()

def render_budget_items_management():
    """Budget Items Management with variance tracking"""
    st.subheader("💰 Highland Tower Development - Budget Line Items")
    
    # Budget performance chart
    budget_df = pd.DataFrame(st.session_state.highland_budget_items)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Budgeted', x=budget_df['description'], y=budget_df['budgeted_amount']))
    fig.add_trace(go.Bar(name='Actual', x=budget_df['description'], y=budget_df['actual_amount']))
    fig.update_layout(title="Budget vs Actual by Category", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Budget items table
    st.write("**💰 Budget Line Items:**")
    st.dataframe(budget_df, use_container_width=True, hide_index=True)

def render_cost_analysis():
    """Cost Analysis and Reporting"""
    st.subheader("📈 Highland Tower Development - Cost Analysis")
    
    # Cost performance indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cost Performance Index", "1.02", "2% under budget")
    with col2:
        st.metric("Schedule Performance Index", "1.05", "5% ahead of schedule")
    with col3:
        st.metric("Estimate at Completion", "$43.4M", "$2.1M savings")
    
    # Cost trend analysis
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    budgeted = [7.5, 15.2, 23.8, 32.1, 40.5]
    actual = [7.2, 14.8, 23.1, 31.2, 39.8]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=budgeted, mode='lines+markers', name='Budgeted'))
    fig.add_trace(go.Scatter(x=months, y=actual, mode='lines+markers', name='Actual'))
    fig.update_layout(title="Highland Tower Development - Monthly Cost Trend (Millions $)")
    st.plotly_chart(fig, use_container_width=True)

def render_module_relations():
    """Show module relationships and data flows"""
    st.subheader("🔗 Highland Tower Development - Module Relations")
    
    st.write("**🔄 Active Module Relationships:**")
    
    relations_data = [
        {"Source Module": "Change Orders", "Target Module": "Cost Management", "Relationship": "Budget Updates", "Status": "Active"},
        {"Source Module": "Change Orders", "Target Module": "SOV", "Relationship": "Line Item Updates", "Status": "Active"},
        {"Source Module": "Daily Reports", "Target Module": "Cost Management", "Relationship": "Labor Cost Sync", "Status": "Active"},
        {"Source Module": "RFIs", "Target Module": "Cost Management", "Relationship": "Cost Impact Tracking", "Status": "Active"},
        {"Source Module": "Material Management", "Target Module": "Cost Management", "Relationship": "Material Cost Updates", "Status": "Active"}
    ]
    
    relations_df = pd.DataFrame(relations_data)
    st.dataframe(relations_df, use_container_width=True, hide_index=True)
    
    st.info("💡 **Module Relations:** When you create or update items in one module, related modules are automatically updated to maintain data consistency across your Highland Tower Development project.")

# Helper functions for CRUD operations

def update_sov_item(item_number: str, work_this_period: float, materials_stored: float):
    """Update SOV item with new progress"""
    for item in st.session_state.highland_sov:
        if item['item_number'] == item_number:
            item['work_completed_current'] = work_this_period
            item['materials_stored'] = materials_stored
            item['total_completed'] = item['work_completed_previous'] + work_this_period + materials_stored
            item['percent_complete'] = (item['total_completed'] / item['scheduled_value']) * 100
            item['balance_to_finish'] = item['scheduled_value'] - item['total_completed']
            break

def create_change_order(description: str, amount: float, co_type: str, reason: str, sov_items: List[str], cost_impact: str):
    """Create new change order"""
    co_number = f"CO-{len(st.session_state.highland_change_orders) + 1:03d}"
    
    sov_item_numbers = [item.split(" - ")[0] for item in sov_items]
    
    new_co = {
        "co_number": co_number,
        "description": description,
        "amount": amount,
        "type": co_type,
        "status": "Pending",
        "sov_items_affected": sov_item_numbers,
        "submitted_date": datetime.now().strftime('%Y-%m-%d'),
        "approved_date": None,
        "reason": reason,
        "cost_impact_analysis": cost_impact
    }
    
    st.session_state.highland_change_orders.append(new_co)

def approve_change_order(co_number: str):
    """Approve a specific change order"""
    for co in st.session_state.highland_change_orders:
        if co['co_number'] == co_number:
            co['status'] = 'Approved'
            co['approved_date'] = datetime.now().strftime('%Y-%m-%d')
            break

def reject_change_order(co_number: str):
    """Reject a specific change order"""
    for co in st.session_state.highland_change_orders:
        if co['co_number'] == co_number:
            co['status'] = 'Rejected'
            break

def approve_pending_change_orders():
    """Approve all pending change orders"""
    for co in st.session_state.highland_change_orders:
        if co['status'] == 'Pending':
            co['status'] = 'Approved'
            co['approved_date'] = datetime.now().strftime('%Y-%m-%d')

def apply_change_orders_to_sov():
    """Apply approved change orders to SOV items"""
    approved_cos = [co for co in st.session_state.highland_change_orders if co['status'] == 'Approved']
    
    for co in approved_cos:
        if co['sov_items_affected']:
            amount_per_item = co['amount'] / len(co['sov_items_affected'])
            
            for sov_item_number in co['sov_items_affected']:
                for sov_item in st.session_state.highland_sov:
                    if sov_item['item_number'] == sov_item_number:
                        sov_item['scheduled_value'] += amount_per_item
                        sov_item['balance_to_finish'] += amount_per_item
                        # Recalculate percentage
                        sov_item['percent_complete'] = (sov_item['total_completed'] / sov_item['scheduled_value']) * 100
                        break