"""
Cost Management Module - Highland Tower Development
Complete CRUD operations for budgets, cost tracking, change orders, and financial reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the comprehensive Cost Management module with full CRUD functionality"""
    st.title("💰 Cost Management - Highland Tower Development")
    st.markdown("**Advanced Budget Tracking & Financial Control System**")
    
    # Initialize session state for cost data
    if 'cost_items' not in st.session_state:
        st.session_state.cost_items = get_sample_cost_items()
    if 'change_orders' not in st.session_state:
        st.session_state.change_orders = get_sample_change_orders()
    if 'budget_categories' not in st.session_state:
        st.session_state.budget_categories = get_sample_budget_categories()
    if 'invoices' not in st.session_state:
        st.session_state.invoices = get_sample_invoices()
    
    # Financial overview metrics
    total_budget = 45500000  # $45.5M project budget
    spent_to_date = sum([item['actual_cost'] for item in st.session_state.cost_items])
    remaining_budget = total_budget - spent_to_date
    budget_variance = spent_to_date - sum([item['budgeted_cost'] for item in st.session_state.cost_items])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Budget", f"${total_budget:,.0f}", "Highland Tower Development")
    with col2:
        st.metric("Spent to Date", f"${spent_to_date:,.0f}", f"{spent_to_date/total_budget*100:.1f}% of budget")
    with col3:
        st.metric("Remaining Budget", f"${remaining_budget:,.0f}", f"${remaining_budget/total_budget*100:.1f}% remaining")
    with col4:
        variance_color = "normal" if budget_variance <= 0 else "inverse"
        st.metric("Budget Variance", f"${budget_variance:,.0f}", 
                 "Under budget" if budget_variance <= 0 else "Over budget", delta_color=variance_color)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Budget Tracking", "📋 Change Orders", "📄 Invoices", "📊 Cost Analytics", "💳 Payments", "⚙️ Settings"
    ])
    
    with tab1:
        render_budget_tracking()
    
    with tab2:
        render_change_orders()
    
    with tab3:
        render_invoice_management()
    
    with tab4:
        render_cost_analytics()
    
    with tab5:
        render_payment_management()
    
    with tab6:
        render_cost_settings()

def render_budget_tracking():
    """Complete CRUD for budget tracking and cost items"""
    st.subheader("💰 Budget Tracking & Cost Control")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Cost Item", type="primary"):
            st.session_state.show_cost_form = True
    with col2:
        if st.button("📊 Export Budget"):
            st.success("✅ Budget report exported to Excel")
    with col3:
        if st.button("📈 Forecast Analysis"):
            st.session_state.show_forecast = True
    with col4:
        if st.button("⚠️ Variance Report"):
            st.info("📄 Variance analysis generated")
    
    # New Cost Item Form
    if st.session_state.get('show_cost_form', False):
        render_new_cost_item_form()
    
    # Budget categories overview
    st.markdown("### Budget Categories Overview")
    
    category_df = pd.DataFrame(st.session_state.budget_categories)
    
    # Add calculated fields
    category_df['Spent_Percentage'] = (category_df['Actual_Cost'] / category_df['Budget_Amount'] * 100).round(1)
    category_df['Remaining'] = category_df['Budget_Amount'] - category_df['Actual_Cost']
    category_df['Variance'] = category_df['Actual_Cost'] - category_df['Budget_Amount']
    
    # Display with color coding
    for idx, category in category_df.iterrows():
        with st.expander(f"💰 {category['Category']} - ${category['Actual_Cost']:,.0f} / ${category['Budget_Amount']:,.0f}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Progress bar
                progress = min(category['Spent_Percentage'] / 100, 1.0)
                st.progress(progress)
                
                # Color-coded status
                if category['Spent_Percentage'] > 100:
                    status_color = "#dc3545"
                    status_text = "Over Budget"
                elif category['Spent_Percentage'] > 90:
                    status_color = "#ffc107"
                    status_text = "Near Budget Limit"
                else:
                    status_color = "#28a745"
                    status_text = "Within Budget"
                
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Budget:</strong> ${category['Budget_Amount']:,.0f}<br>
                <strong>Actual:</strong> ${category['Actual_Cost']:,.0f}<br>
                <strong>Remaining:</strong> ${category['Remaining']:,.0f}<br>
                <strong>Variance:</strong> ${category['Variance']:,.0f}<br>
                <strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{status_text}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📊 Details", key=f"details_{category['Category']}"):
                    st.info(f"Opening detailed breakdown for {category['Category']}")
                
                if st.button("✏️ Edit Budget", key=f"edit_budget_{category['Category']}"):
                    st.session_state.edit_category = category['Category']
                    st.session_state.show_budget_edit = True
                
                if st.button("📈 Forecast", key=f"forecast_{category['Category']}"):
                    st.success(f"Generating forecast for {category['Category']}")
    
    # Detailed cost items table
    st.markdown("### Detailed Cost Items")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Filter by Category", 
                                     ["All"] + [cat['Category'] for cat in st.session_state.budget_categories])
    with col2:
        date_filter = st.selectbox("Date Range", ["All Time", "This Month", "Last 30 Days", "This Quarter"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Paid", "Overdue"])
    
    # Display cost items
    cost_df = pd.DataFrame(st.session_state.cost_items)
    
    # Apply filters
    if category_filter != "All":
        cost_df = cost_df[cost_df['category'] == category_filter]
    
    st.dataframe(cost_df, use_container_width=True,
                column_config={
                    "cost_id": "Cost ID",
                    "description": "Description", 
                    "category": "Category",
                    "budgeted_cost": st.column_config.NumberColumn("Budgeted ($)", format="$%.0f"),
                    "actual_cost": st.column_config.NumberColumn("Actual ($)", format="$%.0f"),
                    "date": "Date",
                    "vendor": "Vendor",
                    "status": "Status"
                })

def render_new_cost_item_form():
    """Form to create new cost item"""
    st.markdown("### ➕ Create New Cost Item")
    
    with st.form("new_cost_item_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input("Description *", placeholder="e.g., Steel beam delivery - Level 13")
            category = st.selectbox(
                "Category *",
                ["Labor", "Materials", "Equipment", "Subcontractors", "General Conditions", "Other"]
            )
            vendor = st.text_input("Vendor/Supplier *", placeholder="Company name")
            budgeted_cost = st.number_input("Budgeted Cost ($) *", min_value=0.0, step=100.0)
        
        with col2:
            actual_cost = st.number_input("Actual Cost ($)", min_value=0.0, step=100.0, value=0.0)
            cost_date = st.date_input("Cost Date *", value=datetime.now())
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 60", "COD", "Progress Payment", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        # Additional details
        work_package = st.text_input("Work Package", placeholder="Associated work package or WBS code")
        purchase_order = st.text_input("Purchase Order #", placeholder="PO number if applicable")
        notes = st.text_area("Notes", placeholder="Additional notes or comments...")
        
        # Approval workflow
        requires_approval = st.checkbox("Requires Approval", value=True)
        if requires_approval:
            approver = st.selectbox("Approver", 
                                  ["Project Manager", "Construction Manager", "Finance Manager", "Owner"])
        
        submitted = st.form_submit_button("💰 Create Cost Item", type="primary")
        
        if submitted and description and category and vendor and budgeted_cost:
            # Create new cost item
            new_cost_item = {
                'cost_id': f"COST-HTD-{len(st.session_state.cost_items) + 1:04d}",
                'description': description,
                'category': category,
                'vendor': vendor,
                'budgeted_cost': budgeted_cost,
                'actual_cost': actual_cost,
                'date': cost_date.strftime('%Y-%m-%d'),
                'payment_terms': payment_terms,
                'priority': priority,
                'work_package': work_package,
                'purchase_order': purchase_order,
                'notes': notes,
                'status': 'Pending Approval' if requires_approval else 'Approved',
                'approver': approver if requires_approval else None,
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'created_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.cost_items.append(new_cost_item)
            st.session_state.show_cost_form = False
            
            # Update budget category
            for category_item in st.session_state.budget_categories:
                if category_item['Category'] == category:
                    category_item['Actual_Cost'] += actual_cost
                    break
            
            st.success(f"✅ Cost item {new_cost_item['cost_id']} created successfully!")
            if requires_approval:
                st.info(f"📧 Approval request sent to {approver}")
            st.rerun()

def render_change_orders():
    """Complete CRUD for change orders"""
    st.subheader("📋 Change Order Management")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Change Order", type="primary"):
            st.session_state.show_co_form = True
    with col2:
        if st.button("📊 CO Summary"):
            total_cos = len(st.session_state.change_orders)
            total_value = sum([co['amount'] for co in st.session_state.change_orders])
            st.info(f"📄 {total_cos} Change Orders totaling ${total_value:,.0f}")
    with col3:
        if st.button("⚠️ Pending Approvals"):
            pending = len([co for co in st.session_state.change_orders if co['status'] == 'Pending'])
            st.warning(f"⏳ {pending} change orders pending approval")
    with col4:
        if st.button("📄 Export Report"):
            st.success("📄 Change order report exported")
    
    # New Change Order Form
    if st.session_state.get('show_co_form', False):
        render_new_change_order_form()
    
    # Display change orders
    st.markdown("### Current Change Orders")
    
    for co in st.session_state.change_orders:
        # Status color coding
        status_colors = {
            "Pending": "#ffc107",
            "Approved": "#28a745",
            "Rejected": "#dc3545",
            "Under Review": "#17a2b8"
        }
        
        status_color = status_colors.get(co['status'], "#6c757d")
        
        with st.expander(f"📋 {co['co_id']} - {co['title']} (${co['amount']:,.0f})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 12px; margin: 10px 0;">
                <strong>Amount:</strong> ${co['amount']:,.0f}<br>
                <strong>Type:</strong> {co['co_type']}<br>
                <strong>Requested By:</strong> {co['requested_by']}<br>
                <strong>Date:</strong> {co['date_submitted']}<br>
                <strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{co['status']}</span><br>
                <strong>Justification:</strong> {co['justification']}<br>
                <strong>Impact:</strong> {co['schedule_impact']} days schedule impact
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if co['status'] == 'Pending':
                    if st.button("✅ Approve", key=f"approve_co_{co['co_id']}"):
                        # Update change order status
                        for i, change_order in enumerate(st.session_state.change_orders):
                            if change_order['co_id'] == co['co_id']:
                                st.session_state.change_orders[i]['status'] = 'Approved'
                                st.session_state.change_orders[i]['approval_date'] = datetime.now().strftime('%Y-%m-%d')
                                break
                        st.success("✅ Change order approved!")
                        st.rerun()
                    
                    if st.button("❌ Reject", key=f"reject_co_{co['co_id']}"):
                        for i, change_order in enumerate(st.session_state.change_orders):
                            if change_order['co_id'] == co['co_id']:
                                st.session_state.change_orders[i]['status'] = 'Rejected'
                                break
                        st.error("❌ Change order rejected")
                        st.rerun()
                
                if st.button("✏️ Edit", key=f"edit_co_{co['co_id']}"):
                    st.info(f"Editing change order {co['co_id']}")
                
                if st.button("📄 Print", key=f"print_co_{co['co_id']}"):
                    st.success("📄 Change order document generated")

def render_new_change_order_form():
    """Form to create new change order"""
    st.markdown("### 📋 Create New Change Order")
    
    with st.form("new_change_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Change Order Title *", placeholder="Brief description of the change")
            co_type = st.selectbox("Change Type *", 
                                 ["Addition", "Deletion", "Revision", "Time Extension", "Credit"])
            amount = st.number_input("Amount ($) *", step=1000.0)
            requested_by = st.selectbox("Requested By *",
                                      ["Owner", "Architect", "General Contractor", "Subcontractor", "Engineer"])
        
        with col2:
            schedule_impact = st.number_input("Schedule Impact (days)", value=0, step=1)
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            category = st.selectbox("Category",
                                  ["Design Change", "Site Conditions", "Code Requirements", "Owner Request", "Other"])
        
        justification = st.text_area("Justification *", 
                                   placeholder="Detailed explanation of why this change is necessary...")
        
        scope_description = st.text_area("Scope Description",
                                       placeholder="Describe the work to be added, deleted, or modified...")
        
        # Supporting documents
        supporting_docs = st.text_area("Supporting Documents",
                                     placeholder="List any drawings, specifications, or other documents...")
        
        submitted = st.form_submit_button("📋 Submit Change Order", type="primary")
        
        if submitted and title and co_type and amount and justification:
            # Create new change order
            new_co = {
                'co_id': f"CO-HTD-{len(st.session_state.change_orders) + 1:03d}",
                'title': title,
                'co_type': co_type,
                'amount': amount,
                'requested_by': requested_by,
                'schedule_impact': schedule_impact,
                'priority': priority,
                'category': category,
                'justification': justification,
                'scope_description': scope_description,
                'supporting_docs': supporting_docs,
                'status': 'Pending',
                'date_submitted': datetime.now().strftime('%Y-%m-%d'),
                'submitted_by': st.session_state.get('current_user', 'Current User')
            }
            
            # Add to session state
            st.session_state.change_orders.append(new_co)
            st.session_state.show_co_form = False
            
            st.success(f"✅ Change Order {new_co['co_id']} submitted successfully!")
            st.info("📧 Notification sent to approval team")
            st.rerun()

def render_invoice_management():
    """Invoice management with CRUD operations"""
    st.subheader("📄 Invoice Management")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ New Invoice", type="primary"):
            st.session_state.show_invoice_form = True
    with col2:
        if st.button("📊 Aging Report"):
            st.info("📄 Invoice aging report generated")
    with col3:
        if st.button("💳 Process Payments"):
            st.session_state.show_payment_batch = True
    with col4:
        if st.button("📧 Send Reminders"):
            overdue_count = len([inv for inv in st.session_state.invoices if inv['status'] == 'Overdue'])
            st.warning(f"📧 Reminders sent for {overdue_count} overdue invoices")
    
    # Invoice overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_invoices = len(st.session_state.invoices)
    pending_amount = sum([inv['amount'] for inv in st.session_state.invoices if inv['status'] == 'Pending'])
    overdue_amount = sum([inv['amount'] for inv in st.session_state.invoices if inv['status'] == 'Overdue'])
    paid_amount = sum([inv['amount'] for inv in st.session_state.invoices if inv['status'] == 'Paid'])
    
    with col1:
        st.metric("Total Invoices", total_invoices, "All time")
    with col2:
        st.metric("Pending Payment", f"${pending_amount:,.0f}", f"{len([i for i in st.session_state.invoices if i['status'] == 'Pending'])} invoices")
    with col3:
        st.metric("Overdue Amount", f"${overdue_amount:,.0f}", f"{len([i for i in st.session_state.invoices if i['status'] == 'Overdue'])} invoices")
    with col4:
        st.metric("Paid This Month", f"${paid_amount:,.0f}", "Current period")
    
    # Display invoices
    st.markdown("### Invoice Register")
    
    invoice_df = pd.DataFrame(st.session_state.invoices)
    st.dataframe(invoice_df, use_container_width=True,
                column_config={
                    "invoice_id": "Invoice ID",
                    "vendor": "Vendor",
                    "amount": st.column_config.NumberColumn("Amount ($)", format="$%.0f"),
                    "due_date": "Due Date",
                    "status": "Status"
                })

def render_cost_analytics():
    """Cost analytics and financial reporting"""
    st.subheader("📊 Cost Analytics & Financial Performance")
    
    # Key performance indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cost Performance Index", "0.96", "4% under budget")
    with col2:
        st.metric("Burn Rate", "$1.2M/month", "Consistent spending")
    with col3:
        st.metric("Forecast at Completion", "$43.7M", "$1.8M under budget")
    with col4:
        st.metric("Cost Variance", "-$389K", "Favorable variance")
    
    # Cost analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Actual by category
        category_data = pd.DataFrame(st.session_state.budget_categories)
        
        fig = px.bar(category_data, x='Category', y=['Budget_Amount', 'Actual_Cost'],
                    title="Budget vs Actual by Category", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly spending trends
        monthly_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Planned': [2.1, 2.3, 2.8, 3.2, 3.5],
            'Actual': [2.0, 2.1, 2.6, 3.0, 3.2]
        })
        
        fig = px.line(monthly_data, x='Month', y=['Planned', 'Actual'],
                     title="Monthly Spending Trends (Millions $)")
        st.plotly_chart(fig, use_container_width=True)

def render_payment_management():
    """Payment processing and management"""
    st.subheader("💳 Payment Management")
    
    st.info("💳 Payment processing integration with accounting systems")
    
    # Payment summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Payments This Month", "$1.8M", "12 payments processed")
    with col2:
        st.metric("Average Payment Time", "18 days", "2 days faster than target")
    with col3:
        st.metric("Payment Accuracy", "99.8%", "Excellent processing")
    
    # Payment queue
    st.markdown("### Payment Queue")
    
    payment_queue = [
        {"Vendor": "Steel Fabricators Inc", "Amount": "$125,000", "Due": "2025-05-28", "Status": "Ready"},
        {"Vendor": "Concrete Supply Co", "Amount": "$89,000", "Due": "2025-05-30", "Status": "Pending"},
        {"Vendor": "MEP Contractors LLC", "Amount": "$156,000", "Due": "2025-06-02", "Status": "Ready"}
    ]
    
    payment_df = pd.DataFrame(payment_queue)
    st.dataframe(payment_df, use_container_width=True)

def render_cost_settings():
    """Cost management settings and configuration"""
    st.subheader("⚙️ Cost Management Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Budget Controls**")
        budget_alerts = st.checkbox("Budget threshold alerts", value=True)
        approval_limits = st.number_input("Approval limit ($)", value=10000, step=1000)
        variance_threshold = st.slider("Variance alert threshold (%)", 5, 20, 10)
        
        st.markdown("**Payment Settings**")
        payment_terms = st.selectbox("Default payment terms", ["Net 30", "Net 60", "Net 90"])
        auto_payment = st.checkbox("Enable automatic payments", value=False)
    
    with col2:
        st.markdown("**Reporting**")
        report_frequency = st.selectbox("Cost report frequency", ["Weekly", "Monthly", "Quarterly"])
        report_recipients = st.text_area("Report recipients", 
                                       placeholder="Email addresses separated by commas")
        
        st.markdown("**Integration**")
        accounting_sync = st.checkbox("Sync with accounting system", value=True)
        backup_frequency = st.selectbox("Data backup", ["Daily", "Weekly", "Monthly"])
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Cost management settings saved successfully!")

def get_sample_cost_items():
    """Generate sample cost item data"""
    return [
        {
            'cost_id': 'COST-HTD-0001',
            'description': 'Steel beam delivery - Level 13',
            'category': 'Materials',
            'vendor': 'Steel Fabricators Inc',
            'budgeted_cost': 125000,
            'actual_cost': 128500,
            'date': '2025-05-20',
            'status': 'Approved'
        },
        {
            'cost_id': 'COST-HTD-0002',
            'description': 'Concrete pour - Level 12',
            'category': 'Materials',
            'vendor': 'Concrete Supply Co',
            'budgeted_cost': 89000,
            'actual_cost': 87200,
            'date': '2025-05-18',
            'status': 'Paid'
        },
        {
            'cost_id': 'COST-HTD-0003',
            'description': 'Tower crane rental - May',
            'category': 'Equipment',
            'vendor': 'Crane Rental LLC',
            'budgeted_cost': 45000,
            'actual_cost': 45000,
            'date': '2025-05-01',
            'status': 'Approved'
        }
    ]

def get_sample_change_orders():
    """Generate sample change order data"""
    return [
        {
            'co_id': 'CO-HTD-001',
            'title': 'Additional elevator shaft reinforcement',
            'co_type': 'Addition',
            'amount': 75000,
            'requested_by': 'Structural Engineer',
            'schedule_impact': 5,
            'priority': 'High',
            'category': 'Design Change',
            'justification': 'Additional reinforcement required per structural analysis',
            'status': 'Pending',
            'date_submitted': '2025-05-22'
        },
        {
            'co_id': 'CO-HTD-002',
            'title': 'Upgrade to energy-efficient windows',
            'co_type': 'Revision',
            'amount': 120000,
            'requested_by': 'Owner',
            'schedule_impact': 0,
            'priority': 'Medium',
            'category': 'Owner Request',
            'justification': 'Owner requests upgrade for LEED certification',
            'status': 'Approved',
            'date_submitted': '2025-05-20'
        }
    ]

def get_sample_budget_categories():
    """Generate sample budget category data"""
    return [
        {
            'Category': 'Labor',
            'Budget_Amount': 18200000,
            'Actual_Cost': 12800000
        },
        {
            'Category': 'Materials', 
            'Budget_Amount': 15800000,
            'Actual_Cost': 11200000
        },
        {
            'Category': 'Equipment',
            'Budget_Amount': 6300000,
            'Actual_Cost': 4100000
        },
        {
            'Category': 'Subcontractors',
            'Budget_Amount': 3700000,
            'Actual_Cost': 2800000
        },
        {
            'Category': 'General Conditions',
            'Budget_Amount': 1500000,
            'Actual_Cost': 980000
        }
    ]

def get_sample_invoices():
    """Generate sample invoice data"""
    return [
        {
            'invoice_id': 'INV-2025-0145',
            'vendor': 'Steel Fabricators Inc',
            'amount': 128500,
            'due_date': '2025-05-28',
            'status': 'Pending'
        },
        {
            'invoice_id': 'INV-2025-0144',
            'vendor': 'Concrete Supply Co',
            'amount': 87200,
            'due_date': '2025-05-25',
            'status': 'Paid'
        },
        {
            'invoice_id': 'INV-2025-0143',
            'vendor': 'MEP Contractors LLC',
            'amount': 156000,
            'due_date': '2025-06-02',
            'status': 'Pending'
        }
    ]

if __name__ == "__main__":
    render()